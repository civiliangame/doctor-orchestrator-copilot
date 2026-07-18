---
record_id: "d57244c4-df7d-9ce7-7878-38361fc0087b::d57244c4-df7d-9ce7-c30b-92c6cf8c0859"
patient_id: d57244c4-df7d-9ce7-7878-38361fc0087b
encounter_id: d57244c4-df7d-9ce7-c30b-92c6cf8c0859
name: Nigel Ankunding
gender: male
birth_date: 1967-04-10
age_at_visit: 52
visit_date: 2019-04-22
visit_title: Annual physical — prediabetes and psychosocial screening
visit_type: General examination of patient (procedure)
encounter_class: ambulatory
provider: "Plymouth Carver Primary Care, P.C."
city: "Plymouth, MA"
marital_status: Never Married
language: English (United States)
transcript_words: 1405
note_words: 583
dataset: synthetic-ambient-fhir-25
synthetic: true
---

# Nigel Ankunding — Annual physical — prediabetes and psychosocial screening

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Nigel Ankunding, 52-year-old man (DOB 1967-04-10), Plymouth, MA. Tobacco: never smoked tobacco. Problem list: Chronic sinusitis; Prediabetes. No current medications on record. Social context: Educated to high school level; Has a criminal record; Medication review due; Social isolation; Stress.

Visit 2019-04-22 (ambulatory at Plymouth Carver Primary Care, P.C.): Annual physical — prediabetes and psychosocial screening. Vitals: BP 111/71, HR 88, BMI 28. Recorded this visit: Medication review due (resolved); Full-time employment (resolved); Social isolation (resolved); Stress (resolved).

## Chart background (full record)

**Problem list**
- Chronic sinusitis
- Prediabetes

**Current medications:** none recorded

**Social & administrative context**
- Educated to high school level
- Has a criminal record
- Medication review due
- Social isolation
- Stress

**Record depth:** 239 Observation, 113 Procedure, 71 DiagnosticReport, 40 Condition, 35 DocumentReference, 35 Encounter, 15 Immunization, 11 MedicationRequest, 6 Device, 3 CarePlan, 3 CareTeam, 3 ImagingStudy, 3 Medication

## This encounter — 2019-04-22

*ambulatory · Plymouth Carver Primary Care, P.C. · General examination of patient (procedure)*

**Conditions recorded**
- Medication review due (resolved)
- Full-time employment (resolved)
- Social isolation (resolved)
- Stress (resolved)

**Vitals**
- Height: 179.6 cm
- Pain severity (0–10): 4
- Weight: 90.4 kg
- BMI: 28 kg/m²
- Blood pressure: 111/71 mmHg
- Heart rate: 88 /min
- Respiratory rate: 13 /min

**Labs**
- Hemoglobin A1c/Hemoglobin.total in Blood: 5.8 %
- Glucose [Mass/volume] in Blood: 81.1 mg/dL
- Urea nitrogen [Mass/volume] in Blood: 20 mg/dL
- Creatinine [Mass/volume] in Blood: 1.1 mg/dL
- Calcium [Mass/volume] in Blood: 9.3 mg/dL
- Sodium [Moles/volume] in Blood: 141.3 mmol/L
- Potassium [Moles/volume] in Blood: 4.8 mmol/L
- Chloride [Moles/volume] in Blood: 105.2 mmol/L
- Carbon dioxide, total [Moles/volume] in Blood: 22.7 mmol/L
- Leukocytes [#/volume] in Blood by Automated count: 8.8 10³/µL
- Erythrocytes [#/volume] in Blood by Automated count: 4.4 10⁶/µL
- Hemoglobin [Mass/volume] in Blood: 13 g/dL
- Hematocrit [Volume Fraction] of Blood by Automated count: 44.6 %
- MCV [Entitic mean volume] in Red Blood Cells by Automated count: 86.1 fL
- MCH [Entitic mass] by Automated count: 29.7 pg
- MCHC [Entitic Mass/volume] in Red Blood Cells by Automated count: 33.6 g/dL
- Erythrocyte [DistWidth] in Blood by Automated count: 42.3 fL
- Platelets [#/volume] in Blood by Automated count: 340.2 10³/µL
- Platelet distribution width [Entitic volume] in Blood by Automated count: 14.8 fL
- Platelet [Entitic mean volume] in Blood by Automated count: 11.4 fL

**Assessments & screenings**
- Tobacco smoking status: Never smoked tobacco
- Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]: What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 130250 /a; How many people are living or staying at this address [#] 2
- Generalized anxiety disorder 7 item (GAD-7) total score [Reported.PHQ]: 4
- Patient Health Questionnaire 2 item (PHQ-2) total score [Reported]: 1
- Total score [AUDIT-C]: 3

**Procedures**
- Medication reconciliation
- Assessment of health and social care needs
- Assessment of anxiety
- Depression screening ×2
- Assessment of substance use
- Assessment using Alcohol Use Disorders Identification Test - Consumption

**Reports**
- Basic metabolic panel - Blood
- CBC panel - Blood by Automated count
- Generalized anxiety disorder 7 item (GAD-7)
- Patient Health Questionnaire 2 item (PHQ-2) [Reported]
- Alcohol Use Disorder Identification Test - Consumption [AUDIT-C]
- History and physical note

**Immunizations**
- Influenza, split virus, trivalent, PF

## Provenance

Derived deterministically from `synthetic-ambient-fhir-25` record `d57244c4-df7d-9ce7-7878-38361fc0087b::d57244c4-df7d-9ce7-c30b-92c6cf8c0859` (FHIR R4, Synthea). The paired ambient transcript (1405 words) and clinical note (583 words) live in the dataset record, keyed by `record_id`. Regenerate: `uv run python scripts/build_patient_contexts.py`.
