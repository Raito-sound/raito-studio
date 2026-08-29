# Raito.studio — Requirements

Last updated: 2026-08-22

## Purpose

Raito.studio is Raito’s English-language personal website for international game and anime work. It establishes Raito as an Okinawa-based composer and sound designer whose fighting-game music has a life beyond the game itself.

## Audience

- Overseas game developers and publishers
- Anime and screen producers
- Music press, event organizers and interviewers
- Players searching for the composer behind MELTY BLOOD and UNDER NIGHT IN-BIRTH

## Site relationship

- Raito.studio: international and English-language inquiries for game and anime work
- lisa-rec.net: Japanese commercial music, sound logos and music for spaces
- Both sites must link to each other and identify Raito as founder and CEO of Lisa-Rec Inc.

## Design direction

- Preserve the strongest ideas from Claude’s Design Concept D3: warm paper, vermilion accent, large typography and a generative wire-wave motif.
- Improve legibility with larger body copy, higher contrast and clearer information hierarchy.
- Use the supplied `raito-logo.svg` as the primary identity in the header and hero.
- Present the four lead works with high-resolution promotional, package or jacket artwork, a strong readability overlay and direct links to each official title page.
- Use the supplied `アー写.jpg` in the profile, cropped non-destructively around Raito.
- Avoid generic stock imagery. Use supplied identity assets, credited work artwork, typography, grids, signal patterns and code-native motion.
- Respect reduced-motion preferences and keep all interactions keyboard accessible.

## Content source of truth

- Site copy: Notion page “Raito.studio｜サイト文章”
- Credits: Notion game/anime works database and the English press kit
- Press facts: `press/Raito_PressKit_2026-08_EN.md`
- The full works list and figures should not be manually changed without checking those sources.

## AI and search requirements

- Use full names and alternate names: Raito, 来兎, RAITO, Masaru Kuba and 久場 超.
- Provide explicit Person, Organization and WebSite JSON-LD.
- Explain the relationship between Raito and Lisa-Rec Inc. in visible copy and machine-readable data.
- Maintain `llms.txt`, `robots.txt`, `sitemap.xml`, canonical metadata and descriptive page metadata.
- Keep important career facts in text, not only in decorative graphics.

## Primary pages

- `/` — portfolio, profile and contact
- `/works/` — complete, searchable game/anime/drama/doujin project index generated from the Notion works database
- `/press/` — press kit

## Deferred pages

- `/tools.html` — creator tools; retained as a working draft and excluded from launch navigation until its content and destinations are complete

## Contact rule

The contact section displays the email address and official social links without additional sales copy.
