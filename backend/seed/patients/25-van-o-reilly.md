---
name: "Van O'Reilly"
dob: 1977-07-14
gender: male
city: "Everett, MA"
marital_status: Married
language: English (United States)
fhir_patient_id: 01573895-dbf5-29c6-4ef9-cd09aecc51f6
record_id: "01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5"
dataset: synthetic-ambient-fhir-25
last_encounter: 2019-07-25
source: patient-context-model
slots: 41
ledger_entries: 43
synthetic: true
---

# Van O'Reilly — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Van O'Reilly, 42-year-old man (DOB 1977-07-14), Everett, MA. Tobacco: never smoked tobacco. Problem list: Localized, primary osteoarthritis of the hand; Body mass index 30+ - obesity. Current medications on record: Naproxen sodium 220 MG Oral Tablet. Social context: Educated to high school level; Medication review due; Stress.

Visit 2019-07-25 (ambulatory at Melrose Internal Medicine Assoc PC): Annual physical — hand osteoarthritis and anxiety screening. Vitals: BP 102/78, HR 74, BMI 28. Recorded this visit: Medication review due (resolved); Stress (resolved).

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2019-07-25 — Annual physical — hand osteoarthritis and anxiety screening (ambulatory · Melrose Internal Medicine Assoc PC)[^1]

**Problems**
- **Localized, primary osteoarthritis of the hand:** On problem list (longitudinal record)[^2]
- **Body mass index 30+ - obesity:** On problem list (longitudinal record)[^3]

**Medications**
- **Naproxen sodium 220 MG Oral Tablet:** On medication list (longitudinal record)[^4]

**Social context**
- **Educated to high school level:** Reported in longitudinal record[^5]
- **Medication review due:** Resolved — recorded at 2019-07-25 encounter[^6]
- **Stress:** Resolved — recorded at 2019-07-25 encounter[^7]
- **Tobacco smoking status:** Never smoked tobacco[^8]

**Vitals**
- **Height:** 162.1 cm[^9]
- **Pain severity (0–10):** 3[^10]
- **Weight:** 73.5 kg[^11]
- **BMI:** 28 kg/m²[^12]
- **Blood pressure:** 102/78 mmHg[^13]
- **Heart rate:** 74 /min[^14]
- **Respiratory rate:** 15 /min[^15]

**Labs**
- **Cholesterol [Mass/volume] in Serum or Plasma:** 157.5 mg/dL[^16]
- **Triglyceride [Mass/volume] in Serum or Plasma:** 134.8 mg/dL[^17]
- **Cholesterol in LDL [Mass/volume] in Serum or Plasma by Direct assay:** 101 mg/dL[^18]
- **Cholesterol in HDL [Mass/volume] in Serum or Plasma:** 29.6 mg/dL[^19]

**Assessments & screenings**
- **Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]:** What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 46526 /a; How many people are living or staying at this address [#] 3[^20]
- **Generalized anxiety disorder 7 item (GAD-7) total score [Reported.PHQ]:** 12[^21]
- **Patient Health Questionnaire 2 item (PHQ-2) total score [Reported]:** 5[^22]
- **Patient Health Questionnaire 9 item (PHQ-9) total score [Reported]:** 4[^23]
- **Total score [AUDIT-C]:** 2[^24]

**Procedures**
- **Medication reconciliation:** Performed this encounter (2019-07-25)[^25]
- **Assessment of health and social care needs:** Performed this encounter (2019-07-25)[^26]
- **Assessment of anxiety:** Performed this encounter (2019-07-25)[^27]
- **Depression screening:** Performed this encounter (2019-07-25) ×2[^28]
- **Depression screening using Patient Health Questionnaire Nine Item score:** Performed this encounter (2019-07-25)[^29]
- **Assessment of substance use:** Performed this encounter (2019-07-25)[^30]
- **Assessment using Alcohol Use Disorders Identification Test - Consumption:** Performed this encounter (2019-07-25)[^31]
- **Patient referral for dental care:** Performed this encounter (2019-07-25)[^32]

**Reports**
- **Lipid panel with direct LDL - Serum or Plasma:** Filed this encounter (2019-07-25)[^33]
- **Generalized anxiety disorder 7 item (GAD-7):** Filed this encounter (2019-07-25)[^34]
- **Patient Health Questionnaire 2 item (PHQ-2) [Reported]:** Filed this encounter (2019-07-25)[^35]
- **PHQ-9 quick depression assessment panel [Reported.PHQ]:** Filed this encounter (2019-07-25)[^36]
- **Alcohol Use Disorder Identification Test - Consumption [AUDIT-C]:** Filed this encounter (2019-07-25)[^37]
- **History and physical note:** Filed this encounter (2019-07-25)[^38]

**Immunizations**
- **Influenza, split virus, trivalent, PF:** Administered this encounter (2019-07-25)[^39]
- **Td (adult), 5 Lf tetanus toxoid, preservative free, adsorbed:** Administered this encounter (2019-07-25)[^40]
- **Hep A, adult:** Administered this encounter (2019-07-25)[^41]

## Provenance

Rendered from the Patient Context Model (41 slots; 43 ledger entries — 43 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Encounter/01573895-dbf5-29c6-f885-ade2bd6537a5` — Melrose Internal Medicine Assoc PC (FHIR record)
[^2]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#longitudinal` — EHR longitudinal record (FHIR record)
[^4]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#longitudinal` — EHR longitudinal record (FHIR record)
[^5]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#longitudinal` — EHR longitudinal record (FHIR record)
[^6]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Condition/01573895-dbf5-29c6-32c3-074c611c7442` — Melrose Internal Medicine Assoc PC (FHIR record) · 2 ledger entries
[^7]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Condition/01573895-dbf5-29c6-7149-d8b85f7d1ceb` — Melrose Internal Medicine Assoc PC (FHIR record) · 2 ledger entries
[^8]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-2e34-681f040eb73c` — Melrose Internal Medicine Assoc PC (FHIR record)
[^9]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-dff4-22c04fb6d551` — Melrose Internal Medicine Assoc PC (FHIR record)
[^10]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-3b35-f150f40da012` — Melrose Internal Medicine Assoc PC (FHIR record)
[^11]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-174b-8a6209edeabb` — Melrose Internal Medicine Assoc PC (FHIR record)
[^12]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-61d0-0b8c8d00c5f2` — Melrose Internal Medicine Assoc PC (FHIR record)
[^13]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-d0ba-e10b081f68e9` — Melrose Internal Medicine Assoc PC (FHIR record)
[^14]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-a0f6-751712c7f175` — Melrose Internal Medicine Assoc PC (FHIR record)
[^15]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-f9f3-dff9e3f39a2e` — Melrose Internal Medicine Assoc PC (FHIR record)
[^16]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-ec65-53ce93489b08` — Melrose Internal Medicine Assoc PC (FHIR record)
[^17]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-e755-b8c16d78c3f7` — Melrose Internal Medicine Assoc PC (FHIR record)
[^18]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-fef7-a2ba8817ce12` — Melrose Internal Medicine Assoc PC (FHIR record)
[^19]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-5a78-159d52470763` — Melrose Internal Medicine Assoc PC (FHIR record)
[^20]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-c34c-c0e4d98b4148` — Melrose Internal Medicine Assoc PC (FHIR record)
[^21]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-6857-6243c15368a3` — Melrose Internal Medicine Assoc PC (FHIR record)
[^22]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-bf0c-cb71365a2e6f` — Melrose Internal Medicine Assoc PC (FHIR record)
[^23]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-bbed-3cb0f6aced99` — Melrose Internal Medicine Assoc PC (FHIR record)
[^24]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Observation/01573895-dbf5-29c6-a698-27d3c791a15d` — Melrose Internal Medicine Assoc PC (FHIR record)
[^25]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Procedure/01573895-dbf5-29c6-8120-f7c552c566ce` — Melrose Internal Medicine Assoc PC (FHIR record)
[^26]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Procedure/01573895-dbf5-29c6-f57e-947aa9a6c182` — Melrose Internal Medicine Assoc PC (FHIR record)
[^27]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Procedure/01573895-dbf5-29c6-cf88-7d5ebc43886c` — Melrose Internal Medicine Assoc PC (FHIR record)
[^28]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Procedure/01573895-dbf5-29c6-7d75-14f4a27c7513,Procedure/01573895-dbf5-29c6-f709-0d263d365d12` — Melrose Internal Medicine Assoc PC (FHIR record)
[^29]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Procedure/01573895-dbf5-29c6-85b7-549a95d0366e` — Melrose Internal Medicine Assoc PC (FHIR record)
[^30]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Procedure/01573895-dbf5-29c6-254e-b50804989f3b` — Melrose Internal Medicine Assoc PC (FHIR record)
[^31]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Procedure/01573895-dbf5-29c6-d848-364bbba48eff` — Melrose Internal Medicine Assoc PC (FHIR record)
[^32]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Procedure/01573895-dbf5-29c6-c5bd-412b700ceaab` — Melrose Internal Medicine Assoc PC (FHIR record)
[^33]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#DiagnosticReport/01573895-dbf5-29c6-1de7-1cb038b0bda8` — Melrose Internal Medicine Assoc PC (FHIR record)
[^34]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#DiagnosticReport/01573895-dbf5-29c6-f096-ec6db5824e1b` — Melrose Internal Medicine Assoc PC (FHIR record)
[^35]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#DiagnosticReport/01573895-dbf5-29c6-2a3a-9b264675285e` — Melrose Internal Medicine Assoc PC (FHIR record)
[^36]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#DiagnosticReport/01573895-dbf5-29c6-deb4-832923afc0c7` — Melrose Internal Medicine Assoc PC (FHIR record)
[^37]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#DiagnosticReport/01573895-dbf5-29c6-9c69-4067816b4857` — Melrose Internal Medicine Assoc PC (FHIR record)
[^38]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#DiagnosticReport/1cb59a2a-a0b8-66f1-7119-4f3ca62383f0` — Melrose Internal Medicine Assoc PC (FHIR record)
[^39]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Immunization/01573895-dbf5-29c6-d45c-68c65beb9b0e` — Melrose Internal Medicine Assoc PC (FHIR record)
[^40]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Immunization/01573895-dbf5-29c6-4250-655efa472e9c` — Melrose Internal Medicine Assoc PC (FHIR record)
[^41]: `fhir:01573895-dbf5-29c6-4ef9-cd09aecc51f6::01573895-dbf5-29c6-f885-ade2bd6537a5#Immunization/01573895-dbf5-29c6-95f1-f6846770a8a4` — Melrose Internal Medicine Assoc PC (FHIR record)
