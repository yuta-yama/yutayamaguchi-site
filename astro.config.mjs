import sitemap from "@astrojs/sitemap";
import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://www.yutayamaguchi.com",
  trailingSlash: "never",
  integrations: [sitemap()],
  build: {
    format: "file",
  },
});
