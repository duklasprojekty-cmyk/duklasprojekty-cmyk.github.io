#!/usr/bin/env python3
"""Generator statycznej strony Komfortowe Ogrody.

Użycie: python3 tools/build_komfortoweogrody.py
Dane firmy (telefon, godziny, adres) są w słowniku BIZ; style i skrypty w komfortoweogrody/assets/.
Katalog komfortoweogrody/ to przyszły katalog główny domeny komfortoweogrody.pl.
"""
import json, os, html

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'komfortoweogrody')
DOMAIN = 'https://komfortoweogrody.pl'

# ---------- dane firmy (jedno miejsce do zmian) ----------
BIZ = {
    'name': 'Komfortowe Ogrody',
    'legal': 'PPHU OLEJNIK Adrian Olejnik',
    'nip': '891-151-33-75',
    'phone_display': '+48 600 927 502',
    'phone_tel': '+48600927502',
    'email': 'kontakt@komfortoweogrody.pl',
    'street': 'Henryka Sienkiewicza 19',
    'postal': '87-700',
    'city': 'Aleksandrów Kujawski',
    'region': 'kujawsko-pomorskie',
    'gmaps': 'https://maps.google.com/?cid=8841425791970558141',
    'map_embed': 'https://maps.google.com/maps?q=Komfortowe+Ogrody%2C+Henryka+Sienkiewicza+19%2C+87-700+Aleksandr%C3%B3w+Kujawski&z=15&ie=UTF8&output=embed',
    'hours_label': 'Pn–Sob 7:00–18:00',
    'desc': 'Od 2013 roku zakładamy i pielęgnujemy ogrody w Aleksandrowie Kujawskim i okolicach: projekty ogrodów z wizualizacją 3D, kompleksowe wykonanie, nawadnianie, oświetlenie, trawniki i nasadzenia oraz stała pielęgnacja zieleni.',
}
ADDRESS_ONE_LINE = f"{BIZ['street']}, {BIZ['postal']} {BIZ['city']}"

Z = 'https://assets.zyrosite.com/cdn-cgi/image/format=auto,'
S = 'YX4yOl7EzMUqEQBQ/'

def zurl(path, w, h=None, trim=None):
    p = f'w={w}'
    if h: p += f',h={h}'
    p += ',fit=crop'
    if trim: p += f',trim={trim}'
    return f'{Z}{p}/{S}{path}'

def img(path, alt, w, h=None, sizes='100vw', cls='', trim=None, lazy=True, extra='', ratio=None):
    """<img> z srcset (1x / 1.5x / 2x) – obrazy z CDN Zyro w formacie auto (WebP/AVIF)."""
    widths = sorted({w // 2, w, int(w * 1.5), w * 2})
    def hh(ww):
        return round(h * ww / w) if h else None
    srcset = ', '.join(f'{zurl(path, ww, hh(ww), trim)} {ww}w' for ww in widths)
    attrs = [f'src="{zurl(path, w, h, trim)}"', f'srcset="{srcset}"', f'sizes="{sizes}"', f'alt="{html.escape(alt)}"']
    if h: attrs += [f'width="{w}"', f'height="{h}"']
    elif ratio: attrs += [f'width="{w}"', f'height="{round(w/ratio)}"']
    if cls: attrs.append(f'class="{cls}"')
    attrs.append('loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"')
    if extra: attrs.append(extra)
    return '<img ' + ' '.join(attrs) + '>'

LOGO = f'{Z}w=700,fit=crop,q=95/{S}zrzut-ekranu-2025-01-17-132825-A3QOJPlwgGujayMq.png'
HERO = '1-m2Wpy8JeOpFqDGKe.jpg'

# ---------- ikony ----------
I = {
 'calc': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 10h2M12 10h2M16 10h0M8 14h2M12 14h2M16 14h0M8 18h2M12 18h2M16 18h0"/></svg>',
 'sun': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
 'map': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3z"/><path d="M9 3v15M15 6v15"/></svg>',
 'copy': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>',
 'layers': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5M2 12l10 5 10-5"/></svg>',
 'cube': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 16V8a2 2 0 0 0-1-1.7l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7l7 4a2 2 0 0 0 2 0l7-4a2 2 0 0 0 1-1.7z"/><path d="M3.3 7 12 12l8.7-5M12 22V12"/></svg>',
 'medal': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="6"/><path d="M15.5 13.5 17 22l-5-3-5 3 1.5-8.5"/></svg>',
 'phone': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
 'mail': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
 'pin': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
 'clock': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
 'check': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
 'leaf': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.2-6.1C9.6 14.4 12 13 13 12"/></svg>',
 'users': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/></svg>',
 'calendar': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
 'star': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>',
 'arrows': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6-6 6 6 6M15 6l6 6-6 6"/></svg>',
 'expand': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>',
 'x': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>',
 'left': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>',
 'right': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>',
 'hand': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 11V6a2 2 0 0 0-4 0v5M14 10V4a2 2 0 0 0-4 0v6M10 10.5V6a2 2 0 0 0-4 0v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.9-6-2.4l-3.6-3.6a2 2 0 0 1 2.8-2.8L7 15"/></svg>',
 'google': '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M22.6 12.3c0-.8-.1-1.5-.2-2.3H12v4.3h5.9a5 5 0 0 1-2.2 3.3v2.8h3.6c2.1-1.9 3.3-4.8 3.3-8.1z"/><path fill="#34A853" d="M12 23c3 0 5.5-1 7.3-2.7l-3.6-2.8c-1 .7-2.2 1.1-3.7 1.1-2.9 0-5.3-1.9-6.2-4.5H2.1v2.9A11 11 0 0 0 12 23z"/><path fill="#FBBC05" d="M5.8 14.1a6.6 6.6 0 0 1 0-4.2V7H2.1a11 11 0 0 0 0 10z"/><path fill="#EA4335" d="M12 5.4c1.6 0 3.1.6 4.2 1.7l3.2-3.2A11 11 0 0 0 2.1 7l3.7 2.9C6.7 7.3 9.1 5.4 12 5.4z"/></svg>',
}

NAV = [('', 'Strona główna', 'home'), ('oferta/', 'Oferta', 'oferta'), ('galeria/', 'Galeria', 'galeria'), ('rzezba/', 'Rzeźba', 'rzezba'), ('wycena/', 'Wycena', 'wycena'), ('kontakt/', 'Kontakt', 'kontakt')]

# ---------- dane strukturalne (wytyczne, pkt 3) ----------
SERVICES = ['Projektowanie ogrodów', 'Zakładanie ogrodów', 'Pielęgnacja ogrodów', 'Instalacje nawadniające',
            'Oświetlenie ogrodowe', 'Układanie kostki brukowej', 'Trawniki i nasadzenia', 'Oczka wodne',
            'Przycinanie żywopłotów', 'Koszenie trawy']

FAQ = [
    ('Czym zajmuje się firma Komfortowe Ogrody?',
     'Zajmujemy się kompleksowo ogrodami: projektujemy je, zakładamy od podstaw i stale pielęgnujemy. Działamy od 2013 roku, a zaufało nam ponad 150 klientów.'),
    ('Czy przed realizacją przygotowujecie projekt ogrodu?',
     'Tak. Przygotowujemy szkic koncepcyjny oraz wizualizację 3D, dzięki czemu jeszcze przed rozpoczęciem prac widzisz, jak będzie wyglądał Twój ogród.'),
    ('Jakie prace obejmuje zakładanie ogrodu?',
     'Wykonujemy ogród od A do Z: niwelację terenu, instalacje nawadniające, oświetlenie, układanie kostki brukowej, trawniki i nasadzenia oraz oczka wodne.'),
    ('Czy zajmujecie się stałą pielęgnacją ogrodów?',
     'Tak. Formujemy rośliny, przycinamy żywopłoty, kosimy trawę i wykonujemy opryski ochronne roślin, żeby ogród był zadbany przez cały rok.'),
    ('Gdzie działacie i jak się z Wami skontaktować?',
     'Nasza siedziba to ul. Henryka Sienkiewicza 19, 87-700 Aleksandrów Kujawski. Zadzwoń pod numer +48 600 927 502 lub napisz na kontakt@komfortoweogrody.pl – jesteśmy dostępni od poniedziałku do soboty w godzinach 7:00–18:00.'),
]

def faq_ld():
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}

def faq_html():
    items = ''.join(f'''
        <details><summary>{q}<span class="pm" aria-hidden="true"></span></summary><div class="ans"><p>{a}</p></div></details>''' for q, a in FAQ)
    return f'''<section class="section section--sand" id="faq">
    <div class="wrap">
      <div class="section-head reveal">
        <span class="eyebrow eyebrow--dark">Pytania i odpowiedzi</span>
        <h2>Najczęściej <span class="mark">zadawane pytania</span></h2>
        <p>Wszystko, co warto wiedzieć, zanim zaczniemy pracę nad Twoim ogrodem.</p>
      </div>
      <div class="faq" data-stagger>{items}
      </div>
    </div>
  </section>'''

AREA = ['Aleksandrów Kujawski', 'Ciechocinek', 'Toruń', 'Włocławek', 'Nieszawa', 'Raciążek', 'Służewo', 'Bądkowo']

def area_html(root, compact=False):
    chips = ''.join(('<li class="is-hq">' if i == 0 else '<li>') + t + '</li>' for i, t in enumerate(AREA))
    return f'''<section class="section section--sand" id="obszar">
    <div class="wrap area">
      <div class="area__text reveal">
        <span class="eyebrow eyebrow--dark">Obszar działania</span>
        <h2>Aleksandrów Kujawski <span class="mark">i okolice</span></h2>
        <p>Nasza siedziba mieści się w Aleksandrowie Kujawskim. Zakładamy i pielęgnujemy ogrody w mieście i okolicznych miejscowościach, m.in.:</p>
        <ul class="area__list" data-stagger>{chips}</ul>
        <p class="area__note">Twoja miejscowość nie jest na liście? Zadzwoń – dojazd ustalamy indywidualnie.</p>
        <a class="btn btn--primary" href="{root}wycena/">{I['calc']}Zapytaj o wycenę</a>
      </div>
      <div class="area__map reveal" aria-hidden="true">
        <svg viewBox="0 0 400 400"><defs><radialGradient id="rg" cx="50%" cy="50%"><stop offset="0" stop-color="#54bf3f" stop-opacity=".35"/><stop offset="1" stop-color="#54bf3f" stop-opacity="0"/></radialGradient></defs>
          <circle class="ring" cx="200" cy="200" r="150"/><circle class="ring" cx="200" cy="200" r="100"/><circle class="ring" cx="200" cy="200" r="50"/>
          <circle cx="200" cy="200" r="150" fill="url(#rg)"/>
          <g class="pins">
            <g transform="translate(200 200)"><circle r="9" class="hq"/><text y="-18">Aleksandrów Kuj.</text></g>
            <g transform="translate(232 158)"><circle r="5"/><text y="-12">Ciechocinek</text></g>
            <g transform="translate(150 70)"><circle r="5"/><text y="-12">Toruń</text></g>
            <g transform="translate(300 310)"><circle r="5"/><text y="-12">Włocławek</text></g>
            <g transform="translate(286 264)"><circle r="5"/><text y="20">Nieszawa</text></g>
            <g transform="translate(232 226)"><circle r="4"/><text y="-11">Raciążek</text></g>
            <g transform="translate(148 232)"><circle r="4"/><text y="18">Służewo</text></g>
            <g transform="translate(120 320)"><circle r="4"/><text y="18">Bądkowo</text></g>
          </g>
        </svg>
      </div>
    </div>
  </section>'''

def local_business():
    return {
        '@context': 'https://schema.org',
        '@type': 'LocalBusiness',
        'name': BIZ['name'],
        'image': LOGO,
        'logo': LOGO,
        '@id': DOMAIN + '/',
        'url': DOMAIN + '/',
        'description': BIZ['name'],
        'disambiguatingDescription': BIZ['desc'],
        'legalName': BIZ['legal'],
        'taxID': BIZ['nip'].replace('-', ''),
        'foundingDate': '2013',
        'telephone': BIZ['phone_tel'],
        'email': BIZ['email'],
        'address': {
            '@type': 'PostalAddress',
            'addressLocality': BIZ['city'],
            'addressRegion': BIZ['region'],
            'postalCode': BIZ['postal'],
            'streetAddress': BIZ['street'],
            'addressCountry': 'PL',
            'telephone': BIZ['phone_tel'],
        },
        'hasMap': BIZ['gmaps'],
        'areaServed': [{'@type': 'City', 'name': t} for t in AREA],
        'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s}} for s in SERVICES],
        'openingHoursSpecification': [{
            '@type': 'OpeningHoursSpecification',
            'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'opens': '07:00',
            'closes': '18:00',
        }],
        'sameAs': [BIZ['gmaps']],
    }

def breadcrumbs_ld(name, slug):
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Strona główna', 'item': DOMAIN + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': name, 'item': f'{DOMAIN}/{slug}'},
        ],
    }

def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + '\n</script>'

# ---------- szablon ----------
def head(title, desc, slug, root, extra_ld=(), og=None, preload_img=None):
    canonical = f'{DOMAIN}/{slug}'
    og_img = og or zurl(HERO, 1200, 630)
    preload = f'<link rel="preload" as="image" href="{preload_img}" fetchpriority="high">\n' if preload_img else ''
    blocks = [ld(local_business())] + [ld(x) for x in extra_ld]
    return f'''<!DOCTYPE html>
<html lang="pl" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#287319">
<meta name="format-detection" content="telephone=no">
<meta name="geo.region" content="PL-KP">
<meta name="geo.placename" content="{BIZ['city']}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pl_PL">
<meta property="og:site_name" content="{BIZ['name']}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{root}assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
<meta property="og:image:alt" content="Ogród zrealizowany przez Komfortowe Ogrody">
<meta name="twitter:image" content="{og_img}">
<meta name="author" content="{BIZ['name']}">
<link rel="alternate" hreflang="pl" href="{canonical}">
<link rel="manifest" href="{root}manifest.webmanifest">
<link rel="preconnect" href="https://assets.zyrosite.com" crossorigin>
<link rel="preload" href="{root}assets/fonts/lato-700-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/lato-400-latin.woff2" as="font" type="font/woff2" crossorigin>
{preload}<link rel="stylesheet" href="{root}assets/fonts.css">
<link rel="stylesheet" href="{root}assets/style.css">
<script src="{root}assets/main.js" defer></script>
{chr(10).join(blocks)}
</head>
<body>
<a class="skip-link" href="#tresc">Przejdź do treści</a>
'''

def header(active, root):
    lis = '\n'.join(
        f'        <li><a href="{root}{href}"' + (' aria-current="page"' if key == active else '') + f'>{label}</a></li>'
        for href, label, key in NAV)
    return f'''<header class="header">
  <div class="wrap header__bar">
    <a class="logo" href="{root}" aria-label="{BIZ['name']} – strona główna">
      <img src="{LOGO}" alt="{BIZ['name']} logo" width="196" height="96">
    </a>
    <nav class="nav" id="menu" aria-label="Menu główne">
      <ul>
{lis}
      </ul>
    </nav>
    <a class="btn btn--primary header__cta" href="tel:{BIZ['phone_tel']}">{I['phone']}<span>{BIZ['phone_display']}</span></a>
    <button class="burger" type="button" aria-controls="menu" aria-expanded="false" aria-label="Otwórz menu"><span></span><span></span><span></span></button>
  </div>
</header>
'''

def hours_table():
    return '''<table class="hours-table">
            <tr data-days="1,2,3,4,5"><th scope="row">Poniedziałek – piątek</th><td>7:00 – 18:00</td></tr>
            <tr data-days="6"><th scope="row">Sobota</th><td>7:00 – 18:00</td></tr>
            <tr data-days="0"><th scope="row">Niedziela</th><td>zamknięte</td></tr>
          </table>'''

def footer(root):
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <span class="name">{BIZ['name']}</span>
        <p>Tworzymy piękne i funkcjonalne ogrody dla Ciebie. Projekt, wykonanie i pielęgnacja od 2013 roku.</p>
        <a class="gbtn" href="{BIZ['gmaps']}" target="_blank" rel="noopener">{I['google']}Znajdź nas w Google</a>
      </div>
      <div>
        <h2>Kontakt</h2>
        <ul class="nap">
          <li>{I['phone']}<a href="tel:{BIZ['phone_tel']}">{BIZ['phone_display']}</a></li>
          <li>{I['mail']}<a href="mailto:{BIZ['email']}">{BIZ['email']}</a></li>
          <li>{I['pin']}<a href="{BIZ['gmaps']}" target="_blank" rel="noopener">{BIZ['street']},<br>{BIZ['postal']} {BIZ['city']}</a></li>
        </ul>
      </div>
      <div>
        <h2>Godziny otwarcia</h2>
        {hours_table()}
        <p style="margin-top:12px"><span class="open-status"></span></p>
      </div>
      <div>
        <h2>Na skróty</h2>
        <ul>
          <li><a href="{root}oferta/#projektowanie">Projektowanie ogrodów</a></li>
          <li><a href="{root}oferta/#zakladanie">Zakładanie ogrodów</a></li>
          <li><a href="{root}oferta/#pielegnacja">Pielęgnacja ogrodów</a></li>
          <li><a href="{root}galeria/">Realizacje przed i po</a></li>
          <li><a href="{root}rzezba/">Rzeźba ogrodowa</a></li>
          <li><a href="{root}wycena/">Zapytaj o wycenę</a></li>
          <li><a href="{root}oferta/#kalendarz">Kalendarz prac w ogrodzie</a></li>
          <li><a href="{root}kontakt/">Kontakt i dojazd</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__legal">
      <span>© <span data-year>2026</span> {BIZ['name']} · {BIZ['legal']} · NIP: {BIZ['nip']}</span>
      <span>{ADDRESS_ONE_LINE} · <a href="{root}polityka-prywatnosci/">Polityka prywatności</a></span>
    </div>
  </div>
</footer>
<a class="fab" href="tel:{BIZ['phone_tel']}" aria-label="Zadzwoń: {BIZ['phone_display']}">{I['phone']}<span class="fab__tip">Zadzwoń: {BIZ['phone_display']}</span></a>
<nav class="action-bar" aria-label="Szybki kontakt">
  <a href="tel:{BIZ['phone_tel']}">{I['phone']}Zadzwoń</a>
  <a href="{root}wycena/">{I['calc']}Wycena</a>
  <a href="{BIZ['gmaps']}" target="_blank" rel="noopener">{I['pin']}Dojazd</a>
</nav>
</body>
</html>
'''

def page_hero(title_html, lead, crumb, bg_path, root):
    return f'''<section class="page-hero">
    {img(bg_path, '', 1600, 700, cls='page-hero__bg', lazy=False)}
    <div class="wrap">
      <nav class="breadcrumbs" aria-label="Ścieżka nawigacji"><ol><li><a href="{root}">Strona główna</a></li><li aria-current="page">{crumb}</li></ol></nav>
      <h1>{title_html}</h1>
      <p>{lead}</p>
    </div>
  </section>'''

def ba_slider(before, after, n, w=900, h=675, sizes='(min-width: 880px) 600px, 100vw', lazy=True):
    return f'''<div class="ba">
            {img(after, f'Realizacja {n} – po', w, h, sizes=sizes, cls='ba__after', lazy=lazy, extra=f'data-full="{Z}w=1800,fit=scale-down/{S}{after}"')}
            {img(before, f'Realizacja {n} – przed', w, h, sizes=sizes, cls='ba__before', lazy=lazy, extra=f'data-full="{Z}w=1800,fit=scale-down/{S}{before}"')}
            <span class="ba__label ba__label--before">PRZED</span>
            <span class="ba__label ba__label--after">PO</span>
            <span class="ba__line"></span>
            <span class="ba__handle">{I['arrows']}</span>
            <input class="ba__range" type="range" min="0" max="100" value="50" aria-label="Porównanie przed i po – realizacja {n}">
          </div>'''

def cta_band(root):
    return f'''<section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="cta-band reveal">
        <div>
          <h2>Porozmawiajmy o <span class="shine">Twoim ogrodzie</span></h2>
          <p>Chętnie odpowiemy na wszystkie Państwa pytania dotyczące ogrodów. Zadzwoń lub napisz – {BIZ['hours_label']}.</p>
        </div>
        <div class="cta-band__actions">
          <a class="btn btn--white" href="tel:{BIZ['phone_tel']}">{I['phone']}{BIZ['phone_display']}</a>
          <a class="btn btn--ghost" href="{root}wycena/">{I['calc']}Zapytaj o wycenę</a>
        </div>
      </div>
    </div>
  </section>'''

# Polska typografia: „sieroty” (a, i, o, u, w, z, na, do…) łączone twardą spacją z następnym
# słowem, twarda spacja w liczbach, cenach, numerze telefonu i kodzie pocztowym.
import re as _re
NBSP = '\u00a0'
_ORPHANS = r'(?<![\w\-–])(a|i|o|u|w|z|A|I|O|U|W|Z|na|do|od|po|we|ze|za|ku|Na|Do|Od|Po|We|Ze|Za|że|się|nie|Nie)'
_RULES = [
    (_re.compile(_ORPHANS + r' (?=[\wĄąĆćĘęŁłŃńÓóŚśŹźŻż„(])'), lambda m: m.group(1) + NBSP),
    (_re.compile(r'(\d) (\d{3})(?!\d)'), lambda m: m.group(1) + NBSP + m.group(2)),        # 11 849,99
    (_re.compile(r'(\d) (zł|r\.|roku|lat|klientów)'), lambda m: m.group(1) + NBSP + m.group(2)),
    (_re.compile(r'\+48 (\d{3}) (\d{3}) (\d{3})'), lambda m: '+48' + NBSP + m.group(1) + NBSP + m.group(2) + NBSP + m.group(3)),
    (_re.compile(r'(\d{2}-\d{3}) (Aleksandrów)'), lambda m: m.group(1) + NBSP + m.group(2)),
    (_re.compile(r'(\d{1,2}:\d{2}) – (\d{1,2}:\d{2})'), lambda m: m.group(1) + NBSP + '–' + NBSP + m.group(2)),
]
_SKIP = _re.compile(r'(<script\b.*?</script>|<style\b.*?</style>|<textarea\b.*?</textarea>|<[^>]+>)', _re.S)

def polish_typography(html_text):
    parts = _SKIP.split(html_text)
    for i in range(0, len(parts), 2):          # parzyste indeksy = tekst poza tagami
        t = parts[i]
        if not t.strip(): continue
        for rx, fn in _RULES: t = rx.sub(fn, t)
        parts[i] = t
    return ''.join(parts)

def write(rel, content):
    if rel.endswith('.html'): content = polish_typography(content)
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

BEFORE = ['t1-YNqy6NwlwasWv3GP.jpg','k5-Yg2W350pRwFM0447.jpg','k4-AVLpyNlwe3Cvl57Q.png','k2-mxBZW8Jq80trZKo4.jpg','k3-A1awGrO2q0TVEO6A.jpg','g1-YanyPBeboZu9ExQ4.png','d1-m2WpVrL7GVU08G1M.jpg','b1-AQEybVKOb2t1q9q6.jpg','8-YBgray2v8EFNkq1p.jpg','7-YlevO5PpO6ivXg2D.JPG','6-dOqyWNQGwktQbyOz.jpg','5-AE0oLv1RgQHlwe41.jpg','4-mv0DNlqgrGiZnPrG.jpg','3-YBgray2n83iN7rw9.JPG','2-mk3za5k6w7HBvpXB.jpg','1-YX4yKzDqlMfPR9B4.jpg']
AFTER = ['t1a-A0xw0rB1GOs68Z1Q.jpg','k6a-mePvMG9VrRceqqQO.jpg','k4a-AzGebDQ2VeSMN2lX.jpg','k1a-AwvMnP62pqHJrq8m.jpg','img_20240810_144943-dJo6nNvXDOt9Ggvv.jpg','g1a-dJo6nNvRGnF9172e.jpg','d1a-A85wPrbK7wFjbJ2N.jpg','b1a-mk3za5kPE9sx0n3Z.jpg','8a-AoPvjN3LbVI2jGb0.jpg','7a-YX4yKzDpePsqMQb1.JPG','6a-YX4yKzD3jVuna42z.jpg','5a-dOqyWNQRzyS37pjb.jpg','4a-YanyPzNR3kTOz7zn.jpg','3a-d95K8rXwO8T56Gpb.JPG','2a-A85wPrb0ept1DwjM.JPG','1a-AE0oLv1K0rFo7VrW.jpg']

OFFER = [
    ('projektowanie', 'Projektowanie ogrodów', 'Zaprojektujemy ogród zgodnie z Twoimi potrzebami oraz aktualnymi trendami.',
     ['szkic koncepcyjny', 'wizualizacja 3D'], '4375db2d-421f-4512-a314-577c463903e2-A85w1ND26vIWDo2L.png', None),
    ('zakladanie', 'Zakładanie ogrodów', 'Zbudujemy twój ogród od A do Z – kompleksowe wykonanie wszystkich prac.',
     ['niwelacja terenu', 'instalacje nawadniające', 'oświetlenie', 'kostka brukowa', 'trawniki i nasadzenia', 'oczka wodne'],
     '3e2a6648-b152-4c60-9568-30530242ed14-AwvMBZOGD3Fzg7kl.png', None),
    ('pielegnacja', 'Pielęgnacja ogrodów', 'Zapewniamy fachową opiekę nad Twoim ogrodem przez cały rok.',
     ['formowanie roślin', 'przycinanie żywopłotów', 'koszenie trawy', 'opryski ochronne roślin'], 's1-A85wPrbRVDfwPQ4j.jpg', None),
]
CARD_IMG = ['1-mjEvxLGk6DIPkV3x.png', '2-YbNvXDK9lgFDjNJY.png', 'dsc_0570-A1awGrORzaS9MeVg.JPG']

# =====================================================================
# STRONA GŁÓWNA
# =====================================================================
def words(text, start=0, cls=''):
    c = f' {cls}' if cls else ''
    toks, out = text.split(), []
    for w in toks:
        if out and len(out[-1].split('\u00a0')[-1]) <= 2 and out[-1].split('\u00a0')[-1].lower() in ('a','i','o','u','w','z','na','do','od','po','we','ze','za'):
            out[-1] += '\u00a0' + w
        else: out.append(w)
    return ' '.join(f'<span class="w{c}" style="--i:{start+i}">{w}</span>' for i, w in enumerate(out))

MARQUEE = ['Projektowanie ogrodów', 'Wizualizacje 3D', 'Zakładanie ogrodów', 'Instalacje nawadniające', 'Oświetlenie ogrodowe',
           'Kostka brukowa', 'Trawniki i nasadzenia', 'Oczka wodne', 'Przycinanie żywopłotów', 'Koszenie trawy', 'Pielęgnacja zieleni']

def marquee():
    ul = ''.join(f'<li>{m}</li>' for m in MARQUEE)
    return f'''<div class="marquee" aria-label="Zakres usług"><div class="marquee__track"><ul>{ul}</ul><ul aria-hidden="true">{ul}</ul></div></div>'''

def build_home():
    r = ''
    cards = ''
    for i, (slug, name, text, items, _, _) in enumerate(OFFER):
        chips = ''.join(f'<li>{x}</li>' for x in items[:4])
        cards += f'''
        <article class="service-card tilt spot">
          <div class="service-card__media">
            {img(CARD_IMG[i], name, 600, 450, sizes='(min-width: 880px) 390px, 100vw')}
            <span class="service-card__num" aria-hidden="true">0{i+1}</span>
          </div>
          <div class="service-card__body">
            <h3>{name}</h3>
            <p>{text}</p>
            <ul class="chips" aria-label="Zakres prac">{chips}</ul>
            <a class="link-arrow" href="oferta/#{slug}">Sprawdź więcej<span class="sr-only"> o usłudze: {name.lower()}</span></a>
          </div>
        </article>'''
    stars = I['star'] * 5
    body = head('Zakładanie ogrodów Aleksandrów Kujawski | Komfortowe Ogrody',
                'Projektowanie, zakładanie i pielęgnacja ogrodów w Aleksandrowie Kujawskim od 2013 r. Ponad 150 zadowolonych klientów. Zadzwoń: 600 927 502.',
                '', r, [faq_ld()], preload_img=zurl(HERO, 1920, 1080)) + header('home', r) + f'''
<main id="tresc">
  <section class="hero">
    {img(HERO, '', 1920, 1080, cls='hero__bg', lazy=False, sizes='100vw', extra='data-parallax')}
    <canvas class="leaves" aria-hidden="true"></canvas>
    <div class="wrap">
      <div class="hero__content">
        <span class="eyebrow">Komfortowe Ogrody · od 2013 roku</span>
        <h1>{words('Zakładanie i pielęgnacja ogrodów')} <span class="accent">{words('w Aleksandrowie Kujawskim', 4, 'shine')}</span></h1>
        <p class="hero__rotator">Projekt · wykonanie · pielęgnacja – <span data-rotate='["projektujemy.","zakładamy.","pielęgnujemy.","dbamy o komfort."]'>projektujemy.</span><span class="caret" aria-hidden="true"></span></p>
        <p class="hero__lead">Zaprojektujemy, wykonamy oraz będziemy odpowiednio pielęgnować Państwa ogrody, tak abyście cały czas czuli się w nich <strong>KOMFORTOWO</strong>!</p>
        <div class="hero__actions">
          <a class="btn btn--lime" href="tel:{BIZ['phone_tel']}" data-smart-cta data-open="Zadzwoń – jesteśmy dostępni" data-closed="Napisz – odpowiemy w godzinach pracy" data-closed-href="wycena/">{I['phone']}<span>Zadzwoń – jesteśmy dostępni</span></a>
          <a class="btn btn--ghost" href="wycena/">Zapytaj o wycenę</a>
        </div>
        <ul class="trust">
          <li>{I['users']}<span><b>150+</b> zaufanych klientów</span></li>
          <li>{I['calendar']}<span>Na rynku <b>od 2013</b> roku</span></li>
          <li>{I['leaf']}<span>Projekt · wykonanie · pielęgnacja</span></li>
        </ul>
      </div>
    </div>
    <span class="hero__scroll" aria-hidden="true"></span>
  </section>
  {marquee()}

  <section class="section" id="oferta">
    <div class="wrap">
      <div class="section-head reveal">
        <span class="eyebrow eyebrow--dark">Nasza oferta</span>
        <h2>Ogród od projektu <span class="mark">po stałą opiekę</span></h2>
        <p>Profesjonalne zakładanie i pielęgnacja ogrodów, aby były funkcjonalne i piękne.</p>
      </div>
      <div class="services" data-stagger>{cards}
      </div>
    </div>
  </section>

  <section class="section section--sand">
    <div class="wrap about">
      <div class="about__text reveal">
        <svg class="vine" viewBox="0 0 120 220" aria-hidden="true"><path d="M60 215C58 170 70 150 62 120S40 70 58 40 70 12 66 4"/><path d="M62 150c14-6 28-4 38 4M60 100C44 94 30 96 20 104M60 60c12-8 24-10 36-6"/><ellipse class="lf" cx="102" cy="154" rx="12" ry="6"/><ellipse class="lf" cx="18" cy="104" rx="12" ry="6"/><ellipse class="lf" cx="98" cy="54" rx="11" ry="5.5"/><ellipse class="lf" cx="66" cy="6" rx="8" ry="5"/></svg>
        <span class="eyebrow eyebrow--dark">O nas</span>
        <h2>Komfortowe Ogrody</h2>
        <p class="big">Zaprojektujemy, wykonamy oraz będziemy odpowiednio pielęgnować Państwa ogrody, tak abyście cały czas czuli się w nich <span class="kom">KOMFORTOWO</span>!</p>
        <p>Od początku poszerzamy naszą wiedzę oraz umiejętności, dzięki czemu nasi klienci obdarzyli nas swoim zaufaniem.</p>
        <div class="stats" data-stagger>
          <div class="stat"><b data-count>150+</b><span>zaufanych klientów</span></div>
          <div class="stat"><b data-years-since="2013" data-count>13+</b><span>lat doświadczenia</span></div>
          <div class="stat"><b>3 w 1</b><span>projekt, wykonanie i pielęgnacja</span></div>
        </div>
      </div>
      <div class="about__media reveal">
        {img('7-mnlv0JvKBZSgwxp6.jpg', 'Ogród zrealizowany przez Komfortowe Ogrody', 720, 900, sizes='(min-width: 880px) 520px, 100vw', cls='img-reveal')}
        <div class="about__badge"><b>2013</b><span>tworzymy ogrody<br>od ponad dekady</span></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head reveal">
        <span class="eyebrow eyebrow--dark">Dlaczego my</span>
        <h2>Jeden wykonawca, <span class="mark">pełen komfort</span></h2>
        <p>Nie musisz szukać osobno projektanta, ekipy i ogrodnika – wszystko załatwisz u nas.</p>
      </div>
      <div class="benefits" data-stagger>
        <div class="benefit spot"><span class="ico">{I['layers']}</span><h3>Wszystko w jednym miejscu</h3><p>Projekt, wykonanie i stała pielęgnacja – jeden kontakt przez cały czas życia ogrodu.</p></div>
        <div class="benefit spot"><span class="ico">{I['cube']}</span><h3>Wizualizacja 3D</h3><p>Zanim wbijemy pierwszą łopatę, zobaczysz swój ogród na szkicu koncepcyjnym i w 3D.</p></div>
        <div class="benefit spot"><span class="ico">{I['medal']}</span><h3>Doświadczenie od 2013</h3><p>Od początku poszerzamy wiedzę i umiejętności – ponad dekada pracy z ogrodami.</p></div>
        <div class="benefit spot"><span class="ico">{I['users']}</span><h3>150+ klientów</h3><p>Ponad 150 osób powierzyło nam swoje ogrody. Zobacz efekty w galerii przed i po.</p></div>
      </div>
    </div>
  </section>

  <section class="section section--sand">
    <div class="wrap">
      <div class="section-head reveal">
        <span class="eyebrow eyebrow--dark">Jak pracujemy</span>
        <h2>Od pierwszej rozmowy <span class="mark">do pięknego ogrodu</span></h2>
        <p>Prosty proces w czterech krokach – wiesz, co dzieje się na każdym etapie.</p>
      </div>
      <ol class="process">
        <li class="step"><span class="step__dot">1</span><h3>Rozmowa</h3><p>Dzwonisz lub piszesz i opowiadasz, jaki ogród sobie wymarzyłeś.</p></li>
        <li class="step"><span class="step__dot">2</span><h3>Projekt</h3><p>Przygotowujemy szkic koncepcyjny i wizualizację 3D Twojego ogrodu.</p></li>
        <li class="step"><span class="step__dot">3</span><h3>Realizacja</h3><p>Zakładamy ogród od A do Z: teren, nawadnianie, oświetlenie, nasadzenia.</p></li>
        <li class="step"><span class="step__dot">4</span><h3>Pielęgnacja</h3><p>Dbamy o ogród przez cały rok, żeby zawsze był zadbany i zdrowy.</p></li>
      </ol>
    </div>
  </section>

  {area_html(r)}

  <section class="section">
    <div class="wrap ba-feature">
      <div class="reveal">
        {ba_slider(BEFORE[0], AFTER[0], 1, w=960, h=720, sizes='(min-width: 880px) 700px, 100vw')}
      </div>
      <div class="ba-feature__text reveal">
        <span class="eyebrow eyebrow--dark">Przed i po</span>
        <h2>Zobacz, jak zmieniamy ogrody</h2>
        <p>Zobacz nasze realizacje przed i po oraz efekty wykonanych pielęgnacji. Przesuń suwak, żeby porównać.</p>
        <span class="hint">{I['hand']}Przeciągnij suwak w lewo i w prawo</span>
        <div><a class="btn btn--primary" href="galeria/">Zobacz całą galerię</a></div>
      </div>
    </div>
  </section>

  <section class="section section--green" id="opinie">
    <div class="wrap">
      <div class="section-head reveal">
        <span class="eyebrow">Opinie</span>
        <h2>Co mówią o nas <span class="mark">klienci</span></h2>
        <p>Zaufaj naszym klientom, którzy doceniają nasze usługi ogrodnicze.</p>
      </div>
      <div class="reviews" data-stagger>
        <figure class="review spot">
          <div class="stars" role="img" aria-label="Ocena 5 na 5">{stars}</div>
          <blockquote>„Dzięki Komfortowym Ogrodom mój ogród wygląda pięknie i jest łatwy w pielęgnacji. Ich nowoczesne rozwiązania naprawdę zaoszczędziły mi czas i pieniądze.”</blockquote>
          <figcaption><span class="avatar" aria-hidden="true">MS</span><span><b>Marek Stanisławski</b><span>Aleksandrów Kujawski</span></span></figcaption>
        </figure>
        <figure class="review spot">
          <div class="stars" role="img" aria-label="Ocena 5 na 5">{stars}</div>
          <blockquote>„Komfortowe ogrody to profesjonaliści, którzy znają się na rzeczy. Polecam!”</blockquote>
          <figcaption><span class="avatar" aria-hidden="true">AB</span><span><b>Anna Borejko</b><span>Toruń</span></span></figcaption>
        </figure>
        <div class="review-cta">
          <span class="g">{I['google']}</span>
          <h3>Opinie w Google</h3>
          <p>Zobacz wszystkie opinie naszych klientów w wizytówce Google i podziel się swoją.</p>
          <a class="btn btn--white" href="{BIZ['gmaps']}" target="_blank" rel="noopener">Zobacz opinie w Google</a>
        </div>
      </div>
    </div>
  </section>

  {faq_html()}

  <div style="height:clamp(64px,9vw,112px)"></div>
  {cta_band(r)}
</main>
''' + footer(r)
    write('index.html', body)

# =====================================================================
# OFERTA
# =====================================================================
CALENDAR = [
    ('Styczeń',     'Czas na projekt: szkic koncepcyjny i wizualizacja 3D, żeby wiosną ruszyć z realizacją.', ['projekt']),
    ('Luty',        'Projektowanie, zamawianie roślin i cięcie prześwietlające drzew oraz krzewów pod koniec miesiąca.', ['projekt', 'pielęgnacja']),
    ('Marzec',      'Porządki po zimie, wertykulacja i pierwsze nawożenie trawnika, cięcie żywopłotów przed wegetacją, niwelacja terenu pod nowe ogrody.', ['pielęgnacja', 'wykonanie']),
    ('Kwiecień',    'Zakładanie trawników z siewu i z rolki, nasadzenia, uruchomienie nawadniania, pierwsze koszenie i opryski profilaktyczne.', ['wykonanie', 'pielęgnacja']),
    ('Maj',         'Nasadzenia bylin i krzewów, regularne koszenie, nawadnianie i ochrona roślin przed szkodnikami.', ['wykonanie', 'pielęgnacja']),
    ('Czerwiec',    'Pierwsze formowanie żywopłotów, cotygodniowe koszenie, nawadnianie, montaż oczek wodnych i oświetlenia.', ['pielęgnacja', 'wykonanie']),
    ('Lipiec',      'Nawadnianie w upały, koszenie, opryski przy chorobach grzybowych, cięcie letnie krzewów.', ['pielęgnacja']),
    ('Sierpień',    'Drugie cięcie żywopłotów, przygotowanie stanowisk pod jesienne nasadzenia, od połowy miesiąca zakładanie trawników.', ['pielęgnacja', 'wykonanie']),
    ('Wrzesień',    'Najlepszy czas na trawnik z siewu, nasadzenia drzew i krzewów, nawożenie jesienne i regeneracja trawnika.', ['wykonanie', 'pielęgnacja']),
    ('Październik', 'Nasadzenia, grabienie liści, ostatnie koszenie, zabezpieczenie instalacji nawadniającej przed zimą.', ['pielęgnacja']),
    ('Listopad',    'Okrywanie roślin wrażliwych, cięcie sanitarne, prace porządkowe i oświetlenie ogrodu na krótkie dni.', ['pielęgnacja', 'wykonanie']),
    ('Grudzień',    'Planowanie i projekt na kolejny sezon, strząsanie śniegu z iglaków, przegląd oświetlenia.', ['projekt', 'pielęgnacja']),
]

def calendar_html(root):
    tabs = ''.join(f'<button class="cal__tab" type="button" role="tab" data-m="{i}" aria-selected="false" id="cal-tab-{i}" aria-controls="cal-panel-{i}">{m[:3]}<span class="sr-only">{m[3:]}</span></button>' for i, (m, _, _) in enumerate(CALENDAR))
    panels = ''.join(f'''
          <div class="cal__panel" role="tabpanel" id="cal-panel-{i}" aria-labelledby="cal-tab-{i}" hidden>
            <h3>{m}</h3><p>{t}</p>
            <ul class="chips">{''.join(f'<li>{x}</li>' for x in tags)}</ul>
          </div>''' for i, (m, t, tags) in enumerate(CALENDAR))
    return f'''<section class="section" id="kalendarz">
    <div class="wrap">
      <div class="section-head reveal">
        <span class="eyebrow eyebrow--dark">Kalendarz ogrodnika</span>
        <h2>Co robimy w ogrodzie <span class="mark">przez cały rok</span></h2>
        <p>Ogród żyje w rytmie pór roku. Sprawdź, jakie prace mają sens w danym miesiącu – i kiedy najlepiej się z nami umówić.</p>
      </div>
      <div class="cal reveal">
        <div class="cal__tabs" role="tablist" aria-label="Miesiące">{tabs}</div>
        <div class="cal__body">{panels}
        </div>
        <p class="cal__cta"><span class="open-status"></span> <a class="link-arrow" href="{root}wycena/">Umów prace na ten sezon</a></p>
      </div>
    </div>
  </section>'''

def build_offer():
    r = '../'
    blocks = ''
    for i, (slug, name, text, items, pic, _) in enumerate(OFFER):
        lis = ''.join(f'<li>{I["check"]}<span>{x[0].upper() + x[1:]}</span></li>' for x in items)
        trim = '255.5066079295154;317.1806167400881;669.6035242290749;264.3171806167401' if pic.startswith('s1-') else None
        blocks += f'''
      <article class="offer-block" id="{slug}">
        <div class="offer-block__media">
          {img(pic, name, 760, 608, sizes='(min-width: 880px) 560px, 100vw', trim=trim, cls='img-reveal')}
          <span class="offer-block__num" aria-hidden="true">0{i+1}</span>
        </div>
        <div class="reveal">
          <span class="eyebrow eyebrow--dark">Usługa 0{i+1}</span>
          <h2>{name}</h2>
          <p>{text}</p>
          <ul class="checklist" data-stagger>{lis}</ul>
          <a class="btn btn--primary" href="{r}kontakt/">Zapytaj o {name.split()[0].lower()}</a>
        </div>
      </article>'''
    body = head('Oferta – projektowanie, zakładanie i pielęgnacja ogrodów',
                'Projekty ogrodów z wizualizacją 3D, nawadnianie, oświetlenie, kostka brukowa, trawniki, oczka wodne i pielęgnacja zieleni – Aleksandrów Kujawski.',
                'oferta/', r, [breadcrumbs_ld('Oferta', 'oferta/')]) + header('oferta', r) + f'''
<main id="tresc">
  {page_hero('Nasza <span class="shine">oferta</span>', 'Profesjonalne zakładanie i pielęgnacja ogrodów, aby były funkcjonalne i piękne. Od projektu, przez kompleksowe wykonanie, po stałą opiekę nad zielenią.', 'Oferta', 'e-YlevO5P81RUZJbyy.JPG', r)}

  <section class="section">
    <div class="wrap">{blocks}
    </div>
  </section>

  <section class="section section--sand">
    <div class="wrap">
      <div class="section-head reveal">
        <span class="eyebrow eyebrow--dark">Z naszych realizacji</span>
        <h2>Ogrody, w których <span class="mark">czuć komfort</span></h2>
      </div>
      <div class="photo-pair">
        {img('img_20240615_135533-YX4yKzDvqkflLBLo.jpg', 'Realizacja ogrodu – Komfortowe Ogrody', 760, 608, sizes='(min-width: 880px) 600px, 100vw', cls='img-reveal')}
        {img('e-YlevO5P81RUZJbyy.JPG', 'Zadbany ogród po realizacji – Komfortowe Ogrody', 760, 608, sizes='(min-width: 880px) 600px, 100vw', cls='img-reveal', trim='205.8319039451115;0;205.8319039451115;0')}
      </div>
      <p style="text-align:center;margin-top:36px"><a class="btn btn--outline" href="{r}galeria/">Zobacz więcej realizacji</a></p>
    </div>
  </section>

  {calendar_html(r)}

  <div style="height:clamp(64px,9vw,112px)"></div>
  {cta_band(r)}
</main>
''' + footer(r)
    write('oferta/index.html', body)

# =====================================================================
# GALERIA
# =====================================================================
def build_gallery():
    r = '../'
    items = ''
    for i, (b, a) in enumerate(zip(BEFORE, AFTER)):
        items += f'''
        <figure class="gallery-item reveal">
          {ba_slider(b, a, i+1)}
          <figcaption class="gallery-item__bar"><span>Realizacja {i+1}</span><button class="zoom-btn" type="button">{I['expand']}Powiększ</button></figcaption>
        </figure>'''
    body = head('Galeria realizacji ogrodów – przed i po | Komfortowe Ogrody',
                'Realizacje ogrodów przed i po: zakładanie ogrodów, trawniki, nasadzenia i pielęgnacja zieleni w Aleksandrowie Kujawskim. Zobacz różnicę!',
                'galeria/', r, [breadcrumbs_ld('Galeria', 'galeria/')]) + header('galeria', r) + f'''
<main id="tresc">
  {page_hero('Galeria <span class="shine">ogrodów</span>', 'Zobacz nasze realizacje ogrodów, które zachwycają funkcjonalnością i pięknem. Przesuń suwak na zdjęciu, żeby porównać stan przed i po.', 'Galeria', AFTER[0], r)}

  <section class="section">
    <div class="wrap">
      <p style="text-align:center"><span class="hint">{I['hand']}Przeciągnij suwak na zdjęciu, żeby zobaczyć różnicę</span></p>
      <p class="gallery-note">Wszystkie zdjęcia pochodzą z naszych realizacji – bez zdjęć stockowych.</p>
      <div class="gallery-grid">{items}
      </div>
    </div>
  </section>

  {cta_band(r)}
</main>

<div class="modal" role="dialog" aria-modal="true" aria-label="Powiększone porównanie przed i po" hidden>
  <button class="modal__close" type="button" aria-label="Zamknij">{I['x']}</button>
  <button class="modal__nav modal__prev" type="button" aria-label="Poprzednia realizacja">{I['left']}</button>
  <div class="modal__inner"></div>
  <button class="modal__nav modal__next" type="button" aria-label="Następna realizacja">{I['right']}</button>
  <span class="modal__count" aria-live="polite"></span>
</div>
''' + footer(r)
    write('galeria/index.html', body)

# =====================================================================
# KONTAKT
# =====================================================================
def build_contact():
    r = '../'
    body = head('Kontakt – Komfortowe Ogrody, Aleksandrów Kujawski',
                f'Komfortowe Ogrody: tel. 600 927 502, {BIZ["email"]}, ul. {BIZ["street"]}, {BIZ["city"]}. Czynne {BIZ["hours_label"]}.',
                'kontakt/', r, [breadcrumbs_ld('Kontakt', 'kontakt/')]) + header('kontakt', r) + f'''
<main id="tresc">
  {page_hero('Skontaktuj się <span class="shine">z nami</span>', 'Chętnie odpowiemy na wszystkie Państwa pytania dotyczące ogrodów. Zadzwoń, napisz albo odwiedź nas w Aleksandrowie Kujawskim.', 'Kontakt', '4-m5KwDlD3lECL8jyQ.png', r)}

  <section class="section">
    <div class="wrap">
      <div class="contact-grid" data-stagger>
        <div class="contact-card spot">
          <span class="ico">{I['phone']}</span><small>Telefon</small><a href="tel:{BIZ['phone_tel']}"><b>{BIZ['phone_display']}</b></a>
          <button class="copy" type="button" data-copy="{BIZ['phone_display']}">{I['copy']}Kopiuj numer</button>
        </div>
        <div class="contact-card spot">
          <span class="ico">{I['mail']}</span><small>E-mail</small><a href="mailto:{BIZ['email']}"><b>{BIZ['email'].replace('@', '@<wbr>')}</b></a>
          <button class="copy" type="button" data-copy="{BIZ['email']}">{I['copy']}Kopiuj adres</button>
        </div>
        <div class="contact-card spot">
          <span class="ico">{I['pin']}</span><small>Adres</small><a href="{BIZ['gmaps']}" target="_blank" rel="noopener"><b>{BIZ['street']},<br>{BIZ['postal']} {BIZ['city']}</b></a>
          <button class="copy" type="button" data-copy="{ADDRESS_ONE_LINE}">{I['copy']}Kopiuj adres</button>
        </div>
        <div class="contact-card spot">
          <span class="ico">{I['clock']}</span><small>Godziny otwarcia</small>
          <span class="hours"><b>Pn–Sob: 7:00–18:00</b><br>Niedziela: zamknięte</span>
          <span class="open-status"></span>
        </div>
      </div>

      <div class="contact-main">
        <div class="map reveal" data-map-src="{BIZ['map_embed']}" data-map-title="Mapa dojazdu – {BIZ['name']}, {ADDRESS_ONE_LINE}">
          <div class="map__consent">
            <span class="ico">{I['pin']}</span>
            <h2>Mapa dojazdu</h2>
            <p>{ADDRESS_ONE_LINE}</p>
            <p class="map__note">Mapa Google załaduje się po kliknięciu. Wtedy Twoja przeglądarka połączy się z serwerami Google (szczegóły w <a href="{r}polityka-prywatnosci/">polityce prywatności</a>).</p>
            <button class="btn btn--primary" type="button" data-map-load>{I['google']}Pokaż mapę Google</button>
            <a class="link-arrow" href="{BIZ['gmaps']}" target="_blank" rel="noopener">Otwórz w aplikacji Google Maps</a>
          </div>
        </div>
        <form class="form reveal" id="contact-form" novalidate>
          <h2>Napisz do nas</h2>
          <p>Opisz krótko, czego potrzebujesz – odpowiemy najszybciej, jak to możliwe.</p>
          <div class="field"><input id="f-name" name="name" type="text" placeholder=" " autocomplete="name"><label for="f-name">Imię i nazwisko</label></div>
          <div class="field"><input id="f-email" name="email" type="email" placeholder=" " autocomplete="email" required><label for="f-email">Adres e-mail*</label></div>
          <div class="field"><input id="f-phone" name="phone" type="tel" placeholder=" " autocomplete="tel"><label for="f-phone">Telefon (opcjonalnie)</label></div>
          <div class="field"><textarea id="f-msg" name="message" rows="6" placeholder=" " required></textarea><label for="f-msg">Wiadomość*</label></div>
          <div class="hp" aria-hidden="true"><label for="f-firma">Nie wypełniaj tego pola</label><input id="f-firma" name="firma" type="text" tabindex="-1" autocomplete="off"></div>
          <button class="btn btn--primary" type="submit">Wyślij zapytanie</button>
          <p class="form__note" role="status" aria-live="polite"></p>
          <p class="form__rodo">Wiadomość otworzy się w Twoim programie pocztowym i trafi bezpośrednio na naszą skrzynkę. Administratorem danych jest {BIZ['legal']}; wykorzystamy je wyłącznie do odpowiedzi na zapytanie. <a href="{r}polityka-prywatnosci/">Polityka prywatności</a>.</p>
        </form>
      </div>

      <div class="company reveal">
        <span><b>{BIZ['name']}</b></span>
        <span>{BIZ['legal']}</span>
        <span>NIP: {BIZ['nip']}</span>
        <span>{ADDRESS_ONE_LINE}</span>
        <span><a href="{BIZ['gmaps']}" target="_blank" rel="noopener">Wizytówka Google</a></span>
      </div>
    </div>
  </section>

  {area_html(r)}
</main>
''' + footer(r)
    write('kontakt/index.html', body)

# =====================================================================
# RZEŹBA
# =====================================================================
SCULPT_PRICE = '11849.99'          # cena w zł (format dla Google)
SCULPT_PRICE_TXT = '11 849,99 zł'  # cena wyświetlana na stronie
SCULPT_VIEWS = ['z przodu', 'z boku', 'z profilu', 'z drugiej strony']
# (plik, opis ujęcia, szerokość, wysokość) – ujęcie studyjne jako główne
VIEWER = [('rzezba-studio', 'studyjne', 768, 1024)] + [(f'rzezba-{i}', SCULPT_VIEWS[i-1], 1200, 1500) for i in range(1, 5)]

def build_sculpture():
    r = '../'
    base = f'{r}assets/rzezba/'
    thumbs = ''.join(f'''
            <button class="viewer__thumb{' is-active' if k == 0 else ''}" type="button" data-i="{k}" aria-label="Pokaż ujęcie {label}"{' aria-current="true"' if k == 0 else ''}>
              <img src="{base}{f}-min.webp" alt="" width="{w}" height="{h}" loading="lazy" decoding="async">
            </button>''' for k, (f, label, w, h) in enumerate(VIEWER))
    frames = ''.join(f'''
              <picture class="viewer__frame{' is-active' if k == 0 else ''}" data-full="{base}{f}.webp">
                <source srcset="{base}{f}.webp" type="image/webp">
                <img src="{base}{f}.jpg" alt="Lustrzana rzeźba ogrodowa na czarnym postumencie – ujęcie {label}" width="{w}" height="{h}" {'fetchpriority="high"' if k == 0 else 'loading="lazy"'} decoding="async">
              </picture>''' for k, (f, label, w, h) in enumerate(VIEWER))
    grid = ''.join(f'''
        <figure class="sculpt-tile spot">
          <picture><source srcset="{base}rzezba-{i}.webp" type="image/webp"><img src="{base}rzezba-{i}.jpg" alt="Rzeźba ogrodowa – ujęcie {SCULPT_VIEWS[i-1]}" width="1200" height="1500" loading="lazy" decoding="async"></picture>
          <figcaption>Ujęcie {SCULPT_VIEWS[i-1]}</figcaption>
        </figure>''' for i in range(1, 5))
    mail = f"mailto:{BIZ['email']}?subject=" + 'Zapytanie%20o%20rze%C5%BAb%C4%99%20ogrodow%C4%85'
    sculpt_ld = {'@context': 'https://schema.org', '@type': 'VisualArtwork', 'name': 'Lustrzana rzeźba ogrodowa',
                 'artform': 'Rzeźba', 'image': [f'{DOMAIN}/assets/rzezba/{f}.jpg' for f, *_ in VIEWER],
                 'description': 'Nowoczesna rzeźba ogrodowa o lustrzanym wykończeniu, ustawiona na czarnym postumencie.',
                 'offers': {'@type': 'Offer', 'price': SCULPT_PRICE, 'priceCurrency': 'PLN', 'url': f'{DOMAIN}/rzezba/',
                            'seller': {'@id': DOMAIN + '/'}}}
    body = head('Lustrzana rzeźba ogrodowa | Komfortowe Ogrody',
                f'Nowoczesna rzeźba ogrodowa o lustrzanym wykończeniu na czarnym postumencie. Cena: {SCULPT_PRICE_TXT}. Zobacz ją z każdej strony – Komfortowe Ogrody.',
                'rzezba/', r, [breadcrumbs_ld('Rzeźba ogrodowa', 'rzezba/'), sculpt_ld], og=f'{DOMAIN}/assets/rzezba/rzezba-og.jpg') + header('rzezba', r) + f'''
<main id="tresc">
  <section class="sculpt-hero">
    <div class="wrap sculpt-hero__grid">
      <div class="sculpt-hero__text">
        <nav class="breadcrumbs breadcrumbs--dark" aria-label="Ścieżka nawigacji"><ol><li><a href="{r}">Strona główna</a></li><li aria-current="page">Rzeźba</li></ol></nav>
        <span class="eyebrow eyebrow--dark">Rzeźba ogrodowa</span>
        <h1>Lustrzana rzeźba, która <span class="mark">odbija Twój ogród</span></h1>
        <p class="sculpt-lead">Nowoczesna, płynna forma o lustrzanym wykończeniu na czarnym postumencie. Odbija zieleń, niebo i światło, więc o każdej porze dnia wygląda inaczej – to efektowny punkt centralny ogrodu, podjazdu lub tarasu.</p>
        <ul class="chips chips--lg">
          <li>Lustrzane wykończenie</li><li>Czarny postument</li><li>Do ogrodu i na taras</li>
        </ul>
        <div class="price-tag">
          <span class="price-tag__label">Cena</span>
          <span class="price-tag__value">{SCULPT_PRICE_TXT}</span>
        </div>
        <div class="sculpt-actions">
          <a class="btn btn--primary" href="tel:{BIZ['phone_tel']}">{I['phone']}Zadzwoń i zamów</a>
          <a class="btn btn--outline" href="{mail}">{I['mail']}Napisz w sprawie rzeźby</a>
        </div>
        <p class="sculpt-note">Wymiary, dostawę i ustawienie w Twoim ogrodzie omówimy telefonicznie lub mailowo.</p>
      </div>
      <div class="viewer" aria-roledescription="podgląd z kilku stron">
        <div class="viewer__stage" tabindex="0" aria-label="Rzeźba – przeciągnij lub użyj strzałek, żeby obejrzeć z innej strony">
          {frames}
          <span class="viewer__lens" aria-hidden="true"></span>
          <span class="viewer__hint" aria-hidden="true">{I['hand']}Przeciągnij, żeby obrócić</span>
          <span class="viewer__count" aria-live="polite">1 / {len(VIEWER)}</span>
        </div>
        <div class="viewer__thumbs">{thumbs}
        </div>
      </div>
    </div>
  </section>

  <section class="section section--sand">
    <div class="wrap">
      <div class="section-head reveal">
        <span class="eyebrow eyebrow--dark">Z każdej strony</span>
        <h2>Każde ujęcie <span class="mark">wygląda inaczej</span></h2>
        <p>Lustrzana powierzchnia za każdym razem odbija otoczenie – zieleń, dom, niebo. Zobacz rzeźbę z czterech stron.</p>
      </div>
      <div class="sculpt-grid" data-stagger>{grid}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="cta-band reveal">
        <div>
          <h2>Chcesz ją u siebie w <span class="shine">ogrodzie</span>?</h2>
          <p>Cena: <strong>{SCULPT_PRICE_TXT}</strong>. Zadzwoń lub napisz – opowiemy o rzeźbie i doradzimy, gdzie najlepiej się zaprezentuje. {BIZ['hours_label']}.</p>
        </div>
        <div class="cta-band__actions">
          <a class="btn btn--white" href="tel:{BIZ['phone_tel']}">{I['phone']}{BIZ['phone_display']}</a>
          <a class="btn btn--ghost" href="{mail}">Napisz do nas</a>
        </div>
      </div>
    </div>
  </section>
</main>
''' + footer(r)
    write('rzezba/index.html', body)

# =====================================================================
# WYCENA – konfigurator zapytania
# =====================================================================
def build_quote():
    r = '../'
    services = [('Projekt ogrodu', 'szkic koncepcyjny + wizualizacja 3D', 'layers'), ('Założenie ogrodu', 'teren, nawadnianie, oświetlenie, trawnik, nasadzenia', 'cube'),
                ('Pielęgnacja', 'koszenie, żywopłoty, formowanie, opryski', 'leaf'), ('Rzeźba ogrodowa', 'lustrzana rzeźba na postumencie', 'medal')]
    svc = ''.join(f'''
              <label class="pick"><input type="checkbox" name="zakres" value="{n}"><span class="pick__box"><span class="ico">{I[ic]}</span><b>{n}</b><small>{d}</small></span></label>''' for n, d, ic in services)
    terms = ['jak najszybciej', 'w tym sezonie', 'w przyszłym sezonie', 'jeszcze nie wiem']
    trm = ''.join(f'<label class="pill"><input type="radio" name="termin" value="{t}"><span>{t}</span></label>' for t in terms)
    lead = f"Cztery krótkie kroki i gotowe. Zapytanie trafi do nas e-mailem – odpowiadamy w godzinach pracy, {BIZ['hours_label']}."
    body = head('Zapytaj o wycenę ogrodu | Komfortowe Ogrody',
                'Opisz swój ogród w 4 prostych krokach – zakres prac, powierzchnia, termin i kontakt. Przygotujemy wycenę projektu, założenia lub pielęgnacji ogrodu.',
                'wycena/', r, [breadcrumbs_ld('Wycena', 'wycena/')]) + header('wycena', r) + f'''
<main id="tresc">
  {page_hero('Zapytaj <span class="shine">o wycenę</span>', lead, 'Wycena', '4375db2d-421f-4512-a314-577c463903e2-A85w1ND26vIWDo2L.png', r)}

  <section class="section">
    <div class="wrap quote">
      <form class="wizard" id="wizard" novalidate>
        <ol class="wizard__steps" aria-label="Kroki">
          <li class="is-active"><span>1</span>Zakres</li><li><span>2</span>Ogród</li><li><span>3</span>Termin</li><li><span>4</span>Kontakt</li>
        </ol>
        <div class="wizard__bar"><span></span></div>

        <fieldset class="wizard__step is-active" data-step="0">
          <legend>Czego potrzebujesz?</legend>
          <p class="wizard__hint">Możesz zaznaczyć kilka opcji.</p>
          <div class="picks">{svc}
          </div>
        </fieldset>

        <fieldset class="wizard__step" data-step="1">
          <legend>Opowiedz o ogrodzie</legend>
          <div class="range">
            <label for="q-area">Powierzchnia ogrodu: <output for="q-area" id="q-area-out">500 m²</output></label>
            <input id="q-area" name="powierzchnia" type="range" min="50" max="5000" step="50" value="500">
            <div class="range__scale"><span>50 m²</span><span>5000 m²</span></div>
          </div>
          <p class="wizard__label">Stan terenu</p>
          <div class="pills">
            <label class="pill"><input type="radio" name="teren" value="nowa działka / plac budowy"><span>Nowa działka</span></label>
            <label class="pill"><input type="radio" name="teren" value="istniejący ogród do odświeżenia"><span>Istniejący ogród</span></label>
            <label class="pill"><input type="radio" name="teren" value="ogród wymaga tylko pielęgnacji"><span>Tylko pielęgnacja</span></label>
          </div>
          <div class="field"><input id="q-city" name="miejscowosc" type="text" placeholder=" " autocomplete="address-level2"><label for="q-city">Miejscowość</label></div>
        </fieldset>

        <fieldset class="wizard__step" data-step="2">
          <legend>Kiedy chcesz zacząć?</legend>
          <div class="pills">{trm}</div>
          <div class="field"><textarea id="q-notes" name="uwagi" rows="4" placeholder=" "></textarea><label for="q-notes">Uwagi (opcjonalnie) – np. co jest dla Ciebie najważniejsze</label></div>
        </fieldset>

        <fieldset class="wizard__step" data-step="3">
          <legend>Jak się z Tobą skontaktować?</legend>
          <div class="field"><input id="q-name" name="name" type="text" placeholder=" " autocomplete="name"><label for="q-name">Imię i nazwisko</label></div>
          <div class="field"><input id="q-phone" name="phone" type="tel" placeholder=" " autocomplete="tel"><label for="q-phone">Telefon</label></div>
          <div class="field"><input id="q-email" name="email" type="email" placeholder=" " autocomplete="email" required><label for="q-email">Adres e-mail*</label></div>
          <div class="hp" aria-hidden="true"><label for="q-firma">Nie wypełniaj tego pola</label><input id="q-firma" name="firma" type="text" tabindex="-1" autocomplete="off"></div>
          <p class="form__rodo">Po kliknięciu „Wyślij zapytanie” otworzy się Twój program pocztowy z gotową, uporządkowaną wiadomością. Administratorem danych jest {BIZ['legal']}. <a href="{r}polityka-prywatnosci/">Polityka prywatności</a>.</p>
        </fieldset>

        <div class="wizard__nav">
          <button class="btn btn--outline" type="button" data-prev hidden>Wstecz</button>
          <button class="btn btn--primary" type="button" data-next>Dalej</button>
          <button class="btn btn--primary" type="submit" data-send hidden>{I['mail']}Wyślij zapytanie</button>
          <p class="form__note" role="status" aria-live="polite"></p>
        </div>
      </form>

      <aside class="quote__side">
        <div class="summary">
          <h2>Twoje zapytanie</h2>
          <dl class="summary__list" id="summary">
            <div><dt>Zakres</dt><dd data-sum="zakres">–</dd></div>
            <div><dt>Powierzchnia</dt><dd data-sum="powierzchnia">500 m²</dd></div>
            <div><dt>Teren</dt><dd data-sum="teren">–</dd></div>
            <div><dt>Miejscowość</dt><dd data-sum="miejscowosc">–</dd></div>
            <div><dt>Termin</dt><dd data-sum="termin">–</dd></div>
          </dl>
          <button class="copy" type="button" data-copy-summary>{I['copy']}Kopiuj podsumowanie</button>
          <p class="summary__alt">Wolisz porozmawiać? <a href="tel:{BIZ['phone_tel']}">{BIZ['phone_display']}</a></p>
        </div>
        <div class="prep">
          <h2>Zanim zadzwonisz</h2>
          <p>Wycena pójdzie szybciej, jeśli przygotujesz:</p>
          <ul class="checklist">
            <li>{I['check']}<span>przybliżone wymiary działki lub ogrodu</span></li>
            <li>{I['check']}<span>kilka zdjęć terenu, najlepiej z różnych stron</span></li>
            <li>{I['check']}<span>pomysły i inspiracje – co lubisz, a czego nie</span></li>
            <li>{I['check']}<span>orientacyjny budżet i termin</span></li>
          </ul>
        </div>
      </aside>
    </div>
  </section>
</main>
''' + footer(r)
    write('wycena/index.html', body)

# =====================================================================
# POLITYKA PRYWATNOŚCI
# =====================================================================
def build_privacy():
    r = '../'
    body = head('Polityka prywatności | Komfortowe Ogrody',
                'Polityka prywatności serwisu komfortoweogrody.pl: administrator danych, cele przetwarzania, pliki cookie, mapa Google i prawa użytkownika.',
                'polityka-prywatnosci/', r, [breadcrumbs_ld('Polityka prywatności', 'polityka-prywatnosci/')]) + header('', r) + f'''
<main id="tresc">
  <section class="section legal">
    <div class="wrap legal__wrap">
      <nav class="breadcrumbs breadcrumbs--dark" aria-label="Ścieżka nawigacji"><ol><li><a href="{r}">Strona główna</a></li><li aria-current="page">Polityka prywatności</li></ol></nav>
      <h1>Polityka prywatności</h1>
      <p class="legal__lead">Szanujemy Twoją prywatność. Ta strona jest statyczną wizytówką firmy – nie zbiera danych automatycznie, nie używa własnych plików cookie ani narzędzi analitycznych i reklamowych.</p>

      <h2>1. Administrator danych</h2>
      <p>Administratorem danych osobowych jest <strong>{BIZ['legal']}</strong>, {ADDRESS_ONE_LINE}, NIP {BIZ['nip']}. Kontakt: <a href="mailto:{BIZ['email']}">{BIZ['email']}</a>, tel. <a href="tel:{BIZ['phone_tel']}">{BIZ['phone_display']}</a>.</p>

      <h2>2. Jakie dane przetwarzamy i po co</h2>
      <p>Przetwarzamy wyłącznie dane, które sam przekażesz, kontaktując się z nami telefonicznie, e-mailem lub przez formularz: imię i nazwisko, adres e-mail, numer telefonu oraz treść wiadomości. Wykorzystujemy je, aby odpowiedzieć na zapytanie, przygotować ofertę i – jeśli zdecydujesz się na współpracę – zrealizować usługę (art. 6 ust. 1 lit. b RODO) oraz w naszym prawnie uzasadnionym interesie, jakim jest obsługa korespondencji (art. 6 ust. 1 lit. f RODO).</p>
      <p>Formularz na stronie nie wysyła danych na żaden serwer: po kliknięciu „Wyślij zapytanie” otwiera się Twój program pocztowy z gotową wiadomością, którą wysyłasz samodzielnie na adres {BIZ['email']}.</p>

      <h2>3. Jak długo przechowujemy dane</h2>
      <p>Przez czas niezbędny do obsługi zapytania i ewentualnej współpracy, a następnie przez okres wymagany przepisami (np. podatkowymi) lub do upływu terminów przedawnienia roszczeń.</p>

      <h2>4. Odbiorcy danych</h2>
      <p>Dane mogą być przetwarzane przez podmioty świadczące dla nas usługi hostingu strony i poczty e-mail – wyłącznie w zakresie niezbędnym do ich działania. Nie sprzedajemy danych ani nie przekazujemy ich do celów marketingowych osób trzecich.</p>

      <h2>5. Pliki cookie i pamięć przeglądarki</h2>
      <p>Strona nie ustawia własnych plików cookie. Jedynie po kliknięciu „Pokaż mapę Google” zapisujemy w pamięci Twojej przeglądarki (localStorage) informację o wyrażonej zgodzie, aby przy kolejnej wizycie mapa załadowała się od razu. Możesz ją usunąć, czyszcząc dane witryny w przeglądarce.</p>

      <h2>6. Usługi zewnętrzne</h2>
      <ul>
        <li><strong>Mapa Google</strong> na podstronie Kontakt jest ładowana dopiero po Twoim kliknięciu. Wtedy przeglądarka łączy się z serwerami Google (Google Ireland Ltd.), które mogą przetwarzać m.in. Twój adres IP zgodnie z <a href="https://policies.google.com/privacy?hl=pl" target="_blank" rel="noopener">polityką prywatności Google</a>.</li>
        <li><strong>Zdjęcia</strong> na stronie są dostarczane z serwerów naszego dostawcy hostingu obrazów; przy ich pobieraniu przekazywany jest adres IP w zakresie technicznie niezbędnym do wyświetlenia strony.</li>
        <li><strong>Czcionki</strong> są hostowane na naszym serwerze – strona nie łączy się z serwerami czcionek Google.</li>
      </ul>

      <h2>7. Twoje prawa</h2>
      <p>Masz prawo dostępu do swoich danych, ich sprostowania, usunięcia lub ograniczenia przetwarzania, prawo do przenoszenia danych oraz prawo sprzeciwu wobec przetwarzania opartego na prawnie uzasadnionym interesie. Masz też prawo wnieść skargę do Prezesa Urzędu Ochrony Danych Osobowych (ul. Stawki 2, 00-193 Warszawa). Aby skorzystać z tych praw, napisz na {BIZ['email']}.</p>

      <h2>8. Zmiany polityki</h2>
      <p>Polityka może być aktualizowana, gdy zmieni się sposób działania strony. Aktualna wersja jest zawsze dostępna pod tym adresem.</p>
      <p class="legal__date">Ostatnia aktualizacja: 30 września 2026 r.</p>
    </div>
  </section>
</main>
''' + footer(r)
    write('polityka-prywatnosci/index.html', body)

def build_manifest():
    write('manifest.webmanifest', json.dumps({
        'name': BIZ['name'], 'short_name': BIZ['name'], 'description': BIZ['desc'],
        'start_url': './', 'scope': './', 'display': 'browser', 'lang': 'pl',
        'background_color': '#ffffff', 'theme_color': '#287319',
        'icons': [{'src': 'assets/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                  {'src': 'assets/icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable'}],
    }, ensure_ascii=False, indent=2) + '\n')

# =====================================================================
# 404
# =====================================================================
def build_404():
    r = '/'
    body = head('Nie znaleziono strony | Komfortowe Ogrody', 'Strona, której szukasz, nie istnieje. Przejdź do strony głównej Komfortowe Ogrody.', '404', r).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">') + header('', r) + f'''
<main id="tresc" class="notfound">
  <div>
    <b>404</b>
    <h1>Nie znaleźliśmy tej strony</h1>
    <p>Możliwe, że adres się zmienił. Zajrzyj na stronę główną albo do naszej oferty.</p>
    <a class="btn btn--primary" href="/">Strona główna</a>
    <a class="btn btn--outline" href="/oferta/">Oferta</a>
  </div>
</main>
''' + footer(r)
    write('404.html', body)

def build_seo_files():
    today = '2026-09-30'
    urls = [('', '1.0'), ('oferta/', '0.9'), ('galeria/', '0.8'), ('rzezba/', '0.7'), ('wycena/', '0.8'), ('kontakt/', '0.8'), ('polityka-prywatnosci/', '0.3')]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{DOMAIN}/{u}</loc><lastmod>{today}</lastmod><priority>{p}</priority></url>\n' for u, p in urls) + '</urlset>\n'
    write('sitemap.xml', sm)
    write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')
    write('.htaccess', '''# Komfortowe Ogrody – konfiguracja dla serwera Apache / LiteSpeed (po migracji na komfortoweogrody.pl)
Options -Indexes
DirectoryIndex index.html
AddType font/woff2 .woff2
AddType application/manifest+json .webmanifest
AddDefaultCharset UTF-8
ErrorDocument 404 /404.html

<IfModule mod_rewrite.c>
  RewriteEngine On
  # Wymuś HTTPS i adres bez „www”
  RewriteCond %{HTTPS} off [OR]
  RewriteCond %{HTTP_HOST} ^www\\. [NC]
  RewriteRule ^ https://komfortoweogrody.pl%{REQUEST_URI} [L,R=301]
  # Stare adresy ze strony Zyro i z podglądu
  RewriteRule ^(oferta|galeria|rzezba|wycena|kontakt|polityka-prywatnosci)$ /$1/ [L,R=301]
  RewriteRule ^(oferta|galeria|kontakt)\\.html$ /$1/ [L,R=301]
  RewriteRule ^strona-g-owna/?$ / [L,R=301]
  RewriteRule ^komfortowe-ogrody-(.*)$ / [L,R=301]
  # Plik pomocniczy tylko dla podglądu w github.io
  RewriteRule ^sw\\.js$ - [G,L]
</IfModule>

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/xml text/plain
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html "access plus 1 hour"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType application/manifest+json "access plus 1 week"
</IfModule>

<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"
  Header always set Strict-Transport-Security "max-age=31536000"
  Header always set Content-Security-Policy "default-src 'self'; img-src 'self' data: https://assets.zyrosite.com https://web.archive.org; frame-src https://maps.google.com https://www.google.com; style-src 'self' 'unsafe-inline'; script-src 'self'; font-src 'self'; connect-src 'self'; base-uri 'self'; form-action 'self' mailto:; frame-ancestors 'self'"
  <FilesMatch "\.(woff2|png|svg|webp|jpg)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
</IfModule>
''')

if __name__ == '__main__':
    build_home(); build_offer(); build_gallery(); build_sculpture(); build_quote(); build_contact(); build_privacy(); build_manifest(); build_404(); build_seo_files()
    print('OK')
