---
name: Monica Hilpert
dob: 1947-11-02
gender: female
city: "Somerville, MA"
marital_status: Married
language: English (United States)
fhir_patient_id: b504cdf2-e13b-979e-9c4a-95456823e3dd
record_id: "b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e"
dataset: synthetic-ambient-fhir-25
last_encounter: 2023-11-27
source: patient-context-model
slots: 25
ledger_entries: 25
synthetic: true
---

# Monica Hilpert — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Monica Hilpert, 76-year-old woman (DOB 1947-11-02), Somerville, MA. Problem list: Loss of teeth; Body mass index 30+ - obesity; Prediabetes; Hyperlipidemia; Osteoporosis. History: Past pregnancy history of miscarriage. Current medications on record: Meperidine Hydrochloride 50 MG Oral Tablet; Naproxen sodium 220 MG Oral Tablet. Social context: Educated to high school level; Has a criminal record; Victim of intimate partner abuse; Social isolation; Not in labor force; Limited social contact.

Visit 2023-11-27 (inpatient at Courtyard Nursing Care Center): SNF admission — rehabilitation and pain management.

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2023-11-27 — SNF admission — rehabilitation and pain management (inpatient · Courtyard Nursing Care Center)[^1]

**Problems**
- **Loss of teeth:** On problem list (longitudinal record)[^2]
- **Body mass index 30+ - obesity:** On problem list (longitudinal record)[^3]
- **Prediabetes:** On problem list (longitudinal record)[^4]
- **Hyperlipidemia:** On problem list (longitudinal record)[^5]
- **Osteoporosis:** On problem list (longitudinal record)[^6]

**Medical / surgical history**
- **Past pregnancy history of miscarriage:** On record (longitudinal)[^7]

**Medications**
- **Meperidine Hydrochloride 50 MG Oral Tablet:** On medication list (longitudinal record)[^8]
- **Naproxen sodium 220 MG Oral Tablet:** On medication list (longitudinal record)[^9]

**Social context**
- **Educated to high school level:** Reported in longitudinal record[^10]
- **Has a criminal record:** Reported in longitudinal record[^11]
- **Victim of intimate partner abuse:** Reported in longitudinal record[^12]
- **Social isolation:** Reported in longitudinal record[^13]
- **Not in labor force:** Reported in longitudinal record[^14]
- **Limited social contact:** Reported in longitudinal record[^15]

**Procedures**
- **History AND physical examination:** Performed this encounter (2023-11-27)[^16]
- **Initial patient assessment:** Performed this encounter (2023-11-27)[^17]
- **Development of individualized plan of care:** Performed this encounter (2023-11-27)[^18]
- **Nursing care/supplementary surveillance:** Performed this encounter (2023-11-27) ×14[^19]
- **Physical therapy procedure:** Performed this encounter (2023-11-27)[^20]
- **Occupational therapy:** Performed this encounter (2023-11-27) ×2[^21]
- **Professional / ancillary services care:** Performed this encounter (2023-11-27) ×4[^22]
- **Pre-discharge assessment:** Performed this encounter (2023-11-27)[^23]
- **Discharge from hospital:** Performed this encounter (2023-11-27)[^24]

**Reports**
- **History and physical note:** Filed this encounter (2023-11-27)[^25]

## Provenance

Rendered from the Patient Context Model (25 slots; 25 ledger entries — 25 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#Encounter/b504cdf2-e13b-979e-4f0c-523d0948189e` — Courtyard Nursing Care Center (FHIR record)
[^2]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#longitudinal` — EHR longitudinal record (FHIR record)
[^4]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#longitudinal` — EHR longitudinal record (FHIR record)
[^5]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#longitudinal` — EHR longitudinal record (FHIR record)
[^6]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#longitudinal` — EHR longitudinal record (FHIR record)
[^7]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#longitudinal` — EHR longitudinal record (FHIR record)
[^8]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#longitudinal` — EHR longitudinal record (FHIR record)
[^9]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#longitudinal` — EHR longitudinal record (FHIR record)
[^10]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#longitudinal` — EHR longitudinal record (FHIR record)
[^11]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#longitudinal` — EHR longitudinal record (FHIR record)
[^12]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#longitudinal` — EHR longitudinal record (FHIR record)
[^13]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#longitudinal` — EHR longitudinal record (FHIR record)
[^14]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#longitudinal` — EHR longitudinal record (FHIR record)
[^15]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#longitudinal` — EHR longitudinal record (FHIR record)
[^16]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#Procedure/b504cdf2-e13b-979e-2001-e0d02f7ab6e6` — Courtyard Nursing Care Center (FHIR record)
[^17]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#Procedure/b504cdf2-e13b-979e-0e95-5b336e39d465` — Courtyard Nursing Care Center (FHIR record)
[^18]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#Procedure/b504cdf2-e13b-979e-139f-255b1ca2e18d` — Courtyard Nursing Care Center (FHIR record)
[^19]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#Procedure/b504cdf2-e13b-979e-7285-21d84d25dac4,Procedure/b504cdf2-e13b-979e-cab4-81e98be2e6a8 +12 more` — Courtyard Nursing Care Center (FHIR record)
[^20]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#Procedure/b504cdf2-e13b-979e-f9e9-3e63a58309fb` — Courtyard Nursing Care Center (FHIR record)
[^21]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#Procedure/b504cdf2-e13b-979e-cab2-2fca609892a7,Procedure/b504cdf2-e13b-979e-4342-2515a8cfd010` — Courtyard Nursing Care Center (FHIR record)
[^22]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#Procedure/b504cdf2-e13b-979e-43e5-3c1b408555f2,Procedure/b504cdf2-e13b-979e-1b59-6d0067297553 +2 more` — Courtyard Nursing Care Center (FHIR record)
[^23]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#Procedure/b504cdf2-e13b-979e-a4a6-a0acb9811df1` — Courtyard Nursing Care Center (FHIR record)
[^24]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#Procedure/b504cdf2-e13b-979e-c3cd-e70b6da34e91` — Courtyard Nursing Care Center (FHIR record)
[^25]: `fhir:b504cdf2-e13b-979e-9c4a-95456823e3dd::b504cdf2-e13b-979e-4f0c-523d0948189e#DiagnosticReport/3524193c-b6cd-aa89-4242-dda51818a5bb` — Courtyard Nursing Care Center (FHIR record)
