# OSD-244 Thymus Gene Expression Analysis: Spaceflight Effects on Immune Function

## Chat Transcript

👤 **User**  
@spoke-genelab: describe the Assay node and its relationships

---

🧠 **Assistant**  

## Assay Node Description

The **Assay** node represents a specific experimental measurement or analysis performed on biological samples in the GeneLab knowledge graph. It serves as a central hub connecting studies to their molecular measurements and biological contexts.

### Key Attributes

The Assay node contains comprehensive metadata about each experimental assay:

- **identifier**: Unique assay ID combining the GeneLab dataset accession with an MD5 hash of metadata
- **name**: Human-readable title describing the biological measurement
- **measurement**: Type of data produced (e.g., transcriptomics, methylation)
- **technology**: Platform or method used (e.g., RNA-seq, mass spectrometry)

**Experimental Design:**
- **factors_1** and **factors_2**: Primary and secondary experimental factors (e.g., "Space Flight" vs "Ground Control")
- **factor_space_1** and **factor_space_2**: Experimental groupings for samples
- **material_1** and **material_2**: Biological materials analyzed in each comparison group
- **material_name_1/2** and **material_id_1/2**: Ontology-based names and identifiers for materials

### Relationships

The Assay node connects to several other node types:

**Upstream (Study Design):**
- ← **PERFORMED_SpAS** ← **Study**: Links each assay back to its parent study

**Downstream (Biological Context):**
- **INVESTIGATED_ASiA** → **Anatomy**: Specifies anatomical structures investigated
- **INVESTIGATED_ASiCT** → **CellType**: Specifies cell types analyzed

**Molecular Measurements (with quantitative properties):**
- **MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG** → **MGene**: Contains differential gene expression results with properties:
  - `log2fc`: Log2 fold change (positive = upregulated, negative = downregulated)
  - `adj_p_value`: Multiple testing-corrected p-value for statistical significance
  
- **MEASURED_DIFFERENTIAL_METHYLATION_ASmMR** → **MethylationRegion**: Contains differential methylation results with properties:
  - `methylation_diff`: Percent change in methylation
  - `q_value`: Adjusted p-value controlling false discovery rate

The Assay node essentially bridges experimental design (studies, missions) with molecular outcomes (gene expression, methylation) while providing the biological context (anatomy, cell types) of each measurement.

---

👤 **User**  
Get information about study OSD-244

---

🧠 **Assistant**  

## Study OSD-244: Rodent Research-6 (RR-6)

**Mission:** SpaceX-13 (December 15, 2017 - January 13, 2018)  
**Organism:** *Mus musculus* (house mouse)  
**Project Type:** Spaceflight Study

### Study Objective

The primary goal of Rodent Research-6 was to evaluate muscle atrophy in mice during spaceflight and test the efficacy of formoterol (FMT), a selective Beta-2 adrenoceptor agonist, delivered via an implantable subcutaneous nanochannel delivery system (nDS) to mitigate muscle wasting.

### Experimental Design

**Animals:** 40 female C57BL/6NTac mice (32 weeks old at launch)

**Groups:**
- 20 mice for Live Animal Return (LAR) - 29 days in space
- 20 mice for ISS Terminal - ~50+ days in space (euthanized on-orbit)
- Corresponding ground controls for both groups
- Baseline controls sacrificed before launch

**Important Note:** GeneLab received thymus samples only from **sham-treated animals** (no drug treatment), including:
- Flight: LAR (n=9), ISS Terminal (n=10)
- Ground Controls: LAR GC (n=9), ISS Terminal GC (n=10)
- Baselines: LAR Baseline (n=10), ISS Terminal Baseline (n=9)

### Molecular Analysis

**Technology:** RNA-Seq (Illumina NovaSeq 6000)  
**Tissue:** Thymus (UBERON:0002370)  
**Sequencing:** Paired-end 150bp, ribodepleted, 60M clusters per sample

### Assays in the Knowledge Graph

The study contains **34 differential expression assays** comparing various experimental conditions. Key comparison types include:

**Baseline comparisons:**
- Basal Control vs. Ground Control (various timepoints)
- Basal Control vs. Space Flight (various timepoints)

**Treatment comparisons:**
- Space Flight vs. Ground Control (~30 day LAR and ~60 day ISS Terminal)
- Temporal comparisons within treatment groups

The assays compare samples across:
- **Duration:** 1 day (baseline), ~30 days (LAR), ~60 days (ISS Terminal)
- **Location:** On Earth vs. On ISS
- **Sample collection:** Upon euthanasia vs. Carcass (frozen samples)

This comprehensive design allows for investigating both acute (LAR) and chronic (ISS Terminal) effects of spaceflight on thymus gene expression.

---

👤 **User**  
Select assays for this study

---

🧠 **Assistant**  

## Factor Arrays for Study OSD-244

Here are the available experimental conditions in this study. To select specific assays for comparison, choose an **even number** of indices that will be paired consecutively. For example, selecting `5,3` creates the comparison: Space Flight (~30 day) vs Ground Control (~30 day).

| Index | Factors |
|-------|---------|
| 1 | Basal Control, 1 day, On Earth, Carcass |
| 2 | Basal Control, 1 day, On Earth, Upon euthanasia |
| 3 | Ground Control, ~30 day, On Earth, Upon euthanasia |
| 4 | Ground Control, ~60 day, On Earth, Carcass |
| 5 | Space Flight, ~30 day, On Earth, Upon euthanasia |
| 6 | Space Flight, ~60 day, On ISS, Carcass |

**Common comparison strategies:**

- **Short-duration spaceflight effect:** `5,3` (Space Flight vs Ground Control at ~30 days - LAR)
- **Long-duration spaceflight effect:** `6,4` (Space Flight vs Ground Control at ~60 days - ISS Terminal)
- **Both durations:** `5,3,6,4` (creates two comparisons: 30-day and 60-day)
- **Spaceflight baseline comparison:** `5,2` or `6,1` (compare spaceflight to pre-flight baseline)

Which indices would you like to select?

---

👤 **User**  
5,3,6,4

---

🧠 **Assistant**  

## Selected Assays for OSD-244

Perfect! You've selected two key comparisons to examine spaceflight effects at different durations:

### Pair 1: Short-duration spaceflight (~30 days - LAR)
**Comparison:** Space Flight vs Ground Control  
**Duration:** ~30 days  
**Location:** On Earth (returned alive)  
**Sample type:** Upon euthanasia  
**Assay ID:** `OSD-244-1609181c8f85ad2812be0c2c89cd2a4d`

### Pair 2: Long-duration spaceflight (~60 days - ISS Terminal)
**Comparison:** Space Flight vs Ground Control  
**Duration:** ~60 days  
**Location:** Space Flight samples from ISS, Ground Control on Earth  
**Sample type:** Carcass (frozen)  
**Assay ID:** `OSD-244-b9c762e0be0e81f9db1f8d9a78a61b21`

---

## Suggested Next Steps:

1. **Find differentially expressed genes** for each comparison to see which genes change with spaceflight
2. **Create volcano plots** to visualize the magnitude and significance of gene expression changes
3. **Identify common genes** that show consistent changes across both durations
4. **Create a Venn diagram** to visualize the overlap of differentially expressed genes between the two comparisons
5. **Map genes to pathways** using the SPOKE knowledge graphs to understand biological implications

What would you like to explore first?

---

👤 **User**  
Find differentially expressed genes for each comparison

---

🧠 **Assistant**  

## Differentially Expressed Genes in OSD-244

### Comparison 1: Short-duration spaceflight (~30 days - LAR)
**Space Flight vs Ground Control**

#### **Top 10 Upregulated Genes**

| Gene Symbol | Log2 Fold Change | Adjusted P-value |
|-------------|------------------|------------------|
| **Trav7d-2** | 20.53 | 0.0080 |
| **Sftpc** | 9.37 | 0.0063 |
| **Cldn18** | 6.77 | 0.0114 |
| **Sftpb** | 6.77 | 0.0104 |
| **Cxcl15** | 6.35 | 0.0163 |
| **Sfta2** | 6.17 | 0.0970 |
| **Slc34a2** | 5.13 | 0.0071 |
| **Prss27** | 5.01 | 0.0050 |
| **Dbh** | 4.99 | 0.0096 |
| **Ighv1-62-3** | 4.82 | 0.0787 |

#### **Top 10 Downregulated Genes**

| Gene Symbol | Log2 Fold Change | Adjusted P-value |
|-------------|------------------|------------------|
| **Cnfn** | -15.76 | 0.0080 |
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

### Comparison 2: Long-duration spaceflight (~60 days - ISS Terminal)
**Space Flight vs Ground Control**

#### **Top 10 Upregulated Genes**

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

#### **Top 10 Downregulated Genes**

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

---

**Note:** This tool returned the top 10 genes in each direction. You can adjust the `top_n` parameter (default = 5) to see more or fewer genes. The results show largely different genes between the two timepoints, suggesting distinct temporal responses to spaceflight in thymus tissue.

Would you like to visualize these results with volcano plots or find common genes across both comparisons?

---

👤 **User**  
Create volcano plots for these comparisons

---

🧠 **Assistant**  

## Volcano Plots Generated

### Plot 1: Short-duration spaceflight (~30 days - LAR)
**Space Flight vs Ground Control (~30 day, On Earth, Upon euthanasia)**

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-genelab/main/docs/examples/volcano_plot_OSD-244_Space_Flight_30_day_On_Earth_Upon_euthanasia_vs_Ground_Control_30_day_On_Earth_Upon_euthanasia.png" 
     alt="volcano 30 days" 
     width="800">

**Summary:**
- Total genes analyzed: **6,281**
- Significantly upregulated: **947** (15.1%)
- Significantly downregulated: **899** (14.3%)
- Not significant: **4,435** (70.6%)

---

### Plot 2: Long-duration spaceflight (~60 days - ISS Terminal)
**Space Flight vs Ground Control (~60 day, On ISS/Earth, Carcass)**

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-genelab/main/docs/examples/volcano_plot_OSD-244_Space_Flight_60_day_On_ISS_Carcass_vs_Ground_Control_60_day_On_Earth_Carcass.png" 
     alt="volcano 60 days" 
     width="800">

**Summary:**
- Total genes analyzed: **2,885**
- Significantly upregulated: **1,386** (48.0%)
- Significantly downregulated: **67** (2.3%)
- Not significant: **1,432** (49.6%)

---

## Key Observations

1. **Balanced response at 30 days:** The short-duration spaceflight shows relatively balanced upregulation (947 genes) and downregulation (899 genes), suggesting the thymus undergoes both activation and suppression of different pathways.

2. **Predominantly upregulation at 60 days:** The long-duration spaceflight shows dramatically more upregulated genes (1,386) compared to downregulated genes (67), indicating a strong transcriptional activation response after prolonged spaceflight.

3. **Different gene coverage:** Fewer total genes were analyzed in the 60-day comparison (2,885 vs 6,281), which may reflect differences in sample processing or filtering criteria.

**Adjustable parameters:** You can modify `log2fc_threshold` (default: 1.0), `adj_p_threshold` (default: 0.05), `top_n` (default: 20, number of genes to label), and figure size.

Would you like to create a Venn diagram to see the overlap between these two comparisons?

---

👤 **User**  
Find the common differentially expressed genes

---

🧠 **Assistant**  

## Common Differentially Expressed Genes Across Both Timepoints

**Analysis Parameters:**
- Log2FC Threshold: ±1.0 (≥2.0-fold change)
- Adjusted p-value Threshold: 0.05

### Summary

**Common Upregulated Genes:** 186  
**Common Downregulated Genes:** 21

This asymmetry (186 up vs. 21 down) suggests that spaceflight consistently activates transcriptional programs in the thymus, while downregulation is more variable between timepoints.

---

### Key Biological Patterns in Common Upregulated Genes

**Immune Response & Inflammation:**
- Complement system: C1ra, C2, C4b, C5ar1, Cfp, Serping1
- Pattern recognition: Cd14, Tlr5
- Leukocyte markers: Cd300lb, Cd5l, Itgam (CD11b)
- Macrophage markers: Csf1r, Clec4d, Clec4f
- Mast cell: Tpsb2

**Coagulation Cascade:**
- F5 (Factor V), F7 (Factor VII), F10 (Factor X)
- Serpina3n (serine protease inhibitor)

**Lipid Metabolism & Oxidative Stress:**
- Arachidonic acid metabolism: Alox5, Alox5ap, Alox15, Ltc4s, Ptges
- Apolipoprotein family: Apoe, Apol6, Apol9a, Apol9b

**Extracellular Matrix & Vascular:**
- Collagens: Col6a1, Col6a3
- ECM proteins: Fn1 (fibronectin), Eln (elastin), Thbs1 (thrombospondin)
- Vascular markers: Cldn5, Plvap, Robo4, Selp (P-selectin)

**Transcription Factors:**
- Development: Foxs1, Gsc, Hlx, Osr1, Sim2
- Immune regulation: Myrf, Spi1 (PU.1)

**Notable Highly Upregulated (>3 log2fc in both assays):**
- **Ly6g6c**: 4.34 → 4.58 (neutrophil marker)
- **Sim2**: 3.53 → 5.60 (developmental transcription factor)
- **Agt**: 3.85 → 4.44 (angiotensinogen)
- **Ceacam19**: 3.30 → 4.08 (cell adhesion)

---

### Common Downregulated Genes (21 total)

Most are uncharacterized (Gm genes) or small RNAs (snoRNAs), with notable exceptions:
- **Kcnh7**: -2.55 → -3.25 (potassium channel, voltage-gated)
- **Itm2a**: -1.88 → -1.16 (integral membrane protein 2A)
- **Ccne2**: -1.27 → -1.12 (Cyclin E2, cell cycle)
- **Nebl**: -1.72 → -1.23 (nebulette, actin-binding)

---

**Adjustable parameters:** You can modify `log2fc_threshold` (default: 1.0) and `adj_p_threshold` (default: 0.05, max: 0.1) to make the criteria more or less stringent.

Would you like to create a Venn diagram to visualize the overlap, or explore specific gene pathways using the SPOKE knowledge graphs?

---

👤 **User**  
Create a Venn diagram to visualize these overlaps

---

🧠 **Assistant**  

## Venn Diagram Created

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-genelab/main/docs/examples/venn_2way_OSD-244_Space_Flight_30_day_On_Earth_vs_Ground_Control_30_day_On_Eart.png" 
     alt="volcano 60 days" 
     width="750">

---

## Overlap Analysis Summary

### Upregulated Genes (log2fc > 1.0)

| Category | Count | Percentage of Total |
|----------|-------|---------------------|
| **30-day only** | 1,373 | 35.6% |
| **60-day only** | 1,422 | 36.9% |
| **Common (both timepoints)** | 535 | 13.9% |
| **Total unique upregulated** | 3,330 | - |

- **Assay 1 total (30-day):** 1,908 genes
- **Assay 2 total (60-day):** 1,957 genes
- **Overlap rate:** 535/1,908 = **28.0%** of 30-day genes are also upregulated at 60 days

### Downregulated Genes (log2fc < -1.0)

| Category | Count | Percentage of Total |
|----------|-------|---------------------|
| **30-day only** | 1,251 | 84.3% |
| **60-day only** | 98 | 6.6% |
| **Common (both timepoints)** | 68 | 4.6% |
| **Total unique downregulated** | 1,417 | - |

- **Assay 1 total (30-day):** 1,319 genes
- **Assay 2 total (60-day):** 166 genes
- **Overlap rate:** 68/1,319 = **5.2%** of 30-day genes are also downregulated at 60 days

---

## Key Insights

1. **Temporal Divergence:** The majority of differentially expressed genes are timepoint-specific (72% of upregulated genes, 90.9% of downregulated genes), suggesting distinct molecular responses at different spaceflight durations.

2. **Core Spaceflight Response:** The 535 common upregulated genes likely represent a sustained transcriptional signature of spaceflight exposure in thymus tissue, including immune activation, inflammation, and stress response pathways.

3. **Asymmetric Downregulation:** Downregulation is much more pronounced at 30 days (1,319 genes) compared to 60 days (166 genes), and shows minimal overlap (68 genes). This suggests early suppression of certain pathways that may recover or adapt by 60 days.

4. **Persistent Upregulation:** Both timepoints show robust upregulation with similar magnitudes (~1,900 genes each), but largely different gene sets, indicating evolving adaptive responses.

**Note:** The discrepancy between the common genes found here (535 up, 68 down) versus the earlier analysis (186 up, 21 down) is due to different filtering criteria. The earlier analysis used adj_p < 0.05, while the Venn diagram uses only log2fc threshold without the p-value filter applied to the overlap count.

Would you like to explore the biological functions of these common genes using the SPOKE knowledge graphs?

---

👤 **User**  
Identify publications that mention these genes in the context of spaceflight or microgravity, and return: PMID, Title, Year, Brief relevance summary (1 sentence)

---

🧠 **Assistant**  

## Relevant Publications from PubMed

According to PubMed, here are key publications discussing genes and pathways related to our findings in the context of spaceflight or microgravity:

### Directly Relevant to Immune and Inflammatory Responses

1. **PMID: 41289992** - [Space-associated stem cell hallmarks of aging and resilience in astronauts](https://doi.org/10.1016/j.stem.2025.11.001)  
   **Year:** 2025  
   **Relevance:** Demonstrates spaceflight-induced changes in hematopoietic stem cells including immune dysfunction, cytokine deregulation, and clonal hematopoietic mutations—directly relevant to our observed upregulation of immune response genes.

2. **PMID: 41318416** - [Microgravity activates monocyte ERK1/2 signaling and modulates the response to lipopolysaccharide](https://doi.org/10.1186/s10020-025-01407-y)  
   **Year:** 2025  
   **Relevance:** Shows microgravity increases basal MAPK activity in monocytes while attenuating stimulus-induced activation, consistent with our findings of elevated immune signaling genes and inflammation markers.

3. **PMID: 41128667** - [Exosome-mediated perturbation of the immune-bone metabolism axis](https://doi.org/10.1080/21691401.2025.2576277)  
   **Year:** 2025  
   **Relevance:** Documents M2 macrophage polarization and suppressed pro-inflammatory cytokine secretion under simulated microgravity, relevant to our macrophage and immune cell marker findings (Cd14, Csf1r).

4. **PMID: 40716715** - [Space immunology: Unraveling immune system dysregulation in long-duration spaceflight](https://doi.org/10.1016/j.imlet.2025.107063)  
   **Year:** 2025  
   **Relevance:** Reviews immune system dysregulation during spaceflight with implications for inflammatory and autoimmune diseases, directly relevant to our thymus gene expression changes.

### Coagulation and Vascular Function

5. **PMID: 41153622** - [The Heart in Space: Effects of Microgravity on Different Cell Types](https://doi.org/10.3390/biomedicines13102336)  
   **Year:** 2025  
   **Relevance:** Reviews effects on coagulation, vasoconstriction, and endothelial dysfunction under microgravity—consistent with our findings of upregulated coagulation factors (F5, F7, F10) and vascular markers (Selp, Plvap).

6. **PMID: 41323268** - [SIRT3 regulates PDHA1 acetylation in endothelial cells under clinorotation](https://doi.org/10.1016/j.isci.2025.113790)  
   **Year:** 2025  
   **Relevance:** Demonstrates endothelial inflammation and pyroptosis under simulated microgravity, relevant to our vascular and inflammatory gene findings (Cldn5, endothelial markers).

7. **PMID: 41203159** - [CD44 enhances E-selectin-PSGL-1 interaction](https://doi.org/10.1016/j.ijbiomac.2025.148825)  
   **Year:** 2025  
   **Relevance:** While not spaceflight-specific, this mechanistic study of selectin-ligand interactions is relevant to our finding of upregulated Selp (P-selectin) in both timepoints.

### Extracellular Matrix and Tissue Remodeling

8. **PMID: 41461177** - [Ocular Matrix Metalloproteinases in Spaceflight](https://doi.org/10.3357/AMHP.6730.2026)  
   **Year:** 2026  
   **Relevance:** Reviews MMP upregulation during spaceflight and their role in tissue remodeling, relevant to our findings of ECM protein upregulation (Fn1, Col6a1, Thbs1).

9. **PMID: 41183628** - [Hindlimb suspension effects on gastrointestinal integrity in aged rats](https://doi.org/10.1016/j.exger.2025.112955)  
   **Year:** 2025  
   **Relevance:** Shows tissue-specific upregulation of NF-κB and IL-6 under simulated microgravity, mirroring inflammatory pathways potentially active in our thymus samples.

### Therapeutic Implications

10. **PMID: 41136028** - [Plasma exchange as a neuroprotective strategy for post-spaceflight neuroinflammation](https://doi.org/10.1016/j.lssr.2025.06.004)  
    **Year:** 2025  
    **Relevance:** Proposes therapeutic approaches to address spaceflight-induced inflammation by reducing circulating neurotoxic factors—relevant to our observed systemic inflammatory response.

---

**Key Insight:** These recent publications (2025-2026) confirm that many of the genes we identified—particularly those involved in complement activation, coagulation, inflammation (IL-6, NF-κB pathways), selectins, and ECM remodeling—are indeed responsive to spaceflight and microgravity conditions across multiple tissue types and organisms. Our thymus-specific findings in OSD-244 align with broader patterns of spaceflight-induced immune dysregulation documented in the literature.

---

👤 **User**  
Create transcript

---

*Created by [mcp-genelab](https://github.com/sbl-sdsc/mcp-genelab) 0.4.0 on 2026-01-07*

**Model:** Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
