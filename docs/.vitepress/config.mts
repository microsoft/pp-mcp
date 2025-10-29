import { defineConfig } from "vitepress";

export default defineConfig({
  title: "#PPMCP Labs & Samples",
  base: "/copilot-studio-mcp/",
  head: [["link", { rel: "icon", href: "/copilot-studio-labs/logo.png" }]],
  description:
    "Welcome to Power Platform MCP Labs & Samples. Curated labs & samples on getting started with Power Platform & MCP.",
  themeConfig: {
    logo: "/copilot-studio-labs/logo.png",
    siteTitle: false,
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
          {
            text: "🌴 Employee Vacations (HTTP - TS)",
            link: "https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/employeevacations-http-typescript/",
          },
          {
            text: "🏬 Events Management (HTTP - TS)",
            link: "https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/events-http-typescript/",
          },
          {
            text: "😁 Jokes (HTTP - TS)",
            link: "https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/jokes-http-typescript/",
          },
          {
            text: "😁 Jokes (SSE - TS)",
            link: "https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/jokes-sse-typescript/",
          },
          {
            text: "🌳🌲 Parks (HTTP - TS)",
            link: "https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/parks-http-typescript/",
          },
          {
            text: "🛒 Zava Inventory (HTTP - Python)",
            link: "https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/zava-inventory-http-python/",
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
          {
            text: "🌴 Employee Vacations (HTTP - TS)",
            link: "https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/employeevacations-http-typescript/",
          },
          {
            text: "🏬 Events Management (HTTP - TS)",
            link: "https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/events-http-typescript/",
          },
          {
            text: "😁 Jokes (HTTP - TS)",
            link: "https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/jokes-http-typescript/",
          },
          {
            text: "😁 Jokes (SSE - TS)",
            link: "https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/jokes-sse-typescript/",
          },
          {
            text: "🌳🌲 Parks (HTTP - TS)",
            link: "https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/parks-http-typescript/",
          },
          {
            text: "🛒 Zava Inventory (HTTP - Python)",
            link: "https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/zava-inventory-http-python/",
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
