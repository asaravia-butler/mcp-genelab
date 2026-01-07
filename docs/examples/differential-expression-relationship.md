# Chat Transcript
Differential Expression Relationship in GeneLab Knowledge Graph

👤 **User**  
Describe the MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG relationship and its properties in @spoke-genelab and include an example for a space flight vs. ground control comparison.

---

🧠 **Assistant**  
## MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG Relationship

The **MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG** relationship connects **Assay** nodes to **MGene** (Model organism Gene) nodes in the spoke-genelab knowledge graph. This relationship captures differential gene expression data from transcriptomic experiments.

### Relationship Properties

The relationship has two key properties stored as edge attributes:

1. **log2fc** (float): Log2-transformed fold change in gene expression between the experimental condition and its reference baseline. 
   - Positive values indicate **up-regulation** (higher transcript abundance in the experimental condition)
   - Negative values indicate **down-regulation** (lower transcript abundance compared to control)

2. **adj_p_value** (float): Multiple testing-corrected p-value assessing the statistical significance of each gene's differential expression after controlling the false discovery rate (FDR).
   - Smaller values (e.g., ≤ 0.05) indicate the observed fold change is unlikely to arise by chance
   - Accounts for the large number of simultaneous tests performed in genome-wide expression experiments

### Example: Space Flight vs. Ground Control

Here's a real example from the GeneLab knowledge graph:

**Study**: OSD-516 (human primary cell RNA-seq experiment)

```
Assay ID: OSD-516-8a1eba7a8026895f2207a77f7bf6615f

Conditions Compared:
├─ Space Flight: Female, 2% human serum, primary cells
└─ Ground Control: Male, media, primary cells

Gene: LOC102724560 (cystathionine beta-synthase like)
Organism: Homo sapiens

Differential Expression:
├─ log2fc: -50.36
└─ adj_p_value: 3.64 × 10⁻⁴⁹
```

**Interpretation**: This gene shows extreme down-regulation in the space flight condition compared to ground control, with a log2 fold change of -50.36 (meaning expression is ~2⁵⁰ times lower in space flight). The adjusted p-value of 3.64 × 10⁻⁴⁹ indicates this difference is highly statistically significant, far exceeding the typical 0.05 threshold.

---

👤 **User**  
Create transcript

---

*Created by [mcp-genelab](https://github.com/sbl-sdsc/mcp-genelab) 0.4.0 on 2026-01-06*

Model: claude-sonnet-4-20250514
