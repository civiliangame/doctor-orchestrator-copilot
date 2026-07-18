---
record_id: "e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc"
patient_id: e1a7c2af-1e7f-300b-44f6-012ae75bbab1
encounter_id: e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc
name: Marty Toy
gender: male
birth_date: 1990-12-10
age_at_visit: 34
visit_date: 2025-03-10
visit_title: Dental referral visit — gingival disease treatment
visit_type: Encounter for check up (procedure)
encounter_class: ambulatory
provider: South Shore Hospital Inc.
city: "Whitman, MA"
marital_status: Never Married
language: English (United States)
transcript_words: 1505
note_words: 522
dataset: synthetic-ambient-fhir-25
synthetic: true
---

# Marty Toy — Dental referral visit — gingival disease treatment

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Marty Toy, 34-year-old man (DOB 1990-12-10), Whitman, MA. Problem list: Body mass index 30+ - obesity; Gingival disease. No current medications on record. Social context: Risk activity involvement; Serving in military service; Educated to high school level; Medication review due.

Visit 2025-03-10 (ambulatory at South Shore Hospital Inc.): Dental referral visit — gingival disease treatment. Recorded this visit: Gingival disease (resolved).

## Chart background (full record)

**Problem list**
- Body mass index 30+ - obesity
- Gingival disease

**Current medications:** none recorded

**Social & administrative context**
- Risk activity involvement
- Serving in military service
- Educated to high school level
- Medication review due

**Record depth:** 79 Observation, 42 Procedure, 25 DiagnosticReport, 16 Condition, 15 DocumentReference, 15 Encounter, 6 Immunization, 3 Device, 2 ImagingStudy, 2 MedicationRequest, 1 Medication

## This encounter — 2025-03-10

*ambulatory · South Shore Hospital Inc. · Encounter for check up (procedure)*

**Conditions recorded**
- Gingival disease (resolved)

**Procedures**
- Dental consultation and report
- Dental care
- Removal of supragingival plaque and calculus from all teeth using dental instrument
- Removal of subgingival plaque and calculus from all teeth using dental instrument
- Dental plain X-ray bitewing
- Examination of gingivae
- Dental surgical procedure
- Dental application of desensitizing medicament
- Gingivectomy or gingivoplasty, per tooth
- Postoperative care for dental procedure
- Dental fluoride treatment
- Oral health education

**Imaging**
- Dental plain X-ray bitewing (procedure)

**Reports**
- History and physical note

**Medications ordered**
- 1 additional medication order(s) (unnamed reference)

## Provenance

Derived deterministically from `synthetic-ambient-fhir-25` record `e1a7c2af-1e7f-300b-44f6-012ae75bbab1::e1a7c2af-1e7f-300b-bc8f-6bb66fcf2ddc` (FHIR R4, Synthea). The paired ambient transcript (1505 words) and clinical note (522 words) live in the dataset record, keyed by `record_id`. Regenerate: `uv run python scripts/build_patient_contexts.py`.
