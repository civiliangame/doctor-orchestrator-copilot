---
record_id: "3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea"
patient_id: 3a3a1f26-ed23-f65c-a7df-c96fac56f464
encounter_id: 3a3a1f26-ed23-f65c-e264-be689558faea
name: Ali Kuhic
gender: male
birth_date: 1991-05-24
age_at_visit: 31
visit_date: 2022-08-05
visit_title: Annual physical — preventive screening and migraine check-in
visit_type: General examination of patient (procedure)
encounter_class: ambulatory
provider: Whitley Wellness LLC
city: "Chelsea, MA"
marital_status: Never Married
language: English (United States)
transcript_words: 1485
note_words: 555
dataset: synthetic-ambient-fhir-25
synthetic: true
---

# Ali Kuhic — Annual physical — preventive screening and migraine check-in

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Ali Kuhic, 31-year-old man (DOB 1991-05-24), Chelsea, MA. Tobacco: never smoked tobacco. Problem list: Chronic intractable migraine without aura; Gingivitis. No current medications on record. Social context: Risk activity involvement; Received higher education; Transport problem; Lack of access to transportation; Stress; Social isolation.

Visit 2022-08-05 (ambulatory at Whitley Wellness LLC): Annual physical — preventive screening and migraine check-in. Vitals: BP 98/83, HR 93, BMI 25.3. Recorded this visit: Full-time employment (resolved); Social isolation (active); Gingivitis (resolved).

## Chart background (full record)

**Problem list**
- Chronic intractable migraine without aura
- Gingivitis

**Current medications:** none recorded

**Social & administrative context**
- Risk activity involvement
- Received higher education
- Transport problem
- Lack of access to transportation
- Stress
- Social isolation

**Record depth:** 84 Observation, 49 Procedure, 34 DiagnosticReport, 25 Condition, 22 DocumentReference, 22 Encounter, 8 Immunization, 5 MedicationRequest, 2 Device, 2 ImagingStudy, 2 Medication, 1 CarePlan, 1 CareTeam

## This encounter — 2022-08-05

*ambulatory · Whitley Wellness LLC · General examination of patient (procedure)*

**Conditions recorded**
- Full-time employment (resolved)
- Social isolation (active)
- Gingivitis (resolved)

**Vitals**
- Height: 176.3 cm
- Pain severity (0–10): 2
- Weight: 78.7 kg
- BMI: 25.3 kg/m²
- Blood pressure: 98/83 mmHg
- Heart rate: 93 /min
- Respiratory rate: 14 /min

**Labs**
- Cholesterol [Mass/volume] in Serum or Plasma: 198.2 mg/dL
- Triglyceride [Mass/volume] in Serum or Plasma: 138.8 mg/dL
- Cholesterol in LDL [Mass/volume] in Serum or Plasma by Direct assay: 137.2 mg/dL
- Cholesterol in HDL [Mass/volume] in Serum or Plasma: 33.2 mg/dL

**Assessments & screenings**
- Tobacco smoking status: Never smoked tobacco
- Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]: What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 26021 /a; How many people are living or staying at this address [#] 7
- Total score [HARK]: 0
- Total score [DAST-10]: 0

**Procedures**
- Medication reconciliation
- Assessment of health and social care needs
- Screening for domestic abuse
- Assessment of substance use
- Screening for drug abuse
- Patient referral for dental care

**Reports**
- Lipid panel with direct LDL - Serum or Plasma
- Humiliation, Afraid, Rape, and Kick questionnaire [HARK]
- Drug Abuse Screening Test-10 [DAST-10]
- History and physical note

**Immunizations**
- Influenza, split virus, trivalent, PF
- Td (adult), 5 Lf tetanus toxoid, preservative free, adsorbed

## Provenance

Derived deterministically from `synthetic-ambient-fhir-25` record `3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea` (FHIR R4, Synthea). The paired ambient transcript (1485 words) and clinical note (555 words) live in the dataset record, keyed by `record_id`. Regenerate: `uv run python scripts/build_patient_contexts.py`.
