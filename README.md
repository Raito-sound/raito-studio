# Raito.studio

Official English-language portfolio for composer and sound designer Raito (来兎).

## Launch scope

- `/` — portfolio, profile and contact
- `/works/` — searchable complete works index
- `/press/` — bilingual press kit
- `/404.html` — not-found page

`tools.html` is retained locally as a working draft and is intentionally excluded from launch navigation and version control until its content and destinations are complete.

## Publishing

The folder is prepared for a standalone GitHub Pages repository using the custom domain `raito.studio`. `CNAME`, `.nojekyll`, canonical metadata, Open Graph metadata, `robots.txt`, `sitemap.xml`, `llms.txt` and a custom 404 page are included.

The existing Wix site should remain active until the GitHub Pages preview has been checked and the DNS cutover is scheduled.

The GitHub repository is `Raito-sound/raito-studio`. Updates to `main` publish through `.github/workflows/pages.yml`. Only the launch HTML, styles, scripts and assets are served; source Markdown and project documentation are excluded from the website artifact.

The initial public URL is `https://raito-sound.github.io/raito-studio/`. Configure the custom domain in GitHub Pages before updating the existing Wix DNS records. Actions deployment uses the Pages setting, rather than the local `CNAME` file.
