---
name: Solomon Macejkovic
dob: 1945-01-06
gender: male
city: "Boston, MA"
marital_status: Married
language: English (United States)
fhir_patient_id: 693a049b-0fd5-c1af-a6ab-e31c329f2891
record_id: "693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529"
dataset: synthetic-ambient-fhir-25
last_encounter: 2020-01-11
source: patient-context-model
slots: 23
ledger_entries: 23
synthetic: true
---

# Solomon Macejkovic — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Solomon Macejkovic, 75-year-old man (DOB 1945-01-06), Boston, MA. Problem list: Body mass index 30+ - obesity; Prediabetes; Anemia; Ischemic heart disease; Abnormal findings diagnostic imaging heart+coronary circulat; Hyperlipidemia; Polyp of colon; Chronic sinusitis. Current medications on record: Clopidogrel 75 MG Oral Tablet; Simvastatin 20 MG Oral Tablet; 24 HR metoprolol succinate 100 MG Extended Release Oral Tablet; Nitroglycerin 0.4 MG/ACTUAT Mucosal Spray. Social context: Received higher education; Limited social contact; Social isolation.

Visit 2020-01-11 (home health at West River Hospice, LLC): Hospice admission — advanced colon cancer with cardiac comorbidity.

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2020-01-11 — Hospice admission — advanced colon cancer with cardiac comorbidity (home health · West River Hospice, LLC)[^1]

**Problems**
- **Body mass index 30+ - obesity:** On problem list (longitudinal record)[^2]
- **Prediabetes:** On problem list (longitudinal record)[^3]
- **Anemia:** On problem list (longitudinal record)[^4]
- **Ischemic heart disease:** On problem list (longitudinal record)[^5]
- **Abnormal findings diagnostic imaging heart+coronary circulat:** On problem list (longitudinal record)[^6]
- **Hyperlipidemia:** On problem list (longitudinal record)[^7]
- **Polyp of colon:** On problem list (longitudinal record)[^8]
- **Chronic sinusitis:** On problem list (longitudinal record)[^9]

**Medications**
- **Clopidogrel 75 MG Oral Tablet:** On medication list (longitudinal record)[^10]
- **Simvastatin 20 MG Oral Tablet:** On medication list (longitudinal record)[^11]
- **24 HR metoprolol succinate 100 MG Extended Release Oral Tablet:** On medication list (longitudinal record)[^12]
- **Nitroglycerin 0.4 MG/ACTUAT Mucosal Spray:** On medication list (longitudinal record)[^13]

**Social context**
- **Received higher education:** Reported in longitudinal record[^14]
- **Limited social contact:** Reported in longitudinal record[^15]
- **Social isolation:** Reported in longitudinal record[^16]

**Procedures**
- **Certification procedure:** Performed this encounter (2020-01-11)[^17]
- **Notifications:** Performed this encounter (2020-01-11)[^18]
- **Initial patient assessment:** Performed this encounter (2020-01-11)[^19]
- **Development of individualized plan of care:** Performed this encounter (2020-01-11)[^20]
- **Hospice care:** Performed this encounter (2020-01-11) ×44[^21]
- **Patient discharge:** Performed this encounter (2020-01-11)[^22]

**Reports**
- **History and physical note:** Filed this encounter (2020-01-11)[^23]

## Provenance

Rendered from the Patient Context Model (23 slots; 23 ledger entries — 23 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#Encounter/693a049b-0fd5-c1af-8dff-09e595625529` — West River Hospice, LLC (FHIR record)
[^2]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#longitudinal` — EHR longitudinal record (FHIR record)
[^4]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#longitudinal` — EHR longitudinal record (FHIR record)
[^5]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#longitudinal` — EHR longitudinal record (FHIR record)
[^6]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#longitudinal` — EHR longitudinal record (FHIR record)
[^7]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#longitudinal` — EHR longitudinal record (FHIR record)
[^8]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#longitudinal` — EHR longitudinal record (FHIR record)
[^9]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#longitudinal` — EHR longitudinal record (FHIR record)
[^10]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#longitudinal` — EHR longitudinal record (FHIR record)
[^11]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#longitudinal` — EHR longitudinal record (FHIR record)
[^12]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#longitudinal` — EHR longitudinal record (FHIR record)
[^13]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#longitudinal` — EHR longitudinal record (FHIR record)
[^14]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#longitudinal` — EHR longitudinal record (FHIR record)
[^15]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#longitudinal` — EHR longitudinal record (FHIR record)
[^16]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#longitudinal` — EHR longitudinal record (FHIR record)
[^17]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#Procedure/693a049b-0fd5-c1af-d2ff-c2132d5c50d2` — West River Hospice, LLC (FHIR record)
[^18]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#Procedure/693a049b-0fd5-c1af-aa4b-086f8e3aebf9` — West River Hospice, LLC (FHIR record)
[^19]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#Procedure/693a049b-0fd5-c1af-6ab4-14906daa5de2` — West River Hospice, LLC (FHIR record)
[^20]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#Procedure/693a049b-0fd5-c1af-1382-59ccd5202256` — West River Hospice, LLC (FHIR record)
[^21]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#Procedure/693a049b-0fd5-c1af-dd51-1bcb074546f8,Procedure/693a049b-0fd5-c1af-fb16-c2c8db8a8a86 +42 more` — West River Hospice, LLC (FHIR record)
[^22]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#Procedure/693a049b-0fd5-c1af-62f0-444bb8cb318c` — West River Hospice, LLC (FHIR record)
[^23]: `fhir:693a049b-0fd5-c1af-a6ab-e31c329f2891::693a049b-0fd5-c1af-8dff-09e595625529#DiagnosticReport/0c82def0-6eac-02f8-05c5-3a085c3fc3a1` — West River Hospice, LLC (FHIR record)
