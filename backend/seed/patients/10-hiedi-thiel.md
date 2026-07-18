---
name: Hiedi Thiel
dob: 1993-07-26
gender: female
city: "Ludlow, MA"
marital_status: Never Married
language: English (United States)
fhir_patient_id: 40cb7be2-9c26-6328-3aa0-71db4ed81e06
record_id: "40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e"
dataset: synthetic-ambient-fhir-25
last_encounter: 2024-07-22
source: patient-context-model
slots: 32
ledger_entries: 34
synthetic: true
---

# Hiedi Thiel — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Hiedi Thiel, 30-year-old woman (DOB 1993-07-26), Ludlow, MA. Problem list: Adolescent idiopathic scoliosis; Severe anxiety (panic); Normal pregnancy; Anemia. Current medications on record: ferrous sulfate 325 MG Oral Tablet; Vitamin B12 5 MG/ML Injectable Solution. Social context: Educated to high school level; Lack of access to transportation; Transport problem; Stress.

Visit 2024-07-22 (ambulatory at Encompass Health Rehab Hospital Of Western Mass): Prenatal intake visit — first trimester, newly identified anemia. Recorded this visit: Normal pregnancy (resolved); Anemia (resolved).

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2024-07-22 — Prenatal intake visit — first trimester, newly identified anemia (ambulatory · Encompass Health Rehab Hospital Of Western Mass)[^1]

**Problems**
- **Adolescent idiopathic scoliosis:** On problem list (longitudinal record)[^2]
- **Severe anxiety (panic):** On problem list (longitudinal record)[^3]
- **Normal pregnancy:** Resolved — recorded at 2024-07-22 encounter[^4]
- **Anemia:** Resolved — recorded at 2024-07-22 encounter[^5]

**Medications**
- **ferrous sulfate 325 MG Oral Tablet:** On medication list (longitudinal record)[^6]
- **Vitamin B12 5 MG/ML Injectable Solution:** On medication list (longitudinal record)[^7]

**Social context**
- **Educated to high school level:** Reported in longitudinal record[^8]
- **Lack of access to transportation:** Reported in longitudinal record[^9]
- **Transport problem:** Reported in longitudinal record[^10]
- **Stress:** Reported in longitudinal record[^11]

**Procedures**
- **Standard pregnancy test:** Performed this encounter (2024-07-22)[^12]
- **Ultrasound scan for fetal viability:** Performed this encounter (2024-07-22)[^13]
- **Evaluation of uterine fundal height:** Performed this encounter (2024-07-22)[^14]
- **Auscultation of the fetal heart:** Performed this encounter (2024-07-22)[^15]
- **Blood group typing:** Performed this encounter (2024-07-22)[^16]
- **Hemogram, automated, with red blood cells, white blood cells, hemoglobin, hematocrit, indices, platelet count, and manual white blood cell differential:** Performed this encounter (2024-07-22)[^17]
- **Hepatitis B surface antigen measurement:** Performed this encounter (2024-07-22)[^18]
- **Human immunodeficiency virus antigen test:** Performed this encounter (2024-07-22)[^19]
- **Chlamydia antigen test:** Performed this encounter (2024-07-22)[^20]
- **Gonorrhea infection titer test:** Performed this encounter (2024-07-22)[^21]
- **Syphilis infectious titer test:** Performed this encounter (2024-07-22)[^22]
- **Urine culture:** Performed this encounter (2024-07-22)[^23]
- **Cytopathology procedure, preparation of smear, genital source:** Performed this encounter (2024-07-22)[^24]
- **Urine screening test for diabetes:** Performed this encounter (2024-07-22)[^25]
- **Hepatitis C antibody, confirmatory test:** Performed this encounter (2024-07-22)[^26]
- **Rubella screening test:** Performed this encounter (2024-07-22)[^27]
- **Measurement of Varicella-zoster virus antibody:** Performed this encounter (2024-07-22)[^28]
- **Skin test for tuberculosis, Tine test:** Performed this encounter (2024-07-22)[^29]
- **Urinalysis, protein, qualitative:** Performed this encounter (2024-07-22)[^30]
- **Physical examination procedure:** Performed this encounter (2024-07-22)[^31]

**Reports**
- **History and physical note:** Filed this encounter (2024-07-22)[^32]

## Provenance

Rendered from the Patient Context Model (32 slots; 34 ledger entries — 34 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Encounter/40cb7be2-9c26-6328-75bd-838e58c2583e` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^2]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#longitudinal` — EHR longitudinal record (FHIR record)
[^4]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Condition/40cb7be2-9c26-6328-c541-7e49380d5a38` — Encompass Health Rehab Hospital Of Western Mass (FHIR record) · 2 ledger entries
[^5]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Condition/40cb7be2-9c26-6328-d8a9-3f0cdfda2442` — Encompass Health Rehab Hospital Of Western Mass (FHIR record) · 2 ledger entries
[^6]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#longitudinal` — EHR longitudinal record (FHIR record)
[^7]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#longitudinal` — EHR longitudinal record (FHIR record)
[^8]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#longitudinal` — EHR longitudinal record (FHIR record)
[^9]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#longitudinal` — EHR longitudinal record (FHIR record)
[^10]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#longitudinal` — EHR longitudinal record (FHIR record)
[^11]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#longitudinal` — EHR longitudinal record (FHIR record)
[^12]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-2525-69841904f7bd` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^13]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-cf41-a5ee60b519b3` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^14]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-5e29-aa4b6f309675` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^15]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-c6ae-5478454973da` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^16]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-cb51-c5026c38cdbd` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^17]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-af82-466fdf2e1542` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^18]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-c1a7-662cea2216f9` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^19]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-9091-6d544a4fb50e` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^20]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-3e36-2425285a7462` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^21]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-3aeb-51d3ca5cfe97` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^22]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-6f6f-73cf580d2b8c` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^23]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-5491-72b37c5eaee8` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^24]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-1ed7-787a4cdfbaa3` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^25]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-6ff6-cabbff4cd5a5` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^26]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-1b0e-7cec1c325df8` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^27]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-601d-41f62c3cc028` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^28]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-e1d0-69b6f0a4e9bb` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^29]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-5c7c-7e1581dff2ec` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^30]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-1944-cccfec68fc0a` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^31]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#Procedure/40cb7be2-9c26-6328-caa0-c633bfaed52e` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
[^32]: `fhir:40cb7be2-9c26-6328-3aa0-71db4ed81e06::40cb7be2-9c26-6328-75bd-838e58c2583e#DiagnosticReport/e4d87b4f-00e7-c266-cb9e-74f321d2e133` — Encompass Health Rehab Hospital Of Western Mass (FHIR record)
