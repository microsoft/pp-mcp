import { defineConfig } from "vitepress";

export default defineConfig({
  title: "MCS MCP Labs",
  base: "/copilot-studio-mcp/",
  head: [
    ["link", { rel: "icon", href: "/copilot-studio-mcp/images/logo.png" }],
  ],
  description:
    "Welcome to Microsoft Copilot Studio & MCP Labs. Curated lessons on getting started with Microsoft Copilot Studio & MCP.",
  themeConfig: {
    logo: "/copilot-studio-mcp/images/logo.png",
    nav: [
      { text: "Home", link: "/" },
      { text: "Our Team", link: "/our-team/" },
    ],

    sidebar: [
      {
        text: "Agent Academy",
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
