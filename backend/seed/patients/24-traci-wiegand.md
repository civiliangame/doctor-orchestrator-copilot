---
name: Traci Wiegand
dob: 1956-10-12
gender: female
city: "Lowell, MA"
marital_status: Never Married
language: English (United States)
fhir_patient_id: 5e93dd7e-1639-0886-8d0e-80ac11f2785c
record_id: "5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0"
dataset: synthetic-ambient-fhir-25
last_encounter: 2021-10-15
source: patient-context-model
slots: 24
ledger_entries: 24
synthetic: true
---

# Traci Wiegand — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Traci Wiegand, 65-year-old woman (DOB 1956-10-12), Lowell, MA. Problem list: Prediabetes; Anemia; Body mass index 30+ - obesity; Diabetes mellitus type 2; Hyperglycemia; Hypertriglyceridemia; Metabolic syndrome X; Chronic sinusitis. History: Past pregnancy history of miscarriage. No current medications on record. Social context: Received higher education; Medication review due; Stress.

Visit 2021-10-15 (inpatient at Sunny Acres Nursing Home, Inc.): Skilled nursing facility admission — diabetes stabilization and rehabilitation.

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2021-10-15 — Skilled nursing facility admission — diabetes stabilization and rehabilitation (inpatient · Sunny Acres Nursing Home, Inc.)[^1]

**Problems**
- **Prediabetes:** On problem list (longitudinal record)[^2]
- **Anemia:** On problem list (longitudinal record)[^3]
- **Body mass index 30+ - obesity:** On problem list (longitudinal record)[^4]
- **Diabetes mellitus type 2:** On problem list (longitudinal record)[^5]
- **Hyperglycemia:** On problem list (longitudinal record)[^6]
- **Hypertriglyceridemia:** On problem list (longitudinal record)[^7]
- **Metabolic syndrome X:** On problem list (longitudinal record)[^8]
- **Chronic sinusitis:** On problem list (longitudinal record)[^9]

**Medical / surgical history**
- **Past pregnancy history of miscarriage:** On record (longitudinal)[^10]

**Social context**
- **Received higher education:** Reported in longitudinal record[^11]
- **Medication review due:** Reported in longitudinal record[^12]
- **Stress:** Reported in longitudinal record[^13]

**Procedures**
- **History AND physical examination:** Performed this encounter (2021-10-15)[^14]
- **Initial patient assessment:** Performed this encounter (2021-10-15)[^15]
- **Development of individualized plan of care:** Performed this encounter (2021-10-15)[^16]
- **Nursing care/supplementary surveillance:** Performed this encounter (2021-10-15) ×58[^17]
- **Occupational therapy:** Performed this encounter (2021-10-15) ×8[^18]
- **Professional / ancillary services care:** Performed this encounter (2021-10-15) ×13[^19]
- **Speech and language therapy regime:** Performed this encounter (2021-10-15) ×2[^20]
- **Physical therapy procedure:** Performed this encounter (2021-10-15) ×2[^21]
- **Pre-discharge assessment:** Performed this encounter (2021-10-15)[^22]
- **Discharge from hospital:** Performed this encounter (2021-10-15)[^23]

**Reports**
- **History and physical note:** Filed this encounter (2021-10-15)[^24]

## Provenance

Rendered from the Patient Context Model (24 slots; 24 ledger entries — 24 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#Encounter/5e93dd7e-1639-0886-70ab-27e7ee37e5a0` — Sunny Acres Nursing Home, Inc. (FHIR record)
[^2]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#longitudinal` — EHR longitudinal record (FHIR record)
[^4]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#longitudinal` — EHR longitudinal record (FHIR record)
[^5]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#longitudinal` — EHR longitudinal record (FHIR record)
[^6]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#longitudinal` — EHR longitudinal record (FHIR record)
[^7]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#longitudinal` — EHR longitudinal record (FHIR record)
[^8]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#longitudinal` — EHR longitudinal record (FHIR record)
[^9]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#longitudinal` — EHR longitudinal record (FHIR record)
[^10]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#longitudinal` — EHR longitudinal record (FHIR record)
[^11]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#longitudinal` — EHR longitudinal record (FHIR record)
[^12]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#longitudinal` — EHR longitudinal record (FHIR record)
[^13]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#longitudinal` — EHR longitudinal record (FHIR record)
[^14]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#Procedure/5e93dd7e-1639-0886-81d5-7f7fb9c0521d` — Sunny Acres Nursing Home, Inc. (FHIR record)
[^15]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#Procedure/5e93dd7e-1639-0886-72e4-c488a6198a39` — Sunny Acres Nursing Home, Inc. (FHIR record)
[^16]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#Procedure/5e93dd7e-1639-0886-6152-25c575ed8410` — Sunny Acres Nursing Home, Inc. (FHIR record)
[^17]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#Procedure/5e93dd7e-1639-0886-b5c0-925a0a5bda77,Procedure/5e93dd7e-1639-0886-00dd-180743b7125c +56 more` — Sunny Acres Nursing Home, Inc. (FHIR record)
[^18]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#Procedure/5e93dd7e-1639-0886-b8a7-51a05c9346c7,Procedure/5e93dd7e-1639-0886-0fe7-83c3d840bdaf +6 more` — Sunny Acres Nursing Home, Inc. (FHIR record)
[^19]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#Procedure/5e93dd7e-1639-0886-e2be-030277d0009c,Procedure/5e93dd7e-1639-0886-c507-8adb2ba3f19a +11 more` — Sunny Acres Nursing Home, Inc. (FHIR record)
[^20]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#Procedure/5e93dd7e-1639-0886-2ae4-d40f955a01cf,Procedure/5e93dd7e-1639-0886-6565-ef6bca963de5` — Sunny Acres Nursing Home, Inc. (FHIR record)
[^21]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#Procedure/5e93dd7e-1639-0886-12e9-c6eea37553f3,Procedure/5e93dd7e-1639-0886-714a-6b24988bcfdd` — Sunny Acres Nursing Home, Inc. (FHIR record)
[^22]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#Procedure/5e93dd7e-1639-0886-784e-c5d48659a88c` — Sunny Acres Nursing Home, Inc. (FHIR record)
[^23]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#Procedure/5e93dd7e-1639-0886-4176-7a099685cfe3` — Sunny Acres Nursing Home, Inc. (FHIR record)
[^24]: `fhir:5e93dd7e-1639-0886-8d0e-80ac11f2785c::5e93dd7e-1639-0886-70ab-27e7ee37e5a0#DiagnosticReport/e0f4f630-5dca-27b0-f235-eb13d9877866` — Sunny Acres Nursing Home, Inc. (FHIR record)
