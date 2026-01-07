## API Reference

### Available Tools

#### `get_neo4j_schema`

Lists all nodes, their attributes, and their relationships to other nodes in the Neo4j database.

**Parameters:**
- None

**Returns:**
- JSON array containing node labels, their attributes (with data types), and relationships to other nodes

**Note:** If this fails with a message that includes "Neo.ClientError.Procedure.ProcedureNotFound", the APOC plugin needs to be installed and enabled on the Neo4j database.

#### `query`

Executes a read-only Cypher query on the Neo4j database.

**Parameters:**
- `query` (string, required): The Cypher query to execute
- `params` (object, optional): Parameters to pass to the Cypher query for parameterized queries

**Returns:**
- JSON object containing query results

**Example:**
```cypher
MATCH (s:Study)-[:PERFORMED_SpAS]->(a:Assay)
WHERE s.organism = $organism
RETURN s.name, a.name
LIMIT 10
```

**Note:** Only read queries (MATCH) are allowed. Write queries (MERGE, CREATE, SET, DELETE, REMOVE, ADD) will raise a ValueError.

#### `get_node_metadata`

Retrieves metadata descriptions for all node types from MetaNode nodes in the knowledge graph.

**Parameters:**
- None

**Returns:**
- JSON array containing detailed descriptions of each node type's properties, including data types and semantic meanings

#### `get_relationship_metadata`

Retrieves descriptions of properties for all relationship types in the knowledge graph.

**Parameters:**
- None

**Returns:**
- JSON array containing descriptions of each relationship type and their properties. Uses fallback approaches if MetaRelationship nodes are not available.

#### `find_differentially_expressed_genes`

Returns the top-N upregulated and downregulated genes for a given assay.

**Parameters:**
- `assay_id` (string, required): Assay identifier (e.g., 'OSD-253-6c5f9f37b9cb2ebeb2743875af4bdc86')
- `top_n` (integer, optional): Number of genes to return for each of up- and down-regulated lists, default: 5

**Returns:**
- Markdown-formatted table containing:
  - Top-N upregulated genes (log2fc > 0, sorted highest first)
  - Top-N downregulated genes (log2fc < 0, sorted lowest first)
  - Gene symbols, log2 fold changes, and adjusted p-values

#### `find_common_differentially_expressed_genes`

Finds common differentially expressed genes across multiple assays.

**Parameters:**
- `assay_ids` (array of strings, required): List of assay identifiers to compare (e.g., ['OSD-253-abc123', 'OSD-253-def456'])
- `log2fc_threshold` (number, optional): Log2 fold change threshold for filtering genes, default: 1.0 (represents 2-fold change)
- `adj_p_threshold` (number, optional): Adjusted p-value threshold for significance, default: 0.05 (max value: 0.1)

**Returns:**
- Markdown-formatted tables showing:
  - Common upregulated genes across all assays with log2fc values for each assay
  - Common downregulated genes across all assays with log2fc values for each assay

**Process:**
1. Gets ALL genes with |log2fc| > threshold and adj_p_value < adj_p_threshold for each assay
2. Performs inner join among upregulated genes and among downregulated genes
3. Returns genes that are differentially expressed in the same direction across all assays

#### `select_assays`

Interactive tool for selecting assays for a study, rendered in markdown format.

**Parameters:**
- `study_id` (string, optional): Study identifier (e.g., 'OSD-253')
- `selection` (string, optional): Comma-separated list of indices for selection (e.g., '1,2,3,4')

**Returns:**
- **First call** (selection=None): 
  - Prompts for study_id if missing
  - Returns numbered menu as markdown table showing unique factor combinations across all assays
- **Second call** (with selection): 
  - Pairs consecutive indices: (i,j), (k,l), ..., (m,n)
  - Returns assay_id(s) for each pair comparison
  - Must provide an even number of indices

**Usage Pattern:**
1. Call without parameters to see available factor combinations
2. Select pairs of conditions to compare
3. Use returned assay_ids with other tools

**Suggested Next Steps:**
- For single pair: Find differentially expressed genes, create volcano plot, map genes to pathways
- For multiple pairs: Find differentially expressed genes for each comparison, create volcano plots, identify consistent changes, map genes to pathways
- For < 4 pairs: Create Venn diagram to show overlap

#### `create_volcano_plot`

Creates a volcano plot for differential gene expression data from a given assay.

**Parameters:**
- `assay_id` (string, required): Assay identifier (e.g., 'OSD-253-6c5f9f37b9cb2ebeb2743875af4bdc86')
- `log2fc_threshold` (number, optional): Log2 fold change threshold for highlighting significant genes, default: 1.0
- `adj_p_threshold` (number, optional): Adjusted p-value threshold for significance, default: 0.05
- `top_n` (integer, optional): How many significant genes to label in the plot, default: 20
- `figsize_width` (integer, optional): Figure width in inches, default: 8
- `figsize_height` (integer, optional): Figure height in inches, default: 5

**Returns:**
- File path of generated volcano plot image saved to Downloads directory (or /mnt/user-data/outputs in Claude.ai environment)
- Markdown-formatted summary with:
  - Study information
  - Factor comparison details
  - Thresholds used
  - Count statistics for significant genes (total, upregulated, downregulated, not significant)

**Visualization:**
- X-axis: log2 fold change
- Y-axis: -log10(adjusted p-value)
- Color coding:
  - Red: upregulated genes (log2fc > threshold, adj_p < threshold)
  - Blue: downregulated genes (log2fc < -threshold, adj_p < threshold)
  - Gray: not significant
- Top N significant genes are labeled with gene symbols

#### `create_venn_diagram`

Creates Venn diagrams comparing differentially expressed genes between 2 or 3 assays.

**Parameters:**
- `assay_id_1` (string, required): First assay identifier (e.g., 'OSD-511-53054e738e335bc645cb620c95916e5f')
- `assay_id_2` (string, required): Second assay identifier (e.g., 'OSD-511-8974299195d78d74d7f3f085f2b48981')
- `assay_id_3` (string, optional): Third assay identifier for 3-way Venn diagram
- `log2fc_threshold` (number, optional): Log2 fold change threshold for filtering genes, default: 1.0
- `figsize_width` (integer, optional): Figure width in inches, default: 10
- `figsize_height` (integer, optional): Figure height in inches, default: 6

**Returns:**
- File path of generated Venn diagram image saved to Downloads directory (or /mnt/user-data/outputs in Claude.ai environment)
- Markdown-formatted summary with:
  - Study information
  - Assay comparisons (factor combinations)
  - Overlap statistics for upregulated genes
  - Overlap statistics for downregulated genes

**Visualization:**
- Side-by-side Venn diagrams:
  - Left: Upregulated genes (log2fc > threshold)
  - Right: Downregulated genes (log2fc < -threshold)
- Supports 2-way or 3-way comparisons
- Color-coded assay legends with factor information
- Consistent color scheme across diagrams:
  - Assay 1: Light red
  - Assay 2: Light blue
  - Assay 3 (if applicable): Light green
  - Overlaps: Blended colors

**Statistics Returned:**
- For 2-way: Only in Assay 1, only in Assay 2, common to both
- For 3-way: Only in each assay, pairwise overlaps, all three overlaps, totals per assay

#### `clean_mermaid_diagram`

Cleans a Mermaid class diagram by removing unwanted elements.

**Parameters:**
- `mermaid_content` (string, required): The raw Mermaid class diagram content

**Returns:**
- Cleaned Mermaid content with unwanted elements removed

**Cleaning Operations:**
- Removes all note statements that would render as unreadable yellow boxes
- Removes empty curly braces from class definitions
- Truncates strings after newline characters (e.g., "ClassName\nextra" becomes "ClassName")
- Removes vertical bars (|) which are not allowed in class diagrams

**Use Case:**
- Use this tool to clean up Mermaid diagrams before rendering to ensure proper visualization

#### `create_chat_transcript`

Provides a prompt template for creating a chat transcript in markdown format.

**Parameters:**
- None

**Returns:**
- Markdown template for documenting conversations with user prompts and assistant responses

**Template Structure:**
```markdown
## Chat Transcript
<Title>

👤 **User**  
<prompt>

---

🧠 **Assistant**  
<entire text response goes here>

*Created by mcp-genelab {version} using {model_string} on {date}*
```

#### `visualize_schema`

Provides a prompt for visualizing the knowledge graph schema using a Mermaid class diagram.

**Parameters:**
- None

**Returns:**
- Detailed instructions for creating a Mermaid class diagram visualization of the knowledge graph schema

**Workflow:**
1. Call `get_neo4j_schema()` to retrieve classes and predicates
2. Generate raw Mermaid class diagram showing nodes, properties, and relationships
3. Set diagram direction to TB (top-to-bottom)
4. Pass diagram through `clean_mermaid_diagram` tool
5. Present cleaned diagram inline in a mermaid code block
6. Create .mermaid file with only the cleaned diagram code (no markdown fences)
7. Save to user's Downloads directory
8. Use `present_files` tool to share the .mermaid file for rendering

**Requirements:**
- The .mermaid file must contain ONLY the Mermaid diagram code
- No markdown code fences in the .mermaid file
- No explanatory text in the .mermaid file
- File should start with "classDiagram"
