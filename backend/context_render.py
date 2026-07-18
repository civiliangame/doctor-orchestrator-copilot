"""Markdown projection of the Patient Context Model.

A patient's context file is a RENDERING of the PCM, never a parallel source of
truth: every line is a slot's current value, footnoted with the ledger entry
that justifies it (source_ref → the exact FHIR resource / transcript turn /
note, plus who contributed it and when). Regenerating after new information
arrives — a scribe session, a new bundle — reflows the same document from the
updated belief state.

Used by scripts/build_patient_contexts.py (seed corpus on disk) and
GET /api/patients/{id}/context.md (live).
"""

import json
import re

from db import jloads, one, q

# Section order + headings for the Current status body.
_SECTIONS = [
    ("encounter", "Encounter"),
    ("problem", "Problems"),
    ("history", "Medical / surgical history"),
    ("medication", "Medications"),
    ("symptom", "Symptoms"),
    ("social", "Social context"),
    ("vital", "Vitals"),
    ("lab", "Labs"),
    ("assessment", "Assessments & screenings"),
    ("procedure", "Procedures"),
    ("imaging", "Imaging"),
    ("report", "Reports"),
    ("immunization", "Immunizations"),
    ("risk", "Risk factors"),
    ("logistics", "Logistics"),
]

_SOURCE_LABEL = {
    "fhir": "FHIR record", "seed": "prior note", "speech": "live speech",
    "typed": "typed", "image": "imaging", "measurement": "measured",
    "inferred": "inferred",
}


def yaml_str(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if re.search(r"[:#\[\]{}\"'|>&*!%@`,]|^\s|\s$|^$", s):
        return json.dumps(s, ensure_ascii=False)
    return s


def short_ref(ref: str, max_len: int = 110) -> str:
    """Display form of a source_ref. Collapsed series can cite dozens of
    resources — keep the first two and count the rest (the ledger holds all)."""
    if len(ref) <= max_len or "#" not in ref:
        return ref
    head, parts = ref.split("#", 1)
    items = parts.split(",")
    if len(items) <= 2:
        return ref
    return f"{head}#{','.join(items[:2])} +{len(items) - 2} more"


def _footnote(prov: dict, history_n: int) -> str:
    """One ledger entry -> footnote text: ref — who (how), when. “quote”"""
    bits = []
    if prov["source_ref"]:
        bits.append(f"`{short_ref(prov['source_ref'])}`")
    who = prov["actor_name"] or prov["actor_role"]
    how = _SOURCE_LABEL.get(prov["source_kind"], prov["source_kind"])
    if prov["from_patient"]:
        how = "patient, " + ("live speech" if prov["extracted_from_speech"] else how)
    bits.append(f"{who} ({how})")
    # FHIR facts carry their clinical date in the value/quote; the ledger ts is
    # merely ingest time and would churn every regeneration — omit it there.
    if prov["ts"] and prov["source_kind"] != "fhir":
        bits.append(prov["ts"][:10])
    line = " — ".join([bits[0], ", ".join(bits[1:])]) if prov["source_ref"] else ", ".join(bits)
    if prov["raw_quote"] and prov["source_kind"] in ("speech", "typed", "seed"):
        line += f" — “{prov['raw_quote']}”"
    if history_n > 1:
        line += f" · {history_n} ledger entries"
    return line


def render_patient_md(patient_id: int) -> str:
    patient = one("SELECT * FROM patients WHERE id=?", (patient_id,))
    if patient is None:
        raise ValueError(f"unknown patient {patient_id}")
    meta = jloads(patient.get("meta_json"), {}) or {}
    slots = q("SELECT * FROM context_slots WHERE patient_id=? ORDER BY id", (patient_id,))
    ledger_counts = {r["slot_key"]: r["n"] for r in q(
        "SELECT slot_key, COUNT(*) AS n FROM context_ledger WHERE patient_id=? GROUP BY slot_key",
        (patient_id,))}
    source_counts = q(
        "SELECT source_kind, COUNT(*) AS n FROM context_ledger WHERE patient_id=? "
        "GROUP BY source_kind ORDER BY n DESC", (patient_id,))
    total_ledger = sum(r["n"] for r in source_counts)

    fm = [
        ("name", patient["name"]),
        ("dob", patient["dob"]),
        ("gender", meta.get("gender")),
        ("city", meta.get("city")),
        ("marital_status", meta.get("marital_status")),
        ("language", meta.get("language")),
        ("fhir_patient_id", patient.get("fhir_patient_id") or None),
        ("record_id", meta.get("record_id")),
        ("dataset", meta.get("dataset")),
        ("last_encounter", meta.get("visit_date")),
        ("source", "patient-context-model"),
        ("slots", len(slots)),
        ("ledger_entries", total_ledger),
        ("synthetic", meta.get("synthetic", False)),
    ]
    lines = ["---"]
    lines += [f"{k}: {yaml_str(v)}" for k, v in fm if v is not None]
    lines += ["---", ""]
    lines.append(f"# {patient['name']} — patient context")
    lines.append("")
    if meta.get("synthetic"):
        lines.append("> Fully synthetic patient (Synthea + LLM transcript). Not a real person.")
        lines.append("")

    if patient["summary_text"]:
        lines.append("## Summary")
        lines.append("")
        lines.append(patient["summary_text"])
        lines.append("")

    lines.append("## Current status")
    lines.append("")
    lines.append(
        "Every line is a belief in the Patient Context Model; its footnote is the "
        "ledger entry justifying it — the exact FHIR resource, transcript turn, or "
        "note it came from, and who contributed it."
    )
    lines.append("")

    by_category: dict[str, list[dict]] = {}
    for s in slots:
        by_category.setdefault(s["category"], []).append(s)

    footnotes: list[str] = []

    def line_for(s: dict) -> str:
        value = s["value"] or "— not yet gathered"
        marker = "" if s["status"] == "known" else f" _({s['status']})_"
        note = ""
        if s["current_ledger_id"]:
            prov = one("SELECT * FROM context_ledger WHERE id=?", (s["current_ledger_id"],))
            if prov:
                footnotes.append(_footnote(prov, ledger_counts.get(s["key"], 1)))
                note = f"[^{len(footnotes)}]"
        return f"- **{s['label']}:** {value}{marker}{note}"

    ordered = [c for c, _ in _SECTIONS] + sorted(
        c for c in by_category if c not in {c for c, _ in _SECTIONS})
    headings = dict(_SECTIONS)
    for category in ordered:
        items = by_category.get(category)
        if not items:
            continue
        lines.append(f"**{headings.get(category, category.capitalize())}**")
        lines += [line_for(s) for s in items]
        lines.append("")

    lines.append("## Provenance")
    lines.append("")
    src_bits = ", ".join(f"{r['n']} {_SOURCE_LABEL.get(r['source_kind'], r['source_kind'])}"
                         for r in source_counts) or "none"
    lines.append(
        f"Rendered from the Patient Context Model ({len(slots)} slots; "
        f"{total_ledger} ledger entries — {src_bits}). The ledger is append-only: "
        f"the patient's context at any past moment is reconstructable by replaying it. "
        f"Live version: `GET /api/patients/<id>/context.md`; seed corpus: "
        f"`uv run python scripts/build_patient_contexts.py`."
    )
    lines.append("")
    for i, fn in enumerate(footnotes, 1):
        lines.append(f"[^{i}]: {fn}")
    lines.append("")
    return "\n".join(lines)
