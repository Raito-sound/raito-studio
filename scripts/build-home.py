#!/usr/bin/env python3
"""Render the raito.studio home page in English (/) and Japanese (/ja/) from templates/home.html
and content/i18n/home.{en,ja}.json. Numbers and the archive list come from content/works.json."""
from pathlib import Path
from html import escape
import importlib.util, json, re

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://raito.studio'
spec = importlib.util.spec_from_file_location('works_build', ROOT / 'scripts' / 'build-works-pages.py')
wb = importlib.util.module_from_spec(spec); spec.loader.exec_module(wb)
WORKS, DATE, SAME_AS, PERSON = wb.WORKS, wb.DATE, wb.SAME_AS, wb.PERSON
BY_SLUG = {w['slug']: w for w in WORKS}
ARCHIVE = ['raiden-iii-mikado-maniax', 'touhou-project-arrangements', 'legend-of-dark-witch', 'bokuben-study', 'osomatsu-san-hesokuri-wars',
           'blazblue-cross-tag-battle', 'rxn-raijin', 'deathsmiles', 'arcana-heart-2', 'cutie-honey-the-live', 'lucky-star',
           'higurashi-image-albums', 'ragnarok-battle-offline', 'lamune', 'glove-on-fight']
LABEL = {'game': 'GAME', 'animation': 'ANIME', 'drama': 'DRAMA', 'doujin': 'DOJIN'}
TEMPLATE = (ROOT / 'templates' / 'home.html').read_text(encoding='utf-8')


def lang_switch(lang, en_url, ja_url, aria):
    cur = ' aria-current="page"'
    return (f'<nav class="lang-switch" aria-label="{aria}">'
            f'<a href="{en_url}" lang="en" hreflang="en" data-lang-switch="en"{cur if lang == "en" else ""}>EN</a>'
            f'<span aria-hidden="true">/</span>'
            f'<a href="{ja_url}" lang="ja" hreflang="ja" data-lang-switch="ja"{cur if lang == "ja" else ""}>日本語</a></nav>')


def jsonld(lang, url, strings):
    person = {
        '@type': 'Person', '@id': PERSON, 'name': 'Raito' if lang == 'en' else '来兎',
        'alternateName': ['来兎', 'らいと', 'RAITO', 'Masaru Kuba', '久場 超'] if lang == 'en' else ['Raito', 'RAITO', 'らいと', '久場 超', 'Masaru Kuba'],
        'url': ORIGIN + '/', 'jobTitle': ['Composer', 'Sound Designer'] if lang == 'en' else ['作曲家', 'サウンドデザイナー'],
        'description': ('Japanese game composer and sound designer based in Naha, Okinawa. Active in game music since 1997 and known for the MELTY BLOOD and UNDER NIGHT IN-BIRTH series. Founder and CEO of Lisa-Rec Inc., where he also composes all of the company\'s commercial (CM) music and sound logos.'
                        if lang == 'en' else '沖縄県那覇市を拠点とする日本のゲーム音楽作曲家・サウンドデザイナー。1997年からゲーム音楽を手がけ、『MELTY BLOOD』『UNDER NIGHT IN-BIRTH』シリーズで知られる。株式会社リサレコ代表取締役として、同社のCM音楽・サウンドロゴもすべて作曲している。'),
        'nationality': {'@type': 'Country', 'name': 'Japan'}, 'homeLocation': {'@type': 'Place', 'name': 'Naha, Okinawa, Japan'},
        'worksFor': {'@id': 'https://lisa-rec.net/#org'}, 'sameAs': SAME_AS,
        'knowsAbout': ['Game music', 'Fighting game music', 'Anime music', 'Sound design', 'Sound effects'] if lang == 'en' else ['ゲーム音楽', '対戦格闘ゲーム音楽', 'アニメ音楽', 'サウンドデザイン', '効果音'],
    }
    data = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebSite', '@id': ORIGIN + '/#website', 'url': ORIGIN + '/', 'name': 'Raito.studio',
         'description': 'Official website of Japanese composer and sound designer Raito (来兎).', 'inLanguage': ['en', 'ja'],
         'about': {'@id': PERSON}, 'dateModified': DATE},
        {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': strings['title'], 'description': strings['meta_description'],
         'inLanguage': lang, 'isPartOf': {'@id': ORIGIN + '/#website'}, 'about': {'@id': PERSON}, 'dateModified': DATE},
        person,
        {'@type': 'Organization', '@id': 'https://lisa-rec.net/#org', 'name': 'Lisa-Rec Inc.' if lang == 'en' else '株式会社リサレコ',
         'alternateName': '株式会社リサレコ' if lang == 'en' else 'Lisa-Rec Inc.', 'url': 'https://lisa-rec.net/', 'founder': {'@id': PERSON}, 'foundingDate': '2010-03'},
    ]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + '</script>'


def archive_list(lang):
    rows = []
    for slug in ARCHIVE:
        w = BY_SLUG[slug]
        years = wb.years(w, 'en') if lang == 'en' else wb.years(w, 'ja')
        title = w['title_en'] if lang == 'en' else w['title_ja']
        roles = w['roles_en'] if lang == 'en' else w['roles_ja']
        rows.append(f'<article><span>{escape(years)}</span><h3><a href="{wb.path_for(slug, lang)}">{escape(title)}</a></h3><p>{escape(roles)}</p><b>{LABEL[w["type"]]}</b></article>')
    return '<div class="archive-list">\n          ' + '\n          '.join(rows) + '\n        </div>'


def strip_empty_headings(html):
    return html.replace('<h2 id="practice-title" class="reveal"></h2>', '')


def render(lang):
    strings = json.loads((ROOT / 'content' / 'i18n' / f'home.{lang}.json').read_text(encoding='utf-8'))
    url = ORIGIN + ('/' if lang == 'en' else '/ja/')
    en_url, ja_url = '/', '/ja/'
    n = len(WORKS)
    strings['index_link'] = re.sub(r'<b>\d+ ?[^<]*</b>', f'<b>{n}{" " if lang == "en" else ""}{strings["index_label_projects"]}</b>', strings['index_link'])
    strings['archive_summary'] = re.sub(r'<b>\d+ ?[^<]*</b>', f'<b>{len(ARCHIVE)}{" " if lang == "en" else ""}{strings["archive_label_credits"]}</b>', strings['archive_summary'])
    values = dict(strings)
    values.update({
        'lang': lang, 'url': url, 'press_lang': lang,
        'tools_prefix': '' if lang == 'en' else 'ja/', 'tools_alt_prefix': 'ja/' if lang == 'en' else '',
        'alternates': (f'<link rel="canonical" href="{url}">\n  <link rel="alternate" hreflang="en" href="{ORIGIN}/">\n  '
                       f'<link rel="alternate" hreflang="ja" href="{ORIGIN}/ja/">\n  <link rel="alternate" hreflang="x-default" href="{ORIGIN}/">'),
        'og_locale': (f'<meta property="og:locale" content="{"en_US" if lang == "en" else "ja_JP"}">\n  '
                      f'<meta property="og:locale:alternate" content="{"ja_JP" if lang == "en" else "en_US"}">'),
        'jsonld': jsonld(lang, url, strings),
        'lang_switch': lang_switch(lang, en_url, ja_url, strings['lang_switch_aria']),
        'archive_list': archive_list(lang),
    })
    html = TEMPLATE
    for _ in range(2):  # values may contain {{tools_prefix}} etc.
        html = re.sub(r'\{\{([a-z_0-9]+)\}\}', lambda m: values[m.group(1)], html)
    assert '{{' not in html, re.findall(r'\{\{[^}]+\}\}', html)[:5]
    dest = ROOT / ('index.html' if lang == 'en' else 'ja/index.html')
    dest.parent.mkdir(parents=True, exist_ok=True)
    html = strip_empty_headings(html)
    dest.write_text(html, encoding='utf-8')


if __name__ == '__main__':
    render('en'); render('ja')
    print('Rendered / and /ja/ home pages.')
