#!/usr/bin/env python3
"""Render one static page per work (English and Japanese) from content/works.json.

Also: links the English works index to the new pages, regenerates its ItemList
JSON-LD, writes the Japanese works index, updates sitemap.xml and llms.txt,
and exports content/work-links.json for the lisa-rec.net repository so its
blog posts and works list can link back to these pages.
"""
from pathlib import Path
from html import escape, unescape
from urllib.parse import quote
import json
import re

ROOT = Path(__file__).resolve().parents[1]
LISAREC = ROOT.parent / 'lisarec'
ORIGIN = 'https://raito.studio'
PERSON = ORIGIN + '/#person'
DATA = json.loads((ROOT / 'content' / 'works.json').read_text(encoding='utf-8'))
WORKS = DATA['works']
DATE = DATA['reviewed']
CSS_V = 'lang-20260911'

SAME_AS = [
    'https://lisa-rec.net/',
    'https://www.wikidata.org/wiki/Q11523677',
    'https://ja.wikipedia.org/wiki/%E6%9D%A5%E5%85%8E',
    'https://vgmdb.net/artist/1585',
    'https://www.imdb.com/name/nm9311908/',
    'https://x.com/lisa_rec',
    'https://www.youtube.com/@raitosound',
    'https://www.instagram.com/raito_sound/',
    'https://open.spotify.com/artist/4gvNo6XIRTD2N0l75sY6II',
    'https://raito-sound.bandcamp.com/',
]

TYPE_LABEL = {
    'en': {'game': 'Game', 'animation': 'Animation', 'drama': 'TV drama', 'doujin': 'Doujin'},
    'ja': {'game': 'ゲーム', 'animation': 'アニメ', 'drama': 'TVドラマ', 'doujin': '同人'},
}

PERSON_BLURB = {
    'en': 'Raito (来兎) is the composer name of Masaru Kuba (久場 超), a Japanese game composer and sound designer based in Naha, Okinawa. He has written game music since 1997, is best known for the MELTY BLOOD and UNDER NIGHT IN-BIRTH series, and is the founder and CEO of Lisa-Rec Inc. (株式会社リサレコ). He also composes all of the commercial (CM) music and sound logos produced by Lisa-Rec Inc. in Japan: more than 150 since 2010.',
    'ja': '来兎（らいと）は、久場 超（くば まさる）の作曲家としての名義です。沖縄県那覇市を拠点に1997年からゲーム音楽を手がけ、『MELTY BLOOD』『UNDER NIGHT IN-BIRTH』シリーズで知られます。株式会社リサレコの代表取締役でもあり、同社が手がけたCM音楽・サウンドロゴ（2010年〜2026年、150件以上）もすべて来兎が作曲しています。英字クレジットは Raito または RAITO、Masaru Kuba。',
}


def path_for(slug, lang):
    return f'/{"ja/" if lang == "ja" else ""}works/{slug}/'


def years(w, lang):
    if w['year_end']:
        return f'{w["year"]}–{w["year_end"]}' if lang == 'en' else f'{w["year"]}〜{w["year_end"]}年'
    return w['year'] if lang == 'en' else f'{w["year"]}年'


def title(w, lang):
    return w['title_en'] if lang == 'en' else w['title_ja']


def credit_sentence(w, lang):
    if lang == 'en':
        return ('Raito (来兎, real name Masaru Kuba), a Japanese game composer and sound designer based in Okinawa '
                'and founder of Lisa-Rec Inc., ' + w['did_en'])
    return '沖縄・那覇を拠点とする作曲家・来兎（らいと、本名：久場 超。株式会社リサレコ代表取締役）は、' + w['did_ja']


def page_title(w, lang):
    if lang == 'en':
        return f'{w["title_en"]} — {w["roles_en"]}: Raito (来兎)'
    return f'{w["title_ja"]}｜{w["roles_ja"]}: 来兎（Raito）'


def description(w, lang):
    if lang == 'en':
        return f'Raito (来兎, Masaru Kuba), Japanese game composer from Okinawa, {w["did_en"]}'
    return f'作曲家・来兎（Raito／久場超）は、{w["did_ja"]}'


# ---------- blog cross-references (lisa-rec.net) ----------

def keyword_pattern(keyword):
    if re.fullmatch(r'[A-Za-z0-9 :\-!.]+', keyword):
        return re.compile(r'(?<![A-Za-z0-9])' + re.escape(keyword) + r'(?![A-Za-z0-9])')
    return re.compile(re.escape(keyword))


def load_blog_posts():
    posts = []
    for source in sorted((LISAREC / 'content' / 'blog').glob('*.json')):
        d = json.loads(source.read_text(encoding='utf-8'))
        text = d['title'] + ' ' + ' '.join(unescape(re.sub(r'<[^>]+>', ' ', b.get('html', ''))) for b in d.get('blocks', []))
        posts.append({'slug': d['slug'], 'title': d['title'], 'published': d['published'], 'text': text,
                      'url': f'https://lisa-rec.net/post/{quote(d["slug"], safe="-._~")}/'})
    posts.sort(key=lambda p: p['published'], reverse=True)
    return posts


def related_posts(w, posts, limit=5):
    patterns = [keyword_pattern(k) for k in w['blog_keywords']]
    hits = [p for p in posts if any(pat.search(p['text']) for pat in patterns)]
    return hits[:limit], len(hits)


# ---------- page rendering ----------

def person_node(lang):
    return {
        '@type': 'Person', '@id': PERSON,
        'name': 'Raito' if lang == 'en' else '来兎',
        'alternateName': ['来兎', 'らいと', 'RAITO', 'Masaru Kuba', '久場 超'] if lang == 'en' else ['Raito', 'RAITO', 'らいと', '久場 超', 'Masaru Kuba'],
        'url': ORIGIN + '/',
        'jobTitle': ['Composer', 'Sound Designer'] if lang == 'en' else ['作曲家', 'サウンドデザイナー'],
        'nationality': {'@type': 'Country', 'name': 'Japan'},
        'homeLocation': {'@type': 'Place', 'name': 'Naha, Okinawa, Japan'},
        'worksFor': {'@type': 'Organization', '@id': 'https://lisa-rec.net/#org', 'name': 'Lisa-Rec Inc.' if lang == 'en' else '株式会社リサレコ', 'url': 'https://lisa-rec.net/'},
        'sameAs': SAME_AS,
    }


def work_node(w):
    node = {
        '@type': w['schema_type'], '@id': ORIGIN + f'/works/{w["slug"]}/#work',
        'name': w['title_en'],
        'alternateName': [t for t in [w['title_ja']] + w['alt_titles'] if t and t != w['title_en']],
        'datePublished': w['year'],
        'genre': TYPE_LABEL['en'][w['type']],
        'contributor': {'@id': PERSON},
    }
    if w['year_end']:
        node['temporalCoverage'] = f'{w["year"]}/{w["year_end"]}'
    if w['client_en']:
        key = 'publisher' if w['schema_type'] in ('VideoGame', 'MusicAlbum', 'CreativeWork') else 'productionCompany'
        node[key] = {'@type': 'Organization', 'name': w['client_en']}
    if w['official_url']:
        node['url'] = w['official_url']
    if w.get('installments'):
        node['hasPart'] = [{'@type': w['schema_type'], '@id': ORIGIN + f'/works/{w["slug"]}/#{i["id"]}', 'name': i['name_en'],
                            'datePublished': i['year'], 'musicBy': {'@id': PERSON}, 'contributor': {'@id': PERSON},
                            'description': f'{i["role_en"]} by Raito (来兎).'} for i in w['installments']]
    musical = {'composer', 'arranger', 'remixer'} & set(w['role_keys'])
    if musical and w['schema_type'] in ('VideoGame', 'TVSeries'):
        node['musicBy'] = {'@id': PERSON}
    if musical and w['schema_type'] == 'MusicAlbum':
        node['creator'] = {'@id': PERSON}
    return node


def faq(w, lang):
    if lang == 'en':
        items = [(f'Who did the music for {w["title_en"]}?', credit_sentence(w, 'en')),
                 (f'What was Raito’s role on {w["title_en"]}?', f'{w["roles_en"]}. {w["summary_en"]} Credited as {w["credited_as"]}.')]
        if w['year_end']:
            items.append((f'Which years does the credit cover?', f'{w["year"]} to {w["year_end"]}.'))
        for i in w.get('installments', []):
            items.append((f'Who did the music for {i["name_en"]}?', f'{i["role_en"]} of {i["name_en"]} ({i["year"]}) by Raito (来兎, Masaru Kuba).'))
    else:
        items = [(f'『{w["title_ja"]}』の音楽は誰が担当しましたか？', credit_sentence(w, 'ja')),
                 ('来兎の担当範囲は？', f'{w["roles_ja"]}。{w["summary_ja"]}クレジット表記は {w["credited_as"]}。')]
        if w['year_end']:
            items.append(('担当した期間は？', f'{w["year"]}年から{w["year_end"]}年まで。'))
        for i in w.get('installments', []):
            items.append((f'『{i["name_ja"]}』の音楽は誰が担当しましたか？', f'『{i["name_ja"]}』（{i["year"]}年）の{i["role_ja"]}を来兎（久場 超）が担当しました。'))
    return items


def render_work(w, lang, posts):
    is_ja = lang == 'ja'
    url = ORIGIN + path_for(w['slug'], lang)
    en, ja = ORIGIN + path_for(w['slug'], 'en'), ORIGIN + path_for(w['slug'], 'ja')
    t = title(w, lang)
    doc_title = page_title(w, lang)
    desc = description(w, lang)
    faq_items = faq(w, lang)
    graph = [
        {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': doc_title, 'description': desc,
         'inLanguage': lang, 'dateModified': DATE, 'isPartOf': {'@id': ORIGIN + '/#website'},
         'about': {'@id': ORIGIN + f'/works/{w["slug"]}/#work'},
         'breadcrumb': {'@type': 'BreadcrumbList', 'itemListElement': [
             {'@type': 'ListItem', 'position': 1, 'name': 'Raito.studio', 'item': ORIGIN + '/'},
             {'@type': 'ListItem', 'position': 2, 'name': 'Works', 'item': ORIGIN + ('/ja/works/' if is_ja else '/works/')},
             {'@type': 'ListItem', 'position': 3, 'name': t, 'item': url}]}},
        work_node(w), person_node(lang),
        {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq_items]},
    ]
    data = {'@context': 'https://schema.org', '@graph': graph}
    ld = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')

    cur = ' aria-current="page"'
    lang_switch = (f'<a href="{path_for(w["slug"], "en")}" lang="en" hreflang="en"{"" if is_ja else cur}>English</a>'
                   f'<span aria-hidden="true">/</span>'
                   f'<a href="{path_for(w["slug"], "ja")}" lang="ja" hreflang="ja"{cur if is_ja else ""}>日本語</a>')
    works_path = '/ja/works/' if is_ja else '/works/'
    cat = f'WORKS / {TYPE_LABEL["en"][w["type"]].upper()} / {years(w, "en")}'

    facts = [(('Year', 'Medium', 'Client', 'Role', 'Credited as') if not is_ja else ('年', '媒体', '発注元', '担当', 'クレジット表記'))]
    facts = list(zip(facts[0], [years(w, lang), TYPE_LABEL[lang][w['type']], w['client_en'] if not is_ja else w['client_ja'], w['roles_en'] if not is_ja else w['roles_ja'], w['credited_as']]))
    facts_html = ''.join(f'<div><dt>{escape(k)}</dt><dd>{escape(v)}</dd></div>' for k, v in facts if v)

    actions = ''
    if w['official_url']:
        actions += f'<a class="app-open" href="{escape(w["official_url"])}" rel="noopener">{"公式サイト" if is_ja else "Official site"} <span aria-hidden="true">↗</span></a>'
    actions += f'<a class="app-secondary" href="{works_path}">{"作品一覧へ" if is_ja else "All works"}</a>'

    faq_html = ''.join(f'<div><dt>{escape(q)}</dt><dd>{escape(a)}</dd></div>' for q, a in faq_items)

    inst_html = ''
    if w.get('installments'):
        rows = ''.join(f'<div id="{i["id"]}"><dt>{escape(i["name_ja"] if is_ja else i["name_en"])} <small>{i["year"]}</small></dt><dd>{escape(i["role_ja"] if is_ja else i["role_en"])}</dd></div>' for i in w['installments'])
        inst_html = f'<section class="app-detail" id="entries"><h2>{"シリーズ各作の担当" if is_ja else "Series entries and credits"}</h2><dl class="app-features">{rows}</dl></section>'
    hits, total = related_posts(w, posts)
    posts_html = ''
    if hits:
        items = ''.join(f'<li><a href="{escape(p["url"])}" hreflang="ja" lang="ja">{escape(p["title"])}</a> <time datetime="{p["published"][:10]}">{p["published"][:10]}</time></li>' for p in hits)
        more = ''
        if total > len(hits):
            more = f'<p class="app-note">{"ほか" + str(total - len(hits)) + "件の記事があります。" if is_ja else f"{total - len(hits)} more posts mention this work."} <a href="https://lisa-rec.net/blog/">{"リサレコブログ" if is_ja else "Lisa-Rec blog (Japanese)"}</a></p>'
        head = '関連するブログ記事（株式会社リサレコ）' if is_ja else 'Related posts on the Lisa-Rec blog (Japanese)'
        posts_html = f'<section class="app-detail"><h2>{head}</h2><ul class="app-steps work-posts">{items}</ul>{more}</section>'

    idx = WORKS.index(w)
    neighbours = [x for x in (WORKS[idx - 1] if idx > 0 else None, WORKS[idx + 1] if idx + 1 < len(WORKS) else None) if x]
    picks = neighbours + [x for x in WORKS if x['featured'] and x is not w and x not in neighbours]
    related = ''.join(f'<a href="{path_for(x["slug"], lang)}">{escape(title(x, lang))} — {escape(x["roles_ja"] if is_ja else x["roles_en"])} · {escape(years(x, lang))}</a>' for x in picks[:5])

    credit_detail = (f'{w["roles_ja"]}。{w["summary_ja"]}クレジット表記は {w["credited_as"]}。' if is_ja
                     else f'{w["roles_en"]}. {w["summary_en"]} Credited as {w["credited_as"]}.')
    source_note = (f'情報確認日: {DATE}。出典: 来兎の公表クレジットとプレスキット（2026年8月）。誤りや更新は contact@raito.studio へ。' if is_ja
                   else f'Information reviewed {DATE}. Source: Raito’s published credits and the August 2026 press kit. Corrections: contact@raito.studio.')

    body = f'''<div class="tools-topline"><nav class="app-breadcrumb" aria-label="Breadcrumb"><a href="/">Raito.studio</a><span aria-hidden="true">/</span><a href="{works_path}">Works</a><span aria-hidden="true">/</span><span>{escape(t)}</span></nav><nav class="language-links" aria-label="Language">{lang_switch}</nav></div>
<article class="work-page-body">
<section class="app-hero"><div><p class="app-category">{cat}</p><h1>{escape(t)}</h1><p class="app-lead">{escape(credit_sentence(w, lang))}</p></div><div class="app-summary"><p>{escape(PERSON_BLURB[lang])}</p><div class="app-actions">{actions}</div></div></section>
<dl class="app-facts">{facts_html}</dl>
<section class="app-detail"><h2>{'担当内容' if is_ja else 'Credit details'}</h2><p class="reading-copy">{escape(credit_detail)}</p></section>
{inst_html}<section class="app-detail"><h2>{'よくある質問' if is_ja else 'Questions'}</h2><dl class="app-features">{faq_html}</dl></section>
{posts_html}
<p class="app-note">{escape(source_note)}</p>
</article>
<aside class="tools-related"><h2>{'来兎のほかの作品' if is_ja else 'More works by Raito'}</h2>{related}</aside>'''

    html = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(doc_title)} | Raito.studio</title>
<meta name="description" content="{escape(desc, quote=True)}">
<meta name="author" content="Raito / 来兎">
<link rel="canonical" href="{url}"><link rel="alternate" hreflang="en" href="{en}"><link rel="alternate" hreflang="ja" href="{ja}"><link rel="alternate" hreflang="x-default" href="{en}">
<meta name="robots" content="index,follow,max-snippet:-1"><meta name="theme-color" content="#efede5">
<meta property="og:type" content="article"><meta property="og:site_name" content="Raito.studio"><meta property="og:locale" content="{'ja_JP' if is_ja else 'en_US'}"><meta property="og:url" content="{url}"><meta property="og:title" content="{escape(doc_title, quote=True)}"><meta property="og:description" content="{escape(desc, quote=True)}"><meta property="og:image" content="{ORIGIN}/og-raito.png"><meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/site.css?v={CSS_V}"><link rel="stylesheet" href="/apps.css?v={CSS_V}">
<script type="application/ld+json">{ld}</script><script src="/lang.js" defer></script></head>
<body id="top" class="app-page work-page"><a class="skip-link" href="#main">{'本文へ' if is_ja else 'Skip to content'}</a>
<header class="site-header"><a class="brand" href="/" aria-label="Raito.studio home"><img src="/assets/raito-logo.svg" alt="Raito / 来兎" width="84" height="44"></a><nav aria-label="{'メインナビゲーション' if is_ja else 'Primary navigation'}"><a href="/">Home</a><a href="{works_path}" aria-current="true">Works</a><a href="{'/ja/tools/' if is_ja else '/tools/'}">Tools</a><a href="/press/?lang={'ja' if is_ja else 'en'}">Press</a></nav><div class="header-right"><nav class="lang-switch" aria-label="Language"><a href="{path_for(w["slug"], "en")}" lang="en" hreflang="en" data-lang-switch="en"{"" if is_ja else cur}>EN</a><span aria-hidden="true">/</span><a href="{path_for(w["slug"], "ja")}" lang="ja" hreflang="ja" data-lang-switch="ja"{cur if is_ja else ""}>日本語</a></nav><a class="header-contact" href="{'/ja/#contact' if is_ja else '/#contact'}">{'お問い合わせ' if is_ja else 'Contact'} ↗</a></div></header>
<main id="main" class="app-main">{body}</main>
<footer><span>© 2026 RAITO.STUDIO</span><a href="{works_path}">{'作品一覧' if is_ja else 'ALL WORKS'}</a><a href="#top">{'ページ先頭へ' if is_ja else 'BACK TO TOP'} ↑</a></footer></body></html>
'''
    dest = ROOT / path_for(w['slug'], lang).strip('/') / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding='utf-8')


def render_ja_index():
    url = ORIGIN + '/ja/works/'
    doc_title = '来兎（Raito）作品一覧｜ゲーム・アニメ・ドラマ音楽の担当作品'
    desc = f'作曲家・来兎（Raito／久場超）が音楽・効果音を担当したゲーム、アニメ、TVドラマ、同人作品{len(WORKS)}件の一覧。各作品の年、発注元、担当範囲を記載。'
    groups = [('game', 'ゲーム'), ('animation', 'アニメ'), ('drama', 'TVドラマ'), ('doujin', '同人')]
    sections = ''
    for key, label in groups:
        items = [w for w in WORKS if w['type'] == key]
        rows = ''.join(f'<div><dt><a href="{path_for(w["slug"], "ja")}">{escape(w["title_ja"])}</a> <small>{escape(years(w, "ja"))}</small></dt><dd>{escape(w["roles_ja"])}。{escape(w["summary_ja"])}</dd></div>' for w in items)
        sections += f'<section class="app-detail"><h2>{label} <small>{len(items)}件</small></h2><dl class="app-features">{rows}</dl></section>'
    data = {'@context': 'https://schema.org', '@type': 'CollectionPage', '@id': url + '#page', 'url': url, 'name': doc_title,
            'description': desc, 'inLanguage': 'ja', 'dateModified': DATE, 'isPartOf': {'@id': ORIGIN + '/#website'},
            'about': {'@id': PERSON},
            'mainEntity': {'@type': 'ItemList', 'name': '来兎 作品一覧', 'numberOfItems': len(WORKS),
                           'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': ORIGIN + path_for(w['slug'], 'ja'), 'name': w['title_ja']} for i, w in enumerate(WORKS)]}}
    ld = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    html = f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(doc_title)} | Raito.studio</title>
<meta name="description" content="{escape(desc, quote=True)}">
<link rel="canonical" href="{url}"><link rel="alternate" hreflang="en" href="{ORIGIN}/works/"><link rel="alternate" hreflang="ja" href="{url}"><link rel="alternate" hreflang="x-default" href="{ORIGIN}/works/">
<meta name="robots" content="index,follow,max-snippet:-1"><meta name="theme-color" content="#efede5">
<meta property="og:type" content="website"><meta property="og:site_name" content="Raito.studio"><meta property="og:locale" content="ja_JP"><meta property="og:url" content="{url}"><meta property="og:title" content="{escape(doc_title, quote=True)}"><meta property="og:description" content="{escape(desc, quote=True)}"><meta property="og:image" content="{ORIGIN}/og-raito.png"><meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/site.css?v={CSS_V}"><link rel="stylesheet" href="/apps.css?v={CSS_V}">
<script type="application/ld+json">{ld}</script><script src="/lang.js" defer></script></head>
<body id="top" class="app-page work-page"><a class="skip-link" href="#main">本文へ</a>
<header class="site-header"><a class="brand" href="/" aria-label="Raito.studio home"><img src="/assets/raito-logo.svg" alt="Raito / 来兎" width="84" height="44"></a><nav aria-label="メインナビゲーション"><a href="/">Home</a><a href="/ja/works/" aria-current="page">Works</a><a href="/ja/tools/">Tools</a><a href="/press/?lang=ja">Press</a></nav><div class="header-right"><nav class="lang-switch" aria-label="言語"><a href="/works/" lang="en" hreflang="en" data-lang-switch="en">EN</a><span aria-hidden="true">/</span><a href="/ja/works/" lang="ja" hreflang="ja" data-lang-switch="ja" aria-current="page">日本語</a></nav><a class="header-contact" href="/ja/#contact">お問い合わせ ↗</a></div></header>
<main id="main" class="app-main"><div class="tools-topline"><nav class="app-breadcrumb" aria-label="Breadcrumb"><a href="/ja/">Raito.studio</a><span aria-hidden="true">/</span><span>Works</span></nav><nav class="language-links" aria-label="Language"><a href="/works/" lang="en" hreflang="en">English</a><span aria-hidden="true">/</span><a href="/ja/works/" lang="ja" hreflang="ja" aria-current="page">日本語</a></nav></div>
<section class="tools-intro"><p class="app-category">RAITO / WORKS</p><h1>来兎の作品一覧</h1><p class="app-lead">{escape(desc)}</p><p>{escape(PERSON_BLURB['ja'])}</p><a class="app-secondary" href="https://lisa-rec.net/#works">CM音楽・サウンドロゴ（150件以上、すべて来兎が作曲）は株式会社リサレコのサイトへ ↗</a></section>
{sections}
<p class="app-note">情報確認日: {DATE}。出典: 来兎の公表クレジットとプレスキット（2026年8月）。</p></main>
<footer><span>© 2026 RAITO.STUDIO</span><a href="/works/">COMPLETE WORKS (EN)</a><a href="#top">ページ先頭へ ↑</a></footer></body></html>
'''
    dest = ROOT / 'ja' / 'works' / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding='utf-8')


# ---------- patches to existing files ----------

INDEX_LABEL = {'game': 'GAME', 'animation': 'ANIMATION', 'drama': 'TV DRAMA', 'doujin': 'DOUJIN'}


def index_entry(i, w):
    cls = 'work-entry reveal' + (' featured' if w['featured'] else '')
    label = INDEX_LABEL[w['type']] + (' / FEATURED' if w['featured'] else '')
    search = ' '.join(x for x in [w['year'], w['year_end'], w['title_en'], w['title_ja'], w['client_en'], w['client_ja'], w['roles_en'], w['roles_ja'], INDEX_LABEL[w['type']].lower()] + w['alt_titles'] if x).lower()
    small = f'<small lang="ja">{escape(w["title_ja"])}</small>' if w['title_ja'] != w['title_en'] else ''
    client = f'<div><dt>Client</dt><dd>{escape(w["client_en"])}</dd></div>' if w['client_en'] else ''
    return (f'        <article class="{cls}" data-category="{w["type"]}" data-search="{escape(search, quote=True)}">\n'
            f'          <span class="work-no">{i:03d}</span><time datetime="{w["year"]}">{w["year"]}</time>'
            f'<div class="work-title"><span>{label}</span><h3><a href="{path_for(w["slug"], "en")}">{escape(w["title_en"])}</a></h3>{small}</div>'
            f'<p>{escape(w["summary_en"])}</p><dl><div><dt>Role</dt><dd>{escape(w["roles_en"])}</dd></div>{client}</dl>\n'
            f'        </article>\n')


def patch_en_index():
    """Regenerate the list, counts and JSON-LD of works/index.html from works.json (the hero copy stays hand-written)."""
    path = ROOT / 'works' / 'index.html'
    html = path.read_text(encoding='utf-8')
    n = len(WORKS)
    counts = {k: sum(1 for w in WORKS if w['type'] == k) for k in INDEX_LABEL}
    years = sorted(int(w['year']) for w in WORKS)
    latest = max(int(w['year_end'] or w['year']) for w in WORKS)

    entries = ''.join(index_entry(i + 1, w) for i, w in enumerate(WORKS))
    html, c = re.subn(r'(<div class="works-list" id="works-list">\n).*?(\s*<p class="empty-state")', lambda m: m.group(1) + entries + m.group(2), html, count=1, flags=re.S)
    assert c == 1, 'works-list block not found'

    html = re.sub(r'<strong>\d+</strong><span>PROJECT RECORDS</span>', f'<strong>{n}</strong><span>PROJECT RECORDS</span>', html)
    html = re.sub(r'<span>\d{4}—\d{4}</span>', f'<span>{years[0]}—{latest}</span>', html, count=1)
    for key, name in [('game', 'Game'), ('animation', 'Animation'), ('drama', 'Drama'), ('doujin', 'Doujin')]:
        html = re.sub(rf'<dt>{name}</dt><dd>\d+</dd>', f'<dt>{name}</dt><dd>{counts[key]}</dd>', html)
        html = re.sub(rf'(data-filter="{key}" aria-pressed="false">{name} <span>)\d+', lambda m: m.group(1) + str(counts[key]), html)
    html = re.sub(r'(data-filter="all" aria-pressed="true">All <span>)\d+', lambda m: m.group(1) + str(n), html)
    html = re.sub(r'<p id="result-count" aria-live="polite">\d+ projects shown</p>', f'<p id="result-count" aria-live="polite">{n} projects shown</p>', html)
    html = re.sub(r'content="\d+ game, animation, drama and doujin projects', f'content="{n} game, animation, drama and doujin projects', html)
    html = html.replace('Raito (来兎) is an Okinawa-based composer and sound designer active since 1997.',
                        'Raito (来兎, real name Masaru Kuba) is a Japanese composer and sound designer based in Okinawa, active in game music since 1997.')
    html = html.replace('content="The complete works index of Okinawa-based composer and sound designer Raito, covering',
                        'content="The complete works index of Japanese composer and sound designer Raito (来兎), based in Okinawa, covering')

    alternates = ('<link rel="canonical" href="https://raito.studio/works/">'
                  '<link rel="alternate" hreflang="en" href="https://raito.studio/works/">'
                  '<link rel="alternate" hreflang="ja" href="https://raito.studio/ja/works/">'
                  '<link rel="alternate" hreflang="x-default" href="https://raito.studio/works/">')
    html = re.sub(r'<link rel="canonical" href="https://raito.studio/works/">(<link rel="alternate"[^>]*>)*', alternates, html, count=1)
    switch = '<nav class="language-links" aria-label="Language"><a href="/works/" lang="en" hreflang="en" aria-current="page">English</a><span aria-hidden="true">/</span><a href="/ja/works/" lang="ja" hreflang="ja">日本語</a></nav>'
    if 'class="language-links"' not in html:
        html = re.sub(r'(<span>\d{4}—\d{4}</span>)</div>', lambda m: m.group(1) + switch + '</div>', html, count=1)
    header_switch = '<div class="header-right"><nav class="lang-switch" aria-label="Language"><a href="/works/" lang="en" hreflang="en" data-lang-switch="en" aria-current="page">EN</a><span aria-hidden="true">/</span><a href="/ja/works/" lang="ja" hreflang="ja" data-lang-switch="ja">日本語</a></nav><a class="header-contact" href="../#contact">Contact <span aria-hidden="true">↗</span></a></div>'
    if 'class="lang-switch"' not in html:
        html = html.replace('<a class="header-contact" href="../#contact">Contact <span aria-hidden="true">↗</span></a>', header_switch, 1)
    if 'lang.js' not in html:
        html = html.replace("<script>document.documentElement.classList.add('js')</script>", "<script>document.documentElement.classList.add('js')</script>\n  <script src=\"/lang.js\" defer></script>", 1)

    items = [{'@type': 'ListItem', 'position': i + 1, 'url': ORIGIN + path_for(w['slug'], 'en'),
              'item': {'@type': w['schema_type'], '@id': ORIGIN + f'/works/{w["slug"]}/#work', 'name': w['title_en'],
                       **({'alternateName': w['title_ja']} if w['title_ja'] != w['title_en'] else {}),
                       'datePublished': w['year'], 'genre': TYPE_LABEL['en'][w['type']], 'url': ORIGIN + path_for(w['slug'], 'en'),
                       'description': w['summary_en'], 'contributor': {'@id': PERSON}}} for i, w in enumerate(WORKS)]
    data = {'@context': 'https://schema.org', '@type': 'CollectionPage', '@id': ORIGIN + '/works/#page', 'url': ORIGIN + '/works/',
            'name': 'Complete Works — Raito / 来兎',
            'description': 'The complete published project index of Japanese composer and sound designer Raito (来兎), based in Okinawa.',
            'inLanguage': 'en', 'dateModified': DATE, 'about': {'@id': PERSON}, 'isPartOf': {'@id': ORIGIN + '/#website'},
            'mainEntity': {'@type': 'ItemList', 'name': 'Raito complete works index', 'numberOfItems': n,
                           'itemListOrder': 'https://schema.org/ItemListOrderDescending', 'itemListElement': items}}
    ld = '<script type="application/ld+json">\n  ' + json.dumps(data, ensure_ascii=False, indent=2).replace('\n', '\n  ').replace('</', '<\\/') + '\n  </script>'
    html, c = re.subn(r'<script type="application/ld\+json">.*?</script>', lambda m: ld, html, count=1, flags=re.S)
    assert c == 1
    path.write_text(html, encoding='utf-8')


def patch_homepage():
    path = ROOT / 'index.html'
    html = path.read_text(encoding='utf-8')
    html = re.sub(r'<b>\d+ PROJECTS</b>', f'<b>{len(WORKS)} PROJECTS</b>', html)
    path.write_text(html, encoding='utf-8')


def patch_sitemap():
    path = ROOT / 'sitemap.xml'
    xml = path.read_text(encoding='utf-8')
    block = ['  <!-- works:start (generated by scripts/build-works-pages.py) -->']
    block.append(f'  <url>\n    <loc>{ORIGIN}/ja/</loc>\n    <lastmod>{DATE}</lastmod>\n  </url>')
    block.append(f'  <url>\n    <loc>{ORIGIN}/ja/works/</loc>\n    <lastmod>{DATE}</lastmod>\n  </url>')
    for w in WORKS:
        for lang in ('en', 'ja'):
            block.append(f'  <url>\n    <loc>{ORIGIN}{path_for(w["slug"], lang)}</loc>\n    <lastmod>{DATE}</lastmod>\n  </url>')
    block.append('  <!-- works:end -->')
    text = '\n'.join(block)
    if '<!-- works:start' in xml:
        xml = re.sub(r'  <!-- works:start.*?<!-- works:end -->', lambda m: text, xml, flags=re.S)
    else:
        xml = xml.replace('</urlset>', text + '\n</urlset>')
    xml = re.sub(r'(<loc>https://raito.studio/works/</loc>\s*<lastmod>)[0-9-]+', lambda m: m.group(1) + DATE, xml)
    path.write_text(xml, encoding='utf-8')


def patch_llms():
    path = ROOT / 'llms.txt'
    text = path.read_text(encoding='utf-8')
    lines = ['## Complete works data', '',
             f'The canonical works list is https://raito.studio/works/ (English) and https://raito.studio/ja/works/ (Japanese). It contains {len(WORKS)} public project records. Each work has its own page in both languages stating the year, medium, client when public, Raito\'s exact role and how he is credited. Information reviewed {DATE}.', '']
    for w in WORKS:
        lines.append(f'- {w["title_en"]} ({years(w, "en")}) — {w["roles_en"]}: {ORIGIN}{path_for(w["slug"], "en")} · 日本語: {ORIGIN}{path_for(w["slug"], "ja")}')
    lines.append('')
    new = '\n'.join(lines)
    text, n = re.subn(r'## Complete works data\n.*?(?=\n## )', lambda m: new, text, count=1, flags=re.S)
    assert n == 1, 'Complete works data section not found in llms.txt'
    path.write_text(text, encoding='utf-8')


def export_lisarec_links():
    """Data for the lisa-rec.net repository: blog cross-links and works-list links."""
    links = [{'slug': w['slug'], 'url': ORIGIN + path_for(w['slug'], 'ja'), 'title_ja': w['title_ja'], 'roles_ja': w['roles_ja'],
              'year': w['year'], 'keywords': w['blog_keywords'], 'lisarec_title': w['lisarec_title']} for w in WORKS]
    dest = LISAREC / 'content' / 'work-links.json'
    dest.write_text(json.dumps({'reviewed': DATE, 'source': 'raito-studio/content/works.json', 'works': links}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    index = LISAREC / 'index.html'
    html = index.read_text(encoding='utf-8')
    linked = 0
    for w in WORKS:
        if not w['lisarec_title']:
            continue
        needle = f'<span class="t">{escape(w["lisarec_title"])}</span>'
        if needle in html:
            html = html.replace(needle, f'<span class="t"><a href="{ORIGIN}{path_for(w["slug"], "ja")}">{escape(w["lisarec_title"])}</a></span>', 1)
            linked += 1
        elif f'<span class="t"><a href="{ORIGIN}{path_for(w["slug"], "ja")}">' not in html:
            print(f'  lisarec row not found: {w["lisarec_title"]}')
    index.write_text(html, encoding='utf-8')
    return linked


def build():
    posts = load_blog_posts() if (LISAREC / 'content' / 'blog').is_dir() else []
    for w in WORKS:
        for lang in ('en', 'ja'):
            render_work(w, lang, posts)
    render_ja_index()
    patch_en_index()
    patch_homepage()
    patch_sitemap()
    patch_llms()
    linked = export_lisarec_links() if LISAREC.is_dir() else 0
    print(f'Rendered {len(WORKS) * 2} work pages + Japanese index; linked EN index, sitemap, llms.txt; lisa-rec rows linked now: {linked}.')


if __name__ == '__main__':
    build()
