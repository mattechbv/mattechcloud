# mat-tech.cloud

Static landing page for [mat-tech.cloud](https://mat-tech.cloud), hosted on GitHub Pages.

## Layout

| Path | What it is |
| --- | --- |
| `public/` | The published site, served at the domain root |
| `public/index.html` | The page, with all meta, icon, Open Graph and structured-data tags |
| `public/favicon.ico`, `favicon.svg`, `favicon-*.png` | Browser and search-result favicons (Google needs a multiple of 48 px) |
| `public/apple-touch-icon.png`, `icon-*.png`, `site.webmanifest` | Home-screen and app icons |
| `public/og-image.png` | 1200 × 630 link-preview image |
| `public/logo.png` | Logo for Google's structured data |
| `public/CNAME` | Custom domain for GitHub Pages |
| `tools/generate-icons.py` | Rebuilds every icon, logo and the preview image |
| `.github/workflows/pages.yml` | Publishes `public/` on every push to `main` |

## Rebuild the icons

```sh
pip install pillow
python tools/generate-icons.py
```

## GitHub Pages setup (once)

1. **Settings → Pages → Build and deployment → Source:** GitHub Actions.
2. **Settings → Pages → Custom domain:** `mat-tech.cloud`, then tick **Enforce HTTPS** once the certificate is issued.
3. DNS at the registrar:
   - `A` records for `mat-tech.cloud`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `AAAA` records: `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
   - `CNAME` for `www`: `<github-user-or-org>.github.io`
4. Verify the domain under the organisation's **Settings → Pages** so nobody else can claim it.

## Getting the icon into Google

Google shows the favicon of the domain's home page. After the site is live:

1. Add `mat-tech.cloud` to [Google Search Console](https://search.google.com/search-console) and submit `https://mat-tech.cloud/sitemap.xml`.
2. Use **URL Inspection → Request indexing** on `https://mat-tech.cloud/`.
3. Check previews with the [Rich Results Test](https://search.google.com/test/rich-results), the [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/) and the [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/).

The favicon in search results can take days to weeks to update after Google recrawls.
