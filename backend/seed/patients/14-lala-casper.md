---
name: Lala Casper
dob: 1972-05-24
gender: female
city: "Springfield, MA"
marital_status: Married
language: English (United States)
fhir_patient_id: 256bea3d-7833-e7f8-74b4-0e4f7e299c73
record_id: "256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07"
dataset: synthetic-ambient-fhir-25
last_encounter: 2020-06-17
source: patient-context-model
slots: 41
ledger_entries: 44
synthetic: true
---

# Lala Casper — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Lala Casper, 48-year-old woman (DOB 1972-05-24), Springfield, MA. Tobacco: never smoked tobacco. Problem list: Recurrent urinary tract infection; Body mass index 30+ - obesity. History: Past pregnancy history of miscarriage; History of tubal ligation. Current medications on record: Hydrocortisone 10 MG/ML Topical Cream; Loratadine 10 MG Oral Tablet; NDA020800 0.3 ML Epinephrine 1 MG/ML Auto-Injector. Social context: Risk activity involvement; Received higher education; Has a criminal record; Medication review due; Stress; Victim of intimate partner abuse.

Visit 2020-06-17 (ambulatory at Caring Health Center, Inc): Annual exam — psychosocial screening with safety disclosure. Vitals: BP 108/77, HR 67, BMI 30.6. Recorded this visit: Medication review due (resolved); Full-time employment (resolved); Stress (resolved); Victim of intimate partner abuse (active).

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2020-06-17 — Annual exam — psychosocial screening with safety disclosure (ambulatory · Caring Health Center, Inc)[^1]

**Problems**
- **Recurrent urinary tract infection:** On problem list (longitudinal record)[^2]
- **Body mass index 30+ - obesity:** On problem list (longitudinal record)[^3]
- **Full-time employment:** Resolved — recorded at 2020-06-17 encounter[^4]

**Medical / surgical history**
- **Past pregnancy history of miscarriage:** On record (longitudinal)[^5]
- **History of tubal ligation:** On record (longitudinal)[^6]

**Medications**
- **Hydrocortisone 10 MG/ML Topical Cream:** On medication list (longitudinal record)[^7]
- **Loratadine 10 MG Oral Tablet:** On medication list (longitudinal record)[^8]
- **NDA020800 0.3 ML Epinephrine 1 MG/ML Auto-Injector:** On medication list (longitudinal record)[^9]

**Social context**
- **Risk activity involvement:** Reported in longitudinal record[^10]
- **Received higher education:** Reported in longitudinal record[^11]
- **Has a criminal record:** Reported in longitudinal record[^12]
- **Medication review due:** Resolved — recorded at 2020-06-17 encounter[^13]
- **Stress:** Resolved — recorded at 2020-06-17 encounter[^14]
- **Victim of intimate partner abuse:** Active — recorded at 2020-06-17 encounter[^15]
- **Tobacco smoking status:** Never smoked tobacco[^16]

**Vitals**
- **Height:** 172.9 cm[^17]
- **Pain severity (0–10):** 1[^18]
- **Weight:** 91.4 kg[^19]
- **BMI:** 30.6 kg/m²[^20]
- **Blood pressure:** 108/77 mmHg[^21]
- **Heart rate:** 67 /min[^22]
- **Respiratory rate:** 16 /min[^23]

**Assessments & screenings**
- **Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]:** What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 10131 /a; How many people are living or staying at this address [#] 8[^24]
- **Generalized anxiety disorder 7 item (GAD-7) total score [Reported.PHQ]:** 7[^25]
- **Total score [HARK]:** 2[^26]
- **Patient Health Questionnaire 2 item (PHQ-2) total score [Reported]:** 0[^27]
- **Total score [DAST-10]:** 2[^28]

**Procedures**
- **Assessment of health and social care needs:** Performed this encounter (2020-06-17)[^29]
- **Assessment of anxiety:** Performed this encounter (2020-06-17)[^30]
- **Screening for domestic abuse:** Performed this encounter (2020-06-17)[^31]
- **Depression screening:** Performed this encounter (2020-06-17) ×2[^32]
- **Assessment of substance use:** Performed this encounter (2020-06-17)[^33]
- **Screening for drug abuse:** Performed this encounter (2020-06-17)[^34]
- **Patient referral for dental care:** Performed this encounter (2020-06-17)[^35]

**Reports**
- **Generalized anxiety disorder 7 item (GAD-7):** Filed this encounter (2020-06-17)[^36]
- **Humiliation, Afraid, Rape, and Kick questionnaire [HARK]:** Filed this encounter (2020-06-17)[^37]
- **Patient Health Questionnaire 2 item (PHQ-2) [Reported]:** Filed this encounter (2020-06-17)[^38]
- **Drug Abuse Screening Test-10 [DAST-10]:** Filed this encounter (2020-06-17)[^39]
- **History and physical note:** Filed this encounter (2020-06-17)[^40]

**Immunizations**
- **Influenza, split virus, trivalent, PF:** Administered this encounter (2020-06-17)[^41]

## Provenance

Rendered from the Patient Context Model (41 slots; 44 ledger entries — 44 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Encounter/256bea3d-7833-e7f8-1c5a-743d9ec18b07` — Caring Health Center, Inc (FHIR record)
[^2]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#longitudinal` — EHR longitudinal record (FHIR record)
[^4]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Condition/256bea3d-7833-e7f8-72c2-2d7279fa69c2` — Caring Health Center, Inc (FHIR record)
[^5]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#longitudinal` — EHR longitudinal record (FHIR record)
[^6]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#longitudinal` — EHR longitudinal record (FHIR record)
[^7]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#longitudinal` — EHR longitudinal record (FHIR record)
[^8]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#longitudinal` — EHR longitudinal record (FHIR record)
[^9]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#longitudinal` — EHR longitudinal record (FHIR record)
[^10]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#longitudinal` — EHR longitudinal record (FHIR record)
[^11]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#longitudinal` — EHR longitudinal record (FHIR record)
[^12]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#longitudinal` — EHR longitudinal record (FHIR record)
[^13]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Condition/256bea3d-7833-e7f8-bac4-bcdcd320c95e` — Caring Health Center, Inc (FHIR record) · 2 ledger entries
[^14]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Condition/256bea3d-7833-e7f8-42bd-c54476332284` — Caring Health Center, Inc (FHIR record) · 2 ledger entries
[^15]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Condition/256bea3d-7833-e7f8-2087-c8e78f364a53` — Caring Health Center, Inc (FHIR record) · 2 ledger entries
[^16]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Observation/256bea3d-7833-e7f8-a366-28ea57208d1d` — Caring Health Center, Inc (FHIR record)
[^17]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Observation/256bea3d-7833-e7f8-7b71-88a49743de47` — Caring Health Center, Inc (FHIR record)
[^18]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Observation/256bea3d-7833-e7f8-90e2-87b55e76d1e8` — Caring Health Center, Inc (FHIR record)
[^19]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Observation/256bea3d-7833-e7f8-480d-172539e0b492` — Caring Health Center, Inc (FHIR record)
[^20]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Observation/256bea3d-7833-e7f8-f53b-07dd8d540c98` — Caring Health Center, Inc (FHIR record)
[^21]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Observation/256bea3d-7833-e7f8-4811-ac7a0e5c92c5` — Caring Health Center, Inc (FHIR record)
[^22]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Observation/256bea3d-7833-e7f8-7a47-cc71bd894bf8` — Caring Health Center, Inc (FHIR record)
[^23]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Observation/256bea3d-7833-e7f8-9f4c-7f352aa94654` — Caring Health Center, Inc (FHIR record)
[^24]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Observation/256bea3d-7833-e7f8-ec6d-684664f3d248` — Caring Health Center, Inc (FHIR record)
[^25]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Observation/256bea3d-7833-e7f8-8100-fb0892c15e09` — Caring Health Center, Inc (FHIR record)
[^26]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Observation/256bea3d-7833-e7f8-6a3d-b4aa81af3282` — Caring Health Center, Inc (FHIR record)
[^27]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Observation/256bea3d-7833-e7f8-a0a8-4f45d50281ab` — Caring Health Center, Inc (FHIR record)
[^28]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Observation/256bea3d-7833-e7f8-1a64-d02aa4df6117` — Caring Health Center, Inc (FHIR record)
[^29]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Procedure/256bea3d-7833-e7f8-4fc7-a2102a478891` — Caring Health Center, Inc (FHIR record)
[^30]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Procedure/256bea3d-7833-e7f8-fb05-95828ba58144` — Caring Health Center, Inc (FHIR record)
[^31]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Procedure/256bea3d-7833-e7f8-70d0-72f5e7142911` — Caring Health Center, Inc (FHIR record)
[^32]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Procedure/256bea3d-7833-e7f8-f67b-4a38d04e105c,Procedure/256bea3d-7833-e7f8-44c4-fbba5fcf5d2c` — Caring Health Center, Inc (FHIR record)
[^33]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Procedure/256bea3d-7833-e7f8-e32f-dcef35b94a1e` — Caring Health Center, Inc (FHIR record)
[^34]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Procedure/256bea3d-7833-e7f8-5123-e2f9da1b65e7` — Caring Health Center, Inc (FHIR record)
[^35]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Procedure/256bea3d-7833-e7f8-9230-a8c9ef600272` — Caring Health Center, Inc (FHIR record)
[^36]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#DiagnosticReport/256bea3d-7833-e7f8-793b-fdea5e3f8020` — Caring Health Center, Inc (FHIR record)
[^37]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#DiagnosticReport/256bea3d-7833-e7f8-36dc-2e5da6c1d338` — Caring Health Center, Inc (FHIR record)
[^38]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#DiagnosticReport/256bea3d-7833-e7f8-1775-18782518ce80` — Caring Health Center, Inc (FHIR record)
[^39]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#DiagnosticReport/256bea3d-7833-e7f8-8d74-52f19c082a34` — Caring Health Center, Inc (FHIR record)
[^40]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#DiagnosticReport/3d655fce-93a3-edaf-ae07-52d4959a92b4` — Caring Health Center, Inc (FHIR record)
[^41]: `fhir:256bea3d-7833-e7f8-74b4-0e4f7e299c73::256bea3d-7833-e7f8-1c5a-743d9ec18b07#Immunization/256bea3d-7833-e7f8-bfff-8bfa537b0f4e` — Caring Health Center, Inc (FHIR record)
