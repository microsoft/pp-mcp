import { defineConfig } from "vitepress";

export default defineConfig({
  title: "#PPMCP Labs & Samples",
  base: "/copilot-studio-mcp/",
  head: [
    ["link", { rel: "icon", href: "/copilot-studio-mcp/images/logo.png" }],
  ],
  description:
    "Welcome to Power Platform MCP Labs & Samples. Curated labs & samples on getting started with Power Platform & MCP.",
  themeConfig: {
    logo: "/copilot-studio-mcp/images/logo.png",
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
            text: "🧮 Calculator (SSE Version) - TypeScript",
            link: "/samples/calculator-sse-typescript/",
          },
        ],
      },
    ],

    sidebar: [
      {
        text: "Power Platform MCP Labs",
        items: [
          { text: "Home", link: "/" },
          { text: "Our Team", link: "/our-team/" },
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
