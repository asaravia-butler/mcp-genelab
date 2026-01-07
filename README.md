# MCP GeneLab Server

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![PyPI version](https://img.shields.io/pypi/v/mcp-genelab?label=PyPI)](https://pypi.org/project/mcp-genelab/)

A Model Context Protocol (MCP) server that converts natural language queries into [Cypher](https://neo4j.com/product/cypher-graph-query-language) queries and executes them against the configured Neo4j endpoints. Customized tools provide seamless access to the NASA [GeneLab Knowledge Graph](https://github.com/BaranziniLab/spoke_genelab), enabling AI-assisted analysis of spaceflight experiments and their biological effects. This server allows researchers to query differential gene expression and DNA methylation data from NASA's space biology experiments through natural language interactions with AI assistants like Claude.

The GeneLab Knowledge Graph with data from NASA's [GeneLab Data Repository](https://genelab.nasa.gov/), part of the NASA [Open Science Data Repository (OSDR)](https://science.nasa.gov/biological-physical/data/osdr/), can be integrated with biomedical knowledge from the [SPOKE](https://spoke.ucsf.edu/) (Scalable Precision Medicine Open Knowledge Engine) knowledge graph. This integration connects spaceflight experimental results with a comprehensive biological context, including genes, proteins, anatomical structures, pathways, and diseases.

This server is part of the NSF-funded [Proto-OKN Project](https://www.proto-okn.net/) (Prototype Open Knowledge Network). It's an extension of the [Neo4j Cypher MCP server](https://github.com/neo4j-contrib/mcp-neo4j/tree/main/servers/mcp-neo4j-cypher).

## Features

- **Natural Language Querying**: Ask questions in plain English - no need to write complex graph queries
- **NASA GeneLab Queries**: Ask questions about spaceflight experiments in the NASA GeneLab knowledge graph
- **Differential Gene Expression Analysis**: Find genes that are upregulated or downregulated in spaceflight conditions compared to ground controls
- **DNA Methylation Data**: Access epigenetic changes observed in spaceflight experiments
- **Multi-Organism Support**: Query data across multiple model organisms including mice, rats, and other species used in space research
- **Tissue-Specific Analysis**: Filter results by specific organs, tissues, or cell types
- **Biomedical Context Integration**: Connect spaceflight gene expression changes to pathways, diseases, and other biological knowledge from SPOKE
- **Federated Queries**: Combine data from GeneLab with other Neo4j knowledge graphs for comprehensive biomedical analysis
- **Multiple Access Methods**: Use through Claude Desktop, VS Code with GitHub Copilot, or programmatically via the MCP protocol
- **Pre-configured Endpoints**: Ready-to-use access to both local and remote Neo4j databases containing the GeneLab Knowledge Graph

## Prerequisites

Before installing the MCP server, ensure you have:

- **Operating System**: macOS, Linux, or Windows
- **Client Application**: One of the following:
  - Claude Desktop with Pro or Max subscription
  - VS Code Insiders with GitHub Copilot subscription
- **Neo4j Knowledge Graphs**:
  - For a local installation of the GeneLab KG see [setup](https://github.com/BaranziniLab/spoke_genelab)
  - For remote access to GeneLab and SPOKE KGs [request](https://github.com/sbl-sdsc/mcp-genelab/issues) credentials

## Installation

[Installation instructions for Claude Desktop and VS Code Insiders](https://github.com/sbl-sdsc/mcp-genelab/tree/main/docs/installation.md)

## Quick Start

Once configured, you can start querying knowledge graphs through natural language prompts in Claude Desktop or VS Code chat interface.

### Select and Configure MCP Tools (Claude Desktop)

From the top menu bar:
```
1. Select: Claude->Settings->Connectors
2. Click: Configure for the MCP endpoints you want to use
3. Select Tool permissions: Always allow
```

In the prompt dialog box, click the `+` button:
```
1. Turn off Web search
2. Toggle MCP services on/off as needed
```

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-genelab/main/docs/images/select_mcp_server.png"
     alt="Tool Selector"
     width="300">

Use @kg_name to refer to a specific knowledge graph in chat (for example, @spoke-genelab).

To create a transcript of a chat (see examples below), use the following prompt: 
```Create a chat transcript```. 
The transcript can then be downloaded in .md or .pdf format.

## Example Queries

### Knowledge Graph Overviews & Class Diagrams

Each link below points to a chat transcript that demonstrates how to generate a knowledge-graph overview and class diagram for a given Neo4j Knowledge Graph.

[spoke-genelab](https://github.com/sbl-sdsc/mcp-genelab/tree/main/docs/examples/spoke-genelab-overview.md)

[spoke-okn](https://github.com/sbl-sdsc/mcp-genelab/tree/main/docs/examples/spoke-okn-overview.md)

### Node and Relationship Metadata Examples

[spoke-genelab: Assay Node Metadata](https://github.com/sbl-sdsc/mcp-genelab/tree/main/docs/examples/assay-node-description.md)

[spoke-genelab: MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG relationship](https://github.com/sbl-sdsc/mcp-genelab/tree/main/docs/examples/differential-expression-relationship.md)

### SPOKE-GeneLab KG Inventory

[spoke-genelab Inventory](https://github.com/sbl-sdsc/mcp-genelab/tree/main/docs/examples/genelab-inventory.md)

### Differential Expression Analysis with MCP tools

[spoke-genelab Study OSD-244](https://github.com/sbl-sdsc/mcp-genelab/tree/main/docs/examples/osd-244-differential-gene-expression.md)

---

## Development

[Instructions for local development](https://github.com/sbl-sdsc/mcp-genelab/tree/main/docs/development.md)

## Building and Publishing (maintainers only)

[Instructions for building, testing, and publishing the mcp-genelab package on PyPI](https://github.com/sbl-sdsc/mcp-genelab/tree/main/docs/build_publish.md)

## API Reference

[mcp-genelab server API](https://github.com/sbl-sdsc/mcp-genelab/tree/main/docs/api.md)

## Troubleshooting

### Common Issues

**MCP server not appearing in Claude Desktop:**
- Ensure you've completely quit and restarted Claude Desktop (not just closed the window)
- Check that your JSON configuration is valid (attach your config file to a chat and ask it to fix any errors)
- Verify that `uvx` is installed and accessible in your PATH

**Connection errors:**
- Verify the Neo4j endpoint URL is correct and accessible
- Some endpoints may have rate limits or temporary downtime

**Performance issues:**
- Complex Cypher queries may take time to execute
- Consider breaking down complex queries into smaller parts
- Check the endpoint's documentation for query best practices

## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for details.

## Citation

If you use MCP GeneLab in your research, please cite the following works:

```bibtex
@software{rose2025mcp-genelab,
  title={MCP GeneLab Server},
  author={Rose, P.W. and Saravia-Butler, A.M. and Nelson, C.A. and Shi, Y. and Baranzini, S.E.},
  year={2025},
  url={https://github.com/sbl-sdsc/mcp-proto-okn}
}

@software{rose2025spoke-genelab,
  title={NASA SPOKE-GeneLab Knowledge Graph},
  author={Rose, P.W. and Nelson, C.A. and Saravia-Butler, A.M. and Gebre, S.G. and Soman, K. and Grigorev, K.A. and Sanders, L.M. and Costes, S.V. and Baranzini, S.E.},
  year={2025},
  url={https://github.com/BaranziniLab/spoke_genelab}
}
```

### Related Publications

- Nelson, C.A., Rose, P.W., Soman, K., Sanders, L.M., Gebre, S.G., Costes, S.V., Baranzini, S.E. (2025). "Nasa Genelab-Knowledge Graph Fabric Enables Deep Biomedical Analysis of Multi-Omics Datasets." *NASA Technical Reports*, 20250000723. [Link](https://ntrs.nasa.gov/citations/20250000723)

- Sanders, L., Costes, S., Soman, K., Rose, P., Nelson, C., Sawyer, A., Gebre, S., Baranzini, S. (2024). "Biomedical Knowledge Graph Capability for Space Biology Knowledge Gain." *45th COSPAR Scientific Assembly*, July 13-21, 2024. [Link](https://ui.adsabs.harvard.edu/abs/2024cosp...45.2183S/abstract)

## Acknowledgments

### Funding

This work is supported in part by:
- **National Science Foundation** Award [#2333819](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2333819): "Proto-OKN Theme 1: Connecting Biomedical information on Earth and in Space via the SPOKE knowledge graph"

### Related Projects

- [Proto-OKN Project](https://www.proto-okn.net/) - Prototype Open Knowledge Network initiative
- [NASA Open Science Data Repository (OSDR)](https://science.nasa.gov/biological-physical/data/osdr/) - Repository of multi-modal space life science data
- [NASA GeneLab Data Repository](https://genelab.nasa.gov/) - GeneLab data repository used to create the GeneLab KG
- [NASA GeneLab KG](https://github.com/BaranziniLab/spoke_genelab) - Git Repository for creating the GeneLab KG
- [Model Context Protocol](https://modelcontextprotocol.io/) - AI assistant integration standard
- [Original Neo4j Cypher MCP server](https://github.com/neo4j-contrib/mcp-neo4j/tree/main/servers/mcp-neo4j-cypher) - Base implementation reference

---

*For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/sbl-sdsc/mcp-genelab).*