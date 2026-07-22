# DNS cutover — yutayamaguchi.com → Cloudflare Pages

Site is already live at https://yutayamaguchi.pages.dev  
Custom domains `yutayamaguchi.com` + `www.yutayamaguchi.com` are attached to the Pages project `yutayamaguchi` (pending DNS).

## Why this step is manual

The current API token can deploy Pages but **cannot create DNS zones**. Adding the domain once in the Cloudflare dashboard unlocks nameservers + apex CNAME flattening.

## Steps (do once)

### 1. Add the domain to Cloudflare

1. Open https://dash.cloudflare.com/?to=/:account/add-site  
2. Enter `yutayamaguchi.com` → Continue  
3. Free plan is fine → Continue  
4. Cloudflare shows **two nameservers** (e.g. `ada.ns.cloudflare.com` / `bob.ns.cloudflare.com`) — copy them  
5. Skip/leave DNS records for now; Pages will manage the web records

### 2. Point the registrar at Cloudflare

Registrar: **Tucows** (often Hover / OpenSRS UI).

1. Log in where you renew `yutayamaguchi.com`  
2. Change **nameservers** from Squarespace/NS1 to the two Cloudflare nameservers from step 1  
3. Save (propagation: often minutes, sometimes up to ~24–48h)

### 3. Finish Pages domain wiring

After the zone is **Active** in Cloudflare:

1. Pages → **yutayamaguchi** → Custom domains  
2. Confirm `yutayamaguchi.com` and `www.yutayamaguchi.com` show **Active**  
3. If needed, re-add them; Cloudflare should auto-create:

| Type  | Name | Target / content              | Proxy |
|-------|------|-------------------------------|-------|
| CNAME | `www` | `yutayamaguchi.pages.dev`    | Proxied |
| CNAME | `@`   | `yutayamaguchi.pages.dev`    | Proxied (flattened) |

### 4. Verify

```bash
dig +short yutayamaguchi.com NS   # should be *.ns.cloudflare.com
curl -sI https://www.yutayamaguchi.com | head -5
curl -sI https://yutayamaguchi.com | head -5
```

Both should serve the Astro portfolio (not Squarespace).

### 5. Cancel Squarespace

Only after verification. Billing change applies on renewals after **Aug 11, 2026**.

## Temporary www-only option (not preferred)

If you can't move nameservers yet, in Squarespace DNS set:

- `www` → CNAME → `yutayamaguchi.pages.dev`

Apex (`yutayamaguchi.com`) still needs Cloudflare DNS for a clean setup.

## After cutover

Tell the agent “domain is on Cloudflare” — it can verify records, HTTPS, and redirects.
