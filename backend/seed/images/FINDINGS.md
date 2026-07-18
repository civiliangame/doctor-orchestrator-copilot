# Beat C — seed images & expected findings

Two staged images drive the imaging-tech upload in the demo. A multimodal read
of each should surface the findings below, **framed as observations flagged for
Dr. Zhang's review — never a diagnosis, never treatment advice** (DEMO_SCRIPT.md
Beat C).

---

## ct_chest.jpg — chest CT axial slice

- **Source:** https://commons.wikimedia.org/wiki/File:CT-Thorax-5.0-B70f-Lungs.jpg
- **Direct file:** https://upload.wikimedia.org/wikipedia/commons/4/4e/CT-Thorax-5.0-B70f-Lungs.jpg
- **Author:** Ptrump16
- **License:** CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0)
- **Attribution (for any on-screen credit):** "CT-Thorax-5.0-B70f-Lungs.jpg by
  Ptrump16, CC BY-SA 4.0, via Wikimedia Commons."
- **Modality:** Axial thoracic CT, lung window. Siemens SOMATOM Sensation 64,
  5.0 mm slice, B70f kernel, 120 kV. 1024x1024 JPEG, grayscale — reads well on a
  projector.

### What is ACTUALLY visible in this specific slice
This is a largely **unremarkable lung-window axial CT** at roughly the mid/lower
thorax:
- Both lungs are aerated and appear dark (air-filled); the normal branching
  pulmonary vascular markings radiate outward from the hila on both sides.
- The **mediastinum** sits centrally (heart/great-vessel soft tissue, bright).
- A **vertebral body** is visible posteriorly in the midline; ribs and the
  chest wall form the bright bony/soft-tissue ring.
- No large, obvious mass, big consolidation, or sizeable pleural effusion stands
  out in this slice. There is **no dramatic focal lesion** — an honest read is
  that findings are subtle at best.

### How it should be framed for the demo
The seeded intake sets a **"radiating-pain escalation ... prioritize views of the
upper-left thoracic region"** brief (DEMO_SCRIPT.md Beat C / imaging node goals).
So the read should:
- Note it is examining/attending to the **upper-left thoracic region** per the
  standing priority, and report what is (or is not) seen there.
- Phrase everything as **"Flagged for Dr. Zhang's review: ..."** — e.g. an
  observation about the left-side lung field / vascular markings and an explicit
  note that any subtle finding warrants correlation, **without** naming a
  disease or recommending treatment.
- It is acceptable (and honest) for the CT read to say the slice looks broadly
  unremarkable and simply flag the prioritized region for the attending — the
  demo value is the *append-to-chart, flagged-for-review* behavior, not a
  dramatic finding.

---

## lab_panel.png — synthetic lab panel (generated)

- **Source:** generated locally by `gen_lab_panel.py` (Pillow). No network, no
  PHI — every value invented for the demo. Title on the image says
  "SYNTHETIC LAB PANEL — DEMO DATA".
- Patient label: **Maria Alvarez**, DOB 1968-03-12.

### Values shown
| Test              | Result         | Reference   | Flag |
|-------------------|----------------|-------------|------|
| Troponin I        | 0.09 ng/mL     | ref < 0.04  | HIGH |
| CK-MB             | 6.8 ng/mL      | ref < 6.3   | HIGH |
| D-dimer           | 0.4 ug/mL FEU  | ref < 0.5   | —    |
| Lipid panel — LDL | 132 mg/dL      | ref < 100   | HIGH |
| CRP               | 1.1 mg/L       | ref < 3.0   | —    |

### Expected findings a multimodal read should surface
The salient pattern is the **elevated cardiac markers**:
- **Troponin I 0.09 ng/mL is above the < 0.04 reference (HIGH)** — the
  headline abnormal value.
- **CK-MB 6.8 ng/mL is above the < 6.3 reference (HIGH)** — corroborating
  cardiac-marker elevation.
- Secondary: **LDL 132 mg/dL is above the < 100 reference (HIGH)** — consistent
  with the borderline-high LDL already in Maria's chart.
- D-dimer (0.4, normal) and CRP (1.1, normal) are within range — a good read
  should NOT flag these.

### How it should be framed for the demo
Each finding phrased as **"Flagged for Dr. Zhang's review: ..."** citing the
**actual numbers and reference ranges** (e.g. "Troponin I 0.09 ng/mL, above the
reference of < 0.04"). Do **not** state or imply a diagnosis (e.g. no "myocardial
infarction"/"heart attack") and do **not** recommend treatment — just flag the
abnormal values for the attending physician.

---

## Demo framing rule (both images)
1 to 3 findings per image, each an observation **flagged for Dr. Zhang's
review**, never a diagnosis, never treatment advice. Lab-panel findings must
cite the abnormal values with their numbers.
