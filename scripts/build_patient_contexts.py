"""Build per-patient context files from the synthetic-ambient-fhir-25 dataset.

Pipeline: FHIR record → Patient Context Model ingestion (backend/fhir_ingest.py;
every fact goes through pcm.record_contribution with a source_ref naming the
exact FHIR resource) → markdown projection (backend/context_render.py). The
files written here are RENDERINGS of a PCM, not a parallel extraction — the
same renderer serves `GET /api/patients/{id}/context.md` against the live app,
where scribe-session contributions appear alongside the FHIR-derived ones.

Deterministic, no LLM. Runs against a throwaway SQLite DB so the app's
database is untouched.

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
import os
import re
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dataset", type=Path,
                    default=REPO_ROOT / "synthetic-ambient-fhir-25" / "synthetic-ambient-fhir-25.jsonl")
    ap.add_argument("--out", type=Path, default=REPO_ROOT / "backend" / "seed" / "patients")
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        # Point the backend at a throwaway DB BEFORE importing it.
        os.environ["DOC_DB"] = str(Path(tmp) / "pcm-build.sqlite3")
        sys.path.insert(0, str(REPO_ROOT / "backend"))
        import context_render
        import fhir_ingest
        from db import init_db

        init_db()
        records = [json.loads(l) for l in args.dataset.read_text().splitlines() if l.strip()]
        dataset_name = args.dataset.stem
        args.out.mkdir(parents=True, exist_ok=True)

        index, roster_rows = [], []
        for i, rec in enumerate(records, 1):
            pid, _ = fhir_ingest.ensure_patient(rec, dataset_name)
            facts = fhir_ingest.ingest_record(rec, pid)
            x = fhir_ingest.extract(rec)
            slug = re.sub(r"[^a-z0-9]+", "-", x["name"].lower()).strip("-")
            fname = f"{i:02d}-{slug}.md"
            (args.out / fname).write_text(context_render.render_patient_md(pid))
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
                "pcm_facts": facts,
                "summary_text": fhir_ingest.narrative(x),
            })
            roster_rows.append(
                f"| [{x['name']}]({fname}) | {x['age']}{x['gender'][:1].upper()} | {x['visit_date']} | {x['visit_title']} |"
            )
            print(f"  {fname:44s} {facts:3d} facts  {x['age']:>3}{x['gender'][:1].upper()}  {x['visit_title']}")

        (args.out / "index.json").write_text(json.dumps(
            {"dataset": dataset_name, "synthetic": True, "patients": index}, indent=1, ensure_ascii=False))

        readme = [
            "# Synthetic patient context files",
            "",
            f"One context file per synthetic patient in the `{dataset_name}` dataset",
            "(25 patients, one encounter each). Each file is a **markdown projection of",
            "that patient's Patient Context Model**: the record's FHIR resources are",
            "ingested into PCM slots (every fact through `pcm.record_contribution`, with",
            "a `source_ref` naming the exact FHIR resource it came from), and the file is",
            "rendered from the resulting belief state by `backend/context_render.py` —",
            "every line footnoted with its provenance. The narrative **Summary** block",
            "(same role as the hand-written Maria Alvarez summary in `backend/seed.py`)",
            "is stored on the patient row at ingest and usable verbatim as an",
            "orchestrator prompt. `index.json` is the machine-readable roster.",
            "",
            "When the app runs with the dataset present, the same ingestion happens into",
            "the live DB at startup and `GET /api/patients/{id}/context.md` renders the",
            "current version — including any scribe-conversation contributions that have",
            "updated the belief state since. These files are also the **chart bridge**",
            "surface (`orchestrator/chart_md.py`): live session updates append under a",
            "DOC-managed section, and hand edits to the authored part flow back into the",
            "PCM. `00-maria-alvarez.md` is the hand-written demo patient's chart (source",
            "of truth: `backend/seed.py`), not part of the dataset.",
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
