# OSD-244 Thymus Spaceflight Analysis

## Chat Transcript

👤 **User**  
Get information about study OSD-244

---

🧠 **Assistant**  
## Study OSD-244: Rodent Research-6

**Overview:**
OSD-244 is a spaceflight study called "Rodent Research-6" (RR-6) that investigated muscle atrophy in mice during spaceflight and tested a therapeutic to mitigate muscle wasting.

**Study Details:**
- **Organism:** Mus musculus (Mouse)
- **Mission:** SpaceX-13 (December 15, 2017 - January 13, 2018)
- **Space Program:** NASA International Space Station (ISS)

**Experimental Design:**
The study used 40 female C57BL/6NTac mice (32 weeks old) that were either sham operated or implanted with a nanochannel delivery system (nDS) containing the drug formoterol or vehicle. The mice were divided into:

- **Live Animal Return (LAR) group:** 20 mice maintained in microgravity for 29 days, returned to Earth alive on January 13, 2018
- **ISS Terminal group:** 20 mice maintained in microgravity for >50 days, euthanized on-orbit

Ground control and baseline groups were also maintained for comparison.

**GeneLab Samples:**
GeneLab received thymus samples from sham-treated animals only (no drug-treated animals) from:
- Flight LAR (n=9) and ISS Terminal (n=10)  
- Ground Controls: LAR GC (n=9) and ISS Terminal GC (n=10)
- Baselines: LAR Baseline (n=10) and ISS Terminal Baseline (n=9)

**Data Type:**
- **Measurement:** Transcription profiling
- **Technology:** RNA Sequencing (RNA-Seq) on Illumina NovaSeq 6000
- **Sequencing depth:** ~60M clusters per sample (ribodepleted, paired-end 150bp)

**Available Assays:**
The study contains 10+ assays comparing different experimental conditions, including comparisons between:
- Basal controls vs. spaceflight at different time points
- Ground controls vs. spaceflight  
- Different duration exposures (~30 day vs ~60 day)
- Different processing methods (upon euthanasia vs. carcass)

---

👤 **User**  
Select assays for this study

---

🧠 **Assistant**  
## Factor Arrays for Study OSD-244

Here are the unique experimental conditions available in this study. To compare conditions, choose an **even number of indices** for pairwise comparisons (e.g., '1,2,3,4' creates pairs: 1 vs 2 and 3 vs 4).

| Index | Factors |
|-------|---------|
| 1 | Basal Control, 1 day, On Earth, Carcass |
| 2 | Basal Control, 1 day, On Earth, Upon euthanasia |
| 3 | Ground Control, ~30 day, On Earth, Upon euthanasia |
| 4 | Ground Control, ~60 day, On Earth, Carcass |
| 5 | Space Flight, ~30 day, On Earth, Upon euthanasia |
| 6 | Space Flight, ~60 day, On ISS, Carcass |

**Suggested comparisons:**

For **short-duration spaceflight effects** (LAR):
- **5,3** - Space Flight vs Ground Control at ~30 days (both upon euthanasia)

For **long-duration spaceflight effects** (ISS Terminal):
- **6,4** - Space Flight vs Ground Control at ~60 days (both carcass)

For **both durations** in one selection:
- **5,3,6,4** - Both short and long duration comparisons

---

👤 **User**  
5,3,6,4

---

🧠 **Assistant**  
## Selected Assays for OSD-244

Perfect! I've selected two pairwise comparisons for you:

### Pair 1: Short-Duration Spaceflight (~30 days, LAR)
**Condition 1:** Space Flight, ~30 day, On Earth, Upon euthanasia  
**Condition 2:** Ground Control, ~30 day, On Earth, Upon euthanasia  
**Assay ID:** `OSD-244-1609181c8f85ad2812be0c2c89cd2a4d`

### Pair 2: Long-Duration Spaceflight (~60 days, ISS Terminal)
**Condition 1:** Space Flight, ~60 day, On ISS, Carcass  
**Condition 2:** Ground Control, ~60 day, On Earth, Carcass  
**Assay ID:** `OSD-244-b9c762e0be0e81f9db1f8d9a78a61b21`

## Suggested Next Steps:

1. **Find differentially expressed genes** for each comparison
2. **Create volcano plots** to visualize the differential expression
3. **Identify common genes** that show consistent changes across both durations
4. **Create a Venn diagram** to show overlap between the two comparisons
5. **Map to pathways/functions** using the SPOKE knowledge graph

---

👤 **User**  
Find differentially expressed genes for each comparison

---

🧠 **Assistant**  
## Differentially Expressed Genes - OSD-244 Comparisons

### Comparison 1: Short-Duration Spaceflight (~30 days, LAR)
**Space Flight vs Ground Control**

#### **Upregulated Genes**

| Gene Symbol | Log2 Fold Change | Adjusted P-value |
|-------------|------------------|------------------|
| **Trav7d-2** | 20.53 | 0.0079 |
| **Sftpc** | 9.37 | 0.0063 |
| **Cldn18** | 6.77 | 0.0114 |
| **Sftpb** | 6.77 | 0.0104 |
| **Cxcl15** | 6.35 | 0.0163 |
| **Sfta2** | 6.17 | 0.0970 |
| **Slc34a2** | 5.13 | 0.0071 |
| **Prss27** | 5.01 | 0.0050 |
| **Dbh** | 4.99 | 0.0096 |
| **Ighv1-62-3** | 4.82 | 0.0787 |

#### **Downregulated Genes**

| Gene Symbol | Log2 Fold Change | Adjusted P-value |
|-------------|------------------|------------------|
| **Cnfn** | -15.76 | 0.0079 |
| **Olfr2** | -6.88 | 0.0653 |
| **Cldn34c6** | -6.64 | 0.0348 |
| **Gpr101** | -6.54 | 0.0086 |
| **Vmn2r42** | -6.32 | 0.0567 |
| **Vmn2r74** | -6.30 | 0.0934 |
| **Vmn1r28** | -6.27 | 0.0328 |
| **Vmn2r94** | -6.25 | 0.0409 |
| **Gm12986** | -6.23 | 0.0873 |
| **Gm14052** | -6.20 | 0.0296 |

---

### Comparison 2: Long-Duration Spaceflight (~60 days, ISS Terminal)
**Space Flight vs Ground Control**

#### **Upregulated Genes**

| Gene Symbol | Log2 Fold Change | Adjusted P-value |
|-------------|------------------|------------------|
| **Krt4** | 9.43 | 1.20e-08 |
| **Myh8** | 8.66 | 1.93e-06 |
| **Krt13** | 8.25 | 1.66e-07 |
| **Klk11** | 6.74 | 0.0051 |
| **Cfap97d2** | 6.59 | 0.0003 |
| **Bpifa1** | 6.32 | 0.0001 |
| **Bpifb1** | 6.07 | 0.0030 |
| **Gm36041** | 5.95 | 0.0018 |
| **Scgb3a1** | 5.94 | 0.0012 |
| **C730027H18Rik** | 5.84 | 0.0033 |

#### **Downregulated Genes**

| Gene Symbol | Log2 Fold Change | Adjusted P-value |
|-------------|------------------|------------------|
| **Ibsp** | -7.21 | 3.48e-05 |
| **Gm25682** | -6.12 | 0.0059 |
| **Gm23686** | -5.31 | 0.0012 |
| **Gm25189** | -4.98 | 0.0336 |
| **Gm23330** | -4.58 | 0.0649 |
| **LOC115490478** | -4.10 | 0.0552 |
| **Gm8325** | -3.31 | 0.0969 |
| **Gm23511** | -3.28 | 0.0427 |
| **Dynlt2a3** | -3.27 | 0.0316 |
| **Kcnh7** | -3.25 | 0.0055 |

**Note:** You can adjust the `top_n` parameter (default: 5) to see more or fewer genes in these lists.

---

👤 **User**  
Create volcano plots for these comparisons

---

🧠 **Assistant**  
## Volcano Plots Generated

### Plot 1: Short-Duration Spaceflight (~30 days, LAR)
**Comparison:** Space Flight vs Ground Control (~30 day, On Earth, Upon euthanasia)

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-genelab/main/docs/examples/volcano_plot_OSD-244_Space_Flight_30_day_On_Earth_Upon_euthanasia_vs_Ground_Control_30_day_On_Earth_Upon_euthanasia.png" 
     alt="volcano 30 days" 
     width="800">

**Summary Statistics:**
- Total genes analyzed: **6,281**
- Significantly upregulated: **947** (15.1%)
- Significantly downregulated: **899** (14.3%)
- Not significant: **4,435** (70.6%)

---

### Plot 2: Long-Duration Spaceflight (~60 days, ISS Terminal)
**Comparison:** Space Flight vs Ground Control (~60 day, On ISS, Carcass)

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-genelab/main/docs/examples/volcano_plot_OSD-244_Space_Flight_60_day_On_ISS_Carcass_vs_Ground_Control_60_day_On_Earth_Carcass.png" 
     alt="volcano 60 days" 
     width="800">

**Summary Statistics:**
- Total genes analyzed: **2,885**
- Significantly upregulated: **1,386** (48.0%)
- Significantly downregulated: **67** (2.3%)
- Not significant: **1,432** (49.6%)

---

**Key Observations:**
- The long-duration spaceflight shows a more dramatic upregulation pattern (48% vs 15%)
- Short-duration has more balanced up/down regulation
- The long-duration comparison has far more upregulated genes than downregulated

**Adjustable parameters:**
- `top_n` (default: 20) - number of genes to label
- `log2fc_threshold` (default: 1.0) - fold change threshold
- `adj_p_threshold` (default: 0.05) - significance threshold
- `figsize_width`, `figsize_height` (defaults: 8, 5) - plot dimensions

---

👤 **User**  
Find the common differentially expressed genes

---

🧠 **Assistant**  
## Common Differentially Expressed Genes Across Both Spaceflight Durations

**Thresholds Used:**
- Log₂ Fold Change: ±1.0 (≥2-fold change)
- Adjusted p-value: 0.05

### Summary Statistics
- **Common upregulated genes:** 186
- **Common downregulated genes:** 21
- **Total common DEGs:** 207

---

### Top Common Upregulated Genes (showing first 20)

| Gene | ~30 Day | ~60 Day | Function/Notes |
|------|---------|---------|----------------|
| **Ly6g6c** | 4.34 | 4.58 | Immune response |
| **Sim2** | 3.53 | 5.60 | Transcription factor |
| **Agt** | 3.85 | 4.44 | Angiotensinogen (blood pressure regulation) |
| **Ceacam19** | 3.30 | 4.08 | Cell adhesion |
| **Hmga1b** | 3.22 | 3.87 | Chromatin architecture |
| **F10** | 3.50 | 3.81 | Coagulation factor X |
| **Ahsg** | 3.19 | 3.56 | Alpha-2-HS-glycoprotein |
| **Alox15** | 3.01 | 3.83 | Arachidonate 15-lipoxygenase |
| **Clca1** | 3.39 | 3.53 | Calcium-activated chloride channel |
| **F7** | 3.37 | 3.40 | Coagulation factor VII |
| **Gsc** | 2.88 | 3.26 | Goosecoid homeobox |
| **Hamp** | 3.17 | 2.85 | Hepcidin (iron regulation) |
| **C4b** | 2.72 | 3.02 | Complement component 4B |
| **F5** | 2.86 | 3.01 | Coagulation factor V |
| **Prkag3** | 3.07 | 3.12 | AMPK regulatory subunit |
| **Thbs1** | 3.02 | 2.32 | Thrombospondin 1 |
| **Asb5** | 3.01 | 2.98 | Ankyrin repeat protein |
| **Crb2** | 2.95 | 2.14 | Cell polarity protein |
| **Rarres2** | 2.85 | 2.09 | Chemerin (adipokine) |
| **Hba-a1** | 2.55 | 2.76 | Hemoglobin alpha |

---

### Common Downregulated Genes (all 21 genes)

| Gene | ~30 Day | ~60 Day | Function/Notes |
|------|---------|---------|----------------|
| **Kcnh7** | -2.55 | -3.25 | Potassium channel |
| **Gm33619** | -2.11 | -1.73 | Predicted gene |
| **Gm12238** | -2.11 | -1.32 | Predicted gene |
| **LOC115487699** | -2.10 | -1.97 | Uncharacterized |
| **Gm24451** | -1.92 | -1.58 | Predicted gene |
| **Rnu12** | -1.89 | -1.61 | Small nuclear RNA |
| **Itm2a** | -1.88 | -1.16 | Integral membrane protein |
| **2310015K22Rik** | -1.86 | -1.75 | Uncharacterized |
| **Gm22488** | -1.84 | -1.70 | Predicted gene |
| **Snora36b** | -1.82 | -1.58 | Small nucleolar RNA |
| **Gm25313** | -1.75 | -1.63 | Predicted gene |
| **Nebl** | -1.72 | -1.23 | Nebulette (muscle protein) |
| **Gm39792** | -1.71 | -1.41 | Predicted gene |
| **Trbv23** | -1.67 | -1.47 | T cell receptor variable gene |
| **Gm26130** | -1.61 | -1.42 | Predicted gene |
| **Lpar6** | -1.47 | -1.05 | Lysophosphatidic acid receptor |
| **Snora23** | -1.44 | -1.33 | Small nucleolar RNA |
| **Gm22620** | -1.40 | -1.38 | Predicted gene |
| **Snora81** | -1.38 | -1.15 | Small nucleolar RNA |
| **Gm25099** | -1.36 | -1.35 | Predicted gene |
| **Ccne2** | -1.27 | -1.12 | Cyclin E2 (cell cycle) |

---

**Key Biological Themes:**
1. **Coagulation factors** (F5, F7, F10) - consistently upregulated
2. **Immune response genes** (Ly6g6c, complement components)
3. **Iron regulation** (Hamp - hepcidin)
4. **Vascular/endothelial markers** (multiple genes)
5. **Fewer downregulated genes** - mainly predicted genes and small RNAs

**Adjustable parameters:**
- `log2fc_threshold` (default: 1.0) - minimum fold change
- `adj_p_threshold` (default: 0.05, max: 0.1) - significance threshold

---

👤 **User**  
Create a Venn diagram to visualize these overlaps

---

🧠 **Assistant**  
## Venn Diagram Generated

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-genelab/main/docs/examples/venn_2way_OSD-244_Space_Flight_30_day_On_Earth_vs_Ground_Control_30_day_On_Eart.png" 
     alt="volcano 60 days" 
     width="750">

**Comparisons:**
- **Assay 1 (Left):** Space Flight vs Ground Control (~30 day)
- **Assay 2 (Right):** Space Flight vs Ground Control (~60 day)

**Log2FC Threshold:** ±1.0

---

### Upregulated Genes (log2fc > 1.0)

| Category | Count | Percentage |
|----------|-------|------------|
| **~30 day only** | 1,373 | 72.0% of Assay 1 |
| **~60 day only** | 1,422 | 72.7% of Assay 2 |
| **Common (both durations)** | 535 | 28.0% of Assay 1, 27.3% of Assay 2 |
| Total Assay 1 | 1,908 | |
| Total Assay 2 | 1,957 | |

### Downregulated Genes (log2fc < -1.0)

| Category | Count | Percentage |
|----------|-------|------------|
| **~30 day only** | 1,251 | 94.8% of Assay 1 |
| **~60 day only** | 98 | 59.0% of Assay 2 |
| **Common (both durations)** | 68 | 5.2% of Assay 1, 41.0% of Assay 2 |
| Total Assay 1 | 1,319 | |
| Total Assay 2 | 166 | |

---

**Key Findings:**

1. **Upregulation is comparable** between both durations with similar total numbers (1,908 vs 1,957)
2. **~28% overlap in upregulated genes** suggests some core spaceflight response genes
3. **Dramatic difference in downregulation**: 
   - Short duration (~30 day): 1,319 downregulated genes
   - Long duration (~60 day): Only 166 downregulated genes
4. **Higher overlap percentage for downregulated genes** in the long duration (41% vs 5.2%)
5. **Duration-specific responses dominate** (~72% unique genes in each condition)

**Adjustable parameters:**
- `log2fc_threshold` (default: 1.0) - minimum fold change
- `figsize_width`, `figsize_height` (defaults: 10, 6) - plot dimensions

This pattern suggests that the thymus response to spaceflight involves both duration-independent core pathways and significant duration-specific changes, particularly in gene downregulation.

---

*Created by [mcp-genelab](https://github.com/sbl-sdsc/mcp-genelab) 0.4.0 on 2026-01-06*

*Model: claude-sonnet-4-20250514*
