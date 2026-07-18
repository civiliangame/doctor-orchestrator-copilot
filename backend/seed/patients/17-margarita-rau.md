---
name: Margarita Rau
dob: 1976-08-20
gender: female
city: "Beverly, MA"
marital_status: Married
language: English (United States)
fhir_patient_id: c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32
record_id: "c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4"
dataset: synthetic-ambient-fhir-25
last_encounter: 2019-09-27
source: patient-context-model
slots: 31
ledger_entries: 32
synthetic: true
---

# Margarita Rau — patient context

> Fully synthetic patient (Synthea + LLM transcript). Not a real person.

## Summary

Margarita Rau, 43-year-old woman (DOB 1976-08-20), Beverly, MA. Problem list: Prediabetes; Anemia; Body mass index 30+ - obesity; Essential hypertension; Metabolic syndrome X; Normal pregnancy. History: Past pregnancy history of miscarriage. No current medications on record. Social context: Educated to high school level; Victim of intimate partner abuse.

Visit 2019-09-27 (ambulatory at Lahey Hospital & Medical Center, Burlington): Initial prenatal visit — new pregnancy at 43. Recorded this visit: Normal pregnancy (resolved).

## Current status

Every line is a belief in the Patient Context Model; its footnote is the ledger entry justifying it — the exact FHIR resource, transcript turn, or note it came from, and who contributed it.

**Encounter**
- **Most recent encounter:** 2019-09-27 — Initial prenatal visit — new pregnancy at 43 (ambulatory · Lahey Hospital & Medical Center, Burlington)[^1]

**Problems**
- **Prediabetes:** On problem list (longitudinal record)[^2]
- **Anemia:** On problem list (longitudinal record)[^3]
- **Body mass index 30+ - obesity:** On problem list (longitudinal record)[^4]
- **Essential hypertension:** On problem list (longitudinal record)[^5]
- **Metabolic syndrome X:** On problem list (longitudinal record)[^6]
- **Normal pregnancy:** Resolved — recorded at 2019-09-27 encounter[^7]

**Medical / surgical history**
- **Past pregnancy history of miscarriage:** On record (longitudinal)[^8]

**Social context**
- **Educated to high school level:** Reported in longitudinal record[^9]
- **Victim of intimate partner abuse:** Reported in longitudinal record[^10]

**Procedures**
- **Standard pregnancy test:** Performed this encounter (2019-09-27)[^11]
- **Ultrasound scan for fetal viability:** Performed this encounter (2019-09-27)[^12]
- **Evaluation of uterine fundal height:** Performed this encounter (2019-09-27)[^13]
- **Auscultation of the fetal heart:** Performed this encounter (2019-09-27)[^14]
- **Blood group typing:** Performed this encounter (2019-09-27)[^15]
- **Hemogram, automated, with red blood cells, white blood cells, hemoglobin, hematocrit, indices, platelet count, and manual white blood cell differential:** Performed this encounter (2019-09-27)[^16]
- **Hepatitis B surface antigen measurement:** Performed this encounter (2019-09-27)[^17]
- **Human immunodeficiency virus antigen test:** Performed this encounter (2019-09-27)[^18]
- **Chlamydia antigen test:** Performed this encounter (2019-09-27)[^19]
- **Gonorrhea infection titer test:** Performed this encounter (2019-09-27)[^20]
- **Syphilis infectious titer test:** Performed this encounter (2019-09-27)[^21]
- **Urine culture:** Performed this encounter (2019-09-27)[^22]
- **Cytopathology procedure, preparation of smear, genital source:** Performed this encounter (2019-09-27)[^23]
- **Urine screening test for diabetes:** Performed this encounter (2019-09-27)[^24]
- **Hepatitis C antibody, confirmatory test:** Performed this encounter (2019-09-27)[^25]
- **Rubella screening test:** Performed this encounter (2019-09-27)[^26]
- **Measurement of Varicella-zoster virus antibody:** Performed this encounter (2019-09-27)[^27]
- **Skin test for tuberculosis, Tine test:** Performed this encounter (2019-09-27)[^28]
- **Urinalysis, protein, qualitative:** Performed this encounter (2019-09-27)[^29]
- **Physical examination procedure:** Performed this encounter (2019-09-27)[^30]

**Reports**
- **History and physical note:** Filed this encounter (2019-09-27)[^31]

## Provenance

Rendered from the Patient Context Model (31 slots; 32 ledger entries — 32 FHIR record). The ledger is append-only: the patient's context at any past moment is reconstructable by replaying it. Live version: `GET /api/patients/<id>/context.md`; seed corpus: `uv run python scripts/build_patient_contexts.py`.

[^1]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Encounter/c2cbc55e-34dc-73c6-4d09-7d9c99b11de4` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^2]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#longitudinal` — EHR longitudinal record (FHIR record)
[^3]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#longitudinal` — EHR longitudinal record (FHIR record)
[^4]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#longitudinal` — EHR longitudinal record (FHIR record)
[^5]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#longitudinal` — EHR longitudinal record (FHIR record)
[^6]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#longitudinal` — EHR longitudinal record (FHIR record)
[^7]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Condition/c2cbc55e-34dc-73c6-7cad-b3aec57af7da` — Lahey Hospital & Medical Center, Burlington (FHIR record) · 2 ledger entries
[^8]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#longitudinal` — EHR longitudinal record (FHIR record)
[^9]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#longitudinal` — EHR longitudinal record (FHIR record)
[^10]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#longitudinal` — EHR longitudinal record (FHIR record)
[^11]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-7f53-f978c78c0225` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^12]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-6ffc-7d5de64265f5` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^13]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-f217-65149c73df72` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^14]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-03a8-aba5cf645e52` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^15]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-676f-fc226c57e8ea` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^16]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-420b-d101b370a4d3` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^17]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-bf48-dd1897d9f3f3` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^18]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-e17b-e7f22b8d594b` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^19]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-e1c4-dda91fe09809` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^20]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-4eda-df0a9242edf1` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^21]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-49ec-200867be5298` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^22]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-608c-65acfe6e8707` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^23]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-ffbe-ca4a594f0dbf` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^24]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-72cc-65749421e93a` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^25]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-b3eb-5ef605a0cf56` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^26]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-2c6f-1ef572296a4e` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^27]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-4739-8ad5d9c9d432` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^28]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-7539-dda6c46dc7fa` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^29]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-5773-7c0ee0ee9ba7` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^30]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#Procedure/c2cbc55e-34dc-73c6-167e-771e36620910` — Lahey Hospital & Medical Center, Burlington (FHIR record)
[^31]: `fhir:c2cbc55e-34dc-73c6-5ee4-cabe0c40fc32::c2cbc55e-34dc-73c6-4d09-7d9c99b11de4#DiagnosticReport/6a79d935-df93-404d-3b64-60626dc42942` — Lahey Hospital & Medical Center, Burlington (FHIR record)
