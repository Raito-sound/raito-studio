# Raito.studio

Official portfolio for composer and sound designer Raito (来兎), with introductions to his browser tools.

## Public pages

- `/` — portfolio, profile, browser tools and contact
- `/works/` — searchable complete works index
- `/press/` — bilingual press kit
- `/tools/` and `/ja/tools/` — English/Japanese directory of all four tools and practical guides
- `/tally/`, `/carve/`, `/keys/`, `/pitch/` — English introductions, with corresponding `/ja/` translations
- `/guides/japanese-lyrics-mora/` and `/guides/audio-loop-seams/` — practical guides, with corresponding `/ja/guides/` translations
- `/404.html` — not-found page

The TALLY and CARVE apps remain in their own GitHub repositories (`Raito-sound/tally` and `Raito-sound/carve`) and publish independently through GitHub Pages. KEYS and PITCH use their existing Sites projects. This repository contains introductions and guides, not copies of the apps.

Edit `scripts/build-tools-pages.py` for bilingual copy, then run `python3 scripts/build-tools-pages.py`. Generated HTML is checked in, so the existing production build needs no new runtime or dependencies. Each translation has its own self-canonical URL and reciprocal English/Japanese hreflang links. Update `sitemap.xml` when adding routes. App and introduction URLs serve different purposes and must not canonicalize to each other.

`tools.html` is an unpublished local draft and is excluded from version control and the site build.

## Publishing

The production site at https://raito.studio/ is hosted on Cloudflare Pages, project `raito-studio`, connected to `Raito-sound/raito-studio` on branch `main`. DNS is managed by Cloudflare.

Run `sh .cloudflare/pages-build.sh` from this directory to produce `_site/`. Cloudflare Pages publishes that output. GitHub Actions uses the same build script for the secondary preview at https://raito-sound.github.io/raito-studio/.

The build explicitly selects public HTML, styles, scripts and assets. Documentation, source Markdown, draft pages and the app repositories are not included in the website artifact.

## App subdomains

The app custom domains use HTTPS. Their Cloudflare CNAME records use DNS-only mode:

- `tally.raito.studio` → `raito-sound.github.io`
- `carve.raito.studio` → `raito-sound.github.io`
- `keys.raito.studio` → `custom-domains.chatgpt.site`
- `pitch.raito.studio` → `custom-domains.chatgpt.site`

The introduction URLs and app URLs serve different purposes; neither redirects to the other. App updates are deployed from each app repository without copying the app into this portfolio.

## トップページと日本語版（`/` と `/ja/`）

トップは `templates/home.html` に `content/i18n/home.en.json` / `home.ja.json` を流し込んで生成する。文面を直すときは JSON を編集して再実行する（`index.html` と `ja/index.html` を直接編集しない）。

```sh
python3 scripts/build-home.py
```

言語の振り分けは `lang.js`。初回訪問だけ `navigator.languages` で `/` か `/ja/` に振り分け、選択は `localStorage` の `site-lang` に保存する。クローラー・`?lang=` 付き・サイト内遷移・`navigator.webdriver` では振り分けない。全ページのヘッダーに EN／日本語 切替（`data-lang-switch`）があり、押すと選択が保存される。各ページは自己 canonical と hreflang（en / ja / x-default）を持つ。

## 作品ページ（works）

作品データの正本はサイト側では `content/works.json`（原本は Notion）。1作品 = 1URL で、英語 `/works/<slug>/` と日本語 `/ja/works/<slug>/` を生成する。

```sh
python3 scripts/build-works-pages.py
```

このコマンドが、作品ページ58本、日本語一覧 `/ja/works/`、英語一覧のリンクと JSON-LD、`sitemap.xml` の works ブロック、`llms.txt` の作品節、隣の `lisarec/content/work-links.json`（ブログと実績一覧からの逆リンク用）を更新する。slug は公開後に変えない。新作は `works.json` に1件足して再実行するだけでよい。

各ページの先頭の一文は「作品名（年・発注元）を、作曲家・来兎（Raito／久場超）が◯◯を担当」の形で固定し、役割は正確に書く（編曲参加を作曲と書かない）。
