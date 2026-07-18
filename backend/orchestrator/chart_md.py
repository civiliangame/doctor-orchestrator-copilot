"""Markdown chart bridge — the PCM's link to the per-patient files in seed/patients.

Each patient row may point at a markdown chart file (patients.md_file). This module
keeps that file and the Patient Context Model in continuous two-way sync:

READ  (markdown -> PCM): `sync_from_markdown(visit_id)` hashes the file's
  hand/dataset-authored content (the DOC-managed section is excluded, so our own
  appends never re-trigger a read). When the content changed since the last sync,
  an LLM pass extracts what the chart establishes into slot contributions — each
  written through pcm.record_contribution with source_kind='seed',
  source_channel='chart_md', source_ref='file:<md_file>', quoting the file
  verbatim. Called at session start and at the top of every accumulator pass, so
  external edits fold in mid-session.

WRITE (PCM -> markdown): `append_update()` is invoked by pcm.record_contribution
  for every LIVE contribution (speech/typed/image/measurement/inferred — not
  fhir/seed, which came from the record), appending one provenance line under the
  '## Visit updates — DOC copilot' section. Append-only: the authored part of the
  file is never rewritten (same discipline as chart_entries).
"""

import asyncio
import hashlib
import logging
import re
import threading

import events
from config import MODEL_SONNET, PATIENTS_DIR
from db import ex, ins, now_iso, one, q
from llm import block

from orchestrator.llm_call import complete_json

log = logging.getLogger("doc.orchestrator")

MANAGED_HEADER = "## Visit updates — DOC copilot"
DEMO_MD_FILE = "00-maria-alvarez.md"   # hand-written demo patient (Maria, seed.py)

MAX_INGEST_SLOTS = 14
_INGEST_STATUS = ("known", "uncertain", "stale")
_CATEGORIES = ("symptom", "vital", "medication", "risk", "history", "logistics")
_KEY_RE = re.compile(r"^[a-z0-9_]+(\.[a-z0-9_]+)*$")

# Provenance actor for everything ingested FROM the file. source_kind='seed' is a
# non-live kind, so record_contribution never mirrors it back into the file.
FILE_ACTOR = {
    "source_kind": "seed", "source_channel": "chart_md", "actor_role": "system",
    "actor_id": "chart_md", "actor_name": "Patient chart file",
    "from_patient": False, "extracted_from_speech": False,
}

_file_lock = threading.Lock()                 # serializes read-modify-write appends
_visit_locks: dict[int, asyncio.Lock] = {}    # one concurrent ingest per visit


def _visit_lock(visit_id: int) -> asyncio.Lock:
    return _visit_locks.setdefault(visit_id, asyncio.Lock())


# ---------------------------------------------------------------- file helpers

def _patient_path(visit_id: int):
    """(visit, patient, path) for a visit whose patient has a chart file, else None."""
    visit = one("SELECT * FROM visits WHERE id=?", (visit_id,))
    if visit is None:
        return None
    patient = one("SELECT * FROM patients WHERE id=?", (visit["patient_id"],))
    if not patient or not patient.get("md_file"):
        return None
    path = PATIENTS_DIR / patient["md_file"]
    if not path.exists():
        return None
    return visit, patient, path


def _split_managed(text: str) -> tuple[str, str]:
    """(authored content, DOC-managed section). Hashing only the authored part
    makes our own appends invisible to the change detector."""
    idx = text.find(MANAGED_HEADER)
    if idx == -1:
        return text, ""
    return text[:idx], text[idx:]


def _hash(text: str) -> str:
    # Trailing-newline normalization: appending the managed section rstrips the
    # authored part, which must not read as an external change.
    return hashlib.sha256(text.rstrip("\n").encode("utf-8")).hexdigest()


def _upsert_state(visit_id: int, path: str, content_hash: str | None = None,
                  synced: bool = False, written: bool = False) -> None:
    ts = now_iso()
    row = one("SELECT * FROM chart_files WHERE visit_id=?", (visit_id,))
    if row is None:
        ins("chart_files", visit_id=visit_id, path=path,
            content_hash=content_hash or "",
            last_synced_ts=ts if synced else "", last_written_ts=ts if written else "")
        return
    sets, params = ["path=?"], [path]
    if content_hash is not None:
        sets.append("content_hash=?"); params.append(content_hash)
    if synced:
        sets.append("last_synced_ts=?"); params.append(ts)
    if written:
        sets.append("last_written_ts=?"); params.append(ts)
    params.append(visit_id)
    ex(f"UPDATE chart_files SET {', '.join(sets)} WHERE visit_id=?", tuple(params))


def mark_synced(visit_id: int) -> None:
    """Record the file's current authored-content hash WITHOUT ingesting — used at
    seed time for the demo patient, whose PCM is seeded from SEED_FACTS instead."""
    found = _patient_path(visit_id)
    if found is None:
        return
    _, _, path = found
    external, _ = _split_managed(path.read_text(encoding="utf-8"))
    _upsert_state(visit_id, str(path), content_hash=_hash(external), synced=True)


# ---------------------------------------------------------------- write path

def _one_line(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    return text[: limit - 1] + "…" if len(text) > limit else text


def append_update(visit_id: int, slot: dict, ledger: dict) -> None:
    """Append one PCM contribution to the patient's chart file. Best-effort: any
    failure is logged, never raised into the orchestrator's write path."""
    try:
        found = _patient_path(visit_id)
        if found is None:
            return
        visit, _, path = found
        node = one("SELECT station FROM journey_nodes WHERE id=?", (ledger["node_id"],)) \
            if ledger.get("node_id") else None
        who = ledger["actor_name"] or ledger["actor_role"]
        via = ledger["source_kind"] + (f" @ {node['station']}" if node else "")
        line = (f"- {ledger['ts']} · visit {visit['date']} · **{slot['key']}** → "
                f"{slot['status']} ({slot['confidence']:.2f}): {_one_line(slot['value'], 200)}"
                f" — {who} ({via})")
        quote = _one_line(ledger["raw_quote"], 160)
        if quote:
            line += f' — "{quote}"'
        with _file_lock:
            text = path.read_text(encoding="utf-8")
            if MANAGED_HEADER not in text:
                text = (text.rstrip("\n")
                        + f"\n\n{MANAGED_HEADER}\n\n"
                        + "*Live Patient Context Model updates, appended by DOC with full "
                        + "provenance. Append-only; the sections above are never rewritten.*\n\n"
                        + line + "\n")
            else:
                text = text.rstrip("\n") + "\n" + line + "\n"
            path.write_text(text, encoding="utf-8")
        _upsert_state(visit_id, str(path), written=True)
    except Exception:
        log.exception("chart_md append failed (visit=%s slot=%s)", visit_id, slot.get("key"))


# ---------------------------------------------------------------- read path

CHART_READER_SYSTEM = """You are DOC's chart file reader. You are given a patient's markdown chart file and the Patient Context Model (PCM) slots already tracked for TODAY's visit. Convert what the FILE establishes into slot updates.

Rules:
- Prefer the EXISTING slot keys listed in the user message when the file speaks to them. Otherwise mint a new key: lowercase dotted snake_case, e.g. "migraine.frequency", "bp.current", "med.lisinopril_adherence". At most {max_slots} slots total — pick the ones most relevant to today's visit.
- status: "known" for facts the file clearly establishes as current; "stale" for values from a PRIOR visit that today's visit should re-verify (old vitals, old symptom descriptions); "uncertain" for hedged or incomplete facts.
- "quote" MUST be copied verbatim from the file — it is stored as the provenance citation.
- "value" is concise clinical shorthand. "label" is a short human display label. "category" is one of: symptom, vital, medication, risk, history, logistics.
- "why_required" says which part of today's visit makes the slot worth tracking (cite the visit title/intent or the file section).
- Do not re-emit a slot whose current PCM value already reflects the file.

Output schema (one JSON object, nothing else):
{{"slot_updates": [{{
  "key": "existing.or.new_key", "label": "short display label",
  "category": "symptom|vital|medication|risk|history|logistics",
  "value": "concise clinical shorthand", "status": "known|uncertain|stale",
  "confidence": 0.0, "quote": "verbatim text from the file",
  "why_required": "short reason this visit needs it"
}}]}}"""


async def _extract_slots(visit: dict, patient: dict, file_text: str) -> list[dict]:
    slot_rows = q(
        "SELECT key, label, status, value FROM context_slots WHERE patient_id=? ORDER BY category, key",
        (patient["id"],),
    )
    slot_lines = "\n".join(
        f"- {s['key']} [{s['status']}] {s['label']}: {s['value'] or '(unknown)'}"
        for s in slot_rows
    ) or "(none yet — mint the keys this visit needs)"
    user = f"""== TODAY'S VISIT ==
Patient: {patient['name']} (DOB {patient['dob']})
Visit date: {visit['date']}
Doctor's intent: {visit['intent_text'] or '(none written yet)'}

== EXISTING PCM SLOTS (prefer these keys) ==
{slot_lines}

== PATIENT CHART FILE ({patient['md_file']}) ==
{file_text}"""
    system = [block(CHART_READER_SYSTEM.format(max_slots=MAX_INGEST_SLOTS))]
    out = await complete_json(MODEL_SONNET, system, user, max_tokens=2000)
    return out.get("slot_updates") or []


def _apply_ingest(visit: dict, patient: dict, items: list[dict]) -> list[dict]:
    """Write extracted facts through the PCM's single write path (patient-scoped,
    source_ref = the chart file). A why_required marks the slot as required for
    THIS visit. Returns the changed slot rows (no-ops and rejects are dropped)."""
    from orchestrator import pcm
    changed = []
    for item in items[:MAX_INGEST_SLOTS]:
        key = (item.get("key") or "").strip().lower()
        value = (item.get("value") or "").strip()
        if not value or not _KEY_RE.match(key):
            continue
        status = item.get("status") if item.get("status") in _INGEST_STATUS else "uncertain"
        try:
            confidence = float(item.get("confidence"))
        except (TypeError, ValueError):
            confidence = 0.5
        label = (item.get("label") or "").strip() or key.replace(".", " ").replace("_", " ")
        category = item.get("category") if item.get("category") in _CATEGORIES else "history"
        slot = pcm.record_contribution(
            patient["id"], key, value, status, confidence,
            visit_id=visit["id"], label=label, category=category,
            source_ref=f"file:{patient['md_file']}",
            raw_quote=(item.get("quote") or "").strip(), **FILE_ACTOR,
        )
        pcm.add_requirement(
            visit["id"], key,
            (item.get("why_required") or "").strip() or "Established by the patient chart file",
        )
        if slot is not None:
            changed.append(slot)
    return changed


async def sync_from_markdown(visit_id: int, session_id: int | None = None,
                             force: bool = False) -> bool:
    """Fold the patient's chart file into the PCM if its authored content changed
    since the last sync. Cheap when unchanged (one file read + hash). Returns True
    when an ingest ran. Pass session_id to broadcast the resulting slot updates."""
    found = _patient_path(visit_id)
    if found is None:
        return False
    visit, patient, path = found
    async with _visit_lock(visit_id):
        external, _ = _split_managed(path.read_text(encoding="utf-8"))
        h = _hash(external)
        state = one("SELECT * FROM chart_files WHERE visit_id=?", (visit_id,))
        if state and state["content_hash"] == h and not force:
            return False
        items = await _extract_slots(visit, patient, external)
        changed = _apply_ingest(visit, patient, items)
        _upsert_state(visit_id, str(path), content_hash=h, synced=True)
    log.info("chart_md ingest: %s -> visit %s (%d extracted, %d applied)",
             patient["md_file"], visit_id, len(items), len(changed))
    if session_id is not None and changed:
        from orchestrator import pcm
        completeness = pcm.completeness(visit_id)
        req = pcm.requirements_for(visit_id)
        for slot in changed:
            await events.broadcast(session_id, "context.slot_updated", {
                "slot": pcm.slot_shape(slot, req, visit_id), "completeness": completeness,
            })
    return True


# ---------------------------------------------------------------- demo patient

def ensure_demo_patient_file() -> None:
    """Maria (the hand-written demo patient) predates the dataset files — write her
    a chart file so the PCM write path has somewhere to land, and mark her visit
    synced so seed_context's carefully staged SEED_FACTS are not re-ingested over."""
    patient = one("SELECT * FROM patients WHERE md_file=?", (DEMO_MD_FILE,))
    if patient is None:
        return
    path = PATIENTS_DIR / DEMO_MD_FILE
    if not path.exists():
        path.write_text(
            f"""---
name: {patient['name']}
birth_date: {patient['dob']}
dataset: hand-written-demo
synthetic: true
---

# {patient['name']} — cardiac follow-up

> Hand-written demo patient (source of truth: backend/seed.py). Not a real person.

## Summary

{patient['summary_text']}
""",
            encoding="utf-8",
        )
    visit = one("SELECT * FROM visits WHERE patient_id=? ORDER BY id DESC LIMIT 1",
                (patient["id"],))
    if visit and one("SELECT id FROM chart_files WHERE visit_id=?", (visit["id"],)) is None:
        mark_synced(visit["id"])
