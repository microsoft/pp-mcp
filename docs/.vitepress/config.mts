import { defineConfig } from "vitepress";

export default defineConfig({
  title: "#PPMCP Labs",
  base: "/copilot-studio-mcp/",
  head: [
    ["link", { rel: "icon", href: "/copilot-studio-mcp/images/logo.png" }],
  ],
  description:
    "Welcome to Power Platform MCP Labs. Curated lessons on getting started with Power Platform & MCP.",
  themeConfig: {
    logo: "/copilot-studio-mcp/images/logo.png",
    nav: [
      { text: "Home", link: "/" },
      { text: "Our Team", link: "/our-team/" },
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
