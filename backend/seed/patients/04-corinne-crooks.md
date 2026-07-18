---
name: Corinne Crooks
dob: 1970-12-13
gender: female
city: "East Sandwich, MA"
marital_status: Married
language: English (United States)
fhir_patient_id: 6b716621-5454-68ec-2017-362939ab6f36
record_id: "6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2"
dataset: synthetic-ambient-fhir-25
last_encounter: 2017-01-01
source: patient-context-model
slots: 47
ledger_entries: 49
synthetic: true
---

# Corinne Crooks — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Corinne Crooks, 46-year-old woman (DOB 1970-12-13), East Sandwich, MA. Tobacco: ex-smoker. Problem list: Chronic sinusitis; Body mass index 30+ - obesity. History: History of tubal ligation. No current medications on record. Social context: Risk activity involvement; Received higher education; Medication review due; Not in labor force.

Visit 2017-01-01 (ambulatory at Leap Into Wellness,LLC): Annual wellness examination — preventive screening and health maintenance. Vitals: BP 102/71, HR 70, BMI 28.1. Recorded this visit: Medication review due (resolved); Not in labor force (resolved).

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2017-01-01 — Annual wellness examination — preventive screening and health maintenance (ambulatory · Leap Into Wellness,LLC)[^1]

**Problems**
- **Chronic sinusitis:** On problem list (longitudinal record)[^2]
- **Body mass index 30+ - obesity:** On problem list (longitudinal record)[^3]

**Medical / surgical history**
- **History of tubal ligation:** On record (longitudinal)[^4]

**Social context**
- **Risk activity involvement:** Reported in longitudinal record[^5]
- **Received higher education:** Reported in longitudinal record[^6]
- **Medication review due:** Resolved — recorded at 2017-01-01 encounter[^7]
- **Not in labor force:** Resolved — recorded at 2017-01-01 encounter[^8]
- **Tobacco smoking status:** Ex-smoker[^9]

**Vitals**
- **Height:** 170.6 cm[^10]
- **Pain severity (0–10):** 1[^11]
- **Weight:** 81.8 kg[^12]
- **BMI:** 28.1 kg/m²[^13]
- **Blood pressure:** 102/71 mmHg[^14]
- **Heart rate:** 70 /min[^15]
- **Respiratory rate:** 14 /min[^16]

**Labs**
- **Cholesterol [Mass/volume] in Serum or Plasma:** 148.4 mg/dL[^17]
- **Triglyceride [Mass/volume] in Serum or Plasma:** 126.5 mg/dL[^18]
- **Cholesterol in LDL [Mass/volume] in Serum or Plasma by Direct assay:** 64.3 mg/dL[^19]
- **Cholesterol in HDL [Mass/volume] in Serum or Plasma:** 58.8 mg/dL[^20]
- **Leukocytes [#/volume] in Blood by Automated count:** 7.4 10³/µL[^21]
- **Erythrocytes [#/volume] in Blood by Automated count:** 4.8 10⁶/µL[^22]
- **Hemoglobin [Mass/volume] in Blood:** 12.3 g/dL[^23]
- **Hematocrit [Volume Fraction] of Blood by Automated count:** 43.1 %[^24]
- **MCV [Entitic mean volume] in Red Blood Cells by Automated count:** 83.6 fL[^25]
- **MCH [Entitic mass] by Automated count:** 28.1 pg[^26]
- **MCHC [Entitic Mass/volume] in Red Blood Cells by Automated count:** 34.2 g/dL[^27]
- **Erythrocyte [DistWidth] in Blood by Automated count:** 45.6 fL[^28]
- **Platelets [#/volume] in Blood by Automated count:** 436.8 10³/µL[^29]
- **Platelet distribution width [Entitic volume] in Blood by Automated count:** 13.9 fL[^30]
- **Platelet [Entitic mean volume] in Blood by Automated count:** 11.4 fL[^31]

**Assessments & screenings**
- **Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]:** What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 53274 /a; How many people are living or staying at this address [#] 2[^32]
- **Generalized anxiety disorder 7 item (GAD-7) total score [Reported.PHQ]:** 1[^33]
- **Patient Health Questionnaire 2 item (PHQ-2) total score [Reported]:** 0[^34]
- **Total score [AUDIT-C]:** 1[^35]

**Procedures**
- **Assessment of health and social care needs:** Performed this encounter (2017-01-01)[^36]
- **Assessment of anxiety:** Performed this encounter (2017-01-01)[^37]
- **Depression screening:** Performed this encounter (2017-01-01) ×2[^38]
- **Assessment of substance use:** Performed this encounter (2017-01-01)[^39]
- **Assessment using Alcohol Use Disorders Identification Test - Consumption:** Performed this encounter (2017-01-01)[^40]

**Reports**
- **Lipid panel with direct LDL - Serum or Plasma:** Filed this encounter (2017-01-01)[^41]
- **CBC panel - Blood by Automated count:** Filed this encounter (2017-01-01)[^42]
- **Generalized anxiety disorder 7 item (GAD-7):** Filed this encounter (2017-01-01)[^43]
- **Patient Health Questionnaire 2 item (PHQ-2) [Reported]:** Filed this encounter (2017-01-01)[^44]
- **Alcohol Use Disorder Identification Test - Consumption [AUDIT-C]:** Filed this encounter (2017-01-01)[^45]
- **History and physical note:** Filed this encounter (2017-01-01)[^46]

**Immunizations**
- **Influenza, split virus, trivalent, PF:** Administered this encounter (2017-01-01)[^47]

## Provenance

Rendered from the Patient Context Model (47 slots; 49 ledger entries — 49 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Encounter/6b716621-5454-68ec-7553-080856a4cfa2` — Leap Into Wellness,LLC (FHIR record)
[^2]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#longitudinal` — EHR longitudinal record (FHIR record)
[^4]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#longitudinal` — EHR longitudinal record (FHIR record)
[^5]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#longitudinal` — EHR longitudinal record (FHIR record)
[^6]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#longitudinal` — EHR longitudinal record (FHIR record)
[^7]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Condition/6b716621-5454-68ec-f322-367ee2342f99` — Leap Into Wellness,LLC (FHIR record) · 2 ledger entries
[^8]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Condition/6b716621-5454-68ec-32b4-67e2b875244e` — Leap Into Wellness,LLC (FHIR record) · 2 ledger entries
[^9]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-c161-496a9ca33762` — Leap Into Wellness,LLC (FHIR record)
[^10]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-75f8-cc7eb6a7601d` — Leap Into Wellness,LLC (FHIR record)
[^11]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-6997-bc33c1a62a13` — Leap Into Wellness,LLC (FHIR record)
[^12]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-a1d8-3e900b3dd5cd` — Leap Into Wellness,LLC (FHIR record)
[^13]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-ad06-efe3d0197f8d` — Leap Into Wellness,LLC (FHIR record)
[^14]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-bded-50845c64c047` — Leap Into Wellness,LLC (FHIR record)
[^15]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-b1ab-619b130b3a67` — Leap Into Wellness,LLC (FHIR record)
[^16]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-4c9e-5772789cc7b8` — Leap Into Wellness,LLC (FHIR record)
[^17]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-a21b-18f066f11735` — Leap Into Wellness,LLC (FHIR record)
[^18]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-ffa2-5f3ea5afee69` — Leap Into Wellness,LLC (FHIR record)
[^19]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-97ef-b97e299e10ec` — Leap Into Wellness,LLC (FHIR record)
[^20]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-a7b5-68993f0c4854` — Leap Into Wellness,LLC (FHIR record)
[^21]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-3df3-f93a7bfa3690` — Leap Into Wellness,LLC (FHIR record)
[^22]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-3e47-b96b713ddd26` — Leap Into Wellness,LLC (FHIR record)
[^23]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-87c9-01a189d4c71f` — Leap Into Wellness,LLC (FHIR record)
[^24]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-567b-6f1b2d9d4905` — Leap Into Wellness,LLC (FHIR record)
[^25]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-b857-508b23725116` — Leap Into Wellness,LLC (FHIR record)
[^26]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-a0db-5d5fbb8d8737` — Leap Into Wellness,LLC (FHIR record)
[^27]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-646c-1d4bf3d6f828` — Leap Into Wellness,LLC (FHIR record)
[^28]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-77c3-c4040aa7bff8` — Leap Into Wellness,LLC (FHIR record)
[^29]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-8a9d-8543b2e867bb` — Leap Into Wellness,LLC (FHIR record)
[^30]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-2df3-a51695caea7b` — Leap Into Wellness,LLC (FHIR record)
[^31]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-4dd7-c8543deb956c` — Leap Into Wellness,LLC (FHIR record)
[^32]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-f811-3e34ab331585` — Leap Into Wellness,LLC (FHIR record)
[^33]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-53ab-0f81e873eb66` — Leap Into Wellness,LLC (FHIR record)
[^34]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-d5bf-0b9c4c726e36` — Leap Into Wellness,LLC (FHIR record)
[^35]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Observation/6b716621-5454-68ec-0740-9c806e6eb9c0` — Leap Into Wellness,LLC (FHIR record)
[^36]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Procedure/6b716621-5454-68ec-2e83-f115fe370406` — Leap Into Wellness,LLC (FHIR record)
[^37]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Procedure/6b716621-5454-68ec-86fb-94f22a74df23` — Leap Into Wellness,LLC (FHIR record)
[^38]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Procedure/6b716621-5454-68ec-dee2-f3fb9a29f63a,Procedure/6b716621-5454-68ec-6f75-0e63cd829b0c` — Leap Into Wellness,LLC (FHIR record)
[^39]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Procedure/6b716621-5454-68ec-7f02-b6b57a24aff2` — Leap Into Wellness,LLC (FHIR record)
[^40]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Procedure/6b716621-5454-68ec-de04-f6a937f0629f` — Leap Into Wellness,LLC (FHIR record)
[^41]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#DiagnosticReport/6b716621-5454-68ec-8d9c-4a4806dd4fd2` — Leap Into Wellness,LLC (FHIR record)
[^42]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#DiagnosticReport/6b716621-5454-68ec-fb46-c17ad726d715` — Leap Into Wellness,LLC (FHIR record)
[^43]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#DiagnosticReport/6b716621-5454-68ec-99d9-e5cba85c6204` — Leap Into Wellness,LLC (FHIR record)
[^44]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#DiagnosticReport/6b716621-5454-68ec-d51f-5da85fae71da` — Leap Into Wellness,LLC (FHIR record)
[^45]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#DiagnosticReport/6b716621-5454-68ec-f1e6-9b4f6b815ece` — Leap Into Wellness,LLC (FHIR record)
[^46]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#DiagnosticReport/b4b75f22-bc37-9455-fefe-ac12120d5fdf` — Leap Into Wellness,LLC (FHIR record)
[^47]: `fhir:6b716621-5454-68ec-2017-362939ab6f36::6b716621-5454-68ec-7553-080856a4cfa2#Immunization/6b716621-5454-68ec-8428-080f6f621682` — Leap Into Wellness,LLC (FHIR record)
