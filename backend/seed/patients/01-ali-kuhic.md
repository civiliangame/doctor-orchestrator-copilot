---
name: Ali Kuhic
dob: 1991-05-24
gender: male
city: "Chelsea, MA"
marital_status: Never Married
language: English (United States)
fhir_patient_id: 3a3a1f26-ed23-f65c-a7df-c96fac56f464
record_id: "3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea"
dataset: synthetic-ambient-fhir-25
last_encounter: 2022-08-05
source: patient-context-model
slots: 37
ledger_entries: 39
synthetic: true
---

# Ali Kuhic — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Ali Kuhic, 31-year-old man (DOB 1991-05-24), Chelsea, MA. Tobacco: never smoked tobacco. Problem list: Chronic intractable migraine without aura; Gingivitis. No current medications on record. Social context: Risk activity involvement; Received higher education; Transport problem; Lack of access to transportation; Stress; Social isolation.

Visit 2022-08-05 (ambulatory at Whitley Wellness LLC): Annual physical — preventive screening and migraine check-in. Vitals: BP 98/83, HR 93, BMI 25.3. Recorded this visit: Full-time employment (resolved); Social isolation (active); Gingivitis (resolved).

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2022-08-05 — Annual physical — preventive screening and migraine check-in (ambulatory · Whitley Wellness LLC)[^1]

**Problems**
- **Chronic intractable migraine without aura:** On problem list (longitudinal record)[^2]
- **Gingivitis:** Resolved — recorded at 2022-08-05 encounter[^3]
- **Full-time employment:** Resolved — recorded at 2022-08-05 encounter[^4]

**Social context**
- **Risk activity involvement:** Reported in longitudinal record[^5]
- **Received higher education:** Reported in longitudinal record[^6]
- **Transport problem:** Reported in longitudinal record[^7]
- **Lack of access to transportation:** Reported in longitudinal record[^8]
- **Stress:** Reported in longitudinal record[^9]
- **Social isolation:** Active — recorded at 2022-08-05 encounter[^10]
- **Tobacco smoking status:** Never smoked tobacco[^11]

**Vitals**
- **Height:** 176.3 cm[^12]
- **Pain severity (0–10):** 2[^13]
- **Weight:** 78.7 kg[^14]
- **BMI:** 25.3 kg/m²[^15]
- **Blood pressure:** 98/83 mmHg[^16]
- **Heart rate:** 93 /min[^17]
- **Respiratory rate:** 14 /min[^18]

**Labs**
- **Cholesterol [Mass/volume] in Serum or Plasma:** 198.2 mg/dL[^19]
- **Triglyceride [Mass/volume] in Serum or Plasma:** 138.8 mg/dL[^20]
- **Cholesterol in LDL [Mass/volume] in Serum or Plasma by Direct assay:** 137.2 mg/dL[^21]
- **Cholesterol in HDL [Mass/volume] in Serum or Plasma:** 33.2 mg/dL[^22]

**Assessments & screenings**
- **Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences [PRAPARE]:** What was your best estimate of the total income of all family members from all sources, before taxes, in last year [PhenX] 26021 /a; How many people are living or staying at this address [#] 7[^23]
- **Total score [HARK]:** 0[^24]
- **Total score [DAST-10]:** 0[^25]

**Procedures**
- **Medication reconciliation:** Performed this encounter (2022-08-05)[^26]
- **Assessment of health and social care needs:** Performed this encounter (2022-08-05)[^27]
- **Screening for domestic abuse:** Performed this encounter (2022-08-05)[^28]
- **Assessment of substance use:** Performed this encounter (2022-08-05)[^29]
- **Screening for drug abuse:** Performed this encounter (2022-08-05)[^30]
- **Patient referral for dental care:** Performed this encounter (2022-08-05)[^31]

**Reports**
- **Lipid panel with direct LDL - Serum or Plasma:** Filed this encounter (2022-08-05)[^32]
- **Humiliation, Afraid, Rape, and Kick questionnaire [HARK]:** Filed this encounter (2022-08-05)[^33]
- **Drug Abuse Screening Test-10 [DAST-10]:** Filed this encounter (2022-08-05)[^34]
- **History and physical note:** Filed this encounter (2022-08-05)[^35]

**Immunizations**
- **Influenza, split virus, trivalent, PF:** Administered this encounter (2022-08-05)[^36]
- **Td (adult), 5 Lf tetanus toxoid, preservative free, adsorbed:** Administered this encounter (2022-08-05)[^37]

## Provenance

Rendered from the Patient Context Model (37 slots; 39 ledger entries — 39 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Encounter/3a3a1f26-ed23-f65c-e264-be689558faea` — Whitley Wellness LLC (FHIR record)
[^2]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Condition/3a3a1f26-ed23-f65c-40f7-7adeeda2aee7` — Whitley Wellness LLC (FHIR record) · 2 ledger entries
[^4]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Condition/3a3a1f26-ed23-f65c-e211-618ac5858a3b` — Whitley Wellness LLC (FHIR record)
[^5]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#longitudinal` — EHR longitudinal record (FHIR record)
[^6]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#longitudinal` — EHR longitudinal record (FHIR record)
[^7]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#longitudinal` — EHR longitudinal record (FHIR record)
[^8]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#longitudinal` — EHR longitudinal record (FHIR record)
[^9]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#longitudinal` — EHR longitudinal record (FHIR record)
[^10]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Condition/3a3a1f26-ed23-f65c-6793-7c12d20dfd90` — Whitley Wellness LLC (FHIR record) · 2 ledger entries
[^11]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Observation/3a3a1f26-ed23-f65c-5f51-373302a31281` — Whitley Wellness LLC (FHIR record)
[^12]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Observation/3a3a1f26-ed23-f65c-6272-2137ffe1facf` — Whitley Wellness LLC (FHIR record)
[^13]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Observation/3a3a1f26-ed23-f65c-2180-6da63bd2c7cf` — Whitley Wellness LLC (FHIR record)
[^14]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Observation/3a3a1f26-ed23-f65c-551b-40f3ebc96dcf` — Whitley Wellness LLC (FHIR record)
[^15]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Observation/3a3a1f26-ed23-f65c-1585-e0c94faa3e98` — Whitley Wellness LLC (FHIR record)
[^16]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Observation/3a3a1f26-ed23-f65c-0bda-d0d977c74807` — Whitley Wellness LLC (FHIR record)
[^17]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Observation/3a3a1f26-ed23-f65c-906d-f9f200ed667e` — Whitley Wellness LLC (FHIR record)
[^18]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Observation/3a3a1f26-ed23-f65c-c136-3e5bc32df973` — Whitley Wellness LLC (FHIR record)
[^19]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Observation/3a3a1f26-ed23-f65c-6ab6-852931d1ffea` — Whitley Wellness LLC (FHIR record)
[^20]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Observation/3a3a1f26-ed23-f65c-9834-6d08d0c46537` — Whitley Wellness LLC (FHIR record)
[^21]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Observation/3a3a1f26-ed23-f65c-cd0a-03c959ea6425` — Whitley Wellness LLC (FHIR record)
[^22]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Observation/3a3a1f26-ed23-f65c-4b65-ba78fca3eef4` — Whitley Wellness LLC (FHIR record)
[^23]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Observation/3a3a1f26-ed23-f65c-7c06-749bd4dd3697` — Whitley Wellness LLC (FHIR record)
[^24]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Observation/3a3a1f26-ed23-f65c-b87e-54d823644e72` — Whitley Wellness LLC (FHIR record)
[^25]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Observation/3a3a1f26-ed23-f65c-45b0-2398155a0076` — Whitley Wellness LLC (FHIR record)
[^26]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Procedure/3a3a1f26-ed23-f65c-405b-e63f78a122bf` — Whitley Wellness LLC (FHIR record)
[^27]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Procedure/3a3a1f26-ed23-f65c-57fb-30acfe7aa8d9` — Whitley Wellness LLC (FHIR record)
[^28]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Procedure/3a3a1f26-ed23-f65c-50d4-c755bcbc705c` — Whitley Wellness LLC (FHIR record)
[^29]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Procedure/3a3a1f26-ed23-f65c-68fc-ec0d73ffa4f4` — Whitley Wellness LLC (FHIR record)
[^30]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Procedure/3a3a1f26-ed23-f65c-5821-2f48a6e38b4f` — Whitley Wellness LLC (FHIR record)
[^31]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Procedure/3a3a1f26-ed23-f65c-cdba-4cc35c6d4bcd` — Whitley Wellness LLC (FHIR record)
[^32]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#DiagnosticReport/3a3a1f26-ed23-f65c-06ba-bd6ede425ddf` — Whitley Wellness LLC (FHIR record)
[^33]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#DiagnosticReport/3a3a1f26-ed23-f65c-1407-13ae0ec2ce11` — Whitley Wellness LLC (FHIR record)
[^34]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#DiagnosticReport/3a3a1f26-ed23-f65c-1dae-c6a4ceb400a6` — Whitley Wellness LLC (FHIR record)
[^35]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#DiagnosticReport/6fda147d-19c3-143b-f948-194f7ca604a7` — Whitley Wellness LLC (FHIR record)
[^36]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Immunization/3a3a1f26-ed23-f65c-8988-a72dc5911afe` — Whitley Wellness LLC (FHIR record)
[^37]: `fhir:3a3a1f26-ed23-f65c-a7df-c96fac56f464::3a3a1f26-ed23-f65c-e264-be689558faea#Immunization/3a3a1f26-ed23-f65c-1a07-31864b15c26e` — Whitley Wellness LLC (FHIR record)
