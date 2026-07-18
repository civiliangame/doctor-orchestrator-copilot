---
record_id: "01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5"
patient_id: 01573895-dbf5-29c6-4ef9-cd09aecc51f6
encounter_id: 01573895-dbf5-29c6-f885-ade2bd6537a5
name: "Van O'Reilly"
gender: male
birth_date: 1977-07-14
age_at_visit: 42
visit_date: 2019-07-25
visit_title: Annual physical — hand osteoarthritis and anxiety screening
visit_type: General examination of patient (procedure)
encounter_class: ambulatory
provider: Melrose Internal Medicine Assoc PC
city: "Everett, MA"
marital_status: Married
language: English (United States)
transcript_words: 1484
note_words: 607
dataset: synthetic-ambient-fhir-25
synthetic: true
---

# Van O'Reilly — Annual physical — hand osteoarthritis and anxiety screening

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Van O'Reilly, 42-year-old man (DOB 1977-07-14), Everett, MA. Tobacco: never smoked tobacco. Problem list: Localized, primary osteoarthritis of the hand; Body mass index 30+ - obesity. Current medications on record: Naproxen sodium 220 MG Oral Tablet. Social context: Educated to high school level; Medication review due; Stress.

Visit 2019-07-25 (ambulatory at Melrose Internal Medicine Assoc PC): Annual physical — hand osteoarthritis and anxiety screening. Vitals: BP 102/78, HR 74, BMI 28. Recorded this visit: Medication review due (resolved); Stress (resolved).

## Chart background (full record)

**Problem list**
- Localized, primary osteoarthritis of the hand
- Body mass index 30+ - obesity

**Current medications**
- Naproxen sodium 220 MG Oral Tablet

**Social & administrative context**
- Educated to high school level
- Medication review due
- Stress

**Record depth:** 89 Observation, 59 Procedure, 36 DiagnosticReport, 18 DocumentReference, 18 Encounter, 15 Condition, 10 Immunization, 1 CarePlan, 1 CareTeam, 1 Device, 1 ImagingStudy, 1 MedicationRequest

## This encounter — 2019-07-25

*ambulatory · Melrose Internal Medicine Assoc PC · General examination of patient (procedure)*

**Conditions recorded**
- Medication review due (resolved)
- Stress (resolved)

**Vitals**
- Height: 162.1 cm
- Pain severity (0–10): 3
- Weight: 73.5 kg
- BMI: 28 kg/m²
- Blood pressure: 102/78 mmHg
- Heart rate: 74 /min
- Respiratory rate: 15 /min

**Labs**
- Cholesterol [Mass/volume] in Serum or Plasma: 157.5 mg/dL
- Triglyceride [Mass/volume] in Serum or Plasma: 134.8 mg/dL
- Cholesterol in LDL [Mass/volume] in Serum or Plasma by Direct assay: 101 mg/dL
- Cholesterol in HDL [Mass/volume] in Serum or Plasma: 29.6 mg/dL

**Assessments & screenings**
- Tobacco smoking status: Never smoked tobacco
- Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]: What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 46526 /a; How many people are living or staying at this address [#] 3
- Generalized anxiety disorder 7 item (GAD-7) total score [Reported.PHQ]: 12
- Patient Health Questionnaire 2 item (PHQ-2) total score [Reported]: 5
- Patient Health Questionnaire 9 item (PHQ-9) total score [Reported]: 4
- Total score [AUDIT-C]: 2

**Procedures**
- Medication reconciliation
- Assessment of health and social care needs
- Assessment of anxiety
- Depression screening ×2
- Depression screening using Patient Health Questionnaire Nine Item score
- Assessment of substance use
- Assessment using Alcohol Use Disorders Identification Test - Consumption
- Patient referral for dental care

**Reports**
- Lipid panel with direct LDL - Serum or Plasma
- Generalized anxiety disorder 7 item (GAD-7)
- Patient Health Questionnaire 2 item (PHQ-2) [Reported]
- PHQ-9 quick depression assessment panel [Reported.PHQ]
- Alcohol Use Disorder Identification Test - Consumption [AUDIT-C]
- History and physical note

**Immunizations**
- Influenza, split virus, trivalent, PF
- Td (adult), 5 Lf tetanus toxoid, preservative free, adsorbed
- Hep A, adult

## Provenance

Derived deterministically from `synthetic-ambient-fhir-25` record `01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5` (FHIR R4, Synthea). The paired ambient transcript (1484 words) and clinical note (607 words) live in the dataset record, keyed by `record_id`. Regenerate: `uv run python scripts/build_patient_contexts.py`.
