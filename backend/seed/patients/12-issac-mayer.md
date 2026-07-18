---
record_id: "be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b"
patient_id: be1b73f7-b0f0-0ca3-b24b-28369ce68943
encounter_id: be1b73f7-b0f0-0ca3-5c23-d051118e002b
name: Issac Mayer
gender: male
birth_date: 1988-05-01
age_at_visit: 31
visit_date: 2019-07-14
visit_title: Annual physical — new adult patient wellness exam
visit_type: General examination of patient (procedure)
encounter_class: ambulatory
provider: "Clarity Health & Wellness LLC"
city: "Wilmington, MA"
marital_status: Divorced
language: English (United States)
transcript_words: 1302
note_words: 515
dataset: synthetic-ambient-fhir-25
synthetic: true
---

# Issac Mayer — Annual physical — new adult patient wellness exam

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Issac Mayer, 31-year-old man (DOB 1988-05-01), Wilmington, MA. Tobacco: never smoked tobacco. Problem list: Body mass index 30+ - obesity. No current medications on record. Social context: Received higher education; Reports of violence in the environment; Medication review due.

Visit 2019-07-14 (ambulatory at Clarity Health & Wellness LLC): Annual physical — new adult patient wellness exam. Vitals: BP 103/67, HR 69, BMI 31.4. Recorded this visit: Medication review due (resolved); Full-time employment (resolved).

## Chart background (full record)

**Problem list**
- Body mass index 30+ - obesity

**Current medications:** none recorded

**Social & administrative context**
- Received higher education
- Reports of violence in the environment
- Medication review due

**Record depth:** 58 Observation, 24 DiagnosticReport, 17 Procedure, 14 Condition, 13 DocumentReference, 13 Encounter, 6 Immunization, 2 CarePlan, 2 CareTeam, 1 MedicationRequest

## This encounter — 2019-07-14

*ambulatory · Clarity Health & Wellness LLC · General examination of patient (procedure)*

**Conditions recorded**
- Medication review due (resolved)
- Full-time employment (resolved)

**Vitals**
- Height: 164.3 cm
- Pain severity (0–10): 1
- Weight: 84.9 kg
- BMI: 31.4 kg/m²
- Blood pressure: 103/67 mmHg
- Heart rate: 69 /min
- Respiratory rate: 15 /min

**Labs**
- Cholesterol [Mass/volume] in Serum or Plasma: 110.2 mg/dL
- Triglyceride [Mass/volume] in Serum or Plasma: 117.1 mg/dL
- Cholesterol in LDL [Mass/volume] in Serum or Plasma by Direct assay: 35.8 mg/dL
- Cholesterol in HDL [Mass/volume] in Serum or Plasma: 51 mg/dL

**Assessments & screenings**
- Tobacco smoking status: Never smoked tobacco
- Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]: What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 100740 /a; How many people are living or staying at this address [#] 4
- Generalized anxiety disorder 7 item (GAD-7) total score [Reported.PHQ]: 1
- Total score [HARK]: 0
- Patient Health Questionnaire 2 item (PHQ-2) total score [Reported]: 2
- Total score [DAST-10]: 2

**Procedures**
- Medication reconciliation
- Assessment of health and social care needs
- Assessment of anxiety
- Screening for domestic abuse
- Depression screening ×2
- Assessment of substance use
- Screening for drug abuse

**Reports**
- Lipid panel with direct LDL - Serum or Plasma
- Generalized anxiety disorder 7 item (GAD-7)
- Humiliation, Afraid, Rape, and Kick questionnaire [HARK]
- Patient Health Questionnaire 2 item (PHQ-2) [Reported]
- Drug Abuse Screening Test-10 [DAST-10]
- History and physical note

**Immunizations**
- Influenza, split virus, trivalent, PF
- Td (adult), 5 Lf tetanus toxoid, preservative free, adsorbed

## Provenance

Derived deterministically from `synthetic-ambient-fhir-25` record `be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b` (FHIR R4, Synthea). The paired ambient transcript (1302 words) and clinical note (515 words) live in the dataset record, keyed by `record_id`. Regenerate: `uv run python scripts/build_patient_contexts.py`.
