---
record_id: "256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07"
patient_id: 256bea3d-7833-e7f8-74b4-0e4f7e299c73
encounter_id: 256bea3d-7833-e7f8-1c5a-743d9ec18b07
name: Lala Casper
gender: female
birth_date: 1972-05-24
age_at_visit: 48
visit_date: 2020-06-17
visit_title: Annual exam — psychosocial screening with safety disclosure
visit_type: General examination of patient (procedure)
encounter_class: ambulatory
provider: "Caring Health Center, Inc"
city: "Springfield, MA"
marital_status: Married
language: English (United States)
transcript_words: 1364
note_words: 582
dataset: synthetic-ambient-fhir-25
synthetic: true
---

# Lala Casper — Annual exam — psychosocial screening with safety disclosure

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Lala Casper, 48-year-old woman (DOB 1972-05-24), Springfield, MA. Tobacco: never smoked tobacco. Problem list: Recurrent urinary tract infection; Body mass index 30+ - obesity. History: Past pregnancy history of miscarriage; History of tubal ligation. Current medications on record: Hydrocortisone 10 MG/ML Topical Cream; Loratadine 10 MG Oral Tablet; NDA020800 0.3 ML Epinephrine 1 MG/ML Auto-Injector. Social context: Risk activity involvement; Received higher education; Has a criminal record; Medication review due; Stress; Victim of intimate partner abuse.

Visit 2020-06-17 (ambulatory at Caring Health Center, Inc): Annual exam — psychosocial screening with safety disclosure. Vitals: BP 108/77, HR 67, BMI 30.6. Recorded this visit: Medication review due (resolved); Full-time employment (resolved); Stress (resolved); Victim of intimate partner abuse (active).

## Chart background (full record)

**Problem list**
- Recurrent urinary tract infection
- Body mass index 30+ - obesity

**Medical / surgical history**
- Past pregnancy history of miscarriage
- History of tubal ligation

**Current medications**
- Hydrocortisone 10 MG/ML Topical Cream
- Loratadine 10 MG Oral Tablet
- NDA020800 0.3 ML Epinephrine 1 MG/ML Auto-Injector

**Social & administrative context**
- Risk activity involvement
- Received higher education
- Has a criminal record
- Medication review due
- Stress
- Victim of intimate partner abuse

**Record depth:** 193 Observation, 107 Procedure, 67 DiagnosticReport, 39 Condition, 37 DocumentReference, 37 Encounter, 14 Immunization, 6 MedicationRequest, 5 Device, 3 AllergyIntolerance, 3 CarePlan, 3 CareTeam, 3 ImagingStudy, 2 Medication

## This encounter — 2020-06-17

*ambulatory · Caring Health Center, Inc · General examination of patient (procedure)*

**Conditions recorded**
- Medication review due (resolved)
- Full-time employment (resolved)
- Stress (resolved)
- Victim of intimate partner abuse (active)

**Vitals**
- Height: 172.9 cm
- Pain severity (0–10): 1
- Weight: 91.4 kg
- BMI: 30.6 kg/m²
- Blood pressure: 108/77 mmHg
- Heart rate: 67 /min
- Respiratory rate: 16 /min

**Assessments & screenings**
- Tobacco smoking status: Never smoked tobacco
- Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]: What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 10131 /a; How many people are living or staying at this address [#] 8
- Generalized anxiety disorder 7 item (GAD-7) total score [Reported.PHQ]: 7
- Total score [HARK]: 2
- Patient Health Questionnaire 2 item (PHQ-2) total score [Reported]: 0
- Total score [DAST-10]: 2

**Procedures**
- Assessment of health and social care needs
- Assessment of anxiety
- Screening for domestic abuse
- Depression screening ×2
- Assessment of substance use
- Screening for drug abuse
- Patient referral for dental care

**Reports**
- Generalized anxiety disorder 7 item (GAD-7)
- Humiliation, Afraid, Rape, and Kick questionnaire [HARK]
- Patient Health Questionnaire 2 item (PHQ-2) [Reported]
- Drug Abuse Screening Test-10 [DAST-10]
- History and physical note

**Immunizations**
- Influenza, split virus, trivalent, PF

## Provenance

Derived deterministically from `synthetic-ambient-fhir-25` record `256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07` (FHIR R4, Synthea). The paired ambient transcript (1364 words) and clinical note (582 words) live in the dataset record, keyed by `record_id`. Regenerate: `uv run python scripts/build_patient_contexts.py`.
