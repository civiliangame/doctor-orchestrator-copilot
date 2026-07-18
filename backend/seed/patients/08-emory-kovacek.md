---
record_id: "1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964"
patient_id: 1ba8eeb9-bc93-7129-4390-0d2ddd560616
encounter_id: 1ba8eeb9-bc93-7129-2e7d-8c427e72b964
name: Emory Kovacek
gender: male
birth_date: 1999-01-19
age_at_visit: 22
visit_date: 2021-04-06
visit_title: General exam — chronic low back pain and positive depression screen
visit_type: General examination of patient (procedure)
encounter_class: ambulatory
provider: Sunrise Healthcare LLC
city: "Westborough, MA"
marital_status: Never Married
language: English (United States)
transcript_words: 1518
note_words: 514
dataset: synthetic-ambient-fhir-25
synthetic: true
---

# Emory Kovacek — General exam — chronic low back pain and positive depression screen

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Emory Kovacek, 22-year-old man (DOB 1999-01-19), Westborough, MA. Tobacco: never smoked tobacco. Problem list: Chronic pain; Chronic low back pain; Gingivitis. History: History of appendectomy. Current medications on record: Ibuprofen 400 MG Oral Tablet [Ibu]. Social context: Received higher education; Stress.

Visit 2021-04-06 (ambulatory at Sunrise Healthcare LLC): General exam — chronic low back pain and positive depression screen. Vitals: BP 136/94, HR 89, BMI 22.5. Recorded this visit: Full-time employment (resolved); Stress (resolved); Gingivitis (resolved).

## Chart background (full record)

**Problem list**
- Chronic pain
- Chronic low back pain
- Gingivitis

**Medical / surgical history**
- History of appendectomy

**Current medications**
- Ibuprofen 400 MG Oral Tablet [Ibu]

**Social & administrative context**
- Received higher education
- Stress

**Record depth:** 177 Observation, 108 Procedure, 62 DiagnosticReport, 32 Condition, 27 DocumentReference, 27 Encounter, 20 MedicationRequest, 17 Immunization, 4 CarePlan, 4 CareTeam, 2 Device, 2 ImagingStudy, 2 Medication

## This encounter — 2021-04-06

*ambulatory · Sunrise Healthcare LLC · General examination of patient (procedure)*

**Conditions recorded**
- Full-time employment (resolved)
- Stress (resolved)
- Gingivitis (resolved)

**Vitals**
- Height: 185.2 cm
- Pain severity (0–10): 4
- Weight: 77 kg
- BMI: 22.5 kg/m²
- Blood pressure: 136/94 mmHg
- Heart rate: 89 /min
- Respiratory rate: 15 /min

**Assessments & screenings**
- Tobacco smoking status: Never smoked tobacco
- Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]: What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 91796 /a; How many people are living or staying at this address [#] 3
- Total score [HARK]: 0
- Patient Health Questionnaire 2 item (PHQ-2) total score [Reported]: 5
- Patient Health Questionnaire 9 item (PHQ-9) total score [Reported]: 17
- Total score [DAST-10]: 1

**Procedures**
- Medication reconciliation
- Assessment of health and social care needs
- Screening for domestic abuse
- Depression screening ×2
- Depression screening using Patient Health Questionnaire Nine Item score
- Assessment of substance use
- Screening for drug abuse
- Patient referral for dental care

**Reports**
- Humiliation, Afraid, Rape, and Kick questionnaire [HARK]
- Patient Health Questionnaire 2 item (PHQ-2) [Reported]
- PHQ-9 quick depression assessment panel [Reported.PHQ]
- Drug Abuse Screening Test-10 [DAST-10]
- History and physical note

**Medications ordered**
- Ibuprofen 400 MG Oral Tablet [Ibu] (completed)

## Provenance

Derived deterministically from `synthetic-ambient-fhir-25` record `1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964` (FHIR R4, Synthea). The paired ambient transcript (1518 words) and clinical note (514 words) live in the dataset record, keyed by `record_id`. Regenerate: `uv run python scripts/build_patient_contexts.py`.
