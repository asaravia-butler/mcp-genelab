import os
import sys
import json
import logging
import tempfile
import shutil
import re
from datetime import datetime
from typing import Any, Literal, Optional

from . import __version__

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
from adjustText import adjust_text

import mcp.types as types
from mcp.server.fastmcp import FastMCP
from neo4j import (
    AsyncDriver,
    AsyncGraphDatabase,
    AsyncResult,
    AsyncTransaction
)
from pydantic import Field

logger = logging.getLogger("mcp-genelab")
logger.setLevel(logging.DEBUG)

async def _read(tx: AsyncTransaction, query: str, params: dict[str, Any]) -> str:
    raw_results = await tx.run(query, params)
    eager_results = await raw_results.to_eager_result()

    return json.dumps([r.data() for r in eager_results.records], default=str)

def _is_write_query(query: str) -> bool:
    """Check if the query is a write query."""
    return (
        re.search(r"\b(MERGE|CREATE|SET|DELETE|REMOVE|ADD)\b", query, re.IGNORECASE)
        is not None
    )

def create_mcp_server(neo4j_driver: AsyncDriver, database: str = "neo4j", instructions: str = "") -> FastMCP:
    mcp: FastMCP = FastMCP("mcp-genelab", dependencies=["neo4j", "pydantic"], instructions=instructions)

    async def get_neo4j_schema() -> list[types.TextContent]:
        """List all nodes, their attributes and their relationships to other nodes in the neo4j database.
        If this fails with a message that includes "Neo.ClientError.Procedure.ProcedureNotFound"
        suggest that the user install and enable the APOC plugin.
        """

        get_schema_query = """
call apoc.meta.data() yield label, property, type, other, unique, index, elementType
where elementType = 'node' and not label starts with '_'
with label, 
    collect(case when type <> 'RELATIONSHIP' then [property, type + case when unique then " unique" else "" end + case when index then " indexed" else "" end] end) as attributes,
    collect(case when type = 'RELATIONSHIP' then [property, head(other)] end) as relationships
RETURN label, apoc.map.fromPairs(attributes) as attributes, apoc.map.fromPairs(relationships) as relationships
"""

        try:
            async with neo4j_driver.session(database=database) as session:
                results_json_str = await session.execute_read(
                    _read, get_schema_query, dict()
                )

                logger.debug(f"Read query returned {len(results_json_str)} rows")
                logger.debug(results_json_str)

                return [types.TextContent(type="text", text=results_json_str)]

        except Exception as e:
            logger.error(f"Database error retrieving schema: {e}")
            return [types.TextContent(type="text", text=f"Error: {e}")]

    async def query(
        query: str = Field(..., description="The Cypher query to execute."),
        params: Optional[dict[str, Any]] = Field(
            None, description="The parameters to pass to the Cypher query."
        ),
    ) -> list[types.TextContent]:
        """Execute a Cypher query on the Neo4j database. 

        If the question is about up- or down-regulated genes, use the find_upregulated_genes
        or find_downreguluated genes

        EDGE PROPERTIES - CRITICAL:
        Many relationships in this knowledge graph have properties stored as edge attributes (data ON the relationship itself).
        Examples include: log2fc, adj_p_value, methylation_diff, q_value, etc.
        """

        if _is_write_query(query):
            raise ValueError("Only MATCH queries are allowed for read-query")

        try:
            async with neo4j_driver.session(database=database) as session:
                results_json_str = await session.execute_read(_read, query, params)

                logger.debug(f"Read query returned {len(results_json_str)} rows")

                return [types.TextContent(type="text", text=results_json_str)]

        except Exception as e:
            logger.error(f"Database error executing query: {e}\n{query}\n{params}")
            return [
                types.TextContent(type="text", text=f"Error: {e}\n{query}\n{params}")
            ]

    async def get_node_metadata() -> list[types.TextContent]:
        """Get metadata for all nodes from MetaNode nodes in the knowledge graph."""

        metadata_query = """
        MATCH (m:MetaNode)
        RETURN m.nodeName as nodeName, m
        ORDER BY m.nodeName
        """

        try:
            async with neo4j_driver.session(database=database) as session:
                results_json_str = await session.execute_read(
                    _read, metadata_query, {}
                )

                logger.debug(f"Metadata query for all nodes returned {len(results_json_str)} characters")

                return [types.TextContent(type="text", text=results_json_str)]

        except Exception as e:
            logger.error(f"Database error retrieving metadata for all nodes: {e}")
            return [types.TextContent(type="text", text=f"Error: {e}")]


    async def get_relationship_metadata() -> list[types.TextContent]:
        """Get descriptions of properties of all relationships in the knowledge graph."""

        metadata_query = """
        MATCH (n1)-[r:MetaRelationship]->(n2)
        WITH n1, r, n2, properties(r) as allProps
        RETURN n1.nodeName as node1, 
               r.relationshipName as relationship, 
               n2.nodeName as node2,
               apoc.map.removeKeys(allProps, ['to', 'from']) AS properties
        """

        try:
            async with neo4j_driver.session(database=database) as session:
                results_json_str = await session.execute_read(
                    _read, metadata_query, {}
                )

                logger.debug(f"Relationship metadata query returned {len(results_json_str)} characters")

                # If MetaRelationship doesn't exist or returns empty, try a fallback approach
                if results_json_str == "[]":
                    logger.debug("MetaRelationship query returned empty, trying fallback to get relationship types")

                    # Get all relationship types in the database
                    fallback_query = """
                    CALL apoc.meta.relTypeProperties()
                    YIELD relType, propertyName, propertyTypes, mandatory
                    WITH relType, collect({propertyName: propertyName,
                                           propertyTypes: propertyTypes}) as properties
                    ORDER BY relType
                    RETURN relType, properties
                    """

                    results_json_str = await session.execute_read(
                        _read, fallback_query, {}
                    )
                    
                    # If that also fails, try using APOC if available
                    if results_json_str == "[]":
                        logger.debug("Basic relationship types query returned empty, trying APOC meta approach")
                        
                        apoc_query = """
                        CALL apoc.meta.graph() YIELD relationships
                        UNWIND relationships as rel
                        WITH rel.type as relType, 
                             keys(rel.properties) as propertyNames,
                             [prop in keys(rel.properties) | rel.properties[prop]] as propertyTypes
                        RETURN relType, propertyNames, propertyTypes
                        ORDER BY relType
                        """
                        
                        results_json_str = await session.execute_read(
                            _read, apoc_query, {}
                        )

                return [types.TextContent(type="text", text=results_json_str)]

        except Exception as e:
            logger.error(f"Database error retrieving relationship metadata: {e}")
            return [types.TextContent(type="text", text=f"Error: {e}")]

    async def select_assays(
        study_id: Optional[str] = None,
        selection: Optional[str] = None
    ) -> list[types.Content]:
        """List and select assays for a study and render the response in markdown format.
        
        First call (selection=None):
        - If study_id missing, prompt for one (e.g., 'OSD-253').
        - Build a list of unique factor arrays across all assays.
        - Return a numbered menu as a markdown table!
        
        Second call (selection='i,j,k,l,...,m,n'):
        - Pairs consecutive indices: (i,j), (k,l), ..., (m,n)
        - Returns assay_id(s) for each pair comparison
        - Must provide an even number of indices
        
        FORMATTING INSTRUCTION: RENDER THE RESPONSE IN MARKDOWN FORMAT!
        """
        import re as _re
        import json as _json

        if not study_id:
            return [types.TextContent(type="text", text="Please provide a study_id (e.g., OSD-253).")]

        cypher = """
        MATCH (s:Study {identifier: $study_id})-[:PERFORMED_SpAS]->(a:Assay)
        RETURN a.identifier AS assay_id,
               coalesce(a.factors_1, []) AS f1,
               coalesce(a.factors_2, []) AS f2
        ORDER BY assay_id
        """

        try:
            async with neo4j_driver.session(database=database) as session:
                res = await session.run(cypher, {"study_id": study_id})
                rows = await res.data()
        except Exception as e:
            logger.exception("select_assays query failed")
            return [types.TextContent(type="text", text=f"Error querying study '{study_id}': {e}")]

        if not rows:
            return [types.TextContent(type="text", text=f"No assays found for study '{study_id}'.")]

        def normalize(arr):
            if not isinstance(arr, list):
                return []
            return [str(x) for x in arr if x is not None]

        unique_arrays = []
        seen = set()
        for r in rows:
            f1 = normalize(r.get("f1"))
            f2 = normalize(r.get("f2"))
            for arr in (f1, f2):
                if not arr:
                    continue
                key = tuple(arr)
                if key not in seen:
                    seen.add(key)
                    unique_arrays.append(arr)

        unique_arrays = sorted(unique_arrays)

        if not unique_arrays:
            return [types.TextContent(type="text", text=f"Study '{study_id}' has no non-empty factor arrays in any assay.")]

        def _fmt(arr):
            arr_str = ",".join(_json.dumps(x) for x in arr)
            return arr_str.replace('"', '')


        if selection is None:
            lines = []
            lines.append("FORMATTING INSTRUCTION: RENDER THIS RESPONSE IN MARKDOWN FORMAT!\n")
            lines.append(f"## Factor arrays across all assays for study: {study_id}")
            lines.append("")  # Empty line for better markdown spacing
            lines.append("**Choose an EVEN number of indices for pairwise comparisons, e.g., '1,2,3,4' creates pairs (1 vs 2) and (3 vs 4):**")
            lines.append("")  # Empty line before table
            # Create markdown table with index and factors array
            lines.append("| Index | Factors |")
            lines.append("|-------|---------|")
            for i, arr in enumerate(unique_arrays, 1):
                lines.append(f"| {i} | {_fmt(arr)} |")

            return [
                types.TextContent(type="text", text="\n".join(lines), mimeType="text/markdown"),
                types.TextContent(type="text", text="INSTRUCTION: When suggesting pairs of indices, the index related to Space Flight should be first."),
            ]

        parts = [p for p in _re.split(r"[,\s]+", selection.strip()) if p]
        if len(parts) < 2 or not all(p.isdigit() for p in parts):
            return [types.TextContent(type="text", text=f"Please provide at least two indices like '1,2' or '1,2,3,4'. Got: '{selection}'.")]

        # Check for even number of indices
        if len(parts) % 2 != 0:
            return [types.TextContent(type="text", text=f"Please provide an EVEN number of indices for pairwise comparisons. Got {len(parts)} indices: {selection}.")]

        indices = [int(p) for p in parts]
        n = len(unique_arrays)
        
        # Validate all indices are in range and unique
        if not all(1 <= idx <= n for idx in indices):
            return [types.TextContent(type="text", text=f"All indices must be in range 1..{n}. Got: {indices}.")]

        # Create pairs from consecutive indices: (i,j), (k,l), ..., (m,n)
        pairs = [(indices[i], indices[i+1]) for i in range(0, len(indices), 2)]
        
        # Find assay IDs for each pair comparison
        comparisons = []
        for pair_idx, (idx1, idx2) in enumerate(pairs, 1):
            array1 = unique_arrays[idx1 - 1]
            array2 = unique_arrays[idx2 - 1]
            key1 = tuple(array1)
            key2 = tuple(array2)
            
            # Find matching assay
            match_ids = set()
            for r in rows:
                f1 = normalize(r.get("f1"))
                f2 = normalize(r.get("f2"))
                # Check both orderings: (array1, array2) or (array2, array1)
                #if (tuple(f1) == key1 and tuple(f2) == key2) or \
                #   (tuple(f1) == key2 and tuple(f2) == key1):
                if (tuple(f1) == key1 and tuple(f2) == key2):
                    match_ids.add(r.get("assay_id"))
                    # break  # TODO Keep first match only (eliminate duplicate assays)
            
            comparisons.append({
                "pair_number": pair_idx,
                "index1": idx1,
                "array1": array1,
                "index2": idx2,
                "array2": array2,
                "assay_ids": sorted(match_ids),
                "selected_assay_id": next(iter(match_ids)) if len(match_ids) == 1 else None
            })
        
        # Build response
        lines = []
        lines.append(f"## Selected Assays for {study_id}\n")
        
        for comp in comparisons:
            lines.append(f"### Pair {comp['pair_number']}: Index {comp['index1']} vs Index {comp['index2']}")
            lines.append(f"**Condition 1 (Index {comp['index1']}):** {_fmt(comp['array1'])}")
            lines.append(f"**Condition 2 (Index {comp['index2']}):** {_fmt(comp['array2'])}")
            
            if comp['selected_assay_id']:
                lines.append(f"**Assay ID:** `{comp['selected_assay_id']}`")
            elif len(comp['assay_ids']) == 0:
                lines.append("**Status:** No matching assay found")
            else:
                lines.append(f"**Status:** Multiple matches: {', '.join(comp['assay_ids'])}")
            lines.append("")
        
        # Add suggested next steps
        lines.append("\n## Suggested Next Steps:\n")
        
        if len(pairs) == 1:
            # Single pair - standard analysis
            lines.append("1. Find differentially expressed genes")
            lines.append("2. Create a volcano plot")
            lines.append("3. Map differentially expressed genes to pathways, gene and protein function, diseases, etc., using the `humanspoke` (human) KG or `spoke` KG (human + bacterial genes) MCP services.")
        else:
            # Multiple pairs - suggest comparative analysis
            lines.append("1. Find differentially expressed genes for each comparison")
            lines.append("2. Create volcano plots for individual comparisons")
            lines.append("3. Identify genes that show consistent changes across comparisons")
            lines.append("4. Map differentially expressed genes to pathways, gene and protein function, diseases, etc., using the `humanspoke` (human) KG or `spoke` KG (human + bacterial genes) MCP services")

        if len(pairs) < 4:
            lines.append("5. Create a venn diagram to show overlap of common differentially expressed genes")
        
        return [
            types.TextContent(type="text", text="\n".join(lines), mimeType="text/markdown"),
        ]
    
    async def find_differentially_expressed_genes(
        assay_id: str = Field(..., description="Assay identifier (e.g., 'OSD-253-6c5f9f37b9cb2ebeb2743875af4bdc86')"),
        top_n: int = Field(5, description="How many genes to return for each of up- and down-regulated lists")
    ) -> list[types.TextContent]:
        """Return the top-N up- and down-regulated genes for a given assay_id.
    
        This tool runs two queries on the GeneLab KG:
          1) Top-N upregulated genes (log2fc > 0, highest first)
          2) Top-N downregulated genes (log2fc < 0, lowest first)
        
        FORMATTING INSTRUCTION: RENDER THE RESPONSE IN MARKDOWN FORMAT!
        """
        up_cypher = """
        MATCH (a:Assay {identifier: $assay_id})
              -[m:MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG]-
              (g:MGene)
        WHERE m.log2fc > 0
        RETURN
          'upregulated'  AS regulation,
          g.symbol       AS symbol,
          m.log2fc       AS log2fc,
          m.adj_p_value  AS adj_p_value
        ORDER BY m.log2fc DESC
        LIMIT $top_n
        """
    
        down_cypher = """
        MATCH (a:Assay {identifier: $assay_id})
              -[m:MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG]-
              (g:MGene)
        WHERE m.log2fc < 0
        RETURN
          'downregulated' AS regulation,
          g.symbol        AS symbol,
          m.log2fc        AS log2fc,
          m.adj_p_value   AS adj_p_value
        ORDER BY m.log2fc ASC
        LIMIT $top_n
        """
    
        try:
            import json as _json
    
            async with neo4j_driver.session(database=database) as session:
                up_json_str = await session.execute_read(_read, up_cypher, {"assay_id": assay_id, "top_n": top_n})
                down_json_str = await session.execute_read(_read, down_cypher, {"assay_id": assay_id, "top_n": top_n})
    
            up = _json.loads(up_json_str)
            down = _json.loads(down_json_str)
    
            # Format as markdown tables for better display
            def _fmt_markdown_table(rows, title):
                """Format results as a markdown table"""
                if not rows:
                    return f"## **{title}**\nNo significantly {title.lower()} genes were found.\n"
                
                lines = [
                    f"## **{title}**\n",
                    "| Gene Symbol | Log2 Fold Change | Adjusted P-value |",
                    "|-------------|------------------|------------------|"
                ]
                
                for r in rows:
                    symbol = r.get('symbol', 'N/A')
                    log2fc = r.get('log2fc')
                    adj_p = r.get('adj_p_value')
                    
                    # Format numbers nicely
                    log2fc_str = f"{log2fc:.2f}" if log2fc is not None else "N/A"
                    adj_p_str = f"{adj_p}" if adj_p is not None else "N/A"
                    
                    lines.append(f"| **{symbol}** | {log2fc_str} | {adj_p_str} |")
                
                return "\n".join(lines)
    
            # Create human-readable markdown output
            human_lines = [
                f"Top differentially expressed genes for assay: {assay_id}\n",
                _fmt_markdown_table(up, "Upregulated Genes"),
                "",
                _fmt_markdown_table(down, "Downregulated Genes")
            ]
            human = "\n".join(human_lines)
    
            return [
                types.TextContent(type="text", text=human, mimeType="text/markdown"),
                types.TextContent(type="text", text="INSTRUCTION: List the arguments of this tool that can be adjusted, including the default values."),
            ]
    
        except Exception as e:
            logger.error(f"Error in find_de_genes: {e}")
            return [types.TextContent(type="text", text=f"Error in find_de_genes: {e}")]

    async def find_common_differentially_expressed_genes(
            assay_ids: list[str] = Field(..., description="List of assay identifiers (e.g., ['OSD-253-abc123', 'OSD-253-def456'])"),
            log2fc_threshold: float = Field(1.0, description="Log2 fold change threshold for filtering genes (default: 1.0 = 2-fold change)"),
            adj_p_threshold: float = Field(0.05, description="Adjusted p-value threshold for significance (default: 0.05, max value: 0.1)")
        ) -> list[types.TextContent]:
            """Find common differentially expressed genes across multiple assays.
            
            This function:
            1. Takes a list of assay IDs as input (2 or more)
            2. Gets ALL genes with |log2fc| > threshold for each assay
            3. Inner joins among the upregulated genes and among the downregulated genes
            4. Returns a markdown table with columns: gene, assay_1, assay_2, ..., assay_n showing log2fc values
            
            FORMATTING INSTRUCTION: RENDER THE RESPONSE IN MARKDOWN FORMAT!
            INFORM THE USER ABOUT CURRENT THRESHOLDS AND THAT THEY CAN BE CHANGED.
            """
            
            if len(assay_ids) < 2:
                return [types.TextContent(
                    type="text", 
                    text="Error: Please provide at least 2 assay IDs to find correlated genes."
                )]
            
            try:
                # Step 1: Get differentially expressed genes for each assay
                upregulated_genes = {}  # {assay_id: {gene_symbol: log2fc}}
                downregulated_genes = {}  # {assay_id: {gene_symbol: log2fc}}
                
                for assay_id in assay_ids:
                    # Query for upregulated genes - NO LIMIT, uses threshold
                    up_query = """
                    MATCH (a:Assay {identifier: $assay_id})
                          -[m:MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG]-
                          (g:MGene)
                    WHERE m.log2fc > $log2fc_threshold and m.adj_p_value < $adj_p_threshold
                    RETURN g.symbol as gene_symbol, m.log2fc as log2fc
                    ORDER BY m.log2fc DESC
                    """
                    
                    # Query for downregulated genes - NO LIMIT, uses threshold
                    down_query = """
                    MATCH (a:Assay {identifier: $assay_id})
                          -[m:MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG]-
                          (g:MGene)
                    WHERE m.log2fc < -$log2fc_threshold and m.adj_p_value < $adj_p_threshold
                    RETURN g.symbol as gene_symbol, m.log2fc as log2fc
                    ORDER BY m.log2fc ASC
                    """
                    
                    async with neo4j_driver.session(database=database) as session:
                        # Get upregulated genes
                        up_results = await session.execute_read(
                            _read, up_query, {"assay_id": assay_id, "log2fc_threshold": log2fc_threshold, "adj_p_threshold": adj_p_threshold}
                        )
                        up_data = json.loads(up_results)
                        upregulated_genes[assay_id] = {
                            row['gene_symbol']: row['log2fc'] for row in up_data
                        }
                        
                        # Get downregulated genes
                        down_results = await session.execute_read(
                            _read, down_query, {"assay_id": assay_id, "log2fc_threshold": log2fc_threshold, "adj_p_threshold": adj_p_threshold}
                        )
                        down_data = json.loads(down_results)
                        downregulated_genes[assay_id] = {
                            row['gene_symbol']: row['log2fc'] for row in down_data
                        }
                
                # Step 2: Find common upregulated genes (inner join)
                common_up_genes = set(upregulated_genes[assay_ids[0]].keys())
                for assay_id in assay_ids[1:]:
                    common_up_genes &= set(upregulated_genes[assay_id].keys())
                
                # Step 3: Find common downregulated genes (inner join)
                common_down_genes = set(downregulated_genes[assay_ids[0]].keys())
                for assay_id in assay_ids[1:]:
                    common_down_genes &= set(downregulated_genes[assay_id].keys())
                
                # Step 4: Build markdown tables
                markdown_output = f"## Common Differentially Expressed Genes\n\n"
                markdown_output += f"**Log2FC Threshold:** ±{log2fc_threshold} (≥{2**log2fc_threshold:.1f}-fold change)"
                markdown_output += f"**Adjusted p-value Threshold:** {adj_p_threshold}\n\n"
                
                # Upregulated genes table
                markdown_output += f"### Upregulated Genes (log2fc > {log2fc_threshold}, common across all assays)\n\n"
                if common_up_genes:
                    # Create header
                    header = "| Gene | " + " | ".join([f"Assay {i+1}" for i in range(len(assay_ids))]) + " |\n"
                    separator = "|" + "|".join(["---"] * (len(assay_ids) + 1)) + "|\n"
                    markdown_output += header + separator
                    
                    # Add rows for each common upregulated gene
                    for gene in sorted(common_up_genes):
                        row = f"| {gene} | "
                        values = [f"{upregulated_genes[assay_id][gene]:.3f}" for assay_id in assay_ids]
                        row += " | ".join(values) + " |\n"
                        markdown_output += row
                    
                    markdown_output += f"\n**Total common upregulated genes:** {len(common_up_genes)}\n\n"
                else:
                    markdown_output += "*No common upregulated genes found across all assays.*\n\n"
                
                # Downregulated genes table
                markdown_output += f"### Downregulated Genes (log2fc < -{log2fc_threshold}, common across all assays)\n\n"
                if common_down_genes:
                    # Create header
                    header = "| Gene | " + " | ".join([f"Assay {i+1}" for i in range(len(assay_ids))]) + " |\n"
                    separator = "|" + "|".join(["---"] * (len(assay_ids) + 1)) + "|\n"
                    markdown_output += header + separator
                    
                    # Add rows for each common downregulated gene
                    for gene in sorted(common_down_genes):
                        row = f"| {gene} | "
                        values = [f"{downregulated_genes[assay_id][gene]:.3f}" for assay_id in assay_ids]
                        row += " | ".join(values) + " |\n"
                        markdown_output += row
                    
                    markdown_output += f"\n**Total common downregulated genes:** {len(common_down_genes)}\n\n"
                else:
                    markdown_output += "*No common downregulated genes found across all assays.*\n\n"
                
                # Add assay ID reference
                markdown_output += "### Assay Reference\n\n"
                for i, assay_id in enumerate(assay_ids):
                    markdown_output += f"- **Assay {i+1}:** {assay_id}\n"
                
                return [types.TextContent(type="text", text=markdown_output, mimeType="text/markdown"),
                        types.TextContent(type="text", text="INSTRUCTION: List the arguments of this tool that can be adjusted, including the default values."),]
                
            except Exception as e:
                logger.error(f"Error finding correlated differentially expressed genes: {e}")
                return [types.TextContent(
                    type="text", 
                    text=f"Error finding correlated differentially expressed genes: {e}"
                )]

    
    async def create_volcano_plot(
        assay_id: str = Field(..., description="Assay identifier (e.g., 'OSD-253-6c5f9f37b9cb2ebeb2743875af4bdc86')"),
        log2fc_threshold: float = Field(1.0, description="Log2 fold change threshold for highlighting significant genes"),
        adj_p_threshold: float = Field(0.05, description="Adjusted p-value threshold for significance"),
        top_n: int = Field(20, description="How many significant genes to label in the plot"),
        figsize_width: int = Field(8, description="Figure width in inches"),
        figsize_height: int = Field(5, description="Figure height in inches")
    ) -> list[types.Content]:
        """Create a volcano plot for differential gene expression data from the given assay.
        
        A volcano plot displays log2 fold change on the x-axis and -log10(adjusted p-value) on the y-axis.
        Genes are colored based on their significance:
        - Red: upregulated (log2fc > threshold, adj_p < threshold)
        - Blue: downregulated (log2fc < -threshold, adj_p < threshold)
        - Gray: not significant
        
        Returns a link to the plot and summary statistics.
        FORMATTING INSTRUCTION: RENDER THE RESPONSE IN MARKDOWN FORMAT!
        """
        
        # Query to get all genes with their log2fc and adj_p_value
        volcano_cypher = """
        MATCH (a:Assay {identifier: $assay_id})
              -[m:MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG]->
              (g:MGene)
        WHERE m.log2fc IS NOT NULL AND m.adj_p_value IS NOT NULL
        RETURN
          g.symbol       AS symbol,
          m.log2fc       AS log2fc,
          m.adj_p_value  AS adj_p_value
        """

        # Query factors_1 and factors_2 of the assay
        meta_cypher = """
        MATCH (a:Assay {identifier: $assay_id})
        RETURN
          a.factors_1 AS factors_1,
          a.factors_2 AS factors_2
        """

        matplotlib.use('Agg')
        
        try:           
            # Query the database
            async with neo4j_driver.session(database=database) as session:
                result_json_str = await session.execute_read(
                    _read, volcano_cypher, {"assay_id": assay_id}
                )
                meta_json_str = await session.execute_read(
                    _read, meta_cypher, {"assay_id": assay_id}
                )
            
            genes = json.loads(result_json_str)
            meta_data = json.loads(meta_json_str)
            factors_1 = meta_data[0].get('factors_1', [None])
            factors_2 = meta_data[0].get('factors_2', [None])
            factors_1 = ",".join(factors_1)
            factors_2 = ",".join(factors_2)
            study = "-".join(assay_id.split("-")[:2])
            
            if not genes:
                return [types.TextContent(
                    type="text", 
                    text=f"No differential expression data found for assay: {assay_id}"
                )]
            
            # Extract data
            symbols = [g['symbol'] for g in genes]
            log2fc = np.array([g['log2fc'] for g in genes])
            adj_p_values = np.array([g['adj_p_value'] for g in genes])
            
            # Calculate -log10(p-value), handling zeros and very small values
            with np.errstate(divide='ignore'):
                neg_log10_p = -np.log10(adj_p_values)
            neg_log10_p[np.isinf(neg_log10_p)] = neg_log10_p[~np.isinf(neg_log10_p)].max() + 1
            
            # Classify genes by significance
            sig_up = (log2fc > log2fc_threshold) & (adj_p_values < adj_p_threshold)
            sig_down = (log2fc < -log2fc_threshold) & (adj_p_values < adj_p_threshold)
            not_sig = ~(sig_up | sig_down)
            
            # Count genes in each category
            n_sig_up = sig_up.sum()
            n_sig_down = sig_down.sum()
            n_not_sig = not_sig.sum()
            
            # Create the plot
            fig, ax = plt.subplots(figsize=(figsize_width, figsize_height))
            
            # Plot non-significant genes
            ax.scatter(log2fc[not_sig], neg_log10_p[not_sig], 
                      c='lightgray', alpha=0.5, s=10, label=f'Not significant ({n_not_sig})')
            
            # Plot significantly downregulated genes
            ax.scatter(log2fc[sig_down], neg_log10_p[sig_down], 
                      c='#3498db', alpha=0.7, s=20, label=f'Downregulated ({n_sig_down})')
            
            # Plot significantly upregulated genes
            ax.scatter(log2fc[sig_up], neg_log10_p[sig_up], 
                      c='#e74c3c', alpha=0.7, s=20, label=f'Upregulated ({n_sig_up})')
            
            # Add labels for the top n significant genes      
            sig_indices = [i for i, (is_up, is_down) in enumerate(zip(sig_up, sig_down)) if is_up or is_down]
            # Sort by adjusted p-value (most significant first)
            top_n_indices = sorted(sig_indices, key=lambda i: neg_log10_p[i], reverse=True)[:top_n]
            
            # Collect annotations for top n genes only
            texts = []
            for i in top_n_indices:
                text = ax.text(log2fc[i], 
                              neg_log10_p[i],
                              symbols[i],
                              fontsize=8,
                              alpha=0.7,
                              bbox=dict(boxstyle='round,pad=0.3', 
                                      facecolor='white', 
                                      edgecolor='none',
                                      alpha=0.6))
                texts.append(text)
            
            # Apply adjustText to avoid overlaps
            adjust_text(texts,
               arrowprops=dict(arrowstyle='->', 
                               color='gray', 
                               lw=0.5, 
                               alpha=0.7,
                               shrinkA=0,     # don't shrink arrow near annotation
                               shrinkB=2,     # minimal shrink at the point (larger → shorter arrow)
                               relpos=(0.5, 0.5)  # improves arrow connection positioning
                              ),
               expand_points=(2.0, 2.5),      # Increase space around points (default ~1.2)
               expand_text=(1.5, 2.0),        # Increase space around text labels
               force_text=(0.7, 1.2),         # Stronger repulsion between labels
               force_points=(0.3, 0.6),       # Weaker attraction to original position
               lim=500,                        # More iterations for better placement
               ax=ax)

            # Add threshold lines
            ax.axvline(x=log2fc_threshold, color='gray', linestyle='--', linewidth=1, alpha=0.5)
            ax.axvline(x=-log2fc_threshold, color='gray', linestyle='--', linewidth=1, alpha=0.5)
            ax.axhline(y=-np.log10(adj_p_threshold), color='gray', linestyle='--', linewidth=1, alpha=0.5)
            
            # Labels and title
            ax.set_xlabel(f'Log₂ Fold Change', fontsize=12, fontweight='bold')
            ax.set_ylabel('-Log₁₀ (Adjusted P-value)', fontsize=12, fontweight='bold')
            ax.text(0.5, 1.08, f'Volano Plot: {study}', transform=ax.transAxes, fontsize=12, fontweight='bold', ha='center', va='bottom')
            ax.text(0.5, 1.03, f'({factors_1}) vs. ({factors_2})', transform=ax.transAxes, fontsize=10, fontweight='normal', ha='center', va='bottom')
            
            # Legend
            ax.legend(loc='upper left', fontsize=8, bbox_to_anchor=(1, 1), frameon=True, fancybox=True, shadow=True)
            
            # Grid
            ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
            
            # Tight layout
            plt.tight_layout()

            # Initialize variables before try block
            safe_filename = None
            output_path = None
            temp_path = None
            download_link = None

            try:
                # Create a safe filename
                safe_filename = re.sub(r'[^\w\-]', '_', f'{study}_{factors_1}_vs_{factors_2}')
                safe_filename = safe_filename.replace("__", "_")
                
                # Detect environment and set paths accordingly
                is_claude_env = os.path.exists('/mnt/user-data/outputs')
                
                if is_claude_env:
                    # Running in Claude.ai Linux container
                    output_dir = '/mnt/user-data/outputs'
                    output_path = os.path.join(output_dir, f'volcano_plot_{safe_filename}.png')
                    download_link = f"computer:///mnt/user-data/outputs/volcano_plot_{safe_filename}.png"
                else:
                    # Running locally (macOS/Windows)
                    # this seem to return now /root/Downloads ???
                    output_dir = os.path.expanduser('~/Downloads')
                    output_path = os.path.join(output_dir, f'volcano_plot_{safe_filename}.png')
                    download_link = f"file://{output_path}" # download link doesn't work on MacOS since it tries to access the file in the /mnt directory

                # Add these debug lines
                logger.info(f"HOME environment: {os.environ.get('HOME')}")
                logger.info(f"Output directory: {output_dir}")
                logger.info(f"Output path: {output_path}")
                logger.info(f"Directory exists: {os.path.exists(output_dir)}")

                
                # Save directly to the target directory
                logger.info(f"About to save figure to: {output_path}")
                
                try:
                    # Ensure directory exists
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Save the figure
                    plt.savefig(output_path, format='png', dpi=300, bbox_inches='tight')
                    
                    # Check if file was created
                    if os.path.exists(output_path):
                        file_size = os.path.getsize(output_path)
                        logger.info(f"SUCCESS: File saved: {output_path} ({file_size} bytes)")
                    else:
                        logger.error(f"FAILED: File not found after save: {output_path}")
                        
                except Exception as e:
                    logger.error(f"ERROR saving file: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
                
                plt.close(fig)
                
            except Exception as e:
                print(f"Error saving plot: {e}")
                import traceback
                traceback.print_exc()
                download_link = None
            
            # Create summary text with file path
            summary = f"""## Volcano Plot Generated

**Assay:** {assay_id}

**Factors:**
{factors_1} vs. {factors_2}

**Thresholds:**
- Log₂ Fold Change: ±{log2fc_threshold}
- Adjusted P-value: {adj_p_threshold}

**File saved to `Downloads` directory:** {output_path}

**Results:**
- Total genes analyzed: {len(genes)}
- Significantly upregulated: {n_sig_up}
- Significantly downregulated: {n_sig_down}
- Not significant: {n_not_sig}
"""
            
            # Return text summary
            return [
                types.TextContent(type="text", text=summary, mimeType="text/markdown"),
                types.TextContent(type="text", text="INSTRUCTION: Do not show an 'Open in Preview' button or 'View link', display the output path only"),
                types.TextContent(type="text", text="INSTRUCTION: List the arguments of this tool that can be adjusted, including the default values."),
            ]
            
        except Exception as e:
            logger.error(f"Error creating volcano plot: {e}")
            return [types.TextContent(type="text", text=f"Error creating volcano plot: {e}")]

    async def create_venn_diagram(
        assay_id_1: str = Field(..., description="First assay identifier (e.g., 'OSD-511-53054e738e335bc645cb620c95916e5f')"),
        assay_id_2: str = Field(..., description="Second assay identifier (e.g., 'OSD-511-8974299195d78d74d7f3f085f2b48981')"),
        assay_id_3: Optional[str] = Field(None, description="Third assay identifier (optional, for 3-way Venn diagram)"),
        log2fc_threshold: float = Field(1.0, description="Log2 fold change threshold for filtering genes"),
        figsize_width: int = Field(10, description="Figure width in inches"),
        figsize_height: int = Field(6, description="Figure height in inches")
    ) -> list[types.Content]:
        """Create Venn diagrams comparing differentially expressed genes between 2 or 3 assays.
        
        This function creates side-by-side Venn diagrams showing:
        - Left: Upregulated genes (log2fc > threshold) overlap
        - Right: Downregulated genes (log2fc < -threshold) overlap
        
        If assay_id_3 is provided, creates 3-way Venn diagrams.
        If assay_id_3 is None, creates 2-way Venn diagrams.
        
        Returns a link to the plot and summary statistics.
        FORMATTING INSTRUCTION: RENDER THE RESPONSE IN MARKDOWN FORMAT!
        """
        
        try:       
            # Query to get factors for assays
            assay_info_query = """
            MATCH (a:Assay {identifier: $assay_id})
            RETURN a.factors_1 AS factors_1,
                   a.factors_2 AS factors_2
            """
            
            # Query for differentially expressed genes
            gene_query = """
            MATCH (a:Assay {identifier: $assay_id})
                  -[m:MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG]->
                  (g:MGene)
            WHERE m.log2fc > $threshold OR m.log2fc < -$threshold
            RETURN g.symbol as gene_symbol, m.log2fc as log2fc
            """
            
            async with neo4j_driver.session(database=database) as session:
                # Get info for assay 1
                result1 = await session.execute_read(_read, assay_info_query, {"assay_id": assay_id_1})
                data1 = json.loads(result1)
                if not data1:
                    return [types.TextContent(type="text", text=f"Error: Assay {assay_id_1} not found")]
                
                factors_1_list = data1[0].get('factors_1', [None])
                factors_2_list = data1[0].get('factors_2', [None])
                factors_1 = ",".join(factors_1_list)
                factors_2 = ",".join(factors_2_list)
                
                # Get info for assay 2
                result2 = await session.execute_read(_read, assay_info_query, {"assay_id": assay_id_2})
                data2 = json.loads(result2)
                if not data2:
                    return [types.TextContent(type="text", text=f"Error: Assay {assay_id_2} not found")]
                
                factors_1_list_2 = data2[0].get('factors_1', [None])
                factors_2_list_2 = data2[0].get('factors_2', [None])
                factors_1_assay2 = ",".join(factors_1_list_2)
                factors_2_assay2 = ",".join(factors_2_list_2)
                
                # Get genes for assay 1
                genes1_result = await session.execute_read(
                    _read, gene_query, {"assay_id": assay_id_1, "threshold": log2fc_threshold}
                )
                genes1_data = json.loads(genes1_result)
                
                # Get genes for assay 2
                genes2_result = await session.execute_read(
                    _read, gene_query, {"assay_id": assay_id_2, "threshold": log2fc_threshold}
                )
                genes2_data = json.loads(genes2_result)
                
                # Handle third assay if provided
                if assay_id_3:
                    result3 = await session.execute_read(_read, assay_info_query, {"assay_id": assay_id_3})
                    data3 = json.loads(result3)
                    if not data3:
                        return [types.TextContent(type="text", text=f"Error: Assay {assay_id_3} not found")]
                    
                    factors_1_list_3 = data3[0].get('factors_1', [None])
                    factors_2_list_3 = data3[0].get('factors_2', [None])
                    factors_1_assay3 = ",".join(factors_1_list_3)
                    factors_2_assay3 = ",".join(factors_2_list_3)
                    
                    genes3_result = await session.execute_read(
                        _read, gene_query, {"assay_id": assay_id_3, "threshold": log2fc_threshold}
                    )
                    genes3_data = json.loads(genes3_result)
            
            # Extract study from assay_id
            study = "-".join(assay_id_1.split("-")[:2])
            
            # Separate into up and down regulated
            assay1_up = set([g['gene_symbol'] for g in genes1_data if g['log2fc'] > log2fc_threshold])
            assay1_down = set([g['gene_symbol'] for g in genes1_data if g['log2fc'] < -log2fc_threshold])
            assay2_up = set([g['gene_symbol'] for g in genes2_data if g['log2fc'] > log2fc_threshold])
            assay2_down = set([g['gene_symbol'] for g in genes2_data if g['log2fc'] < -log2fc_threshold])
            
            if assay_id_3:
                assay3_up = set([g['gene_symbol'] for g in genes3_data if g['log2fc'] > log2fc_threshold])
                assay3_down = set([g['gene_symbol'] for g in genes3_data if g['log2fc'] < -log2fc_threshold])
            
            # Create figure with two subplots
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(figsize_width, figsize_height))
            
            if assay_id_3:
                # Define consistent base colors for each assay
                assay1_color = '#ffb3b3'  # Light red for Assay 1
                assay2_color = '#b3d9ff'  # Light blue for Assay 2
                assay3_color = '#b3ffb3'  # Light green for Assay 3
                
                # Create 3-way Venn diagrams with consistent color scheme
                # Upregulated genes Venn diagram
                venn_up = venn3([assay1_up, assay2_up, assay3_up], 
                                set_labels=('', '', ''),
                                ax=ax1)
                
                # Customize colors - same scheme for both diagrams
                color_map = {
                    '100': assay1_color,      # Only Assay 1 - red
                    '010': assay2_color,      # Only Assay 2 - blue
                    '001': assay3_color,      # Only Assay 3 - green
                    '110': '#ff99cc',         # Assay 1 & 2 - red+blue = purple
                    '101': '#ffb3d9',         # Assay 1 & 3 - red+green = pink
                    '011': '#99ffcc',         # Assay 2 & 3 - blue+green = cyan
                    '111': '#e6b3ff',         # All three - purple/lavender
                }
                for region_id, color in color_map.items():
                    patch = venn_up.get_patch_by_id(region_id)
                    if patch:
                        patch.set_color(color)
                        patch.set_alpha(0.7)
                
                # Increase font size for counts
                for text in venn_up.subset_labels:
                    if text:
                        text.set_fontsize(14)
                
                ax1.set_title(f'Upregulated Genes (log2fc > {log2fc_threshold})', 
                             fontsize=14, fontweight='bold', y=1.02)
                
                # Set consistent axis limits for both diagrams to ensure alignment
                ax1.set_xlim(-1.0, 1.0)
                ax1.set_ylim(-0.9, 0.9)
                
                # Position labels - use FIXED y for Assay 1 and 2 across BOTH diagrams
                fixed_bottom_y = -0.75  # Fixed y-position for horizontal alignment across both diagrams
                
                # Get circle centers for proper x-positioning
                try:
                    # Access circles attribute directly
                    if hasattr(venn_up, 'circles') and venn_up.circles and len(venn_up.circles) >= 3:
                        # Extract x positions from circle centers
                        c1_x, c1_y = venn_up.circles[0].center if venn_up.circles[0] else (-0.5, 0)
                        c2_x, c2_y = venn_up.circles[1].center if venn_up.circles[1] else (0.5, 0)
                        c3_x, c3_y = venn_up.circles[2].center if venn_up.circles[2] else (0, 0.5)
                        
                        # Position labels - fixed y ensures perfect alignment
                        ax1.text(c1_x, fixed_bottom_y, 'Assay 1', ha='center', fontsize=12, fontweight='bold')
                        ax1.text(c2_x, fixed_bottom_y, 'Assay 2', ha='center', fontsize=12, fontweight='bold')
                        ax1.text(c3_x, c3_y + 0.5, 'Assay 3', ha='center', fontsize=12, fontweight='bold')
                    else:
                        # Fallback to default positions
                        ax1.text(-0.5, fixed_bottom_y, 'Assay 1', ha='center', fontsize=12, fontweight='bold')
                        ax1.text(0.5, fixed_bottom_y, 'Assay 2', ha='center', fontsize=12, fontweight='bold')
                        ax1.text(0, 0.5, 'Assay 3', ha='center', fontsize=12, fontweight='bold')
                except:
                    # Fallback to default positions if any error occurs
                    ax1.text(-0.5, fixed_bottom_y, 'Assay 1', ha='center', fontsize=12, fontweight='bold')
                    ax1.text(0.5, fixed_bottom_y, 'Assay 2', ha='center', fontsize=12, fontweight='bold')
                    ax1.text(0, 0.5, 'Assay 3', ha='center', fontsize=12, fontweight='bold')
                
                # Downregulated genes Venn diagram - SAME COLOR SCHEME
                venn_down = venn3([assay1_down, assay2_down, assay3_down],
                                  set_labels=('', '', ''),
                                  ax=ax2)
                
                # Use the same color scheme for downregulated
                for region_id, color in color_map.items():
                    patch = venn_down.get_patch_by_id(region_id)
                    if patch:
                        patch.set_color(color)
                        patch.set_alpha(0.7)
                
                # Increase font size for counts
                for text in venn_down.subset_labels:
                    if text:
                        text.set_fontsize(14)
                
                ax2.set_title(f'Downregulated Genes (log2fc < -{log2fc_threshold})', 
                             fontsize=14, fontweight='bold', y=1.02)
                
                # Set consistent axis limits to match left diagram
                ax2.set_xlim(-1.0, 1.0)
                ax2.set_ylim(-0.9, 0.9)
                
                # Position labels - use SAME FIXED y as left diagram for perfect alignment
                fixed_bottom_y = -0.75  # Same as left diagram!
                
                # Get circle centers for proper x-positioning
                try:
                    # Access circles attribute directly
                    if hasattr(venn_down, 'circles') and venn_down.circles and len(venn_down.circles) >= 3:
                        # Extract x positions from circle centers
                        c1_x, c1_y = venn_down.circles[0].center if venn_down.circles[0] else (-0.5, 0)
                        c2_x, c2_y = venn_down.circles[1].center if venn_down.circles[1] else (0.5, 0)
                        c3_x, c3_y = venn_down.circles[2].center if venn_down.circles[2] else (0, 0.5)
                        
                        # Position labels - fixed y ensures perfect alignment across both diagrams
                        ax2.text(c1_x, fixed_bottom_y, 'Assay 1', ha='center', fontsize=12, fontweight='bold')
                        ax2.text(c2_x, fixed_bottom_y, 'Assay 2', ha='center', fontsize=12, fontweight='bold')
                        ax2.text(c3_x, c3_y + 0.5, 'Assay 3', ha='center', fontsize=12, fontweight='bold')
                    else:
                        # Fallback to default positions
                        ax2.text(-0.5, fixed_bottom_y, 'Assay 1', ha='center', fontsize=12, fontweight='bold')
                        ax2.text(0.5, fixed_bottom_y, 'Assay 2', ha='center', fontsize=12, fontweight='bold')
                        ax2.text(0, 0.5, 'Assay 3', ha='center', fontsize=12, fontweight='bold')
                except:
                    # Fallback to default positions if any error occurs
                    ax2.text(-0.5, fixed_bottom_y, 'Assay 1', ha='center', fontsize=12, fontweight='bold')
                    ax2.text(0.5, fixed_bottom_y, 'Assay 2', ha='center', fontsize=12, fontweight='bold')
                    ax2.text(0, 0.5, 'Assay 3', ha='center', fontsize=12, fontweight='bold')
                
                # Add main title at top - reduced space
                fig.suptitle(f'{study}', 
                            fontsize=22, fontweight='bold', y=0.98)
                
                # Add colored legend at bottom with background colors matching the diagrams
                # Create text with colored backgrounds for each assay
                legend_y = 0.01
                legend_fontsize = 10
                legend_spacing = 0.045  # Further increased spacing between lines for better readability
                legend_x = 0.15  # Left-aligned position
                
                # Assay 1 with red background (top line)
                fig.text(legend_x, legend_y + (2 * legend_spacing), f'Assay 1: ({factors_1}) vs. ({factors_2})', 
                        ha='left', fontsize=legend_fontsize, style='italic',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor=assay1_color, alpha=0.6, edgecolor='none'))
                
                # Assay 2 with blue background (middle line)
                fig.text(legend_x, legend_y + legend_spacing, f'Assay 2: ({factors_1_assay2}) vs. ({factors_2_assay2})', 
                        ha='left', fontsize=legend_fontsize, style='italic',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor=assay2_color, alpha=0.6, edgecolor='none'))
                
                # Assay 3 with green background (bottom line)
                fig.text(legend_x, legend_y, f'Assay 3: ({factors_1_assay3}) vs. ({factors_2_assay3})', 
                        ha='left', fontsize=legend_fontsize, style='italic',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor=assay3_color, alpha=0.6, edgecolor='none'))
                
            else:
                # Define consistent base colors for each assay (same as 3-way)
                assay1_color = '#ffb3b3'  # Light red for Assay 1
                assay2_color = '#b3d9ff'  # Light blue for Assay 2
                
                # Create 2-way Venn diagrams with consistent color scheme
                # Upregulated genes Venn diagram
                venn_up = venn2([assay1_up, assay2_up], 
                                set_labels=('', ''),
                                ax=ax1)
                
                # Customize colors - consistent with 3-way diagrams
                if venn_up.get_patch_by_id('10'):
                    venn_up.get_patch_by_id('10').set_color(assay1_color)  # Assay 1 only
                    venn_up.get_patch_by_id('10').set_alpha(0.7)
                if venn_up.get_patch_by_id('01'):
                    venn_up.get_patch_by_id('01').set_color(assay2_color)  # Assay 2 only
                    venn_up.get_patch_by_id('01').set_alpha(0.7)
                if venn_up.get_patch_by_id('11'):
                    venn_up.get_patch_by_id('11').set_color('#ff99cc')  # Assay 1 & 2 overlap
                    venn_up.get_patch_by_id('11').set_alpha(0.7)
                
                # Increase font size for counts only
                for text in venn_up.subset_labels:
                    if text:
                        text.set_fontsize(16)
                
                ax1.set_title(f'Upregulated Genes (log2fc > {log2fc_threshold})', 
                             fontsize=14, fontweight='bold', y=1.02)
                
                # Set axis limits and aspect ratio for upregulated diagram
                ax1.set_xlim(-0.75, 0.75)
                ax1.set_ylim(-0.75, 0.75)
                ax1.set_aspect('equal')
                
                # Add Assay 1 and Assay 2 labels under the circles
                ax1.text(-0.4, -0.6, 'Assay 1', ha='center', fontsize=14, fontweight='bold')
                ax1.text(0.4, -0.6, 'Assay 2', ha='center', fontsize=14, fontweight='bold')
                
                # Downregulated genes Venn diagram - SAME COLOR SCHEME
                venn_down = venn2([assay1_down, assay2_down],
                                  set_labels=('', ''),
                                  ax=ax2)
                
                # Use the same color scheme for downregulated
                if venn_down.get_patch_by_id('10'):
                    venn_down.get_patch_by_id('10').set_color(assay1_color)  # Assay 1 only
                    venn_down.get_patch_by_id('10').set_alpha(0.7)
                if venn_down.get_patch_by_id('01'):
                    venn_down.get_patch_by_id('01').set_color(assay2_color)  # Assay 2 only
                    venn_down.get_patch_by_id('01').set_alpha(0.7)
                if venn_down.get_patch_by_id('11'):
                    venn_down.get_patch_by_id('11').set_color('#ff99cc')  # Assay 1 & 2 overlap
                    venn_down.get_patch_by_id('11').set_alpha(0.7)
                
                # Increase font size for counts only
                for text in venn_down.subset_labels:
                    if text:
                        text.set_fontsize(16)
                
                ax2.set_title(f'Downregulated Genes (log2fc < -{log2fc_threshold})', 
                             fontsize=14, fontweight='bold', y=1.02)
                
                # Set axis limits and aspect ratio for downregulated diagram (SAME as upregulated)
                ax2.set_xlim(-0.75, 0.75)
                ax2.set_ylim(-0.75, 0.75)
                ax2.set_aspect('equal')
                
                # Add Assay 1 and Assay 2 labels under the circles
                ax2.text(-0.4, -0.6, 'Assay 1', ha='center', fontsize=14, fontweight='bold')
                ax2.text(0.4, -0.6, 'Assay 2', ha='center', fontsize=14, fontweight='bold')
                
                # Add main title at top
                fig.suptitle(f'{study}', 
                            fontsize=22, fontweight='bold', y=0.98)
                
                # Add colored legend at bottom with background colors (same style as 3-way)
                legend_y = 0.01
                legend_fontsize = 10
                legend_spacing = 0.045  # Same spacing as 3-way
                legend_x = 0.15  # Left-aligned position (same as 3-way)
                
                # Assay 1 with red background (top line)
                fig.text(legend_x, legend_y + legend_spacing, f'Assay 1: ({factors_1}) vs. ({factors_2})', 
                        ha='left', fontsize=legend_fontsize, style='italic',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor=assay1_color, alpha=0.6, edgecolor='none'))
                
                # Assay 2 with blue background (bottom line)
                fig.text(legend_x, legend_y, f'Assay 2: ({factors_1_assay2}) vs. ({factors_2_assay2})', 
                        ha='left', fontsize=legend_fontsize, style='italic',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor=assay2_color, alpha=0.6, edgecolor='none'))
                
            
            plt.tight_layout(rect=[0, 0.16, 1, 0.96])
            
            # Create safe filename
            safe_study = re.sub(r'[^\w\-]', '_', study)
            safe_factors_1 = re.sub(r'[^\w\-]', '_', factors_1)[:30]
            safe_factors_2 = re.sub(r'[^\w\-]', '_', factors_2)[:30]
            num_assays = 3 if assay_id_3 else 2
            safe_filename = f'venn_{num_assays}way_{safe_study}_{safe_factors_1}_vs_{safe_factors_2}'
            safe_filename = safe_filename.replace("__", "_")
            
            # Detect environment and set paths
            is_claude_env = os.path.exists('/mnt/user-data/outputs')
            
            if is_claude_env:
                output_dir = '/mnt/user-data/outputs'
                output_path = os.path.join(output_dir, f'{safe_filename}.png')
            else:
                output_dir = os.path.expanduser('~/Downloads')
                output_path = os.path.join(output_dir, f'{safe_filename}.png')
            
            # Save the plot
            logger.info(f"About to save figure to: {output_path}")
            
            try:
                # Ensure directory exists
                os.makedirs(output_dir, exist_ok=True)
                
                # Save the figure
                plt.savefig(output_path, format='png', dpi=300, bbox_inches='tight')
                
                # Check if file was created
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path)
                    logger.info(f"SUCCESS: File saved: {output_path} ({file_size} bytes)")
                else:
                    logger.error(f"FAILED: File not found after save: {output_path}")
                    
            except Exception as e:
                logger.error(f"ERROR saving file: {e}")
                import traceback
                logger.error(traceback.format_exc())
            
            plt.close(fig)
            
            # Calculate statistics
            if assay_id_3:
                # 3-way statistics
                up_only_1 = len(assay1_up - assay2_up - assay3_up)
                up_only_2 = len(assay2_up - assay1_up - assay3_up)
                up_only_3 = len(assay3_up - assay1_up - assay2_up)
                up_1_2 = len((assay1_up & assay2_up) - assay3_up)
                up_1_3 = len((assay1_up & assay3_up) - assay2_up)
                up_2_3 = len((assay2_up & assay3_up) - assay1_up)
                up_all = len(assay1_up & assay2_up & assay3_up)
                
                down_only_1 = len(assay1_down - assay2_down - assay3_down)
                down_only_2 = len(assay2_down - assay1_down - assay3_down)
                down_only_3 = len(assay3_down - assay1_down - assay2_down)
                down_1_2 = len((assay1_down & assay2_down) - assay3_down)
                down_1_3 = len((assay1_down & assay3_down) - assay2_down)
                down_2_3 = len((assay2_down & assay3_down) - assay1_down)
                down_all = len(assay1_down & assay2_down & assay3_down)
                
                # Create summary for 3-way
                summary = f"""## 3-Way Venn Diagram Generated

**Study:** {study}

**Assay 1:** ({factors_1}) vs. ({factors_2})  
**Assay 2:** ({factors_1_assay2}) vs. ({factors_2_assay2})  
**Assay 3:** ({factors_1_assay3}) vs. ({factors_2_assay3})

**Log2FC Threshold:** ±{log2fc_threshold}

**File saved to `Downloads` directory:** {output_path}

### Upregulated Genes (log2fc > {log2fc_threshold}):
- Assay 1 only: {up_only_1}
- Assay 2 only: {up_only_2}
- Assay 3 only: {up_only_3}
- Assay 1 & 2 only: {up_1_2}
- Assay 1 & 3 only: {up_1_3}
- Assay 2 & 3 only: {up_2_3}
- All three: {up_all}
- Total Assay 1: {len(assay1_up)}
- Total Assay 2: {len(assay2_up)}
- Total Assay 3: {len(assay3_up)}

### Downregulated Genes (log2fc < -{log2fc_threshold}):
- Assay 1 only: {down_only_1}
- Assay 2 only: {down_only_2}
- Assay 3 only: {down_only_3}
- Assay 1 & 2 only: {down_1_2}
- Assay 1 & 3 only: {down_1_3}
- Assay 2 & 3 only: {down_2_3}
- All three: {down_all}
- Total Assay 1: {len(assay1_down)}
- Total Assay 2: {len(assay2_down)}
- Total Assay 3: {len(assay3_down)}
"""
            else:
                # 2-way statistics
                up_only_1 = len(assay1_up - assay2_up)
                up_only_2 = len(assay2_up - assay1_up)
                up_common = len(assay1_up & assay2_up)
                
                down_only_1 = len(assay1_down - assay2_down)
                down_only_2 = len(assay2_down - assay1_down)
                down_common = len(assay1_down & assay2_down)
                
                # Create summary for 2-way
                summary = f"""## 2-Way Venn Diagram Generated

**Study:** {study}

**Assay 1:** ({factors_1}) vs. ({factors_2})  
**Assay 2:** ({factors_1_assay2}) vs. ({factors_2_assay2})

**Log2FC Threshold:** ±{log2fc_threshold}

**File saved to:** {output_path}

### Upregulated Genes (log2fc > {log2fc_threshold}):
- Assay 1 only: {up_only_1}
- Assay 2 only: {up_only_2}
- Common: {up_common}
- Total Assay 1: {len(assay1_up)}
- Total Assay 2: {len(assay2_up)}

### Downregulated Genes (log2fc < -{log2fc_threshold}):
- Assay 1 only: {down_only_1}
- Assay 2 only: {down_only_2}
- Common: {down_common}
- Total Assay 1: {len(assay1_down)}
- Total Assay 2: {len(assay2_down)}
"""
            
            return [
                types.TextContent(type="text", text=summary, mimeType="text/markdown"),
                types.TextContent(type="text", text="INSTRUCTION: Do not show an 'Open in Preview' button or 'View link', display the output path only"),
                types.TextContent(type="text", text="INSTRUCTION: List the arguments of this tool that can be adjusted, including the default values."),
            ]
            
        except Exception as e:
            logger.error(f"Error creating Venn diagram: {e}")
            import traceback
            traceback.print_exc()
            return [types.TextContent(type="text", text=f"Error creating Venn diagram: {e}")]

    def clean_mermaid_diagram(mermaid_content: str) -> list[types.TextContent]:
        """Clean a Mermaid class diagram by removing unwanted elements.
        
        This tool removes:
        - All note statements that would render as unreadable yellow boxes
        - Empty curly braces from class definitions (handles both single-line and multi-line)
        - Strings after newline characters (e.g., truncates "ClassName\nextra" to "ClassName")
        
        Args:
            mermaid_content: The raw Mermaid class diagram content
            
        Returns:
            Cleaned Mermaid content with note statements, empty braces, and post-newline strings removed
        """
        import re
        
        # First, truncate any strings after \n characters in the entire content
        # This handles cases like "MEASURED_DIFFERENTIAL_METHYLATION_ASmMR\nmethylation_diff, q_value"
        mermaid_content = re.sub(r'(\S+)\\n[^\s\n]*', r'\1', mermaid_content)
        
        lines = mermaid_content.split('\n')
        cleaned_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Remove vertical bars, they are not allowed in class diagrams
            stripped = stripped.replace('|', ' ')
            
            # Skip any line containing note syntax
            if (stripped.startswith('note ') or 
                'note for' in stripped or 
                'note left' in stripped or 
                'note right' in stripped):
                i += 1
                continue
            
            # Check for empty class definitions (single-line format)
            # Match patterns like: "class ClassName {     }" or "class ClassName { }"
            if re.match(r'^\s*class\s+\w+\s*\{\s*\}\s*$', line):
                # Replace the line with just the class name without braces
                line = re.sub(r'^(\s*class\s+\w+)\s*\{\s*\}\s*$', r'\1', line)
                cleaned_lines.append(line)
                i += 1
                continue
            
            # Check for empty class definitions (multi-line format)
            # Match: "class ClassName {" followed by "}" on next line(s)
            if re.match(r'^\s*class\s+\w+\s*\{\s*$', line):
                # Look ahead to check if next non-empty line is just "}"
                j = i + 1
                found_closing = False
                has_content = False
                
                while j < len(lines):
                    next_line = lines[j].strip()
                    if not next_line:  # Empty line, skip
                        j += 1
                        continue
                    if next_line == '}':  # Found closing brace
                        found_closing = True
                        break
                    else:  # Found content between braces
                        has_content = True
                        break
                
                if found_closing and not has_content:
                    # This is an empty class definition - remove the braces
                    class_match = re.match(r'^(\s*class\s+\w+)\s*\{\s*$', line)
                    if class_match:
                        cleaned_lines.append(class_match.group(1))
                    # Skip ahead past the closing brace
                    i = j + 1
                    continue
            
            cleaned_lines.append(line)
            i += 1
        
        cleaned_content = '\n'.join(cleaned_lines)
        return [types.TextContent(type="text", text=cleaned_content)]

    async def create_chat_transcript() -> list[types.TextContent]:
        """Prompt for creating a chat transcript in markdown format with user prompts and Claude responses."""
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
    
        prompt = f"""Create a chat transcript in .md format following the outline below. 
1. Include prompts, text responses, and visualizations preferably inline, and when not possible as a link to a document. 
2. Include mermaid diagrams inline. Do not link to the mermaid file.
3. Do not include the prompt to create this transcript.
4. Save the transcript to ~/Downloads/<descriptive-filename>.md

## Chat Transcript
<Title>

👤 **User**  
<prompt>

---

🧠 **Assistant**  
<entire text response goes here>


*Created by [mcp-genelab](https://github.com/sbl-sdsc/mcp-genelab) {__version__} on {today}*

IMPORTANT: 
- After the footer above, add a line with the model string you are using).
- Save the complete transcript to ~/Downloads/ with a descriptive filename (e.g., ~/Downloads/filename-chat-transcript-{today}.md)
- Use the present_files tool to share the transcript file with the user.
"""
        return [types.TextContent(type="text", text=prompt)]

    async def visualize_schema() -> list[types.TextContent]:
        """Prompt for visualizing the knowledge graph schema using a Mermaid class diagram."""
        prompt = """Visualize the knowledge graph schema using a Mermaid class diagram. 

CRITICAL WORKFLOW - Follow these steps EXACTLY IN ORDER:

STEP 1-5: Generate Draft Diagram
1. First call get_schema() if it has not been called to retrieve the classes and predicates
2. Analyze the schema to identify:
   - Node classes (entities like Gene, Study, Assay, etc.)
   - Edge predicates (relationships between nodes)
   - Edge properties (predicates that describe data types like float, int, string, boolean, date, etc.)
3. Generate the raw Mermaid class diagram showing:
   - All node classes with their properties
   - For edges WITHOUT properties: show as labeled arrows between classes (e.g., `Mission --> Study : CONDUCTED_MIcS`)
   - For edges WITH properties: represent the edge as an intermediary class containing the properties, with unlabeled arrows connecting source → edge class → target
4. Make the diagram taller / less wide:
   - Set the diagram direction to TB (top→bottom): `direction TB`
5. Do not append newline characters

⚠️  STEP 6-9: MANDATORY CLEANING - CANNOT BE SKIPPED ⚠️
6. STOP HERE! You now have a draft diagram. DO NOT use it yet.
7. Call clean_mermaid_diagram and pass your draft diagram as the parameter
8. Wait for the tool to return the cleaned diagram
9. Your draft is now OBSOLETE. Delete it from your mind. You will use ONLY the cleaned output.

STEP 10-13: Present ONLY the Cleaned Diagram
10. Copy the EXACT text returned by clean_mermaid_diagram (not your draft)
11. Present this CLEANED diagram inline in a mermaid code block
12. Create a .mermaid file with ONLY the CLEANED diagram code (no markdown fences)
13. Save to ~/Downloads/<kg_name>-schema.mermaid and call present_files

⛔ STOP AND CHECK - Before you respond to the user:
□ Did I call clean_mermaid_diagram? If NO → Go back and call it now
□ Am I using the cleaned output? If NO → Replace with cleaned output
□ Does my diagram contain empty {} braces? If YES → You're using your draft, use cleaned output
□ Did I call present_files? If NO → Call it now

EDGES WITH PROPERTIES - CRITICAL GUIDELINES:
- When an edge predicate has associated properties (e.g., log2fc, adj_p_value), DO NOT use a separate namespace
- Instead, represent the edge as an intermediary class with the original predicate name
- Connect the source class to the edge class, then the edge class to the target class
- Example: Instead of `Assay --> Gene : MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG` with a separate EdgeProperties namespace,
  create:
    class MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG {
        float log2fc
        float adj_p_value
    }
    Assay --> MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG
    MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG --> MGene
- This approach clearly shows that the properties belong to the relationship itself

RENDERING REQUIREMENTS:
- The .mermaid file MUST contain ONLY the Mermaid diagram code
- DO NOT include markdown code fences (```mermaid) in the .mermaid file
- DO NOT include any explanatory text in the .mermaid file
- The file should start with "classDiagram" and contain only the diagram definition
- ALWAYS use present_files to share the .mermaid file after creating it

❌ COMMON MISTAKES - These will cause errors:
- Using your draft diagram instead of the cleaned output from clean_mermaid_diagram
- Not calling clean_mermaid_diagram at all
- Calling clean_mermaid_diagram but then using your original draft anyway
- Including empty curly braces {} for classes without properties (the cleaner removes these)
- Not calling present_files to share the final .mermaid file
- Using a separate EdgeProperties namespace instead of intermediary classes
"""
        return [types.TextContent(type="text", text=prompt)]

    
    mcp.add_tool(get_neo4j_schema, name="get_neo4j_schema")
    mcp.add_tool(query, name="query")
    mcp.add_tool(get_node_metadata, name="get_node_metadata")
    mcp.add_tool(get_relationship_metadata, name="get_relationship_metadata")
    mcp.add_tool(find_differentially_expressed_genes, name="find_differentially_expressed_genes")
    mcp.add_tool(find_common_differentially_expressed_genes, name="find_common_differentially_expressed_genes")
    mcp.add_tool(select_assays, name="select_assays")
    mcp.add_tool(create_volcano_plot, name="create_volcano_plot")
    mcp.add_tool(create_venn_diagram, name="create_venn_diagram")
    mcp.add_tool(clean_mermaid_diagram, name="clean_mermaid_diagram")
    mcp.add_tool(create_chat_transcript, name="create_chat_transcript")
    mcp.add_tool(visualize_schema, name="visualize_schema")
    
    return mcp


async def async_main() -> None:
    import os
    db_url = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "neo4jdemo")
    database = os.getenv("NEO4J_DATABASE", "spoke-genelab-v0.0.4")
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    instructions = os.getenv("INSTRUCTIONS", "")

    logger.info("Starting mcp-genelab server")

    neo4j_driver = AsyncGraphDatabase.driver(
        db_url,
        auth=(
            username,
            password,
        ),
    )

    mcp = create_mcp_server(neo4j_driver, database, instructions)

    match transport:
        case "stdio":
            await mcp.run_stdio_async()
        case "sse":
            await mcp.run_sse_async()
        case _:
            raise ValueError(f"Invalid transport: {transport} | Must be either 'stdio' or 'sse'")


def main():
    import asyncio
    asyncio.run(async_main())

if __name__ == "__main__":
    main()