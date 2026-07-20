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

## Live

- **Production:** https://yutayamaguchi.pages.dev
- **GitHub:** https://github.com/yuta-yama/yutayamaguchi-site
- **Cloudflare Pages project:** `yutayamaguchi`

Deploys on push to `main` via `.github/workflows/deploy.yml` (needs `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` repo secrets — already set).

Manual deploy:

```bash
npm run build
npx wrangler pages deploy dist --project-name=yutayamaguchi
```

### DNS cutover (when ready)

Domain is at Tucows; DNS currently on Squarespace. Recommended:

1. Cloudflare dashboard → Pages → `yutayamaguchi` → Custom domains → add `www.yutayamaguchi.com` (+ apex).
2. Move nameservers for `yutayamaguchi.com` to Cloudflare (same account as `yutay.dev`), **or** CNAME `www` → `yutayamaguchi.pages.dev` at the current DNS host.
3. Verify pages, then cancel Squarespace before the next renewal.

## Legacy redirects

`public/_redirects` maps `/films` → `/` for old Squarespace URLs.
