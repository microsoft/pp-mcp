import { defineConfig } from "vitepress";

export default defineConfig({
  title: "Agent 365 Academy",
  base: "/agent-365-academy/",
  head: [["link", { rel: "icon", href: "/agent-365-academy/images/logo.png" }]],
  description:
    "Welcome to Agent 365 Academy. Curated lessons on getting started with Agent 365.",
  themeConfig: {
    logo: "/agent-365-academy/images/logo.png",
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
        link: "https://github.com/microsoft/agent-365-academy/",
      },
    ],
  },
});
