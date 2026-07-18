---
name: Latoyia Wilkinson
dob: 1944-11-15
gender: female
city: "Boston, MA"
marital_status: Never Married
language: English (United States)
fhir_patient_id: 1be66dc9-cf0b-cb78-e88e-ada9a9a5405b
record_id: "1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4"
dataset: synthetic-ambient-fhir-25
last_encounter: 2019-11-20
source: patient-context-model
slots: 30
ledger_entries: 30
synthetic: true
---

# Latoyia Wilkinson — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Latoyia Wilkinson, 75-year-old woman (DOB 1944-11-15), Boston, MA. Problem list: Prediabetes; Anemia; Essential hypertension; Diabetes mellitus type 2; Chronic kidney disease stage 1; Disorder of kidney due to diabetes mellitus; Hypertriglyceridemia; Metabolic syndrome X. History: Past pregnancy history of miscarriage; History of tubal ligation. Current medications on record: Vitamin B12 5 MG/ML Injectable Solution; Clopidogrel 75 MG Oral Tablet; Simvastatin 20 MG Oral Tablet; 24 HR metoprolol succinate 100 MG Extended Release Oral Tablet; Nitroglycerin 0.4 MG/ACTUAT Mucosal Spray. Social context: Received higher education; Has a criminal record.

Visit 2019-11-20 (inpatient at Marian Manor): Skilled nursing facility admission after hospitalization.

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2019-11-20 — Skilled nursing facility admission after hospitalization (inpatient · Marian Manor)[^1]

**Problems**
- **Prediabetes:** On problem list (longitudinal record)[^2]
- **Anemia:** On problem list (longitudinal record)[^3]
- **Essential hypertension:** On problem list (longitudinal record)[^4]
- **Diabetes mellitus type 2:** On problem list (longitudinal record)[^5]
- **Chronic kidney disease stage 1:** On problem list (longitudinal record)[^6]
- **Disorder of kidney due to diabetes mellitus:** On problem list (longitudinal record)[^7]
- **Hypertriglyceridemia:** On problem list (longitudinal record)[^8]
- **Metabolic syndrome X:** On problem list (longitudinal record)[^9]

**Medical / surgical history**
- **Past pregnancy history of miscarriage:** On record (longitudinal)[^10]
- **History of tubal ligation:** On record (longitudinal)[^11]

**Medications**
- **Vitamin B12 5 MG/ML Injectable Solution:** On medication list (longitudinal record)[^12]
- **Clopidogrel 75 MG Oral Tablet:** On medication list (longitudinal record)[^13]
- **Simvastatin 20 MG Oral Tablet:** On medication list (longitudinal record)[^14]
- **24 HR metoprolol succinate 100 MG Extended Release Oral Tablet:** On medication list (longitudinal record)[^15]
- **Nitroglycerin 0.4 MG/ACTUAT Mucosal Spray:** On medication list (longitudinal record)[^16]

**Social context**
- **Received higher education:** Reported in longitudinal record[^17]
- **Has a criminal record:** Reported in longitudinal record[^18]

**Procedures**
- **History AND physical examination:** Performed this encounter (2019-11-20)[^19]
- **Initial patient assessment:** Performed this encounter (2019-11-20)[^20]
- **Development of individualized plan of care:** Performed this encounter (2019-11-20)[^21]
- **Nursing care/supplementary surveillance:** Performed this encounter (2019-11-20) ×52[^22]
- **Occupational therapy:** Performed this encounter (2019-11-20) ×7[^23]
- **Physical therapy procedure:** Performed this encounter (2019-11-20) ×8[^24]
- **Professional / ancillary services care:** Performed this encounter (2019-11-20) ×11[^25]
- **Speech and language therapy regime:** Performed this encounter (2019-11-20)[^26]
- **Care regimes assessment:** Performed this encounter (2019-11-20)[^27]
- **Pre-discharge assessment:** Performed this encounter (2019-11-20)[^28]
- **Discharge from hospital:** Performed this encounter (2019-11-20)[^29]

**Reports**
- **History and physical note:** Filed this encounter (2019-11-20)[^30]

## Provenance

Rendered from the Patient Context Model (30 slots; 30 ledger entries — 30 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#Encounter/1be66dc9-cf0b-cb78-ee14-c92f2fe041a4` — Marian Manor (FHIR record)
[^2]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^4]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^5]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^6]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^7]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^8]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^9]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^10]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^11]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^12]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^13]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^14]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^15]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^16]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^17]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^18]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#longitudinal` — EHR longitudinal record (FHIR record)
[^19]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#Procedure/1be66dc9-cf0b-cb78-3d73-e7d0fe706143` — Marian Manor (FHIR record)
[^20]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#Procedure/1be66dc9-cf0b-cb78-0722-edbecf6f753d` — Marian Manor (FHIR record)
[^21]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#Procedure/1be66dc9-cf0b-cb78-b07b-13c5791069c6` — Marian Manor (FHIR record)
[^22]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#Procedure/1be66dc9-cf0b-cb78-3387-49d2653f6597,Procedure/1be66dc9-cf0b-cb78-3d25-a41458014196 +50 more` — Marian Manor (FHIR record)
[^23]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#Procedure/1be66dc9-cf0b-cb78-25b8-9e7101dcaf76,Procedure/1be66dc9-cf0b-cb78-f8e6-a7de060ddffb +5 more` — Marian Manor (FHIR record)
[^24]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#Procedure/1be66dc9-cf0b-cb78-7128-94fedb05c817,Procedure/1be66dc9-cf0b-cb78-7fc2-3bf64d1380c2 +6 more` — Marian Manor (FHIR record)
[^25]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#Procedure/1be66dc9-cf0b-cb78-8dfb-53462750acc1,Procedure/1be66dc9-cf0b-cb78-4726-3d939f724ca5 +9 more` — Marian Manor (FHIR record)
[^26]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#Procedure/1be66dc9-cf0b-cb78-4de6-2dc7ace891f3` — Marian Manor (FHIR record)
[^27]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#Procedure/1be66dc9-cf0b-cb78-5515-998485cb98ed` — Marian Manor (FHIR record)
[^28]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#Procedure/1be66dc9-cf0b-cb78-f4c5-1609a740452e` — Marian Manor (FHIR record)
[^29]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#Procedure/1be66dc9-cf0b-cb78-0a74-f9bde798932a` — Marian Manor (FHIR record)
[^30]: `fhir:1be66dc9-cf0b-cb78-e88e-ada9a9a5405b::1be66dc9-cf0b-cb78-ee14-c92f2fe041a4#DiagnosticReport/e7d37edf-105f-2bce-6f75-231e312bbd80` — Marian Manor (FHIR record)
