# Gary Doman Portfolio Site

Static multi-page portfolio site generated from the portfolio repository.

## Included
- SEO-focused homepage
- Projects index page
- 35 individual project pages
- `ProfilePage` and page-level JSON-LD
- `robots.txt`
- `sitemap.xml`
- Resume PDF and carried-over SVG assets

## Deploy
### GitHub Pages
1. Create or use the `Portfolio` repository.
2. Upload these files to the repo root.
3. Enable GitHub Pages from the main branch.

### Important after deploy
If your final URL is **not** `https://garebear99.github.io/Portfolio`, update:
- canonical URLs in the HTML
- JSON-LD `url` fields
- `robots.txt`
- `sitemap.xml`

## Recommended next edits
- Replace support links with your actual Buy Me a Coffee / Ko-fi pages if you want them on-site.
- Add screenshots for the flagship projects.
- Add a custom domain if you want stronger branding.


## Added in this updated package
- `stack.html` now acts as the ecosystem routing hub for ARC / AGI / simulation repos.
- `projects.html` now supports client-side search plus category filters.
- Additional routed project pages were added for Proto-AGI, ARC-Turbo-OS, Arc-RAR, and arc-lucifer-cleanroom-runtime.
