---
record_id: "374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00"
patient_id: 374e68b2-ee15-0852-cd48-3c7b6fd8e114
encounter_id: 374e68b2-ee15-0852-8f80-26e1007e6c00
name: Dick Larson
gender: male
birth_date: 1987-05-23
age_at_visit: 36
visit_date: 2024-05-18
visit_title: Annual check-up — post-sepsis recovery and prediabetes
visit_type: Encounter for check up (procedure)
encounter_class: ambulatory
provider: "Children's Hospital Corporation"
city: "Waltham, MA"
marital_status: Married
language: English (United States)
transcript_words: 1601
note_words: 546
dataset: synthetic-ambient-fhir-25
synthetic: true
---

# Dick Larson — Annual check-up — post-sepsis recovery and prediabetes

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Dick Larson, 36-year-old man (DOB 1987-05-23), Waltham, MA. Tobacco: never smoked tobacco. Problem list: Prediabetes; Body mass index 30+ - obesity; Sepsis; Septic shock; Acute respiratory distress syndrome; Anemia. No current medications on record. Social context: Housing unsatisfactory; Received higher education; Medication review due; Unemployed; Social isolation.

Visit 2024-05-18 (ambulatory at Children's Hospital Corporation): Annual check-up — post-sepsis recovery and prediabetes. Vitals: BP 107/69, HR 63, BMI 30.3. Recorded this visit: Medication review due (resolved); Unemployed (active); Social isolation (resolved).

## Chart background (full record)

**Problem list**
- Prediabetes
- Body mass index 30+ - obesity
- Sepsis
- Septic shock
- Acute respiratory distress syndrome
- Anemia

**Current medications:** none recorded

**Social & administrative context**
- Housing unsatisfactory
- Received higher education
- Medication review due
- Unemployed
- Social isolation

**Record depth:** 137 Observation, 36 DiagnosticReport, 32 Procedure, 23 Condition, 15 DocumentReference, 15 Encounter, 6 Immunization, 2 CarePlan, 2 CareTeam, 1 Device, 1 MedicationRequest

## This encounter — 2024-05-18

*ambulatory · Children's Hospital Corporation · Encounter for check up (procedure)*

**Conditions recorded**
- Medication review due (resolved)
- Unemployed (active)
- Social isolation (resolved)

**Vitals**
- Height: 166.8 cm
- Pain severity (0–10): 1
- Weight: 84.4 kg
- BMI: 30.3 kg/m²
- Blood pressure: 107/69 mmHg
- Heart rate: 63 /min
- Respiratory rate: 15 /min

**Labs**
- Hemoglobin A1c/Hemoglobin.total in Blood: 6 %
- Glucose [Mass/volume] in Blood: 86.7 mg/dL
- Urea nitrogen [Mass/volume] in Blood: 13.8 mg/dL
- Creatinine [Mass/volume] in Blood: 1.2 mg/dL
- Calcium [Mass/volume] in Blood: 10 mg/dL
- Sodium [Moles/volume] in Blood: 139.1 mmol/L
- Potassium [Moles/volume] in Blood: 4.9 mmol/L
- Chloride [Moles/volume] in Blood: 104 mmol/L
- Carbon dioxide, total [Moles/volume] in Blood: 28.1 mmol/L

**Assessments & screenings**
- Tobacco smoking status: Never smoked tobacco
- Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]: What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 198810 /a; How many people are living or staying at this address [#] 6
- Patient Health Questionnaire 2 item (PHQ-2) total score [Reported]: 1
- Total score [DAST-10]: 0

**Procedures**
- Medication reconciliation
- Assessment of health and social care needs
- Depression screening ×2
- Assessment of substance use
- Screening for drug abuse

**Reports**
- Basic metabolic panel - Blood
- Patient Health Questionnaire 2 item (PHQ-2) [Reported]
- Drug Abuse Screening Test-10 [DAST-10]
- History and physical note

**Immunizations**
- Influenza, split virus, trivalent, PF

## Provenance

Derived deterministically from `synthetic-ambient-fhir-25` record `374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00` (FHIR R4, Synthea). The paired ambient transcript (1601 words) and clinical note (546 words) live in the dataset record, keyed by `record_id`. Regenerate: `uv run python scripts/build_patient_contexts.py`.
