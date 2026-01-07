## Development

### Installing from Source

If you want to run a development version:

```bash
# Clone the repository
git clone https://github.com/sbl-sdsc/mcp-genelab.git
cd mcp-genelab

# Install dependencies (run this after every local code change)
uv sync

# Copy the dev configuration file to the Claude Desktop configuration directory
# **Make sure to save your current config file under a different name to avoid overwriting it.**
cp ./config/claude_desktop_config_dev.json "$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# update the configuration, including path to this Git repository, URI, username, and password for the Neo4j databases.

# Shutdown Claude Desktop and wait about 10 seconds for the MCP servers to shutdown.

# Restart Claude Desktop
```