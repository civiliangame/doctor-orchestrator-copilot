"""Build per-patient context files from the synthetic-ambient-fhir-25 dataset.

Deterministic extraction — no LLM. Each of the 25 dataset records (one
encounter per synthetic patient) becomes one markdown context file with YAML
frontmatter, in the style of the hand-written Maria Alvarez summary in
backend/seed.py: a narrative summary block plus structured chart background
and encounter findings, all grounded strictly in the record's FHIR resources.

Usage:
    uv run python scripts/build_patient_contexts.py \
        [--dataset synthetic-ambient-fhir-25/synthetic-ambient-fhir-25.jsonl] \
        [--out backend/seed/patients]

Outputs <NN>-<first>-<last>.md per patient, plus index.json (machine-readable
roster) and README.md (human roster) in the output directory.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import OrderedDict
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Label buckets. The dataset is closed (25 records, fixed Synthea modules), so
# social/administrative labels are matched exactly; anything unknown defaults
# to the clinically safe bucket (problem list).
# ---------------------------------------------------------------------------

SOCIAL_LABELS = {
    "Educated to high school level (finding)",
    "Received higher education (finding)",
    "Has a criminal record (finding)",
    "Housing unsatisfactory (finding)",
    "Lack of access to transportation (finding)",
    "Transport problem (finding)",
    "Limited social contact (finding)",
    "Social isolation (finding)",
    "Not in labor force (finding)",
    "Unemployed (finding)",
    "Serving in military service (finding)",
    "Refugee (person)",
    "Reports of violence in the environment (finding)",
    "Risk activity involvement (finding)",
    "Victim of intimate partner abuse (finding)",
    "Stress (finding)",
    "Medication review due (situation)",
}

ENCOUNTER_CLASS = {
    "AMB": "ambulatory",
    "IMP": "inpatient",
    "EMER": "emergency",
    "HH": "home health",
    "ACUTE": "acute inpatient",
    "NONAC": "non-acute inpatient",
    "OBSENC": "observation",
    "PRENC": "pre-admission",
    "SS": "short stay",
    "VR": "virtual",
}

UNIT_DISPLAY = {
    "mm[Hg]": "mmHg",
    "kg/m2": "kg/m²",
    "Cel": "°C",
    "[degF]": "°F",
    "{score}": "",
    "{#}": "",
    "{INR}": "",
    "10*3/uL": "10³/µL",
    "10*6/uL": "10⁶/µL",
}

# Friendlier display names for the common vital-sign LOINC texts.
VITAL_RENAME = {
    "Body Height": "Height",
    "Body Weight": "Weight",
    "Body mass index (BMI) [Ratio]": "BMI",
    "Pain severity - 0-10 verbal numeric rating [Score] - Reported": "Pain severity (0–10)",
    "Oxygen saturation in Arterial blood": "O2 saturation",
    "Body temperature": "Temperature",
    "Head Occipital-frontal circumference": "Head circumference",
}


def strip_tag(label: str) -> str:
    """Drop the SNOMED semantic tag suffix: 'Gingivitis (disorder)' -> 'Gingivitis'."""
    return re.sub(r"\s*\((disorder|finding|situation|person|procedure|regime/therapy|qualifier value)\)$", "", label)


def clean_name(part: str) -> str:
    """Synthea names may carry numeric suffixes ('Ali918') — strip them."""
    return re.sub(r"\d+", "", part).strip()


def title_org(name: str) -> str:
    t = name.title()
    t = re.sub(r"'S\b", "'s", t)
    for raw, fixed in (("Llc", "LLC"), ("Pc", "PC"), ("Snf", "SNF"), ("Ii", "II")):
        t = re.sub(rf"\b{raw}\b", fixed, t)
    return t


def fmt_num(v) -> str:
    if isinstance(v, float):
        return f"{round(v, 1):g}"
    return str(v)


def fmt_quantity(q: dict) -> str:
    unit = q.get("unit") or q.get("code") or ""
    unit = UNIT_DISPLAY.get(unit, unit)
    val = fmt_num(q.get("value"))
    return f"{val} {unit}".strip()


def cc_text(cc: dict | None) -> str | None:
    """CodeableConcept -> display text."""
    if not cc:
        return None
    if cc.get("text"):
        return cc["text"]
    for coding in cc.get("coding", []):
        if coding.get("display"):
            return coding["display"]
    return None


def age_at(birth: str, on: str) -> int:
    b, o = date.fromisoformat(birth), date.fromisoformat(on[:10])
    return o.year - b.year - ((o.month, o.day) < (b.month, b.day))


# ---------------------------------------------------------------------------
# Observation extraction
# ---------------------------------------------------------------------------

def obs_value(o: dict) -> str | None:
    if o.get("valueQuantity"):
        return fmt_quantity(o["valueQuantity"])
    if o.get("valueCodeableConcept"):
        t = cc_text(o["valueCodeableConcept"])
        return strip_tag(t) if t else None
    if o.get("component"):
        parts = {}
        for comp in o["component"]:
            name = cc_text(comp.get("code")) or ""
            if comp.get("valueQuantity"):
                parts[name] = comp["valueQuantity"]
        sys_q = next((q for n, q in parts.items() if "Systolic" in n), None)
        dia_q = next((q for n, q in parts.items() if "Diastolic" in n), None)
        if sys_q and dia_q:
            return f"{fmt_num(sys_q.get('value'))}/{fmt_num(dia_q.get('value'))} mmHg"
        return "; ".join(f"{n} {fmt_quantity(q)}" for n, q in parts.items()) or None
    return None


def obs_category(o: dict) -> str:
    for cat in o.get("category", []):
        for coding in cat.get("coding", []):
            if coding.get("code"):
                return coding["code"]
    return "other"


def collect_observations(observations: list[dict]) -> dict[str, list[dict]]:
    """Group by category, dedupe by code. Repeated codes (hospital stays record
    daily vitals/labs) collapse to 'first → latest (n readings)'."""
    by_code: OrderedDict[str, dict] = OrderedDict()
    for o in sorted(observations, key=lambda x: x.get("effectiveDateTime", "")):
        code = cc_text(o.get("code")) or "Observation"
        val = obs_value(o)
        if val is None:
            continue
        entry = by_code.setdefault(code, {"category": obs_category(o), "values": []})
        entry["values"].append(val)

    grouped: dict[str, list[dict]] = {"vital-signs": [], "laboratory": [], "other": []}
    for code, entry in by_code.items():
        vals = entry["values"]
        if len(vals) == 1:
            display = vals[0]
        elif vals[0] == vals[-1]:
            display = f"{vals[-1]} ({len(vals)} readings, stable)"
        else:
            display = f"{vals[0]} → {vals[-1]} ({len(vals)} readings)"
        # BP panels read better as plain 'Blood pressure'
        name = "Blood pressure" if code.startswith("Blood pressure panel") else VITAL_RENAME.get(code, code)
        cat = entry["category"] if entry["category"] in grouped else "other"
        grouped[cat].append({"name": name, "value": display, "n": len(vals), "latest": vals[-1]})
    return grouped


def find_latest(grouped: dict, *needles: str) -> str | None:
    for cat in grouped.values():
        for item in cat:
            if any(item["name"].startswith(n) for n in needles):
                return item["latest"]
    return None


# ---------------------------------------------------------------------------
# Per-record extraction
# ---------------------------------------------------------------------------

def dedupe_count(names: list[str]) -> list[str]:
    counts: OrderedDict[str, int] = OrderedDict()
    for n in names:
        counts[n] = counts.get(n, 0) + 1
    return [n if c == 1 else f"{n} ×{c}" for n, c in counts.items()]


def extract(rec: dict) -> dict:
    meta = rec["metadata"]
    patient = rec["patient_context"]["patient"]
    longi = rec["patient_context"]["longitudinal_summary"]
    enc = rec["encounter_fhir"]["encounter"]
    rr = rec["encounter_fhir"]["related_resources"]

    # --- identity ---
    name_rec = (patient.get("name") or [{}])[0]
    given = clean_name((name_rec.get("given") or [""])[0])
    family = clean_name(name_rec.get("family") or "")
    full_name = f"{given} {family}".strip() or f"Patient {patient['id'][:8]}"
    gender = patient.get("gender", "unknown")
    noun = {"male": "man", "female": "woman"}.get(gender, "person")
    birth = patient.get("birthDate", "")
    visit_date = meta["date"][:10]
    age = age_at(birth, visit_date) if birth else None
    addr = (patient.get("address") or [{}])[0]
    place = ", ".join(p for p in (addr.get("city"), addr.get("state")) if p)
    marital = cc_text(patient.get("maritalStatus"))
    language = None
    for comm in patient.get("communication", []):
        language = cc_text(comm.get("language")) or language

    # --- chart background ---
    problems, history, social = [], [], []
    for label in longi.get("condition_labels", []):
        if label in SOCIAL_LABELS:
            social.append(strip_tag(label))
        elif label.endswith("(situation)"):
            history.append(strip_tag(label))
        else:
            problems.append(strip_tag(label))
    meds = longi.get("medication_labels", [])
    counts = longi.get("resource_counts", {})

    # --- encounter ---
    enc_class = ENCOUNTER_CLASS.get((enc.get("class") or {}).get("code", ""), (enc.get("class") or {}).get("code", ""))
    provider = (enc.get("serviceProvider") or {}).get("display")
    provider = title_org(provider) if provider else None
    period = enc.get("period", {})

    enc_conditions = []
    for c in rr.get("Condition", []):
        status = ((c.get("clinicalStatus") or {}).get("coding") or [{}])[0].get("code", "")
        label = strip_tag(cc_text(c.get("code")) or "Condition")
        enc_conditions.append(f"{label}" + (f" ({status})" if status else ""))

    grouped_obs = collect_observations(rr.get("Observation", []))

    smoking = None
    for cat in grouped_obs.values():
        for item in cat:
            if item["name"].startswith("Tobacco smoking status"):
                smoking = item["latest"]

    procedures = dedupe_count([strip_tag(cc_text(p.get("code")) or "Procedure") for p in rr.get("Procedure", [])])
    reports = dedupe_count([cc_text(d.get("code")) or "Report" for d in rr.get("DiagnosticReport", [])])
    immunizations = [cc_text(i.get("vaccineCode")) or "Immunization" for i in rr.get("Immunization", [])]
    imaging = [cc_text((s.get("procedureCode") or [None])[0]) or "Imaging study" for s in rr.get("ImagingStudy", [])]

    med_orders, unresolved_orders = [], 0
    for m in rr.get("MedicationRequest", []):
        label = cc_text(m.get("medicationCodeableConcept"))
        if not label and m.get("medicationReference"):
            label = m["medicationReference"].get("display")
        if label:
            status = m.get("status", "")
            med_orders.append(label + (f" ({status})" if status and status != "active" else ""))
        else:
            unresolved_orders += 1
    med_orders = dedupe_count(med_orders)
    if unresolved_orders:
        med_orders.append(f"{unresolved_orders} additional medication order(s) (unnamed reference)")

    return {
        "record_id": rec["id"],
        "patient_id": meta["patient_id"],
        "encounter_id": meta["encounter_id"],
        "name": full_name,
        "gender": gender,
        "noun": noun,
        "birth_date": birth,
        "age": age,
        "place": place,
        "marital": marital,
        "language": language,
        "smoking": smoking,
        "visit_date": visit_date,
        "visit_title": meta["visit_title"],
        "visit_type": meta["visit_type"],
        "enc_class": enc_class,
        "provider": provider,
        "period_start": period.get("start", ""),
        "period_end": period.get("end", ""),
        "problems": problems,
        "history": history,
        "social": social,
        "meds": meds,
        "record_counts": counts,
        "enc_conditions": enc_conditions,
        "obs": grouped_obs,
        "procedures": procedures,
        "reports": reports,
        "immunizations": immunizations,
        "imaging": imaging,
        "med_orders": med_orders,
        "transcript_words": meta.get("transcript_words") or len(rec.get("transcript", "").split()),
        "note_words": meta.get("note_words") or len(rec.get("note", "").split()),
    }


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def narrative(x: dict) -> str:
    """Maria-style summary block: usable verbatim as an orchestrator prompt."""
    bits = [f"{x['name']}, {x['age']}-year-old {x['noun']} (DOB {x['birth_date']})"]
    if x["place"]:
        bits.append(x["place"])
    p1 = ". ".join([", ".join(bits)]) + "."
    if x["smoking"]:
        p1 += f" Tobacco: {x['smoking'].lower()}."
    if x["problems"]:
        p1 += " Problem list: " + "; ".join(x["problems"]) + "."
    else:
        p1 += " No chronic problems on the chart."
    if x["history"]:
        p1 += " History: " + "; ".join(x["history"]) + "."
    if x["meds"]:
        p1 += " Current medications on record: " + "; ".join(x["meds"]) + "."
    else:
        p1 += " No current medications on record."
    if x["social"]:
        p1 += " Social context: " + "; ".join(x["social"]) + "."

    where = " at ".join(p for p in (x["enc_class"], x["provider"]) if p)
    p2 = f"Visit {x['visit_date']} ({where}): {x['visit_title']}."
    vitals_bits = []
    bp = find_latest(x["obs"], "Blood pressure")
    hr = find_latest(x["obs"], "Heart rate")
    temp = find_latest(x["obs"], "Temperature")
    spo2 = find_latest(x["obs"], "O2 saturation")
    bmi = find_latest(x["obs"], "BMI")
    if bp:
        vitals_bits.append(f"BP {bp.replace(' mmHg', '')}")
    if hr:
        vitals_bits.append(f"HR {hr.replace(' /min', '')}")
    if temp:
        vitals_bits.append(f"T {temp}")
    if spo2:
        vitals_bits.append(f"SpO2 {spo2}")
    if bmi:
        vitals_bits.append(f"BMI {bmi.replace(' kg/m²', '')}")
    if vitals_bits:
        p2 += " Vitals: " + ", ".join(vitals_bits) + "."
    if x["enc_conditions"]:
        p2 += " Recorded this visit: " + "; ".join(x["enc_conditions"]) + "."
    return p1 + "\n\n" + p2


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


def render_md(x: dict, dataset_name: str) -> str:
    fm_fields = [
        ("record_id", x["record_id"]),
        ("patient_id", x["patient_id"]),
        ("encounter_id", x["encounter_id"]),
        ("name", x["name"]),
        ("gender", x["gender"]),
        ("birth_date", x["birth_date"]),
        ("age_at_visit", x["age"]),
        ("visit_date", x["visit_date"]),
        ("visit_title", x["visit_title"]),
        ("visit_type", x["visit_type"]),
        ("encounter_class", x["enc_class"]),
        ("provider", x["provider"]),
        ("city", x["place"] or None),
        ("marital_status", x["marital"]),
        ("language", x["language"]),
        ("transcript_words", x["transcript_words"]),
        ("note_words", x["note_words"]),
        ("dataset", dataset_name),
        ("synthetic", True),
    ]
    lines = ["---"]
    lines += [f"{k}: {yaml_str(v)}" for k, v in fm_fields]
    lines.append("---")
    lines.append("")
    lines.append(f"# {x['name']} — {x['visit_title']}")
    lines.append("")
    lines.append("> Fully synthetic patient (Synthea + LLM transcript). Not a real person.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(narrative(x))
    lines.append("")

    lines.append("## Chart background (full record)")
    lines.append("")

    def section(title: str, items: list[str], empty: str | None = None):
        if items:
            lines.append(f"**{title}**")
            lines.extend(f"- {i}" for i in items)
            lines.append("")
        elif empty:
            lines.append(f"**{title}:** {empty}")
            lines.append("")

    section("Problem list", x["problems"], "none recorded")
    section("Medical / surgical history", x["history"])
    section("Current medications", x["meds"], "none recorded")
    section("Social & administrative context", x["social"])
    rc = x["record_counts"]
    depth = ", ".join(f"{v} {k}" for k, v in sorted(rc.items(), key=lambda kv: -kv[1]) if k != "Patient")
    lines.append(f"**Record depth:** {depth}")
    lines.append("")

    hdr = f"## This encounter — {x['visit_date']}"
    lines.append(hdr)
    lines.append("")
    where = " · ".join(p for p in (x["enc_class"], x["provider"], x["visit_type"]) if p)
    lines.append(f"*{where}*")
    lines.append("")
    section("Conditions recorded", x["enc_conditions"])
    section("Vitals", [f"{o['name']}: {o['value']}" for o in x["obs"]["vital-signs"]])
    section("Labs", [f"{o['name']}: {o['value']}" for o in x["obs"]["laboratory"]])
    section("Assessments & screenings", [f"{o['name']}: {o['value']}" for o in x["obs"]["other"]])
    section("Procedures", x["procedures"])
    section("Imaging", x["imaging"])
    section("Reports", x["reports"])
    section("Medications ordered", x["med_orders"])
    section("Immunizations", x["immunizations"])

    lines.append("## Provenance")
    lines.append("")
    lines.append(
        f"Derived deterministically from `{dataset_name}` record `{x['record_id']}` "
        f"(FHIR R4, Synthea). The paired ambient transcript ({x['transcript_words']} words) "
        f"and clinical note ({x['note_words']} words) live in the dataset record, keyed by "
        f"`record_id`. Regenerate: `uv run python scripts/build_patient_contexts.py`."
    )
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    repo_root = Path(__file__).resolve().parent.parent
    ap.add_argument("--dataset", type=Path,
                    default=repo_root / "synthetic-ambient-fhir-25" / "synthetic-ambient-fhir-25.jsonl")
    ap.add_argument("--out", type=Path, default=repo_root / "backend" / "seed" / "patients")
    args = ap.parse_args()

    records = [json.loads(l) for l in args.dataset.read_text().splitlines() if l.strip()]
    dataset_name = args.dataset.stem
    args.out.mkdir(parents=True, exist_ok=True)

    index = []
    roster_rows = []
    for i, rec in enumerate(records, 1):
        x = extract(rec)
        slug = re.sub(r"[^a-z0-9]+", "-", f"{x['name']}".lower()).strip("-")
        fname = f"{i:02d}-{slug}.md"
        (args.out / fname).write_text(render_md(x, dataset_name))
        index.append({
            "file": fname,
            "record_id": x["record_id"],
            "patient_id": x["patient_id"],
            "encounter_id": x["encounter_id"],
            "name": x["name"],
            "gender": x["gender"],
            "birth_date": x["birth_date"],
            "age_at_visit": x["age"],
            "visit_date": x["visit_date"],
            "visit_title": x["visit_title"],
            "visit_type": x["visit_type"],
            "encounter_class": x["enc_class"],
            "problems": x["problems"],
            "medications": x["meds"],
            "summary_text": narrative(x),
        })
        roster_rows.append(
            f"| [{x['name']}]({fname}) | {x['age']}{x['gender'][:1].upper()} | {x['visit_date']} | {x['visit_title']} |"
        )
        print(f"  {fname:44s} {x['age']:>3}{x['gender'][:1].upper()}  {x['visit_title']}")

    (args.out / "index.json").write_text(json.dumps(
        {"dataset": dataset_name, "synthetic": True, "patients": index}, indent=1, ensure_ascii=False))

    readme = [
        "# Synthetic patient context files",
        "",
        f"One context file per synthetic patient in the `{dataset_name}` dataset",
        "(25 patients, one encounter each). Each file pairs YAML frontmatter with a",
        "narrative **Summary** block (same role as the hand-written Maria Alvarez",
        "summary in `backend/seed.py` — usable verbatim as an orchestrator prompt),",
        "plus structured chart background and encounter findings extracted",
        "deterministically from the record's FHIR R4 resources. `index.json` is the",
        "machine-readable roster (includes each patient's `summary_text`).",
        "",
        "**Everything is synthetic** (Synthea patients, LLM-generated transcripts).",
        "No real patient data. Ambient transcripts and clinical notes are NOT copied",
        "here — they stay in the dataset, keyed by `record_id`.",
        "",
        "Regenerate (expects the dataset directory at the repo root):",
        "",
        "```bash",
        "uv run python scripts/build_patient_contexts.py",
        "```",
        "",
        "| Patient | Age | Visit date | Visit |",
        "|---|---|---|---|",
        *roster_rows,
        "",
    ]
    (args.out / "README.md").write_text("\n".join(readme))
    print(f"\nWrote {len(index)} context files + index.json + README.md -> {args.out}")


if __name__ == "__main__":
    main()
