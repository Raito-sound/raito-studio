# Raito.studio

Official portfolio for composer and sound designer Raito (来兎), with introductions to his browser tools.

## Public pages

- `/` — portfolio, profile, browser tools and contact
- `/works/` — searchable complete works index
- `/press/` — bilingual press kit
- `/tally/` — English introduction to TALLY, linking to https://tally.raito.studio/
- `/carve/` — English introduction to CARVE, linking to https://carve.raito.studio/
- `/404.html` — not-found page

The TALLY and CARVE apps remain in their own GitHub repositories (`Raito-sound/tally` and `Raito-sound/carve`) and publish independently through GitHub Pages. This repository contains their introduction pages only.

`tools.html` is an unpublished local draft and is excluded from version control and the site build.

## Publishing

The production site at https://raito.studio/ is hosted on Cloudflare Pages, project `raito-studio`, connected to `Raito-sound/raito-studio` on branch `main`. DNS is managed by Cloudflare.

Run `sh .cloudflare/pages-build.sh` from this directory to produce `_site/`. Cloudflare Pages publishes that output. GitHub Actions uses the same build script for the secondary preview at https://raito-sound.github.io/raito-studio/.

The build explicitly selects public HTML, styles, scripts and assets. Documentation, source Markdown, draft pages and the app repositories are not included in the website artifact.

## App subdomains

Both app repositories have their custom domain registered in GitHub Pages with HTTPS enabled. The corresponding Cloudflare DNS records should be CNAMEs to `raito-sound.github.io`, using DNS-only mode:

- `tally.raito.studio` → `raito-sound.github.io`
- `carve.raito.studio` → `raito-sound.github.io`

The introduction URLs and app URLs serve different purposes; neither redirects to the other. App updates are deployed from each app repository without copying the app into this portfolio.
