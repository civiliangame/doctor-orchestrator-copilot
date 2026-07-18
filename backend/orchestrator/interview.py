"""Stage 4: the voice interview agent — a turn-based tool-use loop per call.

Transport-agnostic (SPEC.md decision 5). The transport only moves utterances:
- sim: speak() is a no-op beyond the call.turn broadcast; the patient answers
  via POST /api/dev/sim-answer -> on_patient_utterance().
- telnyx: speak() synthesizes audio into the media stream; Soniox end-of-turn
  calls on_patient_utterance(). (telephony/, task 7.)

Concurrency: one in-flight model turn per call (phone calls are half-duplex).
Utterances landing mid-turn are buffered and delivered as the next user turn.
"""

import asyncio
import json
import logging

import events
import serialize
from config import MODEL_SONNET
from db import ex, ins, now_iso, one, q
from llm import cached_block, client

from orchestrator import prompts

log = logging.getLogger("doc.interview")

# Active sessions by call_id — the routing table for sim-answer / telnyx STT.
SESSIONS: dict[int, "InterviewSession"] = {}

MAX_TOOL_ROUNDS = 6  # model-call rounds per patient utterance (safety cap)

TOOLS = [
    {
        "name": "record_answer",
        "description": (
            "Record the patient's answer to one interview question once its "
            "completeness criteria are met (complete=true), or after the probe "
            "cap with whatever was obtained (complete=false)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "question_id": {"type": "integer", "description": "The QUESTION id from the plan"},
                "summary_text": {"type": "string", "description": "Clinical restatement of what the patient reported"},
                "complete": {"type": "boolean", "description": "Whether the completeness criteria were met"},
            },
            "required": ["question_id", "summary_text", "complete"],
        },
    },
    {
        "name": "flag_new_finding",
        "description": (
            "Flag a NEW fact from the call that contradicts the record or is "
            "absent from it entirely (new contradiction, new history, new symptom)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "kind": {"type": "string", "enum": ["contradiction", "gap", "ambiguity"]},
                "title": {"type": "string"},
                "detail": {"type": "string"},
                "quote": {"type": "string", "description": "The patient's verbatim words on the call"},
            },
            "required": ["kind", "title", "detail", "quote"],
        },
    },
    {
        "name": "defer_question",
        "description": (
            "Mark a question as unanswerable by the patient on the phone "
            "(needs an exam or measurement at the visit) and move on."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "question_id": {"type": "integer"},
                "reason": {"type": "string"},
            },
            "required": ["question_id", "reason"],
        },
    },
    {
        "name": "end_call",
        "description": (
            "End the call. Use ONLY after every question is answered or "
            "deferred and you have said safety-netting plus a goodbye."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"reason": {"type": "string"}},
            "required": ["reason"],
        },
    },
]


class SimTransport:
    """The call.turn broadcast IS the sim UI; nothing else to do."""

    async def speak(self, text: str) -> None:
        pass

    async def hangup(self) -> None:
        pass


class InterviewSession:
    def __init__(self, run_id: int, call_id: int, transport, on_end) -> None:
        self.run_id = run_id
        self.call_id = call_id
        self.transport = transport
        self.on_end = on_end  # async callback(run_id) -> compile stage
        self.ended = False
        self._finished = False
        self._lock = asyncio.Lock()
        self._pending: list[str] = []
        self.messages: list[dict] = []

        run = one("SELECT * FROM runs WHERE id=?", (run_id,))
        patient = one("SELECT * FROM patients WHERE id=?", (run["patient_id"],))
        self.patient_name = patient["name"]
        questions = [
            serialize.question(r)
            for r in q("SELECT * FROM questions WHERE run_id=? ORDER BY ord", (run_id,))
        ]
        digest = _record_digest(run_id)
        # Cached per-call system prefix: persona + plan + digest (stable text).
        self.system = [
            cached_block(prompts.interview_system(self.patient_name, questions, digest))
        ]

    # ------------------------------------------------------------- lifecycle

    async def start(self) -> None:
        SESSIONS[self.call_id] = self
        await self._user_turn(
            "[The call has connected. The patient just picked up. Greet her, "
            "confirm who you are speaking with, and begin.]"
        )

    async def on_patient_utterance(self, text: str) -> None:
        """THE seam: sim-answer and the telnyx STT path both land here."""
        if self.ended:
            return
        ts = now_iso()
        tid = ins("call_turns", call_id=self.call_id, speaker="patient", text=text, ts=ts)
        await events.broadcast(
            self.run_id, "call.turn",
            {"id": tid, "call_id": self.call_id, "speaker": "patient", "text": text, "ts": ts},
        )
        if self._lock.locked():
            self._pending.append(text)
            return
        await self._user_turn(text)

    async def force_end(self) -> None:
        """Operator hangup / telnyx call.hangup: compile with what we have."""
        self.ended = True
        await self._finish()

    # ------------------------------------------------------------ model loop

    async def _user_turn(self, text: str) -> None:
        async with self._lock:
            self.messages.append({"role": "user", "content": text})
            try:
                await self._model_loop()
            except Exception:
                log.exception("interview model turn failed (call=%s)", self.call_id)
        if self._pending and not self.ended:
            merged = " ".join(self._pending)
            self._pending.clear()
            await self._user_turn(merged)
        elif self.ended:
            await self._finish()

    async def _model_loop(self) -> None:
        for _ in range(MAX_TOOL_ROUNDS):
            resp = await client.messages.create(
                model=MODEL_SONNET,
                max_tokens=700,
                thinking={"type": "disabled"},  # latency: phone budget < 2.5s
                system=self.system,
                tools=TOOLS,
                messages=self.messages,
            )
            self.messages.append({"role": "assistant", "content": resp.content})

            speech = "".join(b.text for b in resp.content if b.type == "text").strip()
            if speech:
                await self._speak(speech)

            tool_uses = [b for b in resp.content if b.type == "tool_use"]
            if not tool_uses:
                break
            results = []
            for tu in tool_uses:
                try:
                    out = await self._handle_tool(tu.name, tu.input)
                except Exception:
                    log.exception("tool %s failed (call=%s)", tu.name, self.call_id)
                    out = "tool error — continue the interview"
                results.append(
                    {"type": "tool_result", "tool_use_id": tu.id, "content": out}
                )
            self.messages.append({"role": "user", "content": results})
            if self.ended:
                break  # end_call: no further model rounds needed

    async def _speak(self, text: str) -> None:
        ts = now_iso()
        tid = ins("call_turns", call_id=self.call_id, speaker="agent", text=text, ts=ts)
        await events.broadcast(
            self.run_id, "call.turn",
            {"id": tid, "call_id": self.call_id, "speaker": "agent", "text": text, "ts": ts},
        )
        await self.transport.speak(text)

    # ----------------------------------------------------------------- tools

    async def _handle_tool(self, name: str, args: dict) -> str:
        if name == "record_answer":
            qid = int(args["question_id"])
            aid = ins("answers", question_id=qid,
                      summary_text=str(args["summary_text"]),
                      complete=1 if args.get("complete", True) else 0, ts=now_iso())
            row = one("SELECT * FROM answers WHERE id=?", (aid,))
            await events.broadcast(self.run_id, "answer.recorded", serialize.answer(row))
            await self._set_question_status(qid, "answered")
            return self._plan_state()

        if name == "defer_question":
            qid = int(args["question_id"])
            await self._set_question_status(qid, "deferred")
            await self._task_from_deferred(qid, str(args.get("reason", "")))
            return self._plan_state()

        if name == "flag_new_finding":
            fid = ins(
                "findings", run_id=self.run_id, specialist_id=None,
                kind=args.get("kind", "gap") if args.get("kind") in
                     ("contradiction", "gap", "ambiguity") else "gap",
                severity="high",
                title=str(args.get("title", ""))[:200],
                detail=str(args.get("detail", "")),
                quotes_json=json.dumps(
                    [{"doc_title": "phone call", "quote": str(args.get("quote", ""))}]),
                patient_answerable=1,
            )
            row = one("SELECT * FROM findings WHERE id=?", (fid,))
            await events.broadcast(self.run_id, "finding.created", serialize.finding(row))
            return "flagged — continue the interview"

        if name == "end_call":
            self.ended = True
            return "call ending"

        return f"unknown tool {name}"

    async def _set_question_status(self, qid: int, status: str) -> None:
        ex("UPDATE questions SET status=? WHERE id=? AND run_id=?",
           (status, qid, self.run_id))
        row = one("SELECT * FROM questions WHERE id=?", (qid,))
        if row:
            await events.broadcast(self.run_id, "question.status", serialize.question(row))
        # advance the "asking" highlight to the next pending question
        nxt = one(
            "SELECT * FROM questions WHERE run_id=? AND status='pending' ORDER BY ord LIMIT 1",
            (self.run_id,),
        )
        if nxt:
            ex("UPDATE questions SET status='asking' WHERE id=?", (nxt["id"],))
            nxt = one("SELECT * FROM questions WHERE id=?", (nxt["id"],))
            await events.broadcast(self.run_id, "question.status", serialize.question(nxt))

    async def _task_from_deferred(self, qid: int, reason: str) -> None:
        row = one("SELECT * FROM questions WHERE id=?", (qid,))
        if not row:
            return
        fids = json.loads(row["finding_ids_json"] or "[]")
        finding_id = fids[0] if fids else 0
        spec_key = "general_medicine"
        if finding_id:
            f = one("SELECT specialist_id FROM findings WHERE id=?", (finding_id,))
            if f and f["specialist_id"]:
                s = one("SELECT key FROM specialists WHERE id=?", (f["specialist_id"],))
                if s:
                    spec_key = s["key"]
        tid = ins("specialist_tasks", run_id=self.run_id, finding_id=finding_id,
                  for_specialist=spec_key,
                  instruction=f"Resolve at visit: {row['question']}",
                  why=reason or "patient could not answer by phone")
        trow = one("SELECT * FROM specialist_tasks WHERE id=?", (tid,))
        await events.broadcast(self.run_id, "plan.task", serialize.specialist_task(trow))

    def _plan_state(self) -> str:
        rows = q("SELECT * FROM questions WHERE run_id=? ORDER BY ord", (self.run_id,))
        remaining = [r for r in rows if r["status"] in ("pending", "asking")]
        if not remaining:
            return ("All questions are answered or deferred. Give safety-netting, "
                    "confirm Monday's visit, say goodbye, then call end_call.")
        lines = "; ".join(f"QUESTION {r['id']}: {r['question']}" for r in remaining)
        return f"Recorded. Remaining questions in order: {lines}"

    # ---------------------------------------------------------------- finish

    async def _finish(self) -> None:
        if self._finished:
            return
        self._finished = True
        SESSIONS.pop(self.call_id, None)
        ex("UPDATE calls SET status='ended', ended_ts=? WHERE id=?",
           (now_iso(), self.call_id))
        row = one("SELECT * FROM calls WHERE id=?", (self.call_id,))
        await events.broadcast(self.run_id, "call.status", serialize.call(row))
        try:
            await self.transport.hangup()
        except Exception:
            log.exception("transport hangup failed (call=%s)", self.call_id)
        await self.on_end(self.run_id)


def _record_digest(run_id: int) -> str:
    """Short per-document digest for the interview system prompt (not the
    full corpus — the phone agent needs context, not the whole chart)."""
    run = one("SELECT * FROM runs WHERE id=?", (run_id,))
    docs = q("SELECT * FROM documents WHERE patient_id=? ORDER BY date, id",
             (run["patient_id"],))
    findings = q("SELECT * FROM findings WHERE run_id=? ORDER BY id", (run_id,))
    doc_lines = "\n".join(f"- {d['title']} ({d['author']}, {d['date']})" for d in docs)
    finding_lines = "\n".join(
        f"- [{f['kind']}] {f['title']}: {f['detail'][:200]}" for f in findings
    )
    return f"Documents on file:\n{doc_lines}\n\nIssues the review panel found:\n{finding_lines}"
