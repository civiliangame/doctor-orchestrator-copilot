"""FHIR → Patient Context Model ingestion (deterministic, no LLM).

The source adapter that folds a synthetic-ambient-fhir-25 record (one patient +
one encounter, FHIR R4) into the PCM through the one write path,
`pcm.record_contribution`. Every fact becomes a context slot whose ledger entry
carries a `source_ref` naming the exact FHIR resource(s) it was derived from:

    fhir:<record_id>#Observation/<id>         one resource
    fhir:<record_id>#Observation/<a>,Observation/<b>   a collapsed series
    fhir:<record_id>#longitudinal             record-level label lists (the
                                              dataset's longitudinal_summary has
                                              no per-resource ids)

The extraction helpers here (label buckets, CodeableConcept handling,
observation grouping) are shared with scripts/build_patient_contexts.py, which
uses them to build the roster index; the markdown context files themselves are
rendered from the PCM by context_render.py, not from FHIR directly.
"""

from __future__ import annotations

import json
import logging
import re
from collections import OrderedDict
from datetime import date
from pathlib import Path

from config import DATASET_PATH
from db import ins, one
from orchestrator import pcm

log = logging.getLogger("doc.fhir_ingest")

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


def fmt_quantity(qty: dict) -> str:
    unit = qty.get("unit") or qty.get("code") or ""
    unit = UNIT_DISPLAY.get(unit, unit)
    val = fmt_num(qty.get("value"))
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
        sys_q = next((qty for n, qty in parts.items() if "Systolic" in n), None)
        dia_q = next((qty for n, qty in parts.items() if "Diastolic" in n), None)
        if sys_q and dia_q:
            return f"{fmt_num(sys_q.get('value'))}/{fmt_num(dia_q.get('value'))} mmHg"
        return "; ".join(f"{n} {fmt_quantity(qty)}" for n, qty in parts.items()) or None
    return None


def obs_category(o: dict) -> str:
    for cat in o.get("category", []):
        for coding in cat.get("coding", []):
            if coding.get("code"):
                return coding["code"]
    return "other"


def collect_observations(observations: list[dict]) -> dict[str, list[dict]]:
    """Group by category, dedupe by code. Repeated codes (hospital stays record
    daily vitals/labs) collapse to 'first → latest (n readings)'. Each grouped
    item keeps the ids of every contributing Observation resource."""
    by_code: OrderedDict[str, dict] = OrderedDict()
    for o in sorted(observations, key=lambda x: x.get("effectiveDateTime", "")):
        code = cc_text(o.get("code")) or "Observation"
        val = obs_value(o)
        if val is None:
            continue
        entry = by_code.setdefault(code, {"category": obs_category(o), "values": [], "ids": []})
        entry["values"].append(val)
        entry["ids"].append(o.get("id", ""))

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
        grouped[cat].append({"name": name, "value": display, "n": len(vals),
                             "latest": vals[-1], "ids": entry["ids"]})
    return grouped


def find_latest(grouped: dict, *needles: str) -> str | None:
    for cat in grouped.values():
        for item in cat:
            if any(item["name"].startswith(n) for n in needles):
                return item["latest"]
    return None


def group_labeled(pairs: list[tuple[str, str]]) -> list[dict]:
    """[(label, resource_id)] -> [{'name', 'count', 'ids'}] preserving order,
    collapsing repeats ('Hemodialysis ×3') while keeping every resource id."""
    grouped: OrderedDict[str, dict] = OrderedDict()
    for label, rid in pairs:
        entry = grouped.setdefault(label, {"name": label, "count": 0, "ids": []})
        entry["count"] += 1
        if rid:
            entry["ids"].append(rid)
    return list(grouped.values())


# ---------------------------------------------------------------------------
# Per-record extraction
# ---------------------------------------------------------------------------

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

    # --- chart background (longitudinal label lists; no per-resource ids) ---
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
        raw_label = cc_text(c.get("code")) or "Condition"
        label = strip_tag(raw_label)
        if raw_label in SOCIAL_LABELS:
            bucket = "social"
        elif raw_label.endswith("(situation)"):
            bucket = "history"
        else:
            bucket = "problem"
        enc_conditions.append({
            "label": label, "status": status, "id": c.get("id", ""), "bucket": bucket,
            "display": label + (f" ({status})" if status else ""),
        })

    grouped_obs = collect_observations(rr.get("Observation", []))

    smoking, smoking_ids = None, []
    for cat in grouped_obs.values():
        for item in cat:
            if item["name"].startswith("Tobacco smoking status"):
                smoking, smoking_ids = item["latest"], item["ids"]

    procedures = group_labeled([
        (strip_tag(cc_text(p.get("code")) or "Procedure"), p.get("id", ""))
        for p in rr.get("Procedure", [])])
    reports = group_labeled([
        (cc_text(d.get("code")) or "Report", d.get("id", ""))
        for d in rr.get("DiagnosticReport", [])])
    immunizations = group_labeled([
        (cc_text(i.get("vaccineCode")) or "Immunization", i.get("id", ""))
        for i in rr.get("Immunization", [])])
    imaging = group_labeled([
        (cc_text((s.get("procedureCode") or [None])[0]) or "Imaging study", s.get("id", ""))
        for s in rr.get("ImagingStudy", [])])

    med_pairs, unresolved_ids = [], []
    for m in rr.get("MedicationRequest", []):
        label = cc_text(m.get("medicationCodeableConcept"))
        if not label and m.get("medicationReference"):
            label = m["medicationReference"].get("display")
        status = m.get("status", "")
        if label:
            med_pairs.append((label + (f" ({status})" if status and status != "active" else ""),
                              m.get("id", "")))
        else:
            unresolved_ids.append(m.get("id", ""))
    med_orders = group_labeled(med_pairs)

    return {
        "record_id": rec["id"],
        "patient_id": meta["patient_id"],
        "patient_fhir_id": patient.get("id", meta["patient_id"]),
        "encounter_id": meta["encounter_id"],
        "encounter_fhir_id": enc.get("id", meta["encounter_id"]),
        "name": full_name,
        "gender": gender,
        "noun": noun,
        "birth_date": birth,
        "age": age,
        "place": place,
        "marital": marital,
        "language": language,
        "smoking": smoking,
        "smoking_ids": smoking_ids,
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
        "unresolved_order_ids": unresolved_ids,
        "transcript_words": meta.get("transcript_words") or len(rec.get("transcript", "").split()),
        "note_words": meta.get("note_words") or len(rec.get("note", "").split()),
    }


def narrative(x: dict) -> str:
    """Maria-style summary block: usable verbatim as an orchestrator prompt.
    Stored on the patient row at ingest time (provenance: the FHIR record)."""
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
        p2 += " Recorded this visit: " + "; ".join(c["display"] for c in x["enc_conditions"]) + "."
    return p1 + "\n\n" + p2


# ---------------------------------------------------------------------------
# PCM ingestion
# ---------------------------------------------------------------------------

_FHIR_CONFIDENCE = 0.95  # deterministic extraction from a structured record


def _slugger():
    """Stable slot-key slugs with per-run collision handling."""
    seen: dict[str, str] = {}

    def slug(label: str) -> str:
        s = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")[:60].rstrip("-") or "item"
        base, n = s, 2
        while seen.get(s, label) != label:
            s, n = f"{base}-{n}", n + 1
        seen[s] = label
        return s

    return slug


def ensure_patient(rec: dict, dataset_name: str) -> tuple[int, bool]:
    """Find or create the patients row for a dataset record. Returns
    (patient_id, created). Matches by FHIR patient id, falling back to name+dob
    (rows created by seed_dataset_patients from index.json, possibly before the
    fhir_patient_id column existed) — never duplicates a roster patient.
    Identity + encounter framing land in meta_json so renderers never need the
    dataset again."""
    from db import ex
    x = extract(rec)
    existing = one("SELECT * FROM patients WHERE fhir_patient_id=?", (x["patient_fhir_id"],)) \
        or one("SELECT * FROM patients WHERE name=? AND dob=?", (x["name"], x["birth_date"]))
    meta = _patient_meta(x, dataset_name)
    if existing:
        # Backfill links/meta on rows that predate this ingester.
        if not existing["fhir_patient_id"]:
            ex("UPDATE patients SET fhir_patient_id=? WHERE id=?",
               (x["patient_fhir_id"], existing["id"]))
        if existing.get("meta_json", "{}") in ("", "{}"):
            ex("UPDATE patients SET meta_json=? WHERE id=?",
               (json.dumps(meta, ensure_ascii=False), existing["id"]))
        return existing["id"], False
    pid = ins("patients", name=x["name"], dob=x["birth_date"] or "unknown",
              summary_text=narrative(x), fhir_patient_id=x["patient_fhir_id"],
              meta_json=json.dumps(meta, ensure_ascii=False))
    return pid, True


def _patient_meta(x: dict, dataset_name: str) -> dict:
    return {
        "record_id": x["record_id"], "dataset": dataset_name, "synthetic": True,
        "patient_fhir_id": x["patient_fhir_id"], "encounter_id": x["encounter_id"],
        "gender": x["gender"], "age_at_visit": x["age"], "city": x["place"] or None,
        "marital_status": x["marital"], "language": x["language"],
        "visit_date": x["visit_date"], "visit_title": x["visit_title"],
        "visit_type": x["visit_type"], "encounter_class": x["enc_class"],
        "provider": x["provider"],
        "transcript_words": x["transcript_words"], "note_words": x["note_words"],
    }


def ingest_record(rec: dict, patient_id: int) -> int:
    """Fold one dataset record into the patient's PCM. Every fact goes through
    pcm.record_contribution with a source_ref naming the exact FHIR resource(s).
    Idempotent: re-ingesting the same record is a no-op (same value + status).
    Returns the number of ledger contributions written."""
    x = extract(rec)
    rid = x["record_id"]
    slug = _slugger()

    def ref(*resources: tuple[str, list[str] | str]) -> str:
        parts = []
        for rtype, ids in resources:
            ids = [ids] if isinstance(ids, str) else ids
            parts += [f"{rtype}/{i}" for i in ids if i]
        return f"fhir:{rid}#{','.join(parts)}" if parts else f"fhir:{rid}#longitudinal"

    enc_actor = {
        "source_kind": "fhir", "source_channel": "fhir_bundle", "actor_role": "ehr",
        "actor_id": "fhir_ingest", "actor_name": x["provider"] or "EHR encounter record",
    }
    longi_actor = {**enc_actor, "actor_name": "EHR longitudinal record"}
    written = 0

    def put(key: str, label: str, category: str, value: str, source_ref: str,
            quote: str, actor: dict) -> None:
        nonlocal written
        # FHIR facts are append-only record assertions: once this exact belief
        # has been asserted from this exact source, re-ingesting the record must
        # not re-write it — even if a later fact in the SAME record superseded it
        # (longitudinal "on problem list" → encounter "resolved" would otherwise
        # ping-pong a ledger pair on every ingest).
        if one("SELECT id FROM context_ledger WHERE patient_id=? AND slot_key=? "
               "AND value_written=? AND source_ref=? LIMIT 1",
               (patient_id, key, value, source_ref)):
            return
        r = pcm.record_contribution(
            patient_id, key, value, "known", _FHIR_CONFIDENCE,
            source_ref=source_ref, raw_quote=quote,
            label=label, category=category, **actor)
        if r is not None:
            written += 1

    # 1. The encounter itself — the patient's most recent contact with care.
    where = " · ".join(p for p in (x["enc_class"], x["provider"]) if p)
    put("encounter.latest", "Most recent encounter", "encounter",
        f"{x['visit_date']} — {x['visit_title']} ({where})",
        ref(("Encounter", x["encounter_fhir_id"])),
        f"Encounter {x['visit_date']}: {x['visit_type']}", enc_actor)

    # 2. Chart background — longitudinal label lists (record-level provenance).
    for label in x["problems"]:
        put(f"problem.{slug(label)}", label, "problem",
            "On problem list (longitudinal record)", ref(), label, longi_actor)
    for label in x["history"]:
        put(f"history.{slug(label)}", label, "history",
            "On record (longitudinal)", ref(), label, longi_actor)
    for label in x["meds"]:
        put(f"med.{slug(label)}", label, "medication",
            "On medication list (longitudinal record)", ref(), label, longi_actor)
    for label in x["social"]:
        put(f"social.{slug(label)}", label, "social",
            "Reported in longitudinal record", ref(), label, longi_actor)

    # 3. Tobacco status — an Observation with exact resource ids.
    if x["smoking"]:
        put("social.tobacco", "Tobacco smoking status", "social", x["smoking"],
            ref(("Observation", x["smoking_ids"])),
            f"Observation: Tobacco smoking status = {x['smoking']}", enc_actor)

    # 4. Conditions recorded at this encounter (may update longitudinal slots —
    #    newer, resource-exact information wins).
    for c in x["enc_conditions"]:
        status_txt = c["status"] or "recorded"
        put(f"{c['bucket']}.{slug(c['label'])}", c["label"], c["bucket"],
            f"{status_txt.capitalize()} — recorded at {x['visit_date']} encounter",
            ref(("Condition", c["id"])),
            f"Condition {c['label']}: clinicalStatus={c['status'] or 'n/a'}", enc_actor)

    # 5. Observations by category.
    obs_categories = (("vital-signs", "vital", "vital"),
                      ("laboratory", "lab", "lab"),
                      ("other", "assessment", "assessment"))
    for group, prefix, category in obs_categories:
        for item in x["obs"][group]:
            if item["name"].startswith("Tobacco smoking status"):
                continue  # handled above as social.tobacco
            put(f"{prefix}.{slug(item['name'])}", item["name"], category,
                item["value"], ref(("Observation", item["ids"])),
                f"Observation {item['name']}: {item['value']}", enc_actor)

    # 6. Things done / ordered this encounter.
    encounter_sets = (
        (x["procedures"], "procedure", "procedure", "Performed this encounter", "Procedure"),
        (x["imaging"], "imaging", "imaging", "Obtained this encounter", "ImagingStudy"),
        (x["reports"], "report", "report", "Filed this encounter", "DiagnosticReport"),
        (x["med_orders"], "med", "medication", "Ordered this encounter", "MedicationRequest"),
        (x["immunizations"], "immunization", "immunization", "Administered this encounter", "Immunization"),
    )
    for items, prefix, category, verb, rtype in encounter_sets:
        for item in items:
            times = f" ×{item['count']}" if item["count"] > 1 else ""
            put(f"{prefix}.{slug(item['name'])}", item["name"], category,
                f"{verb} ({x['visit_date']}){times}", ref((rtype, item["ids"])),
                f"{rtype}: {item['name']}{times}", enc_actor)
    if x["unresolved_order_ids"]:
        n = len(x["unresolved_order_ids"])
        put("med.unnamed-orders", "Medication order(s) with unnamed reference", "medication",
            f"{n} order(s) at {x['visit_date']} encounter (unnamed medication reference)",
            ref(("MedicationRequest", x["unresolved_order_ids"])),
            f"{n} MedicationRequest resource(s) without a resolvable name", enc_actor)

    return written


def ingest_dataset(path: Path | None = None) -> dict:
    """Ingest every record of the dataset into the PCM (creating patients as
    needed). Safe to call when the dataset is absent — returns a skip marker.
    Idempotent per record."""
    path = Path(path or DATASET_PATH)
    if not path.exists():
        log.info("FHIR dataset not found at %s — skipping roster ingest", path)
        return {"skipped": True, "patients": 0, "facts": 0}
    dataset_name = path.stem
    patients = facts = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        pid, created = ensure_patient(rec, dataset_name)
        patients += int(created)
        facts += ingest_record(rec, pid)
    log.info("FHIR ingest: %d new patients, %d contributions from %s",
             patients, facts, path.name)
    return {"skipped": False, "patients": patients, "facts": facts}
