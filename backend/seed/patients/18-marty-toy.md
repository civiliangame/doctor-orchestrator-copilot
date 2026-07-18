---
name: Marty Toy
dob: 1990-12-10
gender: male
city: "Whitman, MA"
marital_status: Never Married
language: English (United States)
fhir_patient_id: e1a7c2af-1e7f-300b-44f6-012ae75bbab1
record_id: "e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc"
dataset: synthetic-ambient-fhir-25
last_encounter: 2025-03-10
source: patient-context-model
slots: 22
ledger_entries: 23
synthetic: true
---

# Marty Toy — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Marty Toy, 34-year-old man (DOB 1990-12-10), Whitman, MA. Problem list: Body mass index 30+ - obesity; Gingival disease. No current medications on record. Social context: Risk activity involvement; Serving in military service; Educated to high school level; Medication review due.

Visit 2025-03-10 (ambulatory at South Shore Hospital Inc.): Dental referral visit — gingival disease treatment. Recorded this visit: Gingival disease (resolved).

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2025-03-10 — Dental referral visit — gingival disease treatment (ambulatory · South Shore Hospital Inc.)[^1]

**Problems**
- **Body mass index 30+ - obesity:** On problem list (longitudinal record)[^2]
- **Gingival disease:** Resolved — recorded at 2025-03-10 encounter[^3]

**Medications**
- **Medication order(s) with unnamed reference:** 1 order(s) at 2025-03-10 encounter (unnamed medication reference)[^4]

**Social context**
- **Risk activity involvement:** Reported in longitudinal record[^5]
- **Serving in military service:** Reported in longitudinal record[^6]
- **Educated to high school level:** Reported in longitudinal record[^7]
- **Medication review due:** Reported in longitudinal record[^8]

**Procedures**
- **Dental consultation and report:** Performed this encounter (2025-03-10)[^9]
- **Dental care:** Performed this encounter (2025-03-10)[^10]
- **Removal of supragingival plaque and calculus from all teeth using dental instrument:** Performed this encounter (2025-03-10)[^11]
- **Removal of subgingival plaque and calculus from all teeth using dental instrument:** Performed this encounter (2025-03-10)[^12]
- **Dental plain X-ray bitewing:** Performed this encounter (2025-03-10)[^13]
- **Examination of gingivae:** Performed this encounter (2025-03-10)[^14]
- **Dental surgical procedure:** Performed this encounter (2025-03-10)[^15]
- **Dental application of desensitizing medicament:** Performed this encounter (2025-03-10)[^16]
- **Gingivectomy or gingivoplasty, per tooth:** Performed this encounter (2025-03-10)[^17]
- **Postoperative care for dental procedure:** Performed this encounter (2025-03-10)[^18]
- **Dental fluoride treatment:** Performed this encounter (2025-03-10)[^19]
- **Oral health education:** Performed this encounter (2025-03-10)[^20]

**Imaging**
- **Dental plain X-ray bitewing (procedure):** Obtained this encounter (2025-03-10)[^21]

**Reports**
- **History and physical note:** Filed this encounter (2025-03-10)[^22]

## Provenance

Rendered from the Patient Context Model (22 slots; 23 ledger entries — 23 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#Encounter/e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc` — South Shore Hospital Inc. (FHIR record)
[^2]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#Condition/e1a7c2af-1e7f-300b-d27e-377bd027dbe0` — South Shore Hospital Inc. (FHIR record) · 2 ledger entries
[^4]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#MedicationRequest/e1a7c2af-1e7f-300b-07a0-584ea1f7b191` — South Shore Hospital Inc. (FHIR record)
[^5]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#longitudinal` — EHR longitudinal record (FHIR record)
[^6]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#longitudinal` — EHR longitudinal record (FHIR record)
[^7]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#longitudinal` — EHR longitudinal record (FHIR record)
[^8]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#longitudinal` — EHR longitudinal record (FHIR record)
[^9]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#Procedure/e1a7c2af-1e7f-300b-96d9-178205a3f3ad` — South Shore Hospital Inc. (FHIR record)
[^10]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#Procedure/e1a7c2af-1e7f-300b-1ca6-d3e35a443982` — South Shore Hospital Inc. (FHIR record)
[^11]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#Procedure/e1a7c2af-1e7f-300b-da6c-fec20af80882` — South Shore Hospital Inc. (FHIR record)
[^12]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#Procedure/e1a7c2af-1e7f-300b-68d3-f570f4604e90` — South Shore Hospital Inc. (FHIR record)
[^13]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#Procedure/e1a7c2af-1e7f-300b-3d83-50e8b56e413a` — South Shore Hospital Inc. (FHIR record)
[^14]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#Procedure/e1a7c2af-1e7f-300b-0e83-0e12c694bbea` — South Shore Hospital Inc. (FHIR record)
[^15]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#Procedure/e1a7c2af-1e7f-300b-66da-0395975dcc36` — South Shore Hospital Inc. (FHIR record)
[^16]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#Procedure/e1a7c2af-1e7f-300b-571e-8ec87df53e32` — South Shore Hospital Inc. (FHIR record)
[^17]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#Procedure/e1a7c2af-1e7f-300b-8641-8dfa54420015` — South Shore Hospital Inc. (FHIR record)
[^18]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#Procedure/e1a7c2af-1e7f-300b-1c58-e25fc991f798` — South Shore Hospital Inc. (FHIR record)
[^19]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#Procedure/e1a7c2af-1e7f-300b-b29b-7a07af36043c` — South Shore Hospital Inc. (FHIR record)
[^20]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#Procedure/e1a7c2af-1e7f-300b-c154-40aae304c334` — South Shore Hospital Inc. (FHIR record)
[^21]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#ImagingStudy/e1a7c2af-1e7f-300b-69fd-f6990634f6c2` — South Shore Hospital Inc. (FHIR record)
[^22]: `fhir:e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc#DiagnosticReport/75e6757f-04ed-55a6-606d-818584964868` — South Shore Hospital Inc. (FHIR record)
