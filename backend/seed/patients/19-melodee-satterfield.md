---
name: Melodee Satterfield
dob: 2005-10-22
gender: female
city: "Acton, MA"
marital_status: Never Married
language: English (United States)
fhir_patient_id: a3292ec4-64b6-20fc-480e-39e1f7f51e50
record_id: "a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881"
dataset: synthetic-ambient-fhir-25
last_encounter: 2026-03-21
source: patient-context-model
slots: 32
ledger_entries: 33
synthetic: true
---

# Melodee Satterfield — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Melodee Satterfield, 20-year-old woman (DOB 2005-10-22), Acton, MA. Problem list: Chronic pain; Chronic low back pain; Chronic neck pain; Normal pregnancy. Current medications on record: Acetaminophen 300 MG / Hydrocodone Bitartrate 5 MG Oral Tablet; tramadol hydrochloride 50 MG Oral Tablet. Social context: Risk activity involvement; Received higher education; Not in labor force; Stress.

Visit 2026-03-21 (ambulatory at The Lowell General Hospital): Prenatal intake visit — first pregnancy with chronic pain. Recorded this visit: Normal pregnancy (active).

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2026-03-21 — Prenatal intake visit — first pregnancy with chronic pain (ambulatory · The Lowell General Hospital)[^1]

**Problems**
- **Chronic pain:** On problem list (longitudinal record)[^2]
- **Chronic low back pain:** On problem list (longitudinal record)[^3]
- **Chronic neck pain:** On problem list (longitudinal record)[^4]
- **Normal pregnancy:** Active — recorded at 2026-03-21 encounter[^5]

**Medications**
- **Acetaminophen 300 MG / Hydrocodone Bitartrate 5 MG Oral Tablet:** On medication list (longitudinal record)[^6]
- **tramadol hydrochloride 50 MG Oral Tablet:** On medication list (longitudinal record)[^7]

**Social context**
- **Risk activity involvement:** Reported in longitudinal record[^8]
- **Received higher education:** Reported in longitudinal record[^9]
- **Not in labor force:** Reported in longitudinal record[^10]
- **Stress:** Reported in longitudinal record[^11]

**Procedures**
- **Standard pregnancy test:** Performed this encounter (2026-03-21)[^12]
- **Ultrasound scan for fetal viability:** Performed this encounter (2026-03-21)[^13]
- **Evaluation of uterine fundal height:** Performed this encounter (2026-03-21)[^14]
- **Auscultation of the fetal heart:** Performed this encounter (2026-03-21)[^15]
- **Blood group typing:** Performed this encounter (2026-03-21)[^16]
- **Hemogram, automated, with red blood cells, white blood cells, hemoglobin, hematocrit, indices, platelet count, and manual white blood cell differential:** Performed this encounter (2026-03-21)[^17]
- **Hepatitis B surface antigen measurement:** Performed this encounter (2026-03-21)[^18]
- **Human immunodeficiency virus antigen test:** Performed this encounter (2026-03-21)[^19]
- **Chlamydia antigen test:** Performed this encounter (2026-03-21)[^20]
- **Gonorrhea infection titer test:** Performed this encounter (2026-03-21)[^21]
- **Syphilis infectious titer test:** Performed this encounter (2026-03-21)[^22]
- **Urine culture:** Performed this encounter (2026-03-21)[^23]
- **Cytopathology procedure, preparation of smear, genital source:** Performed this encounter (2026-03-21)[^24]
- **Urine screening test for diabetes:** Performed this encounter (2026-03-21)[^25]
- **Hepatitis C antibody, confirmatory test:** Performed this encounter (2026-03-21)[^26]
- **Rubella screening test:** Performed this encounter (2026-03-21)[^27]
- **Measurement of Varicella-zoster virus antibody:** Performed this encounter (2026-03-21)[^28]
- **Skin test for tuberculosis, Tine test:** Performed this encounter (2026-03-21)[^29]
- **Urinalysis, protein, qualitative:** Performed this encounter (2026-03-21)[^30]
- **Physical examination procedure:** Performed this encounter (2026-03-21)[^31]

**Reports**
- **History and physical note:** Filed this encounter (2026-03-21)[^32]

## Provenance

Rendered from the Patient Context Model (32 slots; 33 ledger entries — 33 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Encounter/a3292ec4-64b6-20fc-55a4-b753a07a1881` — The Lowell General Hospital (FHIR record)
[^2]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#longitudinal` — EHR longitudinal record (FHIR record)
[^4]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#longitudinal` — EHR longitudinal record (FHIR record)
[^5]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Condition/a3292ec4-64b6-20fc-950f-c0a63feea063` — The Lowell General Hospital (FHIR record) · 2 ledger entries
[^6]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#longitudinal` — EHR longitudinal record (FHIR record)
[^7]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#longitudinal` — EHR longitudinal record (FHIR record)
[^8]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#longitudinal` — EHR longitudinal record (FHIR record)
[^9]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#longitudinal` — EHR longitudinal record (FHIR record)
[^10]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#longitudinal` — EHR longitudinal record (FHIR record)
[^11]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#longitudinal` — EHR longitudinal record (FHIR record)
[^12]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-91a0-592d4241841f` — The Lowell General Hospital (FHIR record)
[^13]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-0486-b7a11a83bc54` — The Lowell General Hospital (FHIR record)
[^14]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-330c-e9e276af1a40` — The Lowell General Hospital (FHIR record)
[^15]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-18de-79a8267dea45` — The Lowell General Hospital (FHIR record)
[^16]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-425a-3cda3ada5d17` — The Lowell General Hospital (FHIR record)
[^17]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-ae84-d83141609dbb` — The Lowell General Hospital (FHIR record)
[^18]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-5def-8678874e3947` — The Lowell General Hospital (FHIR record)
[^19]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-f9cf-4554b6762336` — The Lowell General Hospital (FHIR record)
[^20]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-b739-f4fa1acdb055` — The Lowell General Hospital (FHIR record)
[^21]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-efd1-86bde738da18` — The Lowell General Hospital (FHIR record)
[^22]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-9687-bca7cdff255a` — The Lowell General Hospital (FHIR record)
[^23]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-fc7f-6c6e6cadd2d5` — The Lowell General Hospital (FHIR record)
[^24]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-b48a-c27d9c8e5cd3` — The Lowell General Hospital (FHIR record)
[^25]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-216f-360329d504e7` — The Lowell General Hospital (FHIR record)
[^26]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-3988-cd0d62ce25b4` — The Lowell General Hospital (FHIR record)
[^27]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-2806-883bdb127005` — The Lowell General Hospital (FHIR record)
[^28]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-f4e3-5fa1cea2ffc2` — The Lowell General Hospital (FHIR record)
[^29]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-3442-b6ba806b9c93` — The Lowell General Hospital (FHIR record)
[^30]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-dd9f-a3a715415322` — The Lowell General Hospital (FHIR record)
[^31]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#Procedure/a3292ec4-64b6-20fc-a115-660c3e382f5b` — The Lowell General Hospital (FHIR record)
[^32]: `fhir:a3292ec4-64b6-20fc-480e-39e1f7f51e50::a3292ec4-64b6-20fc-55a4-b753a07a1881#DiagnosticReport/b4126493-2f53-e72f-d6f9-1b1d0c2e3627` — The Lowell General Hospital (FHIR record)
