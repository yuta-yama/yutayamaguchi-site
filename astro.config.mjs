import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://www.yutayamaguchi.com",
  trailingSlash: "never",
  build: {
    format: "file",
  },
});
