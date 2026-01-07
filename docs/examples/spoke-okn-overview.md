# SPOKE Knowledge Graph Schema Visualization

👤 **User**  
@spoke-okn

---

🧠 **Assistant**  
I can help you work with the SPOKE (Scalable Precision Medicine Open Knowledge Engine) knowledge graph! This is a biomedical knowledge graph that integrates data from various sources.

Let me start by getting information about the schema to understand what's available in this knowledge graph.

Great! I can see the SPOKE knowledge graph contains several types of nodes:

**Node Types:**
- **Compound** - Chemical compounds and drugs with properties like name, SMILES structures, and clinical trial phases
- **Disease** - Diseases with identifiers from MeSH and OMIM
- **Gene** - Genes with Ensembl IDs and descriptions
- **Location** - Geographic locations (countries, states, cities, etc.)
- **Organism** - Biological organisms with antimicrobial resistance data
- **SDoH** - Social Determinants of Health
- **Environment** - Environmental factors

**Key Relationships:**
- Compounds can treat diseases, upregulate/downregulate genes, and interact with other compounds
- Diseases associate with genes and can resemble other diseases
- Genes can be markers for diseases and respond to compounds
- Locations track disease prevalence and mortality
- Social determinants of health associate with diseases

What would you like to explore in the SPOKE knowledge graph? I can help you:
- Search for specific compounds, diseases, or genes
- Find relationships between entities
- Explore treatment options for diseases
- Investigate gene-disease associations
- Query location-based health data

What interests you?

---

👤 **User**  
Visualize the schema

---

🧠 **Assistant**  
I've created a visualization of the SPOKE knowledge graph schema! The diagram shows:

**Main Entity Types:**
- **Compound** - Chemical compounds with properties like max phase, SMILES structures
- **Disease** - Diseases with MeSH and OMIM identifiers
- **Gene** - Genes with Ensembl IDs and descriptions
- **Location** - Geographic locations with coordinates
- **Organism** - Biological organisms with antimicrobial resistance data
- **SDoH** - Social Determinants of Health
- **Environment** - Environmental factors

**Key Relationship Patterns:**
- Relationships with properties are shown as intermediary classes (e.g., TREATS_CtD contains sources and phase information)
- Simple relationships are shown as direct arrows with labels
- The diagram flows top to bottom for better readability

The schema reveals a rich biomedical knowledge graph connecting drugs, diseases, genes, and locations with detailed metadata on each relationship.

```mermaid
classDiagram
direction TB

class Compound {
    FLOAT max_phase
    STRING name
    LIST synonyms
    LIST xrefs
    STRING identifier
    STRING smiles
    STRING standardized_smiles
    LIST sources
}

class Disease {
    STRING source
    STRING name
    LIST mesh_list
    STRING identifier
    STRING Linkout
    LIST omim_list
}

class Gene {
    STRING description
    STRING name
    STRING ensembl
    INTEGER identifier
}

class Location {
    STRING state
    STRING abbr
    STRING zipcode_type
    STRING code
    STRING type
    FLOAT Linkout
    STRING state_name
    LIST sources
    STRING county_fips
    STRING name
    STRING city_fips
    STRING iso3
    FLOAT longitude
    FLOAT latitude
    STRING identifier
    STRING state_fips
}

class Organism {
    STRING usa_isolation_country
    STRING biovar
    STRING strain
    STRING isolation_source
    STRING host_age
    STRING salinity
    STRING disease
    STRING antimicrobial_resistance
    LIST sources
    STRING level
    STRING name
    FLOAT genome_size
    STRING collection_date
    STRING isolation_country
    STRING pathovar
    STRING host_gender
    STRING host_is_human
    STRING temperature_range
    STRING host_name
    STRING has_amr_phenotype
    STRING sporulation
    STRING is_resistant
    STRING genbank_accessions
    STRING host_health
    STRING motility
    STRING serovar
    STRING oxygen_requirement
    STRING gram_stain
    STRING identifier
}

class SDoH {
    STRING topic
    FLOAT description
    STRING name
    STRING data_source
    STRING domain
    LIST mesh_ids
    STRING identifier
    LIST sources
}

class Environment {
    STRING name
    LIST synonyms
    STRING identifier
    LIST sources
}

class ASSOCIATES_SaD {
    Double enrichment
    String source
    Long cooccur
    Double fisher
    Double odds
}

class CONTRAINDICATES_CcD {
    StringArray sources
    StringArray act_sources
}

class FOUNDIN_CfL {
    StringArray date
    StringArray date_type
    StringArray unit
    StringArray sources
    StringArray year
    StringArray media
    StringArray metrics
    StringArray value
}

class FOUNDIN_EfL {
    StringArray unit
    StringArray metrics
    StringArray sources
    StringArray year
    StringArray value
}

class HASROLE_ChC {
    StringArray sources
}

class INTERACTS_CiC {
    StringArray sources
    String ddi_risk
    String description
}

class ISA_CiC {
    StringArray sources
}

class ISA_DiD {
    String source
}

class MORTALITY_DmL {
    String usability
    Long ghe_code
    StringArray sources
    Double value
    String mortality_per_100k
    String population
}

class PARTOF_CpC {
    StringArray sources
}

class PARTOF_LpL {
    StringArray sources
}

class PREVALENCEIN_SpL {
    StringArray sources
    LongArray year
    StringArray value
}

class PREVALENCE_DpL {
    String metric_name
    StringArray sources
    Double value
    Long year
    Double lower
    Double upper
}

class RESEMBLES_DrD {
    Double enrichment
    String source
    Long cooccur
    Double fisher
    Double odds
}

class RESPONDS_TO_OrC {
    StringArray measurement_value
    StringArray resistant_phenotype
    StringArray sources
    StringArray laboratory_typing_method
    StringArray vendor
    DoubleArray testing_standard_year
    StringArray measurement_unit
    StringArray laboratory_typing_platform
    StringArray measurement_sign
}

class TREATS_CtD {
    StringArray sources
    Long phase
    StringArray act_sources
}

class ISOLATEDIN_OiL {
    StringArray sources
}

Compound --> Gene : DOWNREGULATES_CdG
Compound --> Gene : UPREGULATES_CuG
Compound --> FOUNDIN_CfL
FOUNDIN_CfL --> Location
Compound --> CONTRAINDICATES_CcD
CONTRAINDICATES_CcD --> Disease
Compound --> PARTOF_CpC
PARTOF_CpC --> Compound
Compound --> TREATS_CtD
TREATS_CtD --> Disease
Compound --> ISA_CiC
ISA_CiC --> Compound
Compound --> HASROLE_ChC
HASROLE_ChC --> Compound
Compound --> INTERACTS_CiC
INTERACTS_CiC --> Compound

Disease --> MORTALITY_DmL
MORTALITY_DmL --> Location
Disease --> Disease : ISA_DiD
Disease --> PREVALENCE_DpL
PREVALENCE_DpL --> Location
Disease --> Gene : ASSOCIATES_DaG
Disease --> RESEMBLES_DrD
RESEMBLES_DrD --> Disease

Gene --> Disease : MARKER_POS_GmpD
Gene --> Disease : EXPRESSEDIN_GeiD
Gene --> Compound : RESPONSE_TO_mGrC
Gene --> Disease : MARKER_NEG_GmnD
Gene --> Compound : RESISTANT_TO_mGrC

Location --> PARTOF_LpL
PARTOF_LpL --> Location

Organism --> ISOLATEDIN_OiL
ISOLATEDIN_OiL --> Location
Organism --> RESPONDS_TO_OrC
RESPONDS_TO_OrC --> Compound

SDoH --> SDoH : ISA_SiS
SDoH --> ASSOCIATES_SaD
ASSOCIATES_SaD --> Disease
SDoH --> PREVALENCEIN_SpL
PREVALENCEIN_SpL --> Location

Environment --> Environment : ISA_EiE
Environment --> FOUNDIN_EfL
FOUNDIN_EfL --> Location
```

---

*Created by [mcp-genelab](https://github.com/sbl-sdsc/mcp-genelab) 0.4.0 on 2026-01-06*

*Model: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)*
