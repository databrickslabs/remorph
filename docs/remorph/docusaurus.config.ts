import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Remorph',
  tagline: 'Simplified Data Migration Toolkit to ease Migration to Databricks',
  favicon: 'img/logo.svg',

  url: 'https://databrickslabs.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/remorph/',
  trailingSlash: true,

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'databrickslabs', // Usually your GitHub org/user name.
  projectName: 'Remorph', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'throw',
  onDuplicateRoutes: 'throw',
  onBrokenAnchors: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  markdown: { mermaid: true },
  themes: ['@docusaurus/theme-mermaid'],

  plugins: [
    async (context, options) => {
      return {
        name: "docusaurus-plugin-tailwindcss",
        configurePostCss(postcssOptions) {
          postcssOptions.plugins = [
            require('tailwindcss'),
            require('autoprefixer'),
          ];
          return postcssOptions;
        },
      }
    },
    'docusaurus-plugin-image-zoom',
    'docusaurus-lunr-search'
  ],

  presets: [
    [
      'classic',
      {
        docs: {
          // routeBasePath: '/',
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/databrickslabs/remorph/tree/main/docs/remorph/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],


  themeConfig: {
    colorMode: {
      defaultMode: 'dark',
      respectPrefersColorScheme: false,
    },
    navbar: {
      title: 'Remorph',
      logo: {
        alt: 'Remorph Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'search',
          position: 'right',
        },
        {
          href: 'https://github.com/databrickslabs/remorph',
          position: 'right',

          className: 'header-github-link',
          'aria-label': 'GitHub repository',
        },

      ],
    },
    footer: {
      links: [
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Databricks Labs. Docs built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.oneLight,
      darkTheme: prismThemes.dracula,
    },
    mermaid: {
      theme: {light: 'grey', dark: 'dark'},
      },
    zoom: {
      selector: 'article img',
      background: {
        light: '#F8FAFC',
        dark: '#F8FAFC',
      },
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
