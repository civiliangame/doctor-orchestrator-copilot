---
name: Dick Larson
dob: 1987-05-23
gender: male
city: "Waltham, MA"
marital_status: Married
language: English (United States)
fhir_patient_id: 374e68b2-ee15-0852-cd48-3c7b6fd8e114
record_id: "374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00"
dataset: synthetic-ambient-fhir-25
last_encounter: 2024-05-18
source: patient-context-model
slots: 42
ledger_entries: 45
synthetic: true
---

# Dick Larson — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Dick Larson, 36-year-old man (DOB 1987-05-23), Waltham, MA. Tobacco: never smoked tobacco. Problem list: Prediabetes; Body mass index 30+ - obesity; Sepsis; Septic shock; Acute respiratory distress syndrome; Anemia. No current medications on record. Social context: Housing unsatisfactory; Received higher education; Medication review due; Unemployed; Social isolation.

Visit 2024-05-18 (ambulatory at Children's Hospital Corporation): Annual check-up — post-sepsis recovery and prediabetes. Vitals: BP 107/69, HR 63, BMI 30.3. Recorded this visit: Medication review due (resolved); Unemployed (active); Social isolation (resolved).

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2024-05-18 — Annual check-up — post-sepsis recovery and prediabetes (ambulatory · Children's Hospital Corporation)[^1]

**Problems**
- **Prediabetes:** On problem list (longitudinal record)[^2]
- **Body mass index 30+ - obesity:** On problem list (longitudinal record)[^3]
- **Sepsis:** On problem list (longitudinal record)[^4]
- **Septic shock:** On problem list (longitudinal record)[^5]
- **Acute respiratory distress syndrome:** On problem list (longitudinal record)[^6]
- **Anemia:** On problem list (longitudinal record)[^7]

**Social context**
- **Housing unsatisfactory:** Reported in longitudinal record[^8]
- **Received higher education:** Reported in longitudinal record[^9]
- **Medication review due:** Resolved — recorded at 2024-05-18 encounter[^10]
- **Unemployed:** Active — recorded at 2024-05-18 encounter[^11]
- **Social isolation:** Resolved — recorded at 2024-05-18 encounter[^12]
- **Tobacco smoking status:** Never smoked tobacco[^13]

**Vitals**
- **Height:** 166.8 cm[^14]
- **Pain severity (0–10):** 1[^15]
- **Weight:** 84.4 kg[^16]
- **BMI:** 30.3 kg/m²[^17]
- **Blood pressure:** 107/69 mmHg[^18]
- **Heart rate:** 63 /min[^19]
- **Respiratory rate:** 15 /min[^20]

**Labs**
- **Hemoglobin A1c/Hemoglobin.total in Blood:** 6 %[^21]
- **Glucose [Mass/volume] in Blood:** 86.7 mg/dL[^22]
- **Urea nitrogen [Mass/volume] in Blood:** 13.8 mg/dL[^23]
- **Creatinine [Mass/volume] in Blood:** 1.2 mg/dL[^24]
- **Calcium [Mass/volume] in Blood:** 10 mg/dL[^25]
- **Sodium [Moles/volume] in Blood:** 139.1 mmol/L[^26]
- **Potassium [Moles/volume] in Blood:** 4.9 mmol/L[^27]
- **Chloride [Moles/volume] in Blood:** 104 mmol/L[^28]
- **Carbon dioxide, total [Moles/volume] in Blood:** 28.1 mmol/L[^29]

**Assessments & screenings**
- **Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]:** What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 198810 /a; How many people are living or staying at this address [#] 6[^30]
- **Patient Health Questionnaire 2 item (PHQ-2) total score [Reported]:** 1[^31]
- **Total score [DAST-10]:** 0[^32]

**Procedures**
- **Medication reconciliation:** Performed this encounter (2024-05-18)[^33]
- **Assessment of health and social care needs:** Performed this encounter (2024-05-18)[^34]
- **Depression screening:** Performed this encounter (2024-05-18) ×2[^35]
- **Assessment of substance use:** Performed this encounter (2024-05-18)[^36]
- **Screening for drug abuse:** Performed this encounter (2024-05-18)[^37]

**Reports**
- **Basic metabolic panel - Blood:** Filed this encounter (2024-05-18)[^38]
- **Patient Health Questionnaire 2 item (PHQ-2) [Reported]:** Filed this encounter (2024-05-18)[^39]
- **Drug Abuse Screening Test-10 [DAST-10]:** Filed this encounter (2024-05-18)[^40]
- **History and physical note:** Filed this encounter (2024-05-18)[^41]

**Immunizations**
- **Influenza, split virus, trivalent, PF:** Administered this encounter (2024-05-18)[^42]

## Provenance

Rendered from the Patient Context Model (42 slots; 45 ledger entries — 45 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Encounter/374e68b2-ee15-0852-8f80-26e1007e6c00` — Children's Hospital Corporation (FHIR record)
[^2]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#longitudinal` — EHR longitudinal record (FHIR record)
[^4]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#longitudinal` — EHR longitudinal record (FHIR record)
[^5]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#longitudinal` — EHR longitudinal record (FHIR record)
[^6]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#longitudinal` — EHR longitudinal record (FHIR record)
[^7]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#longitudinal` — EHR longitudinal record (FHIR record)
[^8]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#longitudinal` — EHR longitudinal record (FHIR record)
[^9]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#longitudinal` — EHR longitudinal record (FHIR record)
[^10]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Condition/374e68b2-ee15-0852-808a-1bd9fcac6a19` — Children's Hospital Corporation (FHIR record) · 2 ledger entries
[^11]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Condition/374e68b2-ee15-0852-5ad0-b67dd25736e1` — Children's Hospital Corporation (FHIR record) · 2 ledger entries
[^12]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Condition/374e68b2-ee15-0852-9e2b-1d15d2435f0e` — Children's Hospital Corporation (FHIR record) · 2 ledger entries
[^13]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-9ff4-1cb862e9ee4f` — Children's Hospital Corporation (FHIR record)
[^14]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-b8b4-3901a5996c14` — Children's Hospital Corporation (FHIR record)
[^15]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-7c01-47e94477e73a` — Children's Hospital Corporation (FHIR record)
[^16]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-60cf-31eead602b22` — Children's Hospital Corporation (FHIR record)
[^17]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-9e1b-f9e6f165e7af` — Children's Hospital Corporation (FHIR record)
[^18]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-fd79-0cd9d92344f4` — Children's Hospital Corporation (FHIR record)
[^19]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-6ca9-eff9a125478c` — Children's Hospital Corporation (FHIR record)
[^20]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-e271-d1520c5dbf1e` — Children's Hospital Corporation (FHIR record)
[^21]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-6539-b8e8880208d2` — Children's Hospital Corporation (FHIR record)
[^22]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-87d6-160204ddf944` — Children's Hospital Corporation (FHIR record)
[^23]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-ab02-db304d38e810` — Children's Hospital Corporation (FHIR record)
[^24]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-e17d-51728c73311c` — Children's Hospital Corporation (FHIR record)
[^25]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-48e4-94d455593770` — Children's Hospital Corporation (FHIR record)
[^26]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-c05f-1a605d77d875` — Children's Hospital Corporation (FHIR record)
[^27]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-80b0-9f3933ff65b6` — Children's Hospital Corporation (FHIR record)
[^28]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-ec5b-c2a35879ba60` — Children's Hospital Corporation (FHIR record)
[^29]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-d41a-a3d1578be99e` — Children's Hospital Corporation (FHIR record)
[^30]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-d050-f2242c106e2a` — Children's Hospital Corporation (FHIR record)
[^31]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-216b-21dedd6d0e95` — Children's Hospital Corporation (FHIR record)
[^32]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Observation/374e68b2-ee15-0852-3938-3d3c8cfe7ce5` — Children's Hospital Corporation (FHIR record)
[^33]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Procedure/374e68b2-ee15-0852-eb0c-b1ba15dc4049` — Children's Hospital Corporation (FHIR record)
[^34]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Procedure/374e68b2-ee15-0852-64a8-c500a6a3a588` — Children's Hospital Corporation (FHIR record)
[^35]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Procedure/374e68b2-ee15-0852-3e06-2e88b94bb0a7,Procedure/374e68b2-ee15-0852-7b6f-08179cde8159` — Children's Hospital Corporation (FHIR record)
[^36]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Procedure/374e68b2-ee15-0852-64f7-9ff99dd1c0a0` — Children's Hospital Corporation (FHIR record)
[^37]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Procedure/374e68b2-ee15-0852-f2d0-d18e794cf070` — Children's Hospital Corporation (FHIR record)
[^38]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#DiagnosticReport/374e68b2-ee15-0852-c70d-bd825ed26b3f` — Children's Hospital Corporation (FHIR record)
[^39]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#DiagnosticReport/374e68b2-ee15-0852-87ec-4e96fff7664f` — Children's Hospital Corporation (FHIR record)
[^40]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#DiagnosticReport/374e68b2-ee15-0852-b6bd-bd0a2e302a16` — Children's Hospital Corporation (FHIR record)
[^41]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#DiagnosticReport/3077759c-3654-b127-0666-d12d99834b4b` — Children's Hospital Corporation (FHIR record)
[^42]: `fhir:374e68b2-ee15-0852-cd48-3c7b6fd8e114::374e68b2-ee15-0852-8f80-26e1007e6c00#Immunization/374e68b2-ee15-0852-45d5-676915a62aa6` — Children's Hospital Corporation (FHIR record)
