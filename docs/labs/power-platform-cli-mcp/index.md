# Power Platform CLI MCP (work-in-progress)

## What is Microsoft Power Platform CLI?

Microsoft Power Platform CLI is a simple, one-stop developer command-line interface that empowers developers and independent software vendors (ISVs) to perform various operations in Microsoft Power Platform. This powerful tool enables you to manage and automate tasks related to:

- **Environment lifecycle** - Create, manage, and configure Power Platform environments
- **Authentication** - Handle secure connections and auth profiles for multiple tenants
- **Microsoft Dataverse environments** - Work with data, tables, and configurations
- **Solution packages** - Import, export, and manage Power Platform solutions
- **Power Pages** - Configure and deploy Power Pages websites
- **Code components** - Create and manage custom Power Apps Component Framework (PCF) controls
- **And much more** - Additional capabilities for comprehensive Power Platform development

The CLI provides a consistent interface on Windows, making it an essential tool for Power Platform developers.

## Installing Power Platform CLI with .NET Tool

The .NET Tool installation method enables you to use Power Platform CLI commands within PowerShell and CMD shells on Windows.

### Prerequisites

Before installing the Power Platform CLI, ensure you have:
- **.NET 6.0 or later** installed on your system
- An **internet connection** for downloading the NuGet package

### Installation Steps

1. **Install the CLI globally** using the .NET tool install command:
   ```bash
   dotnet tool install --global Microsoft.PowerApps.CLI.Tool
   ```

1. **Verify the installation** by checking the version:
   ```bash
   pac
   ```
   You should see output similar to:
   ```
   Microsoft PowerPlatform CLI
   Version: 1.30.3+g0f0e0b9
   ```

### Managing Your Installation

**Update to the latest version:**
```bash
dotnet tool update --global Microsoft.PowerApps.CLI.Tool
```

**Uninstall if needed:**
```bash
dotnet tool uninstall --global Microsoft.PowerApps.CLI.Tool
```

### File Locations

The Power Platform CLI executable is installed to:
- `%USERPROFILE%\.dotnet\tools`

This location is automatically added to your system PATH, allowing you to run `pac` commands from any directory.

### Important Notes

- **Internet connection required**: All installations and updates require internet access to download the latest NuGet package
- **User-specific installation**: The tool is installed per user, not system-wide

### Next Steps

Once installed, you can:
- Run `pac help` to see all available commands
- Use `pac auth create` to connect to your Power Platform environment
- Explore the comprehensive command reference in the [Microsoft Power Platform CLI documentation](https://learn.microsoft.com/power-platform/developer/cli/reference/)
