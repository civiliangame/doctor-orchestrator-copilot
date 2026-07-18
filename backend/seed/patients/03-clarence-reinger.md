---
name: Clarence Reinger
dob: 1993-05-09
gender: female
city: "Somerville, MA"
marital_status: Married
language: English (United States)
fhir_patient_id: b342f27e-56bc-08ac-347c-323279c0d595
record_id: "b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47"
dataset: synthetic-ambient-fhir-25
last_encounter: 2025-06-01
source: patient-context-model
slots: 26
ledger_entries: 27
synthetic: true
---

# Clarence Reinger — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Clarence Reinger, 32-year-old woman (DOB 1993-05-09), Somerville, MA. Problem list: Recurrent urinary tract infection; Normal pregnancy. No current medications on record. Social context: Received higher education; Medication review due.

Visit 2025-06-01 (ambulatory at Cambridge Public Health Commission): Prenatal intake visit — initial obstetric evaluation. Recorded this visit: Normal pregnancy (resolved).

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2025-06-01 — Prenatal intake visit — initial obstetric evaluation (ambulatory · Cambridge Public Health Commission)[^1]

**Problems**
- **Recurrent urinary tract infection:** On problem list (longitudinal record)[^2]
- **Normal pregnancy:** Resolved — recorded at 2025-06-01 encounter[^3]

**Social context**
- **Received higher education:** Reported in longitudinal record[^4]
- **Medication review due:** Reported in longitudinal record[^5]

**Procedures**
- **Standard pregnancy test:** Performed this encounter (2025-06-01)[^6]
- **Ultrasound scan for fetal viability:** Performed this encounter (2025-06-01)[^7]
- **Evaluation of uterine fundal height:** Performed this encounter (2025-06-01)[^8]
- **Auscultation of the fetal heart:** Performed this encounter (2025-06-01)[^9]
- **Blood group typing:** Performed this encounter (2025-06-01)[^10]
- **Hemogram, automated, with red blood cells, white blood cells, hemoglobin, hematocrit, indices, platelet count, and manual white blood cell differential:** Performed this encounter (2025-06-01)[^11]
- **Hepatitis B surface antigen measurement:** Performed this encounter (2025-06-01)[^12]
- **Human immunodeficiency virus antigen test:** Performed this encounter (2025-06-01)[^13]
- **Chlamydia antigen test:** Performed this encounter (2025-06-01)[^14]
- **Gonorrhea infection titer test:** Performed this encounter (2025-06-01)[^15]
- **Syphilis infectious titer test:** Performed this encounter (2025-06-01)[^16]
- **Urine culture:** Performed this encounter (2025-06-01)[^17]
- **Cytopathology procedure, preparation of smear, genital source:** Performed this encounter (2025-06-01)[^18]
- **Urine screening test for diabetes:** Performed this encounter (2025-06-01)[^19]
- **Hepatitis C antibody, confirmatory test:** Performed this encounter (2025-06-01)[^20]
- **Rubella screening test:** Performed this encounter (2025-06-01)[^21]
- **Measurement of Varicella-zoster virus antibody:** Performed this encounter (2025-06-01)[^22]
- **Skin test for tuberculosis, Tine test:** Performed this encounter (2025-06-01)[^23]
- **Urinalysis, protein, qualitative:** Performed this encounter (2025-06-01)[^24]
- **Physical examination procedure:** Performed this encounter (2025-06-01)[^25]

**Reports**
- **History and physical note:** Filed this encounter (2025-06-01)[^26]

## Provenance

Rendered from the Patient Context Model (26 slots; 27 ledger entries — 27 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Encounter/b342f27e-56bc-08ac-24f0-de401f6e3c47` — Cambridge Public Health Commission (FHIR record)
[^2]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Condition/b342f27e-56bc-08ac-2913-b051dda4c455` — Cambridge Public Health Commission (FHIR record) · 2 ledger entries
[^4]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#longitudinal` — EHR longitudinal record (FHIR record)
[^5]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#longitudinal` — EHR longitudinal record (FHIR record)
[^6]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-2127-70aa4d07268b` — Cambridge Public Health Commission (FHIR record)
[^7]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-0058-65475e991270` — Cambridge Public Health Commission (FHIR record)
[^8]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-c974-a60470c91463` — Cambridge Public Health Commission (FHIR record)
[^9]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-b485-24359052ce73` — Cambridge Public Health Commission (FHIR record)
[^10]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-f493-d79edea7421a` — Cambridge Public Health Commission (FHIR record)
[^11]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-d6ab-23330e55a7d5` — Cambridge Public Health Commission (FHIR record)
[^12]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-2183-fbbcbe0f2199` — Cambridge Public Health Commission (FHIR record)
[^13]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-95a5-46a81cafef56` — Cambridge Public Health Commission (FHIR record)
[^14]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-8f91-1dfb367ed988` — Cambridge Public Health Commission (FHIR record)
[^15]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-7bf9-f957d3a59c65` — Cambridge Public Health Commission (FHIR record)
[^16]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-0e86-27c8bff0b571` — Cambridge Public Health Commission (FHIR record)
[^17]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-b97a-ec94f48e7e80` — Cambridge Public Health Commission (FHIR record)
[^18]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-a527-8174196b4c6e` — Cambridge Public Health Commission (FHIR record)
[^19]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-675b-4ae1bff9250d` — Cambridge Public Health Commission (FHIR record)
[^20]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-a9c8-3f5f79e0df23` — Cambridge Public Health Commission (FHIR record)
[^21]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-3aa3-f0d88673f06a` — Cambridge Public Health Commission (FHIR record)
[^22]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-23ae-5f9344d220ee` — Cambridge Public Health Commission (FHIR record)
[^23]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-4237-d04e1eada042` — Cambridge Public Health Commission (FHIR record)
[^24]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-643e-db7b32b7e05d` — Cambridge Public Health Commission (FHIR record)
[^25]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#Procedure/b342f27e-56bc-08ac-ec18-e1b554dff322` — Cambridge Public Health Commission (FHIR record)
[^26]: `fhir:b342f27e-56bc-08ac-347c-323279c0d595::b342f27e-56bc-08ac-24f0-de401f6e3c47#DiagnosticReport/d297dc97-582b-7200-82cd-051642b509a2` — Cambridge Public Health Commission (FHIR record)
