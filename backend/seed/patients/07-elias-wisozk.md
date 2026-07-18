---
name: Elias Wisozk
dob: 1972-05-25
gender: male
city: "Lawrence, MA"
marital_status: Never Married
language: English (United States)
fhir_patient_id: 4b4735a2-ee12-ec86-041f-3ba4d5c81ec9
record_id: "4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab"
dataset: synthetic-ambient-fhir-25
last_encounter: 2026-06-18
source: patient-context-model
slots: 49
ledger_entries: 55
synthetic: true
---

# Elias Wisozk — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Elias Wisozk, 54-year-old man (DOB 1972-05-25), Lawrence, MA. Tobacco: never smoked tobacco. Problem list: Prediabetes; Anemia; Body mass index 30+ - obesity; Essential hypertension; Metabolic syndrome X; Gingivitis. Current medications on record: Vitamin B12 5 MG/ML Injectable Solution; Hydrochlorothiazide 25 MG Oral Tablet. Social context: Received higher education; Social isolation; Stress; Medication review due; Not in labor force.

Visit 2026-06-18 (ambulatory at Greater Lawrence Family Health Center Inc): General adult exam — new hypertension and metabolic syndrome. Vitals: BP 141/100, HR 100, BMI 30.2. Recorded this visit: Essential hypertension (active); Medication review due (resolved); Metabolic syndrome X (active); Not in labor force (active); Gingivitis (resolved).

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2026-06-18 — General adult exam — new hypertension and metabolic syndrome (ambulatory · Greater Lawrence Family Health Center Inc)[^1]

**Problems**
- **Prediabetes:** On problem list (longitudinal record)[^2]
- **Anemia:** On problem list (longitudinal record)[^3]
- **Body mass index 30+ - obesity:** On problem list (longitudinal record)[^4]
- **Essential hypertension:** Active — recorded at 2026-06-18 encounter[^5]
- **Metabolic syndrome X:** Active — recorded at 2026-06-18 encounter[^6]
- **Gingivitis:** Resolved — recorded at 2026-06-18 encounter[^7]

**Medications**
- **Vitamin B12 5 MG/ML Injectable Solution:** On medication list (longitudinal record)[^8]
- **Hydrochlorothiazide 25 MG Oral Tablet:** Ordered this encounter (2026-06-18)[^9]
- **Hydrochlorothiazide 25 MG Oral Tablet (completed):** Ordered this encounter (2026-06-18)[^10]

**Social context**
- **Received higher education:** Reported in longitudinal record[^11]
- **Social isolation:** Reported in longitudinal record[^12]
- **Stress:** Reported in longitudinal record[^13]
- **Medication review due:** Resolved — recorded at 2026-06-18 encounter[^14]
- **Not in labor force:** Active — recorded at 2026-06-18 encounter[^15]
- **Tobacco smoking status:** Never smoked tobacco[^16]

**Vitals**
- **Height:** 176.3 cm[^17]
- **Pain severity (0–10):** 1[^18]
- **Weight:** 93.9 kg[^19]
- **BMI:** 30.2 kg/m²[^20]
- **Blood pressure:** 141/100 mmHg[^21]
- **Heart rate:** 100 /min[^22]
- **Respiratory rate:** 13 /min[^23]

**Labs**
- **Hemoglobin A1c/Hemoglobin.total in Blood:** 6.3 %[^24]
- **Glucose [Mass/volume] in Blood:** 91.1 mg/dL[^25]
- **Urea nitrogen [Mass/volume] in Blood:** 17.4 mg/dL[^26]
- **Creatinine [Mass/volume] in Blood:** 1.1 mg/dL[^27]
- **Calcium [Mass/volume] in Blood:** 9.7 mg/dL[^28]
- **Sodium [Moles/volume] in Blood:** 139.1 mmol/L[^29]
- **Potassium [Moles/volume] in Blood:** 4 mmol/L[^30]
- **Chloride [Moles/volume] in Blood:** 106.1 mmol/L[^31]
- **Carbon dioxide, total [Moles/volume] in Blood:** 22.8 mmol/L[^32]

**Assessments & screenings**
- **Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]:** What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 4829 /a; How many people are living or staying at this address [#] 5[^33]
- **Generalized anxiety disorder 7 item (GAD-7) total score [Reported.PHQ]:** 3[^34]
- **Patient Health Questionnaire 2 item (PHQ-2) total score [Reported]:** 2[^35]
- **Total score [AUDIT-C]:** 3[^36]

**Procedures**
- **Medication reconciliation:** Performed this encounter (2026-06-18)[^37]
- **Assessment of health and social care needs:** Performed this encounter (2026-06-18)[^38]
- **Assessment of anxiety:** Performed this encounter (2026-06-18)[^39]
- **Depression screening:** Performed this encounter (2026-06-18) ×2[^40]
- **Assessment of substance use:** Performed this encounter (2026-06-18)[^41]
- **Assessment using Alcohol Use Disorders Identification Test - Consumption:** Performed this encounter (2026-06-18)[^42]
- **Patient referral for dental care:** Performed this encounter (2026-06-18)[^43]

**Reports**
- **Basic metabolic panel - Blood:** Filed this encounter (2026-06-18)[^44]
- **Generalized anxiety disorder 7 item (GAD-7):** Filed this encounter (2026-06-18)[^45]
- **Patient Health Questionnaire 2 item (PHQ-2) [Reported]:** Filed this encounter (2026-06-18)[^46]
- **Alcohol Use Disorder Identification Test - Consumption [AUDIT-C]:** Filed this encounter (2026-06-18)[^47]
- **History and physical note:** Filed this encounter (2026-06-18)[^48]

**Immunizations**
- **Influenza, split virus, trivalent, PF:** Administered this encounter (2026-06-18)[^49]

## Provenance

Rendered from the Patient Context Model (49 slots; 55 ledger entries — 55 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Encounter/4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab` — Greater Lawrence Family Health Center Inc (FHIR record)
[^2]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#longitudinal` — EHR longitudinal record (FHIR record)
[^4]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#longitudinal` — EHR longitudinal record (FHIR record)
[^5]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Condition/4b4735a2-ee12-ec86-43f9-72c6a9c11cad` — Greater Lawrence Family Health Center Inc (FHIR record) · 2 ledger entries
[^6]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Condition/4b4735a2-ee12-ec86-b2be-3ebe10489c19` — Greater Lawrence Family Health Center Inc (FHIR record) · 2 ledger entries
[^7]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Condition/4b4735a2-ee12-ec86-e4d2-99abda3ceb16` — Greater Lawrence Family Health Center Inc (FHIR record) · 2 ledger entries
[^8]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#longitudinal` — EHR longitudinal record (FHIR record)
[^9]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#MedicationRequest/4b4735a2-ee12-ec86-2f73-08977934c44b` — Greater Lawrence Family Health Center Inc (FHIR record) · 2 ledger entries
[^10]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#MedicationRequest/4b4735a2-ee12-ec86-d642-408f094ead4a` — Greater Lawrence Family Health Center Inc (FHIR record)
[^11]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#longitudinal` — EHR longitudinal record (FHIR record)
[^12]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#longitudinal` — EHR longitudinal record (FHIR record)
[^13]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#longitudinal` — EHR longitudinal record (FHIR record)
[^14]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Condition/4b4735a2-ee12-ec86-8210-4beec40926b3` — Greater Lawrence Family Health Center Inc (FHIR record) · 2 ledger entries
[^15]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Condition/4b4735a2-ee12-ec86-edcf-56b458bd42f5` — Greater Lawrence Family Health Center Inc (FHIR record) · 2 ledger entries
[^16]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-25e0-44e3c723e60f` — Greater Lawrence Family Health Center Inc (FHIR record)
[^17]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-cb9d-ba4dd411d328` — Greater Lawrence Family Health Center Inc (FHIR record)
[^18]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-4c13-ce1dbcf80615` — Greater Lawrence Family Health Center Inc (FHIR record)
[^19]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-7eab-bd73807bb3df` — Greater Lawrence Family Health Center Inc (FHIR record)
[^20]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-54b5-79ea10828c86` — Greater Lawrence Family Health Center Inc (FHIR record)
[^21]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-1daf-98eae3ddff3d` — Greater Lawrence Family Health Center Inc (FHIR record)
[^22]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-f9a7-3ac77536ff4a` — Greater Lawrence Family Health Center Inc (FHIR record)
[^23]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-c09f-0d0cf7893ef4` — Greater Lawrence Family Health Center Inc (FHIR record)
[^24]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-ec1c-954838b6643a` — Greater Lawrence Family Health Center Inc (FHIR record)
[^25]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-f359-d2e8f750458c` — Greater Lawrence Family Health Center Inc (FHIR record)
[^26]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-a6ab-a313f846d2ce` — Greater Lawrence Family Health Center Inc (FHIR record)
[^27]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-6585-51b4adc44abb` — Greater Lawrence Family Health Center Inc (FHIR record)
[^28]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-86b1-c4e0bd8a71c6` — Greater Lawrence Family Health Center Inc (FHIR record)
[^29]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-fe3e-3469bc508826` — Greater Lawrence Family Health Center Inc (FHIR record)
[^30]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-e6b6-148f2f2eb3c3` — Greater Lawrence Family Health Center Inc (FHIR record)
[^31]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-433d-87922efbca8d` — Greater Lawrence Family Health Center Inc (FHIR record)
[^32]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-eb95-984619b8983c` — Greater Lawrence Family Health Center Inc (FHIR record)
[^33]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-1ef6-1e2cd1adea0a` — Greater Lawrence Family Health Center Inc (FHIR record)
[^34]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-030c-9beffd1e1b22` — Greater Lawrence Family Health Center Inc (FHIR record)
[^35]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-2e9f-19c850b08b93` — Greater Lawrence Family Health Center Inc (FHIR record)
[^36]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Observation/4b4735a2-ee12-ec86-e6bb-c6408c3f5cfc` — Greater Lawrence Family Health Center Inc (FHIR record)
[^37]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Procedure/4b4735a2-ee12-ec86-cb89-cacd2d81ec75` — Greater Lawrence Family Health Center Inc (FHIR record)
[^38]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Procedure/4b4735a2-ee12-ec86-7e88-f05e26e4eaa9` — Greater Lawrence Family Health Center Inc (FHIR record)
[^39]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Procedure/4b4735a2-ee12-ec86-309c-7073a4a81c85` — Greater Lawrence Family Health Center Inc (FHIR record)
[^40]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Procedure/4b4735a2-ee12-ec86-fd7f-88dd1094ad14,Procedure/4b4735a2-ee12-ec86-e2da-079f25bcd0bb` — Greater Lawrence Family Health Center Inc (FHIR record)
[^41]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Procedure/4b4735a2-ee12-ec86-e99b-5df5fa80442f` — Greater Lawrence Family Health Center Inc (FHIR record)
[^42]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Procedure/4b4735a2-ee12-ec86-0c58-c7be52a55192` — Greater Lawrence Family Health Center Inc (FHIR record)
[^43]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Procedure/4b4735a2-ee12-ec86-33e0-eeab2e10d03a` — Greater Lawrence Family Health Center Inc (FHIR record)
[^44]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#DiagnosticReport/4b4735a2-ee12-ec86-df3d-f00e7b3505c6` — Greater Lawrence Family Health Center Inc (FHIR record)
[^45]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#DiagnosticReport/4b4735a2-ee12-ec86-b03f-5809f085b605` — Greater Lawrence Family Health Center Inc (FHIR record)
[^46]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#DiagnosticReport/4b4735a2-ee12-ec86-273b-f2d25936b329` — Greater Lawrence Family Health Center Inc (FHIR record)
[^47]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#DiagnosticReport/4b4735a2-ee12-ec86-63b7-adc3166cbf16` — Greater Lawrence Family Health Center Inc (FHIR record)
[^48]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#DiagnosticReport/b5c0f962-a71a-88f5-7c13-e1f20fb65e9b` — Greater Lawrence Family Health Center Inc (FHIR record)
[^49]: `fhir:4b4735a2-ee12-ec86-041f-3ba4d5c81ec9::4b4735a2-ee12-ec86-c1c9-c610cc6ef8ab#Immunization/4b4735a2-ee12-ec86-27e3-8e468a734fbd` — Greater Lawrence Family Health Center Inc (FHIR record)
