import { defineConfig } from "vitepress";

export default defineConfig({
  title: "#PPMCP Labs & Samples",
  base: "/copilot-studio-mcp/",
  head: [["link", { rel: "icon", href: "/copilot-studio-labs/logo.png" }]],
  description:
    "Welcome to Power Platform MCP Labs & Samples. Curated labs & samples on getting started with Power Platform & MCP.",
  themeConfig: {
    logo: "/copilot-studio-labs/logo.png",
    nav: [
      { text: "Home", link: "/" },
      { text: "Our Team", link: "/our-team/" },
      {
        text: "Labs",
        items: [
          {
            text: "Microsoft Copilot Studio ❤️ MCP",
            link: "https://aka.ms/mcsmcplab",
          },
          {
            text: "Dataverse MCP Labs",
            link: "https://aka.ms/dataverse/mcp/lab",
          },
        ],
      },
      {
        text: "Samples",
        items: [
          {
            text: "🧮 Calculator (SSE - TS)",
            link: "https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/calculator-sse-typescript/",
          },
          {
            text: "🌴 Employee Vacations (HTTP - .NET)",
            link: "https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/employeevacations-http-csharp/",
          },
        ],
      },
    ],
    sidebar: [
      {
        text: "Home",
        link: "/",
      },
      {
        text: "Our Team",
        link: "/our-team/",
      },
      {
        text: "Labs",
        collapse: true,
        items: [
          {
            text: "Microsoft Copilot Studio ❤️ MCP",
            link: "https://aka.ms/mcsmcplab",
          },
          {
            text: "Dataverse MCP Labs",
            link: "https://aka.ms/dataverse/mcp/lab",
          },
        ],
      },
      {
        text: "Samples",
        collapse: true,
        items: [
          {
            text: "🧮 Calculator (SSE - TS)",
            link: "https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/calculator-sse-typescript/",
          },
          {
            text: "🌴 Employee Vacations (HTTP - .NET)",
            link: "https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/employeevacations-http-csharp/",
          },
        ],
      },
    ],
    socialLinks: [
      {
        icon: "github",
        link: "https://github.com/microsoft/copilot-studio-mcp/",
      },
    ],
  },
});
