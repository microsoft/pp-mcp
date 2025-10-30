# ⚡ Power Platform CLI MCP (work-in-progress)

## ❓ What is Microsoft Power Platform CLI?

Microsoft Power Platform CLI is a simple, one-stop developer command-line interface that empowers developers and independent software vendors (ISVs) to perform various operations in Microsoft Power Platform. This powerful tool enables you to manage and automate tasks related to:

- **Environment lifecycle** - Create, manage, and configure Power Platform environments
- **Authentication** - Handle secure connections and auth profiles for multiple tenants
- **Microsoft Dataverse environments** - Work with data, tables, and configurations
- **Solution packages** - Import, export, and manage Power Platform solutions
- **Power Pages** - Configure and deploy Power Pages websites
- **Code components** - Create and manage custom Power Apps Component Framework (PCF) controls
- **And much more** - Additional capabilities for comprehensive Power Platform development

The CLI provides a consistent interface on Windows, making it an essential tool for Power Platform developers.

## 💾 Installing Power Platform CLI with .NET Tool

The .NET Tool installation method enables you to use Power Platform CLI commands within PowerShell and CMD shells on Windows.

### ✅ Prerequisites

Before installing the Power Platform CLI, ensure you have:

- **.NET 8.0 or later (preferably install the latest version)** installed on your system ([Download .NET](https://dotnet.microsoft.com/download))
- An **internet connection** for downloading the NuGet package

### 🚀 Installation Steps

1. **Install the CLI globally** using the .NET tool install command:

   ```bash
   dotnet tool install --global Microsoft.PowerApps.CLI.Tool
   ```

1. **Verify the installation** by checking the version:

   ```bash
   pac
   ```

   You should see output similar to:

   ```text
   Microsoft PowerPlatform CLI
   Version: 1.30.3+g0f0e0b9
   ```

### 🔧 Managing Your Installation

**Update to the latest version:**

```bash
dotnet tool update --global Microsoft.PowerApps.CLI.Tool
```

**Uninstall if needed:**

```bash
dotnet tool uninstall --global Microsoft.PowerApps.CLI.Tool
```

### 📁 File Locations

The Power Platform CLI executable is installed to:

- `%USERPROFILE%\.dotnet\tools`

This location is automatically added to your system PATH, allowing you to run `pac` commands from any directory.

## 🤖 Power Platform CLI MCP

The Power Platform CLI (version 1.44+) includes a built-in **Model Context Protocol (MCP) server** that enables AI-powered interactions with Power Platform environments directly through chat interfaces. This integration allows you to perform Power Platform operations using natural language commands in supported AI tools like VS Code Copilot, Visual Studio, and other MCP-compatible applications.

### 🚀 What is MCP Integration?

The MCP server exposes Power Platform CLI commands as tools that AI assistants can invoke on your behalf. Instead of memorizing complex CLI syntax, you can simply describe what you want to accomplish in natural language, and the AI will execute the appropriate commands.

**Key Benefits:**

- **Natural Language Interface** - Describe tasks in plain English instead of remembering CLI syntax
- **Intelligent Command Selection** - AI chooses the right commands based on your intent  
- **Contextual Assistance** - Get help with Power Platform operations without leaving your development environment
- **Selective Tool Access** - Choose which CLI commands to expose for security and simplicity

### 📋 Supported Operations

The MCP server currently supports **20+ Power Platform CLI commands** including:

- **Environment Management** - List, create, and manage Power Platform environments
- **Solution Operations** - Import, export, and package solutions
- **Authentication** - Handle auth profiles and tenant connections
- **Dataverse Operations** - Work with tables, data, and configurations
- **Power Pages** - Manage website deployments and configurations
- **Component Management** - Handle PCF controls and other components

### ⚙️ Setting Up PAC CLI MCP

#### 1. Locate the MCP Executable

After installing Power Platform CLI via the .NET tool, the MCP server executable is available at:

```text
%USERPROFILE%\.dotnet\tools\.store\microsoft.powerapps.cli.tool\[version]\microsoft.powerapps.cli.tool\[version]\tools\net8.0\any\pac-mcp.exe
```

**Quick way to find the location:**

```bash
pac copilot mcp
```

This command will display the exact path to your `pac-mcp.exe` file.

#### 2. Configure MCP in Visual Studio Code

To use the Power Platform CLI MCP server in Visual Studio Code:

1. Open Visual Studio Code settings (Ctrl+,)
1. Search for "MCP" or navigate to Extensions > GitHub Copilot > MCP Servers
1. Add a new MCP server configuration with:
   - **Name**: `powerplatform-cli`
   - **Executable Path**: Full path to `pac-mcp.exe`
   - **Arguments**: (optional command-line arguments)

#### 3. Configure MCP in Visual Studio

For Visual Studio integration:

1. Go to Tools > Options > GitHub Copilot > MCP Servers
1. Click "Add" to create a new server entry
1. Provide the path to `pac-mcp.exe`
1. Select which tools/commands to enable

### 💬 Using Power Platform CLI with AI Chat

Once configured, you can interact with Power Platform using natural language:

**Example Commands:**

View all available Power Platform environments in your tenant:

```text
List all my Power Platform environments
```

Export a specific solution from your development environment:

```text
Export the solution named 'MySolution' from the development environment
```

Check your current authentication configuration:

```text
Show me the authentication profiles configured
```

Create a new environment for testing purposes:

```text
Create a new environment for testing
```

Deploy a solution package to your production environment:

```text
Import the solution package into production
```

The AI will translate these requests into appropriate `pac` commands and execute them through the MCP server.

### 🛡️ Security and Tool Selection

The MCP integration allows you to **selectively enable** specific CLI commands, giving you control over which operations the AI can perform. This ensures security by limiting access to only the tools you need for your workflow.

**Best Practices:**

- Enable only the commands you regularly use
- Review tool permissions before granting access
- Use environment-specific configurations for different projects
- Monitor MCP server logs for executed commands

### 🔧 Troubleshooting

**Common Issues:**

1. **MCP Server Not Found**
   - Verify the path to `pac-mcp.exe` using `pac copilot mcp`
   - Ensure Power Platform CLI version 1.44+ is installed

1. **Authentication Errors**
   - Run `pac auth list` to verify your authentication profiles
   - Set up authentication using `pac auth create` if needed

1. **Tool Access Warnings**
   - Check the Output window in VS Code for MCP-related messages
   - Verify tool permissions in MCP server configuration

### 📚 Learn More

- [Adding an MCP server in Visual Studio](https://learn.microsoft.com/visualstudio/ide/mcp-servers#adding-an-mcp-server)
- [Power Platform CLI Documentation](https://learn.microsoft.com/power-platform/developer/cli/introduction)
- [GitHub Discussion: PAC CLI MCP Preview](https://github.com/microsoft/powerplatform-build-tools/discussions/1182)
