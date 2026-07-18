# Synthetic patient context files

One context file per synthetic patient in the `synthetic-ambient-fhir-25` dataset
(25 patients, one encounter each). Each file is a **markdown projection of
that patient's Patient Context Model**: the record's FHIR resources are
ingested into PCM slots (every fact through `pcm.record_contribution`, with
a `source_ref` naming the exact FHIR resource it came from), and the file is
rendered from the resulting belief state by `backend/context_render.py` —
every line footnoted with its provenance. The narrative **Summary** block
(same role as the hand-written Maria Alvarez summary in `backend/seed.py`)
is stored on the patient row at ingest and usable verbatim as an
orchestrator prompt. `index.json` is the machine-readable roster.

When the app runs with the dataset present, the same ingestion happens into
the live DB at startup and `GET /api/patients/{id}/context.md` renders the
current version — including any scribe-conversation contributions that have
updated the belief state since. These files are also the **chart bridge**
surface (`orchestrator/chart_md.py`): live session updates append under a
DOC-managed section, and hand edits to the authored part flow back into the
PCM. `00-maria-alvarez.md` is the hand-written demo patient's chart (source
of truth: `backend/seed.py`), not part of the dataset.

**Everything is synthetic** (Synthea patients, LLM-generated transcripts).
No real patient data. Ambient transcripts and clinical notes are NOT copied
here — they stay in the dataset, keyed by `record_id`.

Regenerate (expects the dataset directory at the repo root):

```bash
uv run python scripts/build_patient_contexts.py
```

| Patient | Age | Visit date | Visit |
|---|---|---|---|
| [Ali Kuhic](01-ali-kuhic.md) | 31M | 2022-08-05 | Annual physical — preventive screening and migraine check-in |
| [Ariane Runolfsson](02-ariane-runolfsson.md) | 80F | 2021-01-03 | Inpatient admission — COVID-19 isolation with pneumonia and hypoxemia |
| [Clarence Reinger](03-clarence-reinger.md) | 32F | 2025-06-01 | Prenatal intake visit — initial obstetric evaluation |
| [Corinne Crooks](04-corinne-crooks.md) | 46F | 2017-01-01 | Annual wellness examination — preventive screening and health maintenance |
| [Delana Gutkowski](05-delana-gutkowski.md) | 22F | 2025-05-23 | Young adult preventive exam — prediabetes and allergy follow-up |
| [Dick Larson](06-dick-larson.md) | 36M | 2024-05-18 | Annual check-up — post-sepsis recovery and prediabetes |
| [Elias Wisozk](07-elias-wisozk.md) | 54M | 2026-06-18 | General adult exam — new hypertension and metabolic syndrome |
| [Emory Kovacek](08-emory-kovacek.md) | 22M | 2021-04-06 | General exam — chronic low back pain and positive depression screen |
| [Eva Casas](09-eva-casas.md) | 62F | 2016-08-30 | Annual general exam — prediabetes, hyperlipidemia, and knee osteoarthritis |
| [Hiedi Thiel](10-hiedi-thiel.md) | 30F | 2024-07-22 | Prenatal intake visit — first trimester, newly identified anemia |
| [Isreal Howell](11-isreal-howell.md) | 85M | 2024-10-07 | Annual physical — geriatric cardiometabolic follow-up |
| [Issac Mayer](12-issac-mayer.md) | 31M | 2019-07-14 | Annual physical — new adult patient wellness exam |
| [Julius Renner](13-julius-renner.md) | 35M | 2025-07-13 | General exam — hypertension treatment initiation and chronic low back pain |
| [Lala Casper](14-lala-casper.md) | 48F | 2020-06-17 | Annual exam — psychosocial screening with safety disclosure |
| [Lamont Ernser](15-lamont-ernser.md) | 52M | 2023-05-20 | General adult exam — preventive screening and sleep review |
| [Latoyia Wilkinson](16-latoyia-wilkinson.md) | 75F | 2019-11-20 | Skilled nursing facility admission after hospitalization |
| [Margarita Rau](17-margarita-rau.md) | 43F | 2019-09-27 | Initial prenatal visit — new pregnancy at 43 |
| [Marty Toy](18-marty-toy.md) | 34M | 2025-03-10 | Dental referral visit — gingival disease treatment |
| [Melodee Satterfield](19-melodee-satterfield.md) | 20F | 2026-03-21 | Prenatal intake visit — first pregnancy with chronic pain |
| [Monica Hilpert](20-monica-hilpert.md) | 76F | 2023-11-27 | SNF admission — rehabilitation and pain management |
| [Nigel Ankunding](21-nigel-ankunding.md) | 52M | 2019-04-22 | Annual physical — prediabetes and psychosocial screening |
| [Nola Kling](22-nola-kling.md) | 75F | 2022-05-18 | Hospice admission — end-stage colon cancer |
| [Solomon Macejkovic](23-solomon-macejkovic.md) | 75M | 2020-01-11 | Hospice admission — advanced colon cancer with cardiac comorbidity |
| [Traci Wiegand](24-traci-wiegand.md) | 65F | 2021-10-15 | Skilled nursing facility admission — diabetes stabilization and rehabilitation |
| [Van O'Reilly](25-van-o-reilly.md) | 42M | 2019-07-25 | Annual physical — hand osteoarthritis and anxiety screening |
