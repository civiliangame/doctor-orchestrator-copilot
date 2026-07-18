---
name: Nola Kling
dob: 1947-05-14
gender: female
city: "Weymouth, MA"
marital_status: Widowed
language: English (United States)
fhir_patient_id: 25fb1227-d194-b15e-e099-7cffcd6081ec
record_id: "25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141"
dataset: synthetic-ambient-fhir-25
last_encounter: 2022-05-18
source: patient-context-model
slots: 20
ledger_entries: 20
synthetic: true
---

# Nola Kling — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Nola Kling, 75-year-old woman (DOB 1947-05-14), Weymouth, MA. Problem list: Body mass index 30+ - obesity; Prediabetes; Anemia; Hyperlipidemia; Chronic pain; Chronic low back pain; Polyp of colon; Recurrent rectal polyp. History: Past pregnancy history of miscarriage; History of tubal ligation. No current medications on record. Social context: Received higher education; Victim of intimate partner abuse.

Visit 2022-05-18 (home health at New England Hospice II LLC): Hospice admission — end-stage colon cancer.

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2022-05-18 — Hospice admission — end-stage colon cancer (home health · New England Hospice II LLC)[^1]

**Problems**
- **Body mass index 30+ - obesity:** On problem list (longitudinal record)[^2]
- **Prediabetes:** On problem list (longitudinal record)[^3]
- **Anemia:** On problem list (longitudinal record)[^4]
- **Hyperlipidemia:** On problem list (longitudinal record)[^5]
- **Chronic pain:** On problem list (longitudinal record)[^6]
- **Chronic low back pain:** On problem list (longitudinal record)[^7]
- **Polyp of colon:** On problem list (longitudinal record)[^8]
- **Recurrent rectal polyp:** On problem list (longitudinal record)[^9]

**Medical / surgical history**
- **Past pregnancy history of miscarriage:** On record (longitudinal)[^10]
- **History of tubal ligation:** On record (longitudinal)[^11]

**Social context**
- **Received higher education:** Reported in longitudinal record[^12]
- **Victim of intimate partner abuse:** Reported in longitudinal record[^13]

**Procedures**
- **Certification procedure:** Performed this encounter (2022-05-18)[^14]
- **Notifications:** Performed this encounter (2022-05-18)[^15]
- **Initial patient assessment:** Performed this encounter (2022-05-18)[^16]
- **Development of individualized plan of care:** Performed this encounter (2022-05-18)[^17]
- **Hospice care:** Performed this encounter (2022-05-18) ×40[^18]
- **Patient discharge:** Performed this encounter (2022-05-18)[^19]

**Reports**
- **History and physical note:** Filed this encounter (2022-05-18)[^20]

## Provenance

Rendered from the Patient Context Model (20 slots; 20 ledger entries — 20 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#Encounter/25fb1227-d194-b15e-ecd8-6fcb9efd8141` — New England Hospice II LLC (FHIR record)
[^2]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#longitudinal` — EHR longitudinal record (FHIR record)
[^4]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#longitudinal` — EHR longitudinal record (FHIR record)
[^5]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#longitudinal` — EHR longitudinal record (FHIR record)
[^6]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#longitudinal` — EHR longitudinal record (FHIR record)
[^7]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#longitudinal` — EHR longitudinal record (FHIR record)
[^8]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#longitudinal` — EHR longitudinal record (FHIR record)
[^9]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#longitudinal` — EHR longitudinal record (FHIR record)
[^10]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#longitudinal` — EHR longitudinal record (FHIR record)
[^11]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#longitudinal` — EHR longitudinal record (FHIR record)
[^12]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#longitudinal` — EHR longitudinal record (FHIR record)
[^13]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#longitudinal` — EHR longitudinal record (FHIR record)
[^14]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#Procedure/25fb1227-d194-b15e-2126-93b7565c7cca` — New England Hospice II LLC (FHIR record)
[^15]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#Procedure/25fb1227-d194-b15e-f8b2-9408936afcfd` — New England Hospice II LLC (FHIR record)
[^16]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#Procedure/25fb1227-d194-b15e-04e0-9821a676ecd6` — New England Hospice II LLC (FHIR record)
[^17]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#Procedure/25fb1227-d194-b15e-1bfc-d811779c07c2` — New England Hospice II LLC (FHIR record)
[^18]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#Procedure/25fb1227-d194-b15e-043a-7f95c2580b8b,Procedure/25fb1227-d194-b15e-0303-5f224f4bf89f +38 more` — New England Hospice II LLC (FHIR record)
[^19]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#Procedure/25fb1227-d194-b15e-8428-5d4701bc79a7` — New England Hospice II LLC (FHIR record)
[^20]: `fhir:25fb1227-d194-b15e-e099-7cffcd6081ec::25fb1227-d194-b15e-ecd8-6fcb9efd8141#DiagnosticReport/ff43a7bc-367a-00f4-ba49-75260ab54192` — New England Hospice II LLC (FHIR record)
