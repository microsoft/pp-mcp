import { defineConfig } from "vitepress";

export default defineConfig({
  title: "#PPMCP Labs & Samples",
  base: "/copilot-studio-mcp/",
  ignoreDeadLinks: [
    // ignore exact url "./http/requests.http"
    "./http/requests.http",
    // ignore all localhost links
    /^https?:\/\/localhost/,
    (url) => {
      return url.toLowerCase().includes("ignore");
    },
  ],
  head: [["link", { rel: "icon", href: "/copilot-studio-mcp/logo.png" }]],
  description:
    "Welcome to Power Platform MCP Labs & Samples. Curated labs & samples on getting started with Power Platform & MCP.",
  themeConfig: {
    logo: "/logo.png",
    siteTitle: false,
    nav: [
      { text: "🏠 Home", link: "/" },
      { text: "❤️ Contributions", link: "/contributions/" },
      {
        text: "🧪 Labs",
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
        text: "✨ Samples",
        items: [
          {
            text: "🧮 Calculator (SSE - TS)",
            link: "/samples/calculator-sse-typescript/",
          },
          {
            text: "🌴 Employee Vacations (HTTP - .NET)",
            link: "/samples/employeevacations-http-csharp/",
          },
          {
            text: "🌴 Employee Vacations (HTTP - TS)",
            link: "/samples/employeevacations-http-typescript/",
          },
          {
            text: "🏬 Events Management (HTTP - TS)",
            link: "/samples/events-http-typescript/",
          },
          {
            text: "😁 Jokes (HTTP - TS)",
            link: "/samples/jokes-http-typescript/",
          },
          {
            text: "😁 Jokes (SSE - TS)",
            link: "/samples/jokes-sse-typescript/",
          },
          {
            text: "🌳🌲 Parks (HTTP - TS)",
            link: "/samples/parks-http-typescript/",
          },
          {
            text: "🛒 Zava Inventory (HTTP - Python)",
            link: "/samples/zava-inventory-http-python/",
          },
        ],
      },
    ],
    sidebar: [
      {
        text: "🏠 Home",
        link: "/",
      },
      { text: "❤️ Contributions", link: "/contributions/" },
      {
        text: "🧪 Labs",
        collapsed: true,
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
        text: "✨ Samples",
        collapsed: true,
        items: [
          {
            text: "🧮 Calculator (SSE - TS)",
            link: "/samples/calculator-sse-typescript/",
          },
          {
            text: "🌴 Employee Vacations (HTTP - .NET)",
            link: "/samples/employeevacations-http-csharp/",
          },
          {
            text: "🌴 Employee Vacations (HTTP - TS)",
            link: "/samples/employeevacations-http-typescript/",
          },
          {
            text: "🏬 Events Management (HTTP - TS)",
            link: "/samples/events-http-typescript/",
          },
          {
            text: "😁 Jokes (HTTP - TS)",
            link: "/samples/jokes-http-typescript/",
          },
          {
            text: "😁 Jokes (SSE - TS)",
            link: "/samples/jokes-sse-typescript/",
          },
          {
            text: "🌳🌲 Parks (HTTP - TS)",
            link: "/samples/parks-http-typescript/",
          },
          {
            text: "🛒 Zava Inventory (HTTP - Python)",
            link: "/samples/zava-inventory-http-python/",
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
