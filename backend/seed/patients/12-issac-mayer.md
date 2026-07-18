---
name: Issac Mayer
dob: 1988-05-01
gender: male
city: "Wilmington, MA"
marital_status: Divorced
language: English (United States)
fhir_patient_id: be1b73f7-b0f0-0ca3-b24b-28369ce68943
record_id: "be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b"
dataset: synthetic-ambient-fhir-25
last_encounter: 2019-07-14
source: patient-context-model
slots: 38
ledger_entries: 39
synthetic: true
---

# Issac Mayer — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Issac Mayer, 31-year-old man (DOB 1988-05-01), Wilmington, MA. Tobacco: never smoked tobacco. Problem list: Body mass index 30+ - obesity. No current medications on record. Social context: Received higher education; Reports of violence in the environment; Medication review due.

Visit 2019-07-14 (ambulatory at Clarity Health & Wellness LLC): Annual physical — new adult patient wellness exam. Vitals: BP 103/67, HR 69, BMI 31.4. Recorded this visit: Medication review due (resolved); Full-time employment (resolved).

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2019-07-14 — Annual physical — new adult patient wellness exam (ambulatory · Clarity Health & Wellness LLC)[^1]

**Problems**
- **Body mass index 30+ - obesity:** On problem list (longitudinal record)[^2]
- **Full-time employment:** Resolved — recorded at 2019-07-14 encounter[^3]

**Social context**
- **Received higher education:** Reported in longitudinal record[^4]
- **Reports of violence in the environment:** Reported in longitudinal record[^5]
- **Medication review due:** Resolved — recorded at 2019-07-14 encounter[^6]
- **Tobacco smoking status:** Never smoked tobacco[^7]

**Vitals**
- **Height:** 164.3 cm[^8]
- **Pain severity (0–10):** 1[^9]
- **Weight:** 84.9 kg[^10]
- **BMI:** 31.4 kg/m²[^11]
- **Blood pressure:** 103/67 mmHg[^12]
- **Heart rate:** 69 /min[^13]
- **Respiratory rate:** 15 /min[^14]

**Labs**
- **Cholesterol [Mass/volume] in Serum or Plasma:** 110.2 mg/dL[^15]
- **Triglyceride [Mass/volume] in Serum or Plasma:** 117.1 mg/dL[^16]
- **Cholesterol in LDL [Mass/volume] in Serum or Plasma by Direct assay:** 35.8 mg/dL[^17]
- **Cholesterol in HDL [Mass/volume] in Serum or Plasma:** 51 mg/dL[^18]

**Assessments & screenings**
- **Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]:** What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 100740 /a; How many people are living or staying at this address [#] 4[^19]
- **Generalized anxiety disorder 7 item (GAD-7) total score [Reported.PHQ]:** 1[^20]
- **Total score [HARK]:** 0[^21]
- **Patient Health Questionnaire 2 item (PHQ-2) total score [Reported]:** 2[^22]
- **Total score [DAST-10]:** 2[^23]

**Procedures**
- **Medication reconciliation:** Performed this encounter (2019-07-14)[^24]
- **Assessment of health and social care needs:** Performed this encounter (2019-07-14)[^25]
- **Assessment of anxiety:** Performed this encounter (2019-07-14)[^26]
- **Screening for domestic abuse:** Performed this encounter (2019-07-14)[^27]
- **Depression screening:** Performed this encounter (2019-07-14) ×2[^28]
- **Assessment of substance use:** Performed this encounter (2019-07-14)[^29]
- **Screening for drug abuse:** Performed this encounter (2019-07-14)[^30]

**Reports**
- **Lipid panel with direct LDL - Serum or Plasma:** Filed this encounter (2019-07-14)[^31]
- **Generalized anxiety disorder 7 item (GAD-7):** Filed this encounter (2019-07-14)[^32]
- **Humiliation, Afraid, Rape, and Kick questionnaire [HARK]:** Filed this encounter (2019-07-14)[^33]
- **Patient Health Questionnaire 2 item (PHQ-2) [Reported]:** Filed this encounter (2019-07-14)[^34]
- **Drug Abuse Screening Test-10 [DAST-10]:** Filed this encounter (2019-07-14)[^35]
- **History and physical note:** Filed this encounter (2019-07-14)[^36]

**Immunizations**
- **Influenza, split virus, trivalent, PF:** Administered this encounter (2019-07-14)[^37]
- **Td (adult), 5 Lf tetanus toxoid, preservative free, adsorbed:** Administered this encounter (2019-07-14)[^38]

## Provenance

Rendered from the Patient Context Model (38 slots; 39 ledger entries — 39 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Encounter/be1b73f7-b0f0-0ca3-5c23-d051118e002b` — Clarity Health & Wellness LLC (FHIR record)
[^2]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Condition/be1b73f7-b0f0-0ca3-c0da-7972e932db09` — Clarity Health & Wellness LLC (FHIR record)
[^4]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#longitudinal` — EHR longitudinal record (FHIR record)
[^5]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#longitudinal` — EHR longitudinal record (FHIR record)
[^6]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Condition/be1b73f7-b0f0-0ca3-8db2-83983fd78014` — Clarity Health & Wellness LLC (FHIR record) · 2 ledger entries
[^7]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-38f3-c2930a20cc4a` — Clarity Health & Wellness LLC (FHIR record)
[^8]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-644d-018e39836f34` — Clarity Health & Wellness LLC (FHIR record)
[^9]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-c571-2750dee08592` — Clarity Health & Wellness LLC (FHIR record)
[^10]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-a252-416c9c45bbfe` — Clarity Health & Wellness LLC (FHIR record)
[^11]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-3092-84d78440e3fe` — Clarity Health & Wellness LLC (FHIR record)
[^12]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-1add-7a51e6b96d22` — Clarity Health & Wellness LLC (FHIR record)
[^13]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-35d9-ae9e17c831b1` — Clarity Health & Wellness LLC (FHIR record)
[^14]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-ba09-4f0bfa7e63ad` — Clarity Health & Wellness LLC (FHIR record)
[^15]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-dc86-ced91eb292df` — Clarity Health & Wellness LLC (FHIR record)
[^16]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-fb51-79a72c10cf80` — Clarity Health & Wellness LLC (FHIR record)
[^17]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-b396-99031a2e3606` — Clarity Health & Wellness LLC (FHIR record)
[^18]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-9add-3f9ad2a3bc6b` — Clarity Health & Wellness LLC (FHIR record)
[^19]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-afee-d3c77a674f15` — Clarity Health & Wellness LLC (FHIR record)
[^20]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-7f6e-86c5912d006d` — Clarity Health & Wellness LLC (FHIR record)
[^21]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-8d0b-0a1d0081944c` — Clarity Health & Wellness LLC (FHIR record)
[^22]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-178e-47f5258d368c` — Clarity Health & Wellness LLC (FHIR record)
[^23]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Observation/be1b73f7-b0f0-0ca3-c9bd-6f3d5a90be29` — Clarity Health & Wellness LLC (FHIR record)
[^24]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Procedure/be1b73f7-b0f0-0ca3-14c0-ba32e62e57b1` — Clarity Health & Wellness LLC (FHIR record)
[^25]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Procedure/be1b73f7-b0f0-0ca3-b068-be7a1e0516b9` — Clarity Health & Wellness LLC (FHIR record)
[^26]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Procedure/be1b73f7-b0f0-0ca3-0102-32d5090d87e0` — Clarity Health & Wellness LLC (FHIR record)
[^27]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Procedure/be1b73f7-b0f0-0ca3-8edf-937f8fe5d30d` — Clarity Health & Wellness LLC (FHIR record)
[^28]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Procedure/be1b73f7-b0f0-0ca3-0843-9a59da49969a,Procedure/be1b73f7-b0f0-0ca3-f56c-82ddf232660a` — Clarity Health & Wellness LLC (FHIR record)
[^29]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Procedure/be1b73f7-b0f0-0ca3-dac1-5b40539c4ad1` — Clarity Health & Wellness LLC (FHIR record)
[^30]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Procedure/be1b73f7-b0f0-0ca3-d5c6-a60aa1ac1de8` — Clarity Health & Wellness LLC (FHIR record)
[^31]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#DiagnosticReport/be1b73f7-b0f0-0ca3-a208-e4261ffd406e` — Clarity Health & Wellness LLC (FHIR record)
[^32]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#DiagnosticReport/be1b73f7-b0f0-0ca3-a6db-449718f978f9` — Clarity Health & Wellness LLC (FHIR record)
[^33]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#DiagnosticReport/be1b73f7-b0f0-0ca3-d7af-5316499628a3` — Clarity Health & Wellness LLC (FHIR record)
[^34]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#DiagnosticReport/be1b73f7-b0f0-0ca3-f986-81dadecc9f57` — Clarity Health & Wellness LLC (FHIR record)
[^35]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#DiagnosticReport/be1b73f7-b0f0-0ca3-9b2b-74afa72c8c6c` — Clarity Health & Wellness LLC (FHIR record)
[^36]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#DiagnosticReport/cfff98c3-c24d-64ef-1f0f-8c200431f0f8` — Clarity Health & Wellness LLC (FHIR record)
[^37]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Immunization/be1b73f7-b0f0-0ca3-5f7e-bc4e5b59ddde` — Clarity Health & Wellness LLC (FHIR record)
[^38]: `fhir:be1b73f7-b0f0-0ca3-b24b-28369ce68943::be1b73f7-b0f0-0ca3-5c23-d051118e002b#Immunization/be1b73f7-b0f0-0ca3-7a29-13cd41ad7f55` — Clarity Health & Wellness LLC (FHIR record)
