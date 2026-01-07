# Chat Transcript: GeneLab Knowledge Graph Schema Visualization

## Chat Transcript

👤 **User**  
@spoke-genelab

---

🧠 **Assistant**  
I can help you explore the NASA GeneLab knowledge graph! This database contains information about spaceflight experiments, gene expression data, and biological responses to space environments.

Here are some things I can help you with:

**Explore Studies & Experiments**
- Search for specific studies (e.g., OSD-253, GLDS-47)
- Find experiments by organism, tissue type, or spaceflight conditions
- Compare different assays within a study

**Analyze Gene Expression**
- Find differentially expressed genes (upregulated/downregulated)
- Compare gene expression across multiple experiments
- Create volcano plots and Venn diagrams
- Identify common genes across different conditions

**Knowledge Graph Queries**
- Explore relationships between genes, diseases, pathways, and compounds
- Custom Cypher queries for complex analyses
- Visualize the knowledge graph schema

**Example questions you could ask:**
- "What studies involve mouse muscle tissue in spaceflight?"
- "Show me the top upregulated genes in study OSD-253"
- "Compare gene expression between microgravity and ground control conditions"
- "What pathways are associated with bone loss in spaceflight?"

What would you like to explore in the GeneLab knowledge graph?

---

👤 **User**  
Visualize the schema

---

🧠 **Assistant**  
Here's the GeneLab knowledge graph schema! The diagram shows:

**Core Entities:**
- **Mission** → **Study** → **Assay**: The hierarchical structure of spaceflight experiments
- **MGene**: Mouse genes with differential expression data
- **Gene**: Generic gene references (for ortholog relationships)
- **MethylationRegion**: DNA methylation sites
- **Anatomy** & **CellType**: Tissue and cell type annotations

**Key Relationships with Properties:**
- **MEASURED_DIFFERENTIAL_EXPRESSION**: Links assays to genes with `log2fc` (fold change) and `adj_p_value` (statistical significance)
- **MEASURED_DIFFERENTIAL_METHYLATION**: Links assays to methylation regions with `methylation_diff` and `q_value`

This structure allows you to query everything from mission-level metadata down to individual gene expression changes, making it possible to compare experiments across different spaceflight conditions, organisms, and tissue types.

```mermaid
classDiagram
direction TB

class Mission {
    STRING identifier
    STRING name
    STRING space_program
    STRING flight_program
    DATE start_date
    DATE end_date
}

class Study {
    STRING identifier
    STRING name
    STRING project_title
    STRING description
    STRING organism
    STRING taxonomy
    STRING project_type
}

class Assay {
    STRING identifier
    STRING name
    STRING measurement
    STRING technology
    STRING material_1
    STRING material_name_1
    STRING material_id_1
    LIST factors_1
    STRING factor_space_1
    STRING material_2
    STRING material_name_2
    STRING material_id_2
    LIST factors_2
    STRING factor_space_2
}

class MGene {
    STRING identifier
    STRING name
    STRING symbol
    STRING organism
    STRING taxonomy
}

class Gene {
    INTEGER identifier
}

class MethylationRegion {
    STRING identifier
    STRING name
    STRING chromosome
    INTEGER start
    INTEGER end
    BOOLEAN in_promoter
    BOOLEAN in_exon
    BOOLEAN in_intron
    INTEGER dist_to_feature
}

class Anatomy {
    STRING identifier
}

class CellType {
    STRING identifier
}

class MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG {
    float log2fc
    float adj_p_value
}

class MEASURED_DIFFERENTIAL_METHYLATION_ASmMR {
    float methylation_diff
    float q_value
}

Mission --> Study : CONDUCTED_MIcS
Study --> Assay : PERFORMED_SpAS
Assay --> MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG
MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG --> MGene
Assay --> MEASURED_DIFFERENTIAL_METHYLATION_ASmMR
MEASURED_DIFFERENTIAL_METHYLATION_ASmMR --> MethylationRegion
Assay --> Anatomy : INVESTIGATED_ASiA
Assay --> CellType : INVESTIGATED_ASiCT
MGene --> MethylationRegion : METHYLATED_IN_MGmMR
MGene --> Gene : IS_ORTHOLOG_MGiG
```

---

*Created by [mcp-genelab](https://github.com/sbl-sdsc/mcp-genelab) 0.4.0 on 2026-01-06*  
*Model: claude-sonnet-4-20250514*
