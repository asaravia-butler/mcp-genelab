## Installation

### Prerequisites

The MCP GeneLab server requires installing the `uv` package manager on your system. If you don't have it installed, run:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Check if `uv` is in the PATH
```bash
which uv
```

If `uv` is not found, add the following line to your `~/.zshrc` file for zsh or `/.bash_profile` for bash.
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then reload the shell.
```bash
source ~/.zshrc  # or source ~/.bash_profile
```

If you are using `macOS 12`, you also need to install `realpath`.

To check if you have `realpath` installed, run:
```bash
which realpath
```

Download the [Homebrew installer](https://github.com/Homebrew/brew/releases/download/4.6.17/Homebrew-4.6.17.pkg) and click on the downloaded package to install Homebrew.

Then run the following command to install coreutils and check if `realpath` is available.
```bash
brew install coreutils
which realpath
```


# Windows
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

> **Note**: Once `uv` is installed, the `uvx` command in the configuration below will automatically download and run the latest version of the MCP server from PyPI when needed.

### Claude Desktop Setup

**Recommended for most users**

1. **Download and Install Claude Desktop**

   Visit [https://claude.ai/download](https://claude.ai/download) and install Claude Desktop for your operating system.

   > **Requirements**: Claude Pro or Max subscription is required for MCP server functionality.

2. **Configure MCP Server**

   **Option A: Download Pre-configured File (Recommended)**

   Download the pre-configured `claude_desktop_config.json` file with Neo4j endpoints from the repository and copy it to the appropriate location:

   **macOS**:
   ```bash
   # Download the config file
   curl -o /tmp/claude_desktop_config.json https://raw.githubusercontent.com/sbl-sdsc/mcp-genelab/main/config/claude_desktop_config.json
   
   # Copy to Claude Desktop configuration directory
   cp /tmp/claude_desktop_config.json "$HOME/Library/Application Support/Claude/"
   ```

   **Windows PowerShell**:
   ```powershell
   # Download the config file
   Invoke-WebRequest -Uri "https://raw.githubusercontent.com/sbl-sdsc/mcp-genelab/main/config/claude_desktop_config.json" -OutFile "$env:TEMP\claude_desktop_config.json"
   
   # Copy to Claude Desktop configuration directory
   Copy-Item "$env:TEMP\claude_desktop_config.json" "$env:APPDATA\Claude\"
   ```

   **Option B: Manual Configuration**

   Alternatively, you can manually edit the configuration file in Claude Desktop. Navigate to `Claude->Settings->Developer->Edit Config`
   to edit it.

   Below is an example of how to configure local and remote Neo4j endpoints. For remotely hosted Neo4j servers, update the url, username, and password.

   ```json
   {
     "mcpServers": {
      "genelab-local": {
         "command": "uvx",
         "args": ["mcp-genelab"],
         "env": {
           "NEO4J_URI": "bolt://localhost:7687",
           "NEO4J_USERNAME": "neo4j",
           "NEO4J_PASSWORD": "neo4jdemo",
           "NEO4J_DATABASE": "spoke-genelab-v0.0.4",
           "INSTRUCTIONS": "Query the GeneLab Knowledge Graph to identify NASA spaceflight experiments containing omics datasets, specifically differential gene expression (transcriptomics) and DNA methylation (epigenomics) data."
         }
       },
       "genelab": {
         "command": "uvx",
         "args": ["mcp-genelab"],
         "env": {
           "NEO4J_URI": "uri",
           "NEO4J_USERNAME": "username",
           "NEO4J_PASSWORD": "password",
           "NEO4J_DATABASE": "spoke-genelab-v0.0.4",
           "INSTRUCTIONS": "Query the GeneLab Knowledge Graph to identify NASA spaceflight experiments containing omics datasets, specifically differential gene expression (transcriptomics) and DNA methylation (epigenomics) data."
         }
      }
   }
   ```

   > **Important**: If you have existing MCP server configurations, do not use Option A as it will overwrite your existing configuration. Instead, use Option B and manually merge the Neo4j endpoints with your existing `mcpServers` configuration.

3. **Restart Claude Desktop**

   After saving the configuration file, quit Claude Desktop completely and restart it. The application needs to restart to load the new configuration and start the MCP servers.

4. **Verify Installation**

   1. Launch Claude Desktop
   2. Navigate to `Claude->Settings->Connectors`
   3. Verify that the configured Neo4j endpoints appear in the connector list
   4. You can configure each service to always ask for permission or to run it unsupervised (recommended)

### VS Code Setup

**For advanced users and developers**

1. **Install VS Code Insiders**

   Download and install VS Code Insiders from [https://code.visualstudio.com/insiders/](https://code.visualstudio.com/insiders/)

   > **Note**: VS Code Insiders is required as it includes the latest MCP (Model Context Protocol) features.

2. **Install GitHub Copilot Extension**

   - Open VS Code Insiders
   - Sign in with your GitHub account
   - Install the GitHub Copilot extension

   > **Requirements**: GitHub Copilot subscription is required for MCP integration.

3. **Configure MCP Server**

   **Option A: Download Pre-configured File (Recommended)**

   Download the pre-configured `mcp.json` file from the repository and copy it to the appropriate location.

   **macOS**:
   ```bash
   # Download the config file
   curl -o /tmp/mcp.json https://raw.githubusercontent.com/sbl-sdsc/mcp-genelab/main/config/mcp.json

   # Copy to VS Code Insiders configuration directory
   cp /tmp/mcp.json "$HOME/Library/Application Support/Code - Insiders/User/mcp.json"
   ```
 > **Note**: VS Code Insiders mcp.json file is identical to the claude_desktop_config.json file, except "mcpServer" is replaced by "server".

4. **Use the MCP Server**

   1. Open a new chat window in VS Code
   2. Select **Agent** mode
   3. Choose **Claude Sonnet 4.5 or later** model for optimal performance
   4. The MCP servers will automatically connect and provide knowledge graph access
