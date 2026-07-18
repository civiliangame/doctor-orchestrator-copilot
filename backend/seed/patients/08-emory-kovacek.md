---
name: Emory Kovacek
dob: 1999-01-19
gender: male
city: "Westborough, MA"
marital_status: Never Married
language: English (United States)
fhir_patient_id: 1ba8eeb9-bc93-7129-4390-0d2ddd560616
record_id: "1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964"
dataset: synthetic-ambient-fhir-25
last_encounter: 2021-04-06
source: patient-context-model
slots: 36
ledger_entries: 38
synthetic: true
---

# Emory Kovacek — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Emory Kovacek, 22-year-old man (DOB 1999-01-19), Westborough, MA. Tobacco: never smoked tobacco. Problem list: Chronic pain; Chronic low back pain; Gingivitis. History: History of appendectomy. Current medications on record: Ibuprofen 400 MG Oral Tablet [Ibu]. Social context: Received higher education; Stress.

Visit 2021-04-06 (ambulatory at Sunrise Healthcare LLC): General exam — chronic low back pain and positive depression screen. Vitals: BP 136/94, HR 89, BMI 22.5. Recorded this visit: Full-time employment (resolved); Stress (resolved); Gingivitis (resolved).

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2021-04-06 — General exam — chronic low back pain and positive depression screen (ambulatory · Sunrise Healthcare LLC)[^1]

**Problems**
- **Chronic pain:** On problem list (longitudinal record)[^2]
- **Chronic low back pain:** On problem list (longitudinal record)[^3]
- **Gingivitis:** Resolved — recorded at 2021-04-06 encounter[^4]
- **Full-time employment:** Resolved — recorded at 2021-04-06 encounter[^5]

**Medical / surgical history**
- **History of appendectomy:** On record (longitudinal)[^6]

**Medications**
- **Ibuprofen 400 MG Oral Tablet [Ibu]:** On medication list (longitudinal record)[^7]
- **Ibuprofen 400 MG Oral Tablet [Ibu] (completed):** Ordered this encounter (2021-04-06)[^8]

**Social context**
- **Received higher education:** Reported in longitudinal record[^9]
- **Stress:** Resolved — recorded at 2021-04-06 encounter[^10]
- **Tobacco smoking status:** Never smoked tobacco[^11]

**Vitals**
- **Height:** 185.2 cm[^12]
- **Pain severity (0–10):** 4[^13]
- **Weight:** 77 kg[^14]
- **BMI:** 22.5 kg/m²[^15]
- **Blood pressure:** 136/94 mmHg[^16]
- **Heart rate:** 89 /min[^17]
- **Respiratory rate:** 15 /min[^18]

**Assessments & screenings**
- **Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]:** What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 91796 /a; How many people are living or staying at this address [#] 3[^19]
- **Total score [HARK]:** 0[^20]
- **Patient Health Questionnaire 2 item (PHQ-2) total score [Reported]:** 5[^21]
- **Patient Health Questionnaire 9 item (PHQ-9) total score [Reported]:** 17[^22]
- **Total score [DAST-10]:** 1[^23]

**Procedures**
- **Medication reconciliation:** Performed this encounter (2021-04-06)[^24]
- **Assessment of health and social care needs:** Performed this encounter (2021-04-06)[^25]
- **Screening for domestic abuse:** Performed this encounter (2021-04-06)[^26]
- **Depression screening:** Performed this encounter (2021-04-06) ×2[^27]
- **Depression screening using Patient Health Questionnaire Nine Item score:** Performed this encounter (2021-04-06)[^28]
- **Assessment of substance use:** Performed this encounter (2021-04-06)[^29]
- **Screening for drug abuse:** Performed this encounter (2021-04-06)[^30]
- **Patient referral for dental care:** Performed this encounter (2021-04-06)[^31]

**Reports**
- **Humiliation, Afraid, Rape, and Kick questionnaire [HARK]:** Filed this encounter (2021-04-06)[^32]
- **Patient Health Questionnaire 2 item (PHQ-2) [Reported]:** Filed this encounter (2021-04-06)[^33]
- **PHQ-9 quick depression assessment panel [Reported.PHQ]:** Filed this encounter (2021-04-06)[^34]
- **Drug Abuse Screening Test-10 [DAST-10]:** Filed this encounter (2021-04-06)[^35]
- **History and physical note:** Filed this encounter (2021-04-06)[^36]

## Provenance

Rendered from the Patient Context Model (36 slots; 38 ledger entries — 38 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Encounter/1ba8eeb9-bc93-7129-2e7d-8c427e72b964` — Sunrise Healthcare LLC (FHIR record)
[^2]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#longitudinal` — EHR longitudinal record (FHIR record)
[^4]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Condition/1ba8eeb9-bc93-7129-e7f7-69583b7b0da5` — Sunrise Healthcare LLC (FHIR record) · 2 ledger entries
[^5]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Condition/1ba8eeb9-bc93-7129-6ecd-9d966de64a51` — Sunrise Healthcare LLC (FHIR record)
[^6]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#longitudinal` — EHR longitudinal record (FHIR record)
[^7]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#longitudinal` — EHR longitudinal record (FHIR record)
[^8]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#MedicationRequest/1ba8eeb9-bc93-7129-7358-8f8e398e28cf` — Sunrise Healthcare LLC (FHIR record)
[^9]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#longitudinal` — EHR longitudinal record (FHIR record)
[^10]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Condition/1ba8eeb9-bc93-7129-70d3-15e2e4c35a22` — Sunrise Healthcare LLC (FHIR record) · 2 ledger entries
[^11]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Observation/1ba8eeb9-bc93-7129-5d07-3db1be12f111` — Sunrise Healthcare LLC (FHIR record)
[^12]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Observation/1ba8eeb9-bc93-7129-0565-3add998485a2` — Sunrise Healthcare LLC (FHIR record)
[^13]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Observation/1ba8eeb9-bc93-7129-8ea1-f7338c8b8bd4` — Sunrise Healthcare LLC (FHIR record)
[^14]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Observation/1ba8eeb9-bc93-7129-6a20-86920a19d5a6` — Sunrise Healthcare LLC (FHIR record)
[^15]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Observation/1ba8eeb9-bc93-7129-b869-8e917aa37743` — Sunrise Healthcare LLC (FHIR record)
[^16]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Observation/1ba8eeb9-bc93-7129-7f62-cbb8a20da3d9` — Sunrise Healthcare LLC (FHIR record)
[^17]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Observation/1ba8eeb9-bc93-7129-ec07-100190076a1d` — Sunrise Healthcare LLC (FHIR record)
[^18]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Observation/1ba8eeb9-bc93-7129-8228-724e4fb72e01` — Sunrise Healthcare LLC (FHIR record)
[^19]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Observation/1ba8eeb9-bc93-7129-0f48-dc67d1ebf35c` — Sunrise Healthcare LLC (FHIR record)
[^20]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Observation/1ba8eeb9-bc93-7129-27e6-8d0a347d17e7` — Sunrise Healthcare LLC (FHIR record)
[^21]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Observation/1ba8eeb9-bc93-7129-12ac-8b6a91946ac1` — Sunrise Healthcare LLC (FHIR record)
[^22]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Observation/1ba8eeb9-bc93-7129-462c-51953054a943` — Sunrise Healthcare LLC (FHIR record)
[^23]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Observation/1ba8eeb9-bc93-7129-7bf2-bf5e414deabc` — Sunrise Healthcare LLC (FHIR record)
[^24]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Procedure/1ba8eeb9-bc93-7129-d4f5-dffc1e703df7` — Sunrise Healthcare LLC (FHIR record)
[^25]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Procedure/1ba8eeb9-bc93-7129-e529-fda6c90da100` — Sunrise Healthcare LLC (FHIR record)
[^26]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Procedure/1ba8eeb9-bc93-7129-7636-8bd4a3399e1e` — Sunrise Healthcare LLC (FHIR record)
[^27]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Procedure/1ba8eeb9-bc93-7129-0c06-271b3901ebe7,Procedure/1ba8eeb9-bc93-7129-7b7a-f621d99f1f71` — Sunrise Healthcare LLC (FHIR record)
[^28]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Procedure/1ba8eeb9-bc93-7129-e1cc-f3820f55f5cf` — Sunrise Healthcare LLC (FHIR record)
[^29]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Procedure/1ba8eeb9-bc93-7129-3d8f-1643774bf9e0` — Sunrise Healthcare LLC (FHIR record)
[^30]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Procedure/1ba8eeb9-bc93-7129-be90-4d62117d5b38` — Sunrise Healthcare LLC (FHIR record)
[^31]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#Procedure/1ba8eeb9-bc93-7129-4b40-0467b5f64b54` — Sunrise Healthcare LLC (FHIR record)
[^32]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#DiagnosticReport/1ba8eeb9-bc93-7129-4ec0-8337dada20ae` — Sunrise Healthcare LLC (FHIR record)
[^33]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#DiagnosticReport/1ba8eeb9-bc93-7129-86fc-0a56459b74fa` — Sunrise Healthcare LLC (FHIR record)
[^34]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#DiagnosticReport/1ba8eeb9-bc93-7129-443f-9febc0839d25` — Sunrise Healthcare LLC (FHIR record)
[^35]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#DiagnosticReport/1ba8eeb9-bc93-7129-b1f4-8515e3430252` — Sunrise Healthcare LLC (FHIR record)
[^36]: `fhir:1ba8eeb9-bc93-7129-4390-0d2ddd560616::1ba8eeb9-bc93-7129-2e7d-8c427e72b964#DiagnosticReport/04c1d030-b37c-c19d-7150-a7150a8e07e0` — Sunrise Healthcare LLC (FHIR record)
