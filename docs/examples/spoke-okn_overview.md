# Chat Transcript: SPOKE Knowledge Graph Schema Visualization

👤 **User**  
@spoke-okn

---

🧠 **Assistant**  
I can see that you've mentioned the SPOKE (Scalable Precision Medicine Oriented Knowledge Engine) MCP server. I have access to various tools for querying this knowledge graph database about biomedical relationships and gene expression data.

What would you like to explore? I can help you with:

- **Schema exploration**: View the structure and types of nodes/relationships in the knowledge graph
- **Gene expression analysis**: Find differentially expressed genes from specific assays
- **Comparative analysis**: Compare gene expression across multiple conditions
- **Visualizations**: Create volcano plots and Venn diagrams for gene expression data
- **Custom queries**: Run specific Cypher queries on the Neo4j database

What biomedical or gene expression questions can I help you investigate?

---

👤 **User**  
Visualize the schema

---

🧠 **Assistant**  
Here's the SPOKE knowledge graph schema visualization:

```mermaid
classDiagram
direction TB

class Compound {
  max_phase: FLOAT
  name: STRING
  synonyms: LIST
  xrefs: LIST
  identifier: STRING
  smiles: STRING
  standardized_smiles: STRING
  sources: LIST
}

class Disease {
  source: STRING
  name: STRING
  mesh_list: LIST
  identifier: STRING
  Linkout: STRING
  omim_list: LIST
}

class Gene {
  description: STRING
  name: STRING
  ensembl: STRING
  identifier: INTEGER
}

class Location {
  state: STRING
  zipcode_type: STRING
  code: STRING
  type: STRING
  Linkout: FLOAT
  state_name: STRING
  sources: LIST
  county_fips: STRING
  name: STRING
  city_fips: STRING
  iso3: STRING
  longitude: FLOAT
  latitude: FLOAT
  identifier: STRING
  state_fips: STRING
}

class Organism {
  usa_isolation_country: STRING
  biovar: STRING
  strain: STRING
  isolation_source: STRING
  host_age: STRING
  salinity: STRING
  disease: STRING
  antimicrobial_resistance: STRING
  sources: LIST
  level: STRING
  name: STRING
  genome_size: FLOAT
  collection_date: STRING
  isolation_country: STRING
  pathovar: STRING
  host_gender: STRING
  host_is_human: STRING
  temperature_range: STRING
  host_name: STRING
  has_amr_phenotype: STRING
  sporulation: STRING
  is_resistant: STRING
  genbank_accessions: STRING
  host_health: STRING
  motility: STRING
  serovar: STRING
  oxygen_requirement: STRING
  gram_stain: STRING
  identifier: STRING
}

class SDoH {
  topic: STRING
  description: FLOAT
  name: STRING
  data_source: STRING
  domain: STRING
  mesh_ids: LIST
  identifier: STRING
  sources: LIST
}

class Environment {
  name: STRING
  synonyms: LIST
  identifier: STRING
  sources: LIST
}

Compound --> Compound : ISA_CiC
Compound --> Compound : HASROLE_ChC
Compound --> Compound : INTERACTS_CiC
Compound --> Gene : DOWNREGULATES_CdG
Compound --> Gene : UPREGULATES_CuG
Compound --> Location : FOUNDIN_CfL
Compound --> Disease : CONTRAINDICATES_CcD
Compound --> Compound : PARTOF_CpC
Compound --> Disease : TREATS_CtD

Disease --> Location : MORTALITY_DmL
Disease --> Disease : ISA_DiD
Disease --> Location : PREVALENCE_DpL
Disease --> Gene : ASSOCIATES_DaG
Disease --> Disease : RESEMBLES_DrD

Gene --> Disease : MARKER_POS_GmpD
Gene --> Disease : EXPRESSEDIN_GeiD
Gene --> Compound : RESPONSE_TO_mGrC
Gene --> Disease : MARKER_NEG_GmnD
Gene --> Compound : RESISTANT_TO_mGrC

Location --> Location : PARTOF_LpL

Organism --> Location : ISOLATEDIN_OiL
Organism --> Compound : RESPONDS_TO_OrC

SDoH --> SDoH : ISA_SiS
SDoH --> Disease : ASSOCIATES_SaD
SDoH --> Location : PREVALENCEIN_SpL

Environment --> Environment : ISA_EiE
Environment --> Location : FOUNDIN_EfL
```

The schema shows 7 main entity types with their properties and relationships:

**Entities:**
- **Compound**: Chemical compounds with drug information, SMILES structures, and clinical trial phases
- **Disease**: Medical conditions with MESH and OMIM identifiers
- **Gene**: Genetic elements with Ensembl IDs and descriptions
- **Location**: Geographic entities with coordinates and administrative codes
- **Organism**: Biological organisms with detailed microbiological characteristics
- **SDoH** (Social Determinants of Health): Socioeconomic and environmental health factors
- **Environment**: Environmental contexts where organisms or compounds are found

**Key Relationships:**
- Compounds can upregulate/downregulate genes, treat or contraindicate diseases
- Diseases associate with genes and have prevalence/mortality data by location
- Genes serve as disease markers and respond to compounds
- Organisms are isolated in locations and respond to compounds
- SDoH factors associate with diseases and have prevalence in locations

---

👤 **User**  
Create transcript

---

*Created by [mcp-genelab](https://github.com/nasa/mcp-genelab) 0.3.0 using claude-sonnet-4-20250514 on 2024-12-24*
