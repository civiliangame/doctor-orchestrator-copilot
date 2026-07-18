---
name: Lamont Ernser
dob: 1971-05-08
gender: male
city: "New Bedford, MA"
marital_status: Divorced
language: English (United States)
fhir_patient_id: 4c893b3e-df6f-a2f0-5d03-98714cbad61a
record_id: "4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4"
dataset: synthetic-ambient-fhir-25
last_encounter: 2023-05-20
source: patient-context-model
slots: 52
ledger_entries: 53
synthetic: true
---

# Lamont Ernser — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Lamont Ernser, 52-year-old man (DOB 1971-05-08), New Bedford, MA. Tobacco: ex-smoker. Problem list: Body mass index 30+ - obesity; Gingivitis. Current medications on record: diphenhydrAMINE Hydrochloride 25 MG Oral Tablet. Social context: Educated to high school level; Social isolation; Limited social contact; Has a criminal record; Medication review due.

Visit 2023-05-20 (ambulatory at Greater New Bedford Community Health Center Inc): General adult exam — preventive screening and sleep review. Vitals: BP 143/75, HR 75, BMI 30.1. Recorded this visit: Gingivitis (resolved).

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2023-05-20 — General adult exam — preventive screening and sleep review (ambulatory · Greater New Bedford Community Health Center Inc)[^1]

**Problems**
- **Body mass index 30+ - obesity:** On problem list (longitudinal record)[^2]
- **Gingivitis:** Resolved — recorded at 2023-05-20 encounter[^3]

**Medications**
- **diphenhydrAMINE Hydrochloride 25 MG Oral Tablet:** On medication list (longitudinal record)[^4]

**Social context**
- **Educated to high school level:** Reported in longitudinal record[^5]
- **Social isolation:** Reported in longitudinal record[^6]
- **Limited social contact:** Reported in longitudinal record[^7]
- **Has a criminal record:** Reported in longitudinal record[^8]
- **Medication review due:** Reported in longitudinal record[^9]
- **Tobacco smoking status:** Ex-smoker[^10]

**Vitals**
- **Height:** 180.6 cm[^11]
- **Pain severity (0–10):** 0[^12]
- **Weight:** 98.1 kg[^13]
- **BMI:** 30.1 kg/m²[^14]
- **Blood pressure:** 143/75 mmHg[^15]
- **Heart rate:** 75 /min[^16]
- **Respiratory rate:** 14 /min[^17]

**Labs**
- **Cholesterol [Mass/volume] in Serum or Plasma:** 114.7 mg/dL[^18]
- **Triglyceride [Mass/volume] in Serum or Plasma:** 141.6 mg/dL[^19]
- **Cholesterol in LDL [Mass/volume] in Serum or Plasma by Direct assay:** 30.3 mg/dL[^20]
- **Cholesterol in HDL [Mass/volume] in Serum or Plasma:** 56.1 mg/dL[^21]
- **Leukocytes [#/volume] in Blood by Automated count:** 7.8 10³/µL[^22]
- **Erythrocytes [#/volume] in Blood by Automated count:** 4.8 10⁶/µL[^23]
- **Hemoglobin [Mass/volume] in Blood:** 17.4 g/dL[^24]
- **Hematocrit [Volume Fraction] of Blood by Automated count:** 48.1 %[^25]
- **MCV [Entitic mean volume] in Red Blood Cells by Automated count:** 91.8 fL[^26]
- **MCH [Entitic mass] by Automated count:** 29.4 pg[^27]
- **MCHC [Entitic Mass/volume] in Red Blood Cells by Automated count:** 34.5 g/dL[^28]
- **Erythrocyte [DistWidth] in Blood by Automated count:** 42.5 fL[^29]
- **Platelets [#/volume] in Blood by Automated count:** 318.6 10³/µL[^30]
- **Platelet distribution width [Entitic volume] in Blood by Automated count:** 11 fL[^31]
- **Platelet [Entitic mean volume] in Blood by Automated count:** 9.5 fL[^32]

**Assessments & screenings**
- **Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]:** What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 143750 /a; How many people are living or staying at this address [#] 2[^33]
- **Generalized anxiety disorder 7 item (GAD-7) total score [Reported.PHQ]:** 2[^34]
- **Total score [HARK]:** 0[^35]
- **Patient Health Questionnaire 2 item (PHQ-2) total score [Reported]:** 0[^36]
- **Total score [AUDIT-C]:** 2[^37]

**Procedures**
- **Assessment of health and social care needs:** Performed this encounter (2023-05-20)[^38]
- **Assessment of anxiety:** Performed this encounter (2023-05-20)[^39]
- **Screening for domestic abuse:** Performed this encounter (2023-05-20)[^40]
- **Depression screening:** Performed this encounter (2023-05-20) ×2[^41]
- **Assessment of substance use:** Performed this encounter (2023-05-20)[^42]
- **Assessment using Alcohol Use Disorders Identification Test - Consumption:** Performed this encounter (2023-05-20)[^43]
- **Patient referral for dental care:** Performed this encounter (2023-05-20)[^44]

**Reports**
- **Lipid panel with direct LDL - Serum or Plasma:** Filed this encounter (2023-05-20)[^45]
- **CBC panel - Blood by Automated count:** Filed this encounter (2023-05-20)[^46]
- **Generalized anxiety disorder 7 item (GAD-7):** Filed this encounter (2023-05-20)[^47]
- **Humiliation, Afraid, Rape, and Kick questionnaire [HARK]:** Filed this encounter (2023-05-20)[^48]
- **Patient Health Questionnaire 2 item (PHQ-2) [Reported]:** Filed this encounter (2023-05-20)[^49]
- **Alcohol Use Disorder Identification Test - Consumption [AUDIT-C]:** Filed this encounter (2023-05-20)[^50]
- **History and physical note:** Filed this encounter (2023-05-20)[^51]

**Immunizations**
- **Influenza, split virus, trivalent, PF:** Administered this encounter (2023-05-20)[^52]

## Provenance

Rendered from the Patient Context Model (52 slots; 53 ledger entries — 53 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Encounter/4c893b3e-df6f-a2f0-3e2d-587d1263ccd4` — Greater New Bedford Community Health Center Inc (FHIR record)
[^2]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Condition/4c893b3e-df6f-a2f0-8593-4bdb192d7b3b` — Greater New Bedford Community Health Center Inc (FHIR record) · 2 ledger entries
[^4]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#longitudinal` — EHR longitudinal record (FHIR record)
[^5]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#longitudinal` — EHR longitudinal record (FHIR record)
[^6]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#longitudinal` — EHR longitudinal record (FHIR record)
[^7]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#longitudinal` — EHR longitudinal record (FHIR record)
[^8]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#longitudinal` — EHR longitudinal record (FHIR record)
[^9]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#longitudinal` — EHR longitudinal record (FHIR record)
[^10]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-40b3-93ccb2f12372` — Greater New Bedford Community Health Center Inc (FHIR record)
[^11]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-ce47-6250bec9541a` — Greater New Bedford Community Health Center Inc (FHIR record)
[^12]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-03c5-f8806d16e731` — Greater New Bedford Community Health Center Inc (FHIR record)
[^13]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-bf5c-90b61bc93dcc` — Greater New Bedford Community Health Center Inc (FHIR record)
[^14]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-301e-e963214bbcd4` — Greater New Bedford Community Health Center Inc (FHIR record)
[^15]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-0e8a-bb5f0ecd7a82` — Greater New Bedford Community Health Center Inc (FHIR record)
[^16]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-3ec4-050d8950ae5d` — Greater New Bedford Community Health Center Inc (FHIR record)
[^17]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-2ca0-38239e0dc8d2` — Greater New Bedford Community Health Center Inc (FHIR record)
[^18]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-dd9f-1219413c94c2` — Greater New Bedford Community Health Center Inc (FHIR record)
[^19]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-6fb7-51bcf6d06192` — Greater New Bedford Community Health Center Inc (FHIR record)
[^20]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-ad46-82e960f42053` — Greater New Bedford Community Health Center Inc (FHIR record)
[^21]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-d852-3348558a4348` — Greater New Bedford Community Health Center Inc (FHIR record)
[^22]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-aeb2-1f729853c2ea` — Greater New Bedford Community Health Center Inc (FHIR record)
[^23]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-9f53-693a927be444` — Greater New Bedford Community Health Center Inc (FHIR record)
[^24]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-2803-280862a77179` — Greater New Bedford Community Health Center Inc (FHIR record)
[^25]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-b87b-74677f33fe8d` — Greater New Bedford Community Health Center Inc (FHIR record)
[^26]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-c943-feb63caf8ff9` — Greater New Bedford Community Health Center Inc (FHIR record)
[^27]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-bef1-f11dd9fd078b` — Greater New Bedford Community Health Center Inc (FHIR record)
[^28]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-f82f-7cbf8657fb8a` — Greater New Bedford Community Health Center Inc (FHIR record)
[^29]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-fa92-862dea9c5c1d` — Greater New Bedford Community Health Center Inc (FHIR record)
[^30]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-a6cd-251bc6988aec` — Greater New Bedford Community Health Center Inc (FHIR record)
[^31]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-4e39-eb562676c907` — Greater New Bedford Community Health Center Inc (FHIR record)
[^32]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-cd71-26f4edb51f06` — Greater New Bedford Community Health Center Inc (FHIR record)
[^33]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-4e8c-9f1e611a4346` — Greater New Bedford Community Health Center Inc (FHIR record)
[^34]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-480a-e5bf8e465b44` — Greater New Bedford Community Health Center Inc (FHIR record)
[^35]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-e218-c529887c2951` — Greater New Bedford Community Health Center Inc (FHIR record)
[^36]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-3b4e-fc33858fc31e` — Greater New Bedford Community Health Center Inc (FHIR record)
[^37]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Observation/4c893b3e-df6f-a2f0-2445-240d9adf79ff` — Greater New Bedford Community Health Center Inc (FHIR record)
[^38]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Procedure/4c893b3e-df6f-a2f0-57be-208bebc4ecf3` — Greater New Bedford Community Health Center Inc (FHIR record)
[^39]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Procedure/4c893b3e-df6f-a2f0-854a-254f1706737d` — Greater New Bedford Community Health Center Inc (FHIR record)
[^40]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Procedure/4c893b3e-df6f-a2f0-8029-08c367a00bb7` — Greater New Bedford Community Health Center Inc (FHIR record)
[^41]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Procedure/4c893b3e-df6f-a2f0-b686-6c8452b10f93,Procedure/4c893b3e-df6f-a2f0-b1a8-ddd765b17d72` — Greater New Bedford Community Health Center Inc (FHIR record)
[^42]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Procedure/4c893b3e-df6f-a2f0-ac2a-04eee6da661e` — Greater New Bedford Community Health Center Inc (FHIR record)
[^43]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Procedure/4c893b3e-df6f-a2f0-dc19-a5265604d77c` — Greater New Bedford Community Health Center Inc (FHIR record)
[^44]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Procedure/4c893b3e-df6f-a2f0-c979-79bad8c9a5a7` — Greater New Bedford Community Health Center Inc (FHIR record)
[^45]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#DiagnosticReport/4c893b3e-df6f-a2f0-6182-5f429216c333` — Greater New Bedford Community Health Center Inc (FHIR record)
[^46]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#DiagnosticReport/4c893b3e-df6f-a2f0-73db-2e0951417404` — Greater New Bedford Community Health Center Inc (FHIR record)
[^47]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#DiagnosticReport/4c893b3e-df6f-a2f0-2f83-6bc621952fa8` — Greater New Bedford Community Health Center Inc (FHIR record)
[^48]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#DiagnosticReport/4c893b3e-df6f-a2f0-8a9d-2b90c122d5b0` — Greater New Bedford Community Health Center Inc (FHIR record)
[^49]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#DiagnosticReport/4c893b3e-df6f-a2f0-0c70-653742f3db54` — Greater New Bedford Community Health Center Inc (FHIR record)
[^50]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#DiagnosticReport/4c893b3e-df6f-a2f0-2a75-a4d1050d2385` — Greater New Bedford Community Health Center Inc (FHIR record)
[^51]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#DiagnosticReport/4b9f599f-062a-b6c3-a8af-0d15caebd753` — Greater New Bedford Community Health Center Inc (FHIR record)
[^52]: `fhir:4c893b3e-df6f-a2f0-5d03-98714cbad61a::4c893b3e-df6f-a2f0-3e2d-587d1263ccd4#Immunization/4c893b3e-df6f-a2f0-7830-cd86ec70a7c7` — Greater New Bedford Community Health Center Inc (FHIR record)
