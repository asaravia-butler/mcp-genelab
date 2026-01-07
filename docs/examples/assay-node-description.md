# Chat Transcript: GeneLab Assay Node Description

👤 **User**  
Describe the Assay node and its properties in @spoke-genelab, and include an example for a space flight vs ground control comparison.

---

🧠 **Assistant**  
I'll query the GeneLab knowledge graph to get information about the Assay node and its properties.

## Assay Node in the GeneLab Knowledge Graph

The **Assay** node represents a specific experimental measurement or analysis performed in a GeneLab study. It captures the comparison between experimental conditions (typically Space Flight vs Ground Control) and contains detailed metadata about the biological materials analyzed and the technology used.

### Key Properties

**Identification:**
- `identifier` - Unique assay ID combining the GeneLab dataset accession (e.g., "OSD-1") and an MD5 hash of metadata
- `name` - Human-readable title describing the biological measurement

**Measurement Details:**
- `measurement` - Type of data produced (e.g., "transcription profiling", "proteomics")
- `technology` - Platform or method used (e.g., "DNA microarray", "RNA-Seq", "mass spectrometry")

**Experimental Factors:**
- `factor_space_1` - Primary experimental condition (typically "Space Flight")
- `factor_space_2` - Comparative/control condition (typically "Ground Control", "Basal Control", or "Vivarium Control")
- `factors_1` - Array of all primary experimental factors applied to group 1
- `factors_2` - Array of all secondary/control factors for group 2

**Biological Materials:**
- `material_1` / `material_2` - Biological materials analyzed in each group (e.g., tissue, cell type, organ)
- `material_name_1` / `material_name_2` - Ontology-based names (e.g., UBERON terms)
- `material_id_1` / `material_id_2` - Controlled ontology identifiers (e.g., UBERON codes)

### Example: Space Flight vs Ground Control Comparison

Here's a real example from the GeneLab knowledge graph:

```
Assay ID: OSD-1-a46c350d406c6c0daf2cec787f97cdac
Name: OSD-1_transcription-profiling_dna-microarray_Affymetrix

Measurement: transcription profiling
Technology: DNA microarray

Biological Material:
  - Group 1: Whole Organism
  - Group 2: Whole Organism

Experimental Comparison:
  - Primary factors (Group 1): ["Space Flight", "infected with Beauveria bassiana"]
  - Control factors (Group 2): ["Ground Control", "infected with Beauveria bassiana"]
  
Space Conditions:
  - factor_space_1: "Space Flight"
  - factor_space_2: "Ground Control"
```

In this example, the assay compares gene expression in whole organisms infected with *Beauveria bassiana* (a fungal pathogen) under two conditions: Space Flight versus Ground Control. The assay uses DNA microarray technology to measure transcription profiling, allowing researchers to identify differentially expressed genes between the spaceflight and ground control groups.

---

*Created by [mcp-genelab](https://github.com/sbl-sdsc/mcp-genelab) 0.4.0 on 2026-01-06*

Model: claude-sonnet-4-20250514
