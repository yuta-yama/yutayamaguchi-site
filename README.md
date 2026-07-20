# yutayamaguchi.com

Static portfolio site for Yuta Yamaguchi — migrated from Squarespace to Astro + Markdown.

## Stack

- **Astro 5** — static site generator
- **Markdown** — one file per project in `content/projects/`
- **Cloudflare Pages** — hosting (build `dist/`)

## Commands

```bash
npm install
npm run dev      # http://localhost:4321
npm run build
npm run preview
```

## Content

- **Projects:** `src/content/projects/<slug>.md` — frontmatter: `title`, `order`, `cover`, `stills`, `vimeo`, `youtube`, `links`
- **Pages:** `src/content/pages/contact.md`, `bio.md`
- **Stills:** `public/stills/<slug>/`

### Add a new project

1. Create `src/content/projects/my-project.md` with frontmatter and body copy.
2. Add stills to `public/stills/my-project/`.
3. Set `order` to control homepage position.
4. `npm run build`

### Re-export from Squarespace

While the old site is still live:

```bash
npm run export
```

## Cloudflare Pages deploy

1. Push repo to GitHub (or connect this folder).
2. Cloudflare Pages → Create project → connect repo.
3. Build settings:
   - **Root directory:** `yutayamaguchi-site`
   - **Build command:** `npm run build`
   - **Output directory:** `dist`
4. Preview on `*.pages.dev`, then update DNS for `yutayamaguchi.com`.

### DNS cutover (when ready)

Domain is at Tucows; options:

- **A)** Move DNS to Cloudflare (recommended — you already use `yutay.dev` there), add `yutayamaguchi.com`, point to Pages.
- **B)** Keep Tucows DNS, CNAME `www` → `<project>.pages.dev`, apex via Cloudflare redirect or CNAME flattening.

Cancel Squarespace after DNS propagates and you've verified all project URLs.

## Legacy redirects

`public/_redirects` maps `/films` → `/` for old Squarespace URLs.
