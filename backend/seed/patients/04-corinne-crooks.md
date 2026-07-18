---
record_id: "6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2"
patient_id: 6b716621-5454-68ec-2017-362939ab6f36
encounter_id: 6b716621-5454-68ec-7553-080856a4cfa2
name: Corinne Crooks
gender: female
birth_date: 1970-12-13
age_at_visit: 46
visit_date: 2017-01-01
visit_title: Annual wellness examination — preventive screening and health maintenance
visit_type: General examination of patient (procedure)
encounter_class: ambulatory
provider: "Leap Into Wellness,LLC"
city: "East Sandwich, MA"
marital_status: Married
language: English (United States)
transcript_words: 1336
note_words: 499
dataset: synthetic-ambient-fhir-25
synthetic: true
---

# Corinne Crooks — Annual wellness examination — preventive screening and health maintenance

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Corinne Crooks, 46-year-old woman (DOB 1970-12-13), East Sandwich, MA. Tobacco: ex-smoker. Problem list: Chronic sinusitis; Body mass index 30+ - obesity. History: History of tubal ligation. No current medications on record. Social context: Risk activity involvement; Received higher education; Medication review due; Not in labor force.

Visit 2017-01-01 (ambulatory at Leap Into Wellness,LLC): Annual wellness examination — preventive screening and health maintenance. Vitals: BP 102/71, HR 70, BMI 28.1. Recorded this visit: Medication review due (resolved); Not in labor force (resolved).

## Chart background (full record)

**Problem list**
- Chronic sinusitis
- Body mass index 30+ - obesity

**Medical / surgical history**
- History of tubal ligation

**Current medications:** none recorded

**Social & administrative context**
- Risk activity involvement
- Received higher education
- Medication review due
- Not in labor force

**Record depth:** 139 Observation, 65 Procedure, 44 DiagnosticReport, 21 Condition, 20 DocumentReference, 20 Encounter, 12 Immunization, 5 MedicationRequest, 2 Device, 2 Medication, 1 ImagingStudy

## This encounter — 2017-01-01

*ambulatory · Leap Into Wellness,LLC · General examination of patient (procedure)*

**Conditions recorded**
- Medication review due (resolved)
- Not in labor force (resolved)

**Vitals**
- Height: 170.6 cm
- Pain severity (0–10): 1
- Weight: 81.8 kg
- BMI: 28.1 kg/m²
- Blood pressure: 102/71 mmHg
- Heart rate: 70 /min
- Respiratory rate: 14 /min

**Labs**
- Cholesterol [Mass/volume] in Serum or Plasma: 148.4 mg/dL
- Triglyceride [Mass/volume] in Serum or Plasma: 126.5 mg/dL
- Cholesterol in LDL [Mass/volume] in Serum or Plasma by Direct assay: 64.3 mg/dL
- Cholesterol in HDL [Mass/volume] in Serum or Plasma: 58.8 mg/dL
- Leukocytes [#/volume] in Blood by Automated count: 7.4 10³/µL
- Erythrocytes [#/volume] in Blood by Automated count: 4.8 10⁶/µL
- Hemoglobin [Mass/volume] in Blood: 12.3 g/dL
- Hematocrit [Volume Fraction] of Blood by Automated count: 43.1 %
- MCV [Entitic mean volume] in Red Blood Cells by Automated count: 83.6 fL
- MCH [Entitic mass] by Automated count: 28.1 pg
- MCHC [Entitic Mass/volume] in Red Blood Cells by Automated count: 34.2 g/dL
- Erythrocyte [DistWidth] in Blood by Automated count: 45.6 fL
- Platelets [#/volume] in Blood by Automated count: 436.8 10³/µL
- Platelet distribution width [Entitic volume] in Blood by Automated count: 13.9 fL
- Platelet [Entitic mean volume] in Blood by Automated count: 11.4 fL

**Assessments & screenings**
- Tobacco smoking status: Ex-smoker
- Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]: What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 53274 /a; How many people are living or staying at this address [#] 2
- Generalized anxiety disorder 7 item (GAD-7) total score [Reported.PHQ]: 1
- Patient Health Questionnaire 2 item (PHQ-2) total score [Reported]: 0
- Total score [AUDIT-C]: 1

**Procedures**
- Assessment of health and social care needs
- Assessment of anxiety
- Depression screening ×2
- Assessment of substance use
- Assessment using Alcohol Use Disorders Identification Test - Consumption

**Reports**
- Lipid panel with direct LDL - Serum or Plasma
- CBC panel - Blood by Automated count
- Generalized anxiety disorder 7 item (GAD-7)
- Patient Health Questionnaire 2 item (PHQ-2) [Reported]
- Alcohol Use Disorder Identification Test - Consumption [AUDIT-C]
- History and physical note

**Immunizations**
- Influenza, split virus, trivalent, PF

## Provenance

Derived deterministically from `synthetic-ambient-fhir-25` record `6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2` (FHIR R4, Synthea). The paired ambient transcript (1336 words) and clinical note (499 words) live in the dataset record, keyed by `record_id`. Regenerate: `uv run python scripts/build_patient_contexts.py`.
