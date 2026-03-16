# Dockerfile for mcp-genelab MCP Server
# Runs the MCP GeneLab server with Streamable HTTP transport
# for remote deployment behind a TLS reverse proxy (Caddy).

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for matplotlib
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the project files
COPY pyproject.toml .
COPY src/ src/

# Install the package and its dependencies
RUN pip install --no-cache-dir .

# Default environment variables (override at runtime)
ENV NEO4J_URI="bolt://neo4j-kg:7687"
ENV NEO4J_USERNAME="neo4j"
ENV NEO4J_PASSWORD="changeme123"
ENV NEO4J_DATABASE="neo4j"
ENV MCP_TRANSPORT="streamable-http"
ENV MCP_HOST="0.0.0.0"
ENV MCP_PORT="8000"
ENV INSTRUCTIONS="Query the GeneLab KG to identify NASA spaceflight experiments containing omics datasets, specifically differential gene expression (transcriptomics), DNA methylation (epigenomics), and Amplicon (metagenomics) data."

EXPOSE 8000

# Run the MCP server
CMD ["mcp-genelab"]
