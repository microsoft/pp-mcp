<script setup>
import {
  VPTeamPage,
  VPTeamPageTitle,
  VPTeamMembers,
  VPTeamPageSection
} from 'vitepress/theme'

const powerAdvocacy = [
  {
    avatar: 'https://www.github.com/aprildunnam.png',
    name: 'April Dunnam',
    title: 'Principal Cloud Advocate',
    links: [
      { icon: 'github', link: 'https://github.com/aprildunnam' },
      { icon: 'twitter', link: 'https://twitter.com/aprildunnam' }
    ]
  },
  {
    avatar: 'https://www.github.com/elaizabenitez.png',
    name: 'Elaiza Benitez',
    title: 'Senior Cloud Advocate',
    links: [
      { icon: 'github', link: 'https://github.com/elaizabenitez' },
      { icon: 'twitter', link: 'https://twitter.com/benitezhere' },
      { icon: 'linkedin', link: 'https://linkedin.com/in/elaiza-benitez' }
    ]
  },
  {
    avatar: 'https://www.github.com/laskewitz.png',
    name: 'Daniel Laskewitz',
    title: 'Principal Cloud Advocate',
    links: [
      { icon: 'github', link: 'https://github.com/laskewitz' },
      { icon: 'twitter', link: 'https://twitter.com/laskewitz' },
      { icon: 'linkedin', link: 'https://linkedin.com/in/laskewitz' }
    ]
  },
  {
    avatar: 'https://www.github.com/scottdurow.png',
    name: 'Scott Durow',
    title: 'Senior Cloud Advocate',
    links: [
      { icon: 'github', link: 'https://github.com/scottdurow' },
      { icon: 'twitter', link: 'https://twitter.com/scottdurow' },
      { icon: 'linkedin', link: 'https://linkedin.com/in/scottdurow' }
    ]
  }
]

const communityContributors = [
  {
    avatar: 'https://www.github.com/biswapm.png',
    name: 'Pujarini Mohapatra',
    title: 'Principal Architect @ Microsoft',
    links: [
      { icon: 'github', link: 'https://github.com/biswapm' },
      { icon: 'twitter', link: 'https://twitter.com/biswapm' },
      { icon: 'linkedin', link: 'https://linkedin.com/in/biswapm' }
    ]
  },
  {
    avatar: 'https://www.github.com/qmatteoq.png',
    name: 'Matteo Pagani',
    title: 'Cloud Solution Architect @ Microsoft',
    links: [
      { icon: 'github', link: 'https://github.com/qmatteoq' },
      { icon: 'twitter', link: 'https://twitter.com/qmatteoq' },
      { icon: 'linkedin', link: 'https://linkedin.com/in/matteopagani' }
    ]
  }
]
</script>

# Contributions

Say hello to the team behind these Power Platform MCP labs!

## Community Contributors

The following people have provided samples to this project! Thanks for all your contributions!

<VPTeamMembers size="small" :members="communityContributors" />

## Power Platform Advocacy

This project is started by Power Platform Advocacy. The team members are listed below.

<VPTeamMembers size="small" ::members="powerAdvocacy" />
