#!/usr/bin/env python3
"""Baut die statische Müller-&-Welte-Website. Aufruf: python3 build.py"""
import json, re, html, os

ROOT = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(f'{ROOT}/_src/products.json', encoding='utf8'))

import time
V = int(time.time())
SITE = 'Müller & Welte Metall GmbH'
TEL = '07464 9897-0'; TEL_HREF = '+49746498970'
MAIL = 'info@mueller-welte.de'
# Platzhalter: URL des Online-Shops / Kundenportals hier eintragen
SHOP_URL = 'https://www.mueller-welte.de/account/login'

def ic(name):
    d = {
     'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
     'scissors': '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.1 15.9M14.5 14.5 20 20M8.1 8.1 12 12"/>',
     'truck': '<path d="M14 18V6a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v11h2M14 9h4l4 4v4h-2"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/><path d="M9 18h6"/>',
     'warehouse': '<path d="M3 21V9l9-5 9 5v12M7 21v-6h10v6M7 17h10"/>',
     'shield': '<path d="M12 3 4 6v6c0 5 3.4 8.2 8 9 4.6-.8 8-4 8-9V6z"/><path d="m9 12 2.2 2.2L15.5 10"/>',
     'phone': '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
     'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
     'pin': '<path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
     'leaf': '<path d="M5 19c0-9 5-14 15-14 0 10-5 15-14 15"/><path d="M5 19c3-5 6-7.5 10-9"/>',
     'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
     'box': '<path d="m21 8-9-5-9 5v8l9 5 9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/>',
     'award': '<circle cx="12" cy="9" r="6"/><path d="m8.5 14.5-1.5 7 5-3 5 3-1.5-7"/>',
     'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6M16 5a3.5 3.5 0 0 1 0 6.5M18.5 14.5c1.8.8 3 2.6 3 5.5"/>',
     'ruler': '<path d="m3 17 14-14 4 4L7 21z"/><path d="m7 13 2 2M10 10l2 2M13 7l2 2"/>',
     'recycle': '<path d="M7 19H4.8a1.8 1.8 0 0 1-1.6-2.7L5 13M11 5l1.6-2.5a1.8 1.8 0 0 1 3 0L19 9M17 13l3 5.3a1.8 1.8 0 0 1-1.6 2.7H14"/><path d="m9 16-2-3-3 1M14 7l3 .5.8-3M15 19l-2 2 2 2"/>',
    }[name]
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'

MATS = [
 dict(slug='aluminium', name='Aluminium', c='#9fb0be', tile='mw-header-home-02.jpg', hero='mw-header-aluminium.jpg',
      tag='Leicht, vielseitig, bleifrei erhältlich',
      lead='Stangen, Profile, Rohre, Bleche und Präzisionsplatten – vom Reinaluminium bis zur bleifreien Automatenlegierung EN AW-6026 LF.'),
 dict(slug='messing', name='Messing', c='#c6a043', tile='20240606_mw_144.jpg', hero='messing-drehteil-spanbruch.jpg',
      tag='Zerspanbar, korrosionsbeständig, bleifrei möglich',
      lead='Kupfer-Zink-Legierungen für Drehteile, Armaturen und Installation – inklusive bleifreier Alternativen zu CuZn39Pb3.'),
 dict(slug='kupfer', name='Kupfer', c='#b9693d', tile='20240606_mw_148.jpg', hero='20240606_mw_148.jpg',
      tag='Beste Leitfähigkeit für Strom und Wärme',
      lead='Vom hochleitfähigen Cu-ETP bis zu zerspanbaren Tellur- und Schwefelkupfern für Elektro- und Wärmetechnik.'),
 dict(slug='bronze', name='Bronze', c='#8b5e34', tile='mw-header-bronze.jpg', hero='mw-header-bronze.jpg',
      tag='Gleitlager, Federn, Seewasser',
      lead='Zinn- und Aluminiumbronzen sowie Rotguss für hoch belastete Gleit- und Verschleißteile.'),
 dict(slug='neusilber', name='Neusilber', c='#b4bcc0', tile='20240606_mw_155.jpg', hero='20240606_mw_155.jpg',
      tag='Silbrig, anlaufbeständig, gut umformbar',
      lead='Kupfer-Nickel-Zink- und Kupfer-Nickel-Legierungen für Feinmechanik, Optik, Schmuck und Seewasser.'),
]
MATBY = {m['slug']: m for m in MATS}

NAV = [
 ('Produkte', 'produkte.html', [(m['name'], f"{m['slug']}.html", m['c']) for m in MATS]),
 ('Service', None, [('Dienstleistungen', 'dienstleistungen.html', None), ('Branchen', 'branchen.html', None)]),
 ('Wissen', 'wissen.html', None),
 ('Unternehmen', 'unternehmen.html', None),
 ('Kontakt', 'kontakt.html', None),
]

def header(active):
    items = []
    for label, href, sub in NAV:
        cur = ' aria-current="page"' if active == label else ''
        if sub:
            li = f'<li class="has-sub"><button type="button" aria-expanded="false" aria-haspopup="true"{cur}>{label}<svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="2"/></svg></button><ul class="sub">'
            if href: li += f'<li><a href="{href}">Alle Werkstoffe</a></li>'
            for l, h, c in sub:
                dot = f'<span class="dot" style="background:{c}"></span>' if c else ''
                li += f'<li><a href="{h}">{dot}{l}</a></li>'
            li += '</ul></li>'
        else:
            li = f'<li><a href="{href}"{cur}>{label}</a></li>'
        items.append(li)
    return f'''<a class="skip" href="#main">Zum Inhalt springen</a>
<div class="topbar"><div class="wrap"><span>NE-Metalle ab Lager Tuningen · Zuschnitt ab Losgröße 1</span><span><a href="tel:{TEL_HREF}">{TEL}</a><a href="mailto:{MAIL}">{MAIL}</a></span></div></div>
<header class="site"><div class="wrap">
<a class="brand" href="index.html" aria-label="Müller &amp; Welte – Startseite"><img src="img/logo-dunkel.svg" alt="Müller &amp; Welte Metall GmbH" width="86" height="58"></a>
<nav class="main" id="nav" aria-label="Hauptnavigation"><ul>{''.join(items)}</ul></nav>
<div class="header-cta"><a class="tel" href="tel:{TEL_HREF}">{TEL}</a><a class="btn btn-primary" href="kontakt.html">Anfrage stellen</a>
<button class="burger" type="button" aria-label="Menü" aria-expanded="false" aria-controls="nav"><span></span></button></div>
</div></header>'''

FOOTER = f'''<footer class="site"><div class="wrap">
<div><a class="brand" href="index.html"><img src="img/logo-weiss.svg" alt="Müller &amp; Welte" width="103" height="70"></a>
<p>Metall GmbH Müller &amp; Welte<br>Händler für Nichteisen-Metalle seit 1987. Familiengeführt in zweiter Generation.</p></div>
<div><h4>Produkte</h4><ul>{''.join(f'<li><a href="{m["slug"]}.html">{m["name"]}</a></li>' for m in MATS)}</ul></div>
<div><h4>Service</h4><ul><li><a href="dienstleistungen.html">Dienstleistungen</a></li><li><a href="branchen.html">Branchen</a></li><li><a href="wissen.html">Wissen</a></li><li><a href="unternehmen.html">Unternehmen</a></li><li><a href="kontakt.html">Kontakt</a></li></ul></div>
<div><h4>Kontakt</h4><address class="addr" style="font-style:normal"><p>Gewerbestr. 20<br>78609 Tuningen</p><p>Tel. <a href="tel:{TEL_HREF}">{TEL}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p></address></div>
</div><div class="legal"><div class="wrap"><span>© 2026 Metall GmbH Müller &amp; Welte</span><span><a href="datenschutz.html">Datenschutz</a><a href="kontakt.html">Kontakt</a><a href="impressum.html">Impressum</a></span></div></div></footer>
<script src="main.js?v={V}"></script>'''

def page(fname, title, desc, active, body, og='img/20240606_mw_187.jpg'):
    out = f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:type" content="website"><meta property="og:image" content="{og}">
<meta name="theme-color" content="#1d2329">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&amp;family=Barlow+Semi+Condensed:wght@500;600;700&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={V}"></head>
<body>{header(active)}
<main id="main">{body}</main>
{FOOTER}</body></html>'''
    open(f'{ROOT}/{fname}', 'w', encoding='utf8').write(out)

def sub_hero(crumbs, h1, lead, img, color=None):
    cs = ' <span>/</span> '.join(f'<a href="{h}">{l}</a>' if h else l for l, h in crumbs)
    st = f' style="--c:{color}"' if color else ''
    return f'''<section class="page-hero"{st}><img src="img/{img}" alt="" loading="eager"><div class="wrap"><div class="crumbs">{cs}</div><h1>{h1}</h1><p class="lead">{lead}</p></div><div class="stripe"></div></section>'''

def cta_band(h='Material gesucht oder Zuschnitt gewünscht?', p='Wir beraten persönlich – Anruf oder Mail genügen, oft ist die Ware noch am selben Tag bereit.'):
    return f'''<section class="s" style="padding-top:0"><div class="wrap"><div class="cta-band rv"><div><h2>{h}</h2><p>{p}</p></div>
<div class="acts"><a class="btn" href="tel:{TEL_HREF}">{ic("phone")} {TEL}</a><a class="btn o" href="kontakt.html">Anfrage senden</a></div></div></div></section>'''

def person(name='Heiko Müller', mail=MAIL, img='mw-ansprechpartner-heiko-mueller.jpg'):
    return f'''<div class="person"><img src="img/{img}" alt="{name}" width="110" height="110" loading="lazy" decoding="async"><div><p style="font-size:.85rem;text-transform:uppercase;letter-spacing:.1em;font-weight:600;color:var(--accent)">Ihr Ansprechpartner</p><h3>{name}</h3><p>Müller &amp; Welte Metall GmbH</p><p><a href="tel:{TEL_HREF}">+49 7464 9897-0</a> · <a href="mailto:{mail}">{mail}</a></p></div></div>'''

# ---------------------------------------------------------------- Startseite
def home():
    mats = ''.join(f'''<a class="mat rv" href="{m["slug"]}.html" style="--c:{m["c"]}"><img src="img/{m["tile"]}" alt="" loading="lazy" decoding="async"><div><h3>{m["name"]}</h3><p>{m["tag"]}</p><span class="go">Sortiment ansehen {ic("arrow").replace("<svg","<svg width=16 height=16")}</span></div></a>''' for m in MATS)
    br = [('Automotive','mw-branchen-automotive.jpg','Über ein Viertel unserer Lieferungen'),('Medizintechnik','mw-branchen-medizintechnik.jpg','Rund 15 % unserer Lieferungen'),('Maschinenbau','mw-branchen-maschinenbau.jpg','Vom Einzelzuschnitt bis zur Serie'),('Elektro-Industrie','mw-branchen-elektroindustrie.jpg','14 % der NE-Metalle in D'),('Drehteile','mw-branchen-drehteile.jpg','Messing, Alu, Kupfer, Bronze')]
    brs = ''.join(f'<a class="br rv" href="branchen.html"><img src="img/{i}" alt="" loading="lazy" decoding="async"><div><h3>{n}</h3><span>{s}</span></div></a>' for n,i,s in br)
    wissen = ''.join(wissen_card(a) for a in ARTICLES[:3])
    body = f'''
<section class="hero"><div class="wrap">
<div><span class="eyebrow">Metallhandel seit 1987 · Tuningen</span>
<h1>Metalle für das <em>Anspruchsvolle.</em></h1>
<p class="lead">Aluminium, Messing, Kupfer, Bronze und Neusilber – über 3.500 Artikel ab Lager, zugeschnitten ab Losgröße 1 und frei Haus geliefert. Von Menschen, die ihre Kunden noch mit Namen kennen.</p>
<div class="cta-row"><a class="btn btn-primary" href="produkte.html">Sortiment entdecken {ic("arrow")}</a><a class="btn btn-ghost" href="kontakt.html">Anfrage stellen</a></div></div>
<div class="hero-media"><img class="main" src="img/20240606_mw_187.jpg" alt="Das Team von Müller &amp; Welte im Lager in Tuningen" width="1200" height="900" fetchpriority="high">
<div class="hero-badge"><strong>1987</strong><span>gegründet<br>2. Generation</span></div>
<div class="hero-badge b2"><strong>ISO 9001</strong><span>zertifiziert<br>seit 1995</span></div></div>
</div></section>
<section class="stats" aria-label="Zahlen und Fakten"><div class="wrap">
<div class="stat"><strong>3.500<small>+</small></strong><span>Artikel ab Lager</span></div>
<div class="stat"><strong>2.500<small>m²</small></strong><span>Lagerfläche</span></div>
<div class="stat"><strong>11<small>mm</small></strong><span>kleinste Fixlänge beim Stangenzuschnitt</span></div>
<div class="stat"><strong>100<small>km</small></strong><span>eigene Lieferung, frei Haus ab 500 kg</span></div>
<div class="stat"><strong>20</strong><span>Mitarbeitende, alle vom Fach</span></div></div></section>

<section class="s"><div class="wrap">
<div class="sec-head row"><div><span class="eyebrow">Sortiment</span><h2>Fünf Werkstoffe. Jede Form, jede Größe.</h2><p class="lead">Stangen, Rohre, Profile, Bleche und Platten – ausschließlich Qualitätsware direkt von den besten Herstellern aus Westeuropa.</p></div><a class="link-arrow" href="produkte.html">Alle Werkstoffe</a></div>
<div class="mat-grid">{mats}</div></div></section>

<section class="s soft"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Service</span><h2>Vom Anruf bis zur Lieferung – einfach und schnell.</h2></div>
<div class="steps">
<div class="step rv"><h3>Anfragen oder bestellen</h3><p>Telefonisch, per Mail oder direkt im Kundenportal. Persönliche Beratung ist jederzeit inklusive.</p></div>
<div class="step rv"><h3>Zuschnitt nach Maß</h3><p>Platten und Bleche bis 100 mm, Stangen bis Ø 400 mm – toleranzgenau auf Mayer- und Behringer-Maschinen.</p></div>
<div class="step rv"><h3>Selbst abholen</h3><p>Anruf genügt: Ihre Ware steht oft noch am selben Tag in Tuningen bereit.</p></div>
<div class="step rv"><h3>Frei Haus geliefert</h3><p>Mit eigenem Fuhrpark im Umkreis von 100 km kostenfrei ab 500 kg – deutschland- und europaweit per Spedition.</p></div></div>
</div></section>

<section class="s"><div class="wrap split">
<img class="rv" src="img/mw-home-verarbeitung.jpg" alt="Plattenzuschnitt auf der Säge bei Müller &amp; Welte" loading="lazy" decoding="async">
<div class="rv"><span class="eyebrow">Zuschnitt &amp; Logistik</span><h2>Millimeterarbeit, die sich sehen lässt.</h2>
<p class="lead">Ob Einzelstück oder Großauftrag – wir bearbeiten jeden Auftrag mit derselben Sorgfalt.</p>
<ul class="checks"><li>Plattenzuschnitt bis 100 mm Stärke, winklig und mit sauberen Schnittkanten</li><li>Stangenzuschnitt bis Ø 400 mm, Fixlängen ab 11 mm</li><li>Abschnitte und Reststücke kurzfristig zu Tagespreisen</li><li>Späne-Recycling mit Gutschrift auf Ihrem Umarbeitungskonto</li></ul>
<a class="btn btn-ghost" href="dienstleistungen.html">Alle Dienstleistungen</a></div></div></section>

<section class="s dark"><div class="wrap">
<div class="sec-head"><span class="eyebrow" style="color:#ff6b72">Branchen</span><h2>Wo Buntmetalle stecken, sind wir dabei.</h2><p class="lead">60 bis 70 % unserer Kunden sind – wie wir – inhabergeführte Familienunternehmen. Dazu Global Player, Werkstätten, Schulen und Hobby-Bastler.</p></div>
<div class="branchen">{brs}</div></div></section>

<section class="s"><div class="wrap split rev">
<div class="rv"><span class="eyebrow">Unternehmen</span><h2>Einmal Metaller, immer Metaller.</h2>
<p class="lead">Wir kennen unsere Kunden noch mit Namen und Gesicht – und das soll auch so bleiben.</p>
<p>Seit 1987 sind wir als Händler in der Welt der Nichteisen-Metalle zuhause. Qualitätsmanagement nach DIN EN ISO 9001, ausgezeichnet seit 1995, ist unser Garant für gleichbleibend hohe Leistung.</p>
<div class="cta-row"><a class="btn btn-primary" href="unternehmen.html">Über uns &amp; Team</a><a class="btn btn-ghost" href="unternehmen.html#historie">Unsere Geschichte</a></div></div>
<img class="rv" src="img/20240606_mw_170.jpg" alt="Mitarbeiter vor dem Müller-&amp;-Welte-Lkw" loading="lazy" decoding="async"></div></section>

<section class="s soft"><div class="wrap">
<div class="sec-head row"><div><span class="eyebrow">Wissen</span><h2>Fachwissen aus der Praxis.</h2><p class="lead">Werkstoffzeugnisse, bleifreie Legierungen, Toleranzen – verständlich erklärt.</p></div><a class="link-arrow" href="wissen.html">Alle Beiträge</a></div>
<div class="cards">{wissen}</div></div></section>

<section class="s"><div class="wrap"><div class="cta-band rv"><div><h2>Wir freuen uns, Sie kennenzulernen.</h2><p>Egal ob kleine oder große Unternehmen, regelmäßige Abnehmer oder Spontankäufer – für uns ist jeder Kunde wichtig.</p></div>
<div class="acts"><a class="btn" href="tel:{TEL_HREF}">{ic("phone")} {TEL}</a><a class="btn o" href="kontakt.html">Anfrage senden</a></div></div></div></section>'''
    page('index.html', 'NE-Metalle ab Lager Tuningen | Aluminium, Messing, Kupfer | Müller & Welte',
         'Halbzeuge und Zuschnitte aus Aluminium, Messing, Kupfer, Bronze und Neusilber. Über 3.500 Artikel ab Lager Tuningen, Zuschnitt ab Losgröße 1. Seit 1987.', '', body)

# ---------------------------------------------------------------- Wissen
ARTICLES = [
 dict(t='2.1, 2.2, 3.1 oder 3.2: Welches Werkstoffzeugnis Sie wirklich brauchen', d='18. August 2026', u='werkstoffzeugnis-en-10204', img='werkstoffzeugnis-en-10204-pruefbescheinigung.jpg', tags=['EN 10204','Werkstoffzeugnis','Rückverfolgbarkeit'], x='Was in welchem Zeugnis steht, wer es ausstellen darf – und was beim Zuschnitt mit der Rückverfolgbarkeit passiert.'),
 dict(t='6060, 6082, 2007 oder 6026 LF: Welche Aluminiumlegierung passt zu Ihrem Bauteil?', d='18. August 2026', u='aluminium-legierung-auswahl-zerspanung', img='aluminium-stangen-legierungen-farbcodierung.jpg', tags=['Aluminium','Zerspanbarkeit','Werkstoffauswahl'], x='Vier Fragen, ein Entscheidungsbaum und eine Kennwerttabelle – von der Legierung über den Zustand bis zur Lieferform.'),
 dict(t='CuZn39Pb3 ersetzen: Welche bleifreie Messinglegierung passt zu welcher Anwendung?', d='18. August 2026', u='cuzn39pb3-ersetzen-bleifreies-messing', img='dsc_9855_-3-.jpg', tags=['Messing','Bleifrei','Trinkwasser'], x='CW724R, CW510L, CW511L oder CW725R? Entscheidungsmatrix für den Ersatz von CW614N – mit Fristen.'),
 dict(t='Klasse A oder Klasse B: Welche Toleranz Sie bei gezogenen Stangen erwarten dürfen', d='18. August 2026', u='toleranzen-gezogene-stangen', img='mw-unternehmen-rundstangen.jpg', tags=['Messing','Aluminium','Toleranzen'], x='Warum normkonforme Stangen für Ihren Stangenlader zu krumm sein können – und was in die Bestellung gehört.'),
 dict(t='Kupfer zerspanen: CW118C Tellurkupfer und die Alternativen', d='18. August 2026', u='kupfer-zerspanen-tellurkupfer', img='20240606_mw_148.jpg', tags=['Kupfer','Tellurkupfer','Zerspanbarkeit'], x='Hohe Leitfähigkeit und vernünftige Zerspanbarkeit: Cu-ETP, CuTeP, CuSP und CuCr1Zr im Vergleich.'),
 dict(t='R410, H080, T651: Was die Zustandsangaben auf Ihrer Bestellung bedeuten', d='18. August 2026', u='zustandsbezeichnungen-verstehen', img='20240606_mw_155.jpg', tags=['Messing','Aluminium','Zustandsbezeichnung'], x='Zwei Systeme, zwei Logiken: EN 1173 bei Kupferwerkstoffen, EN 515 bei Aluminium – und wo es schiefgeht.'),
 dict(t='Zerspanbarkeit von Messing: die bleihaltigen und bleifreien Legierungen im Vergleich', d='18. August 2026', u='zerspanbarkeit-messing-vergleich', img='messing-drehteil-spanbruch.jpg', tags=['Messing','Bleifrei','Zerspanbarkeit'], x='CW614N, CW728R, CW724R, CW510L, CW509L, CW508L: Was der Wechsel auf bleifrei kostet.'),
 dict(t='EN AW-6026LF im Lebensmittelkontakt: was die Prüfungen zeigen', d='6. Dezember 2025', u='aluminiumlegierung-6026lf-jetzt-als-lebensmittelecht-bestaetigt', img='eural-gnutti-6026lf.jpg', tags=['Bleifrei','EN AW-6026 LF','Lebensmittelkontakt'], x='Sehr niedrige Wismut-Migration – und trotzdem keine pauschale Freigabe. Was Sie selbst bewerten müssen.'),
 dict(t='Blei in NE-Metallen: Was CLP, RoHS, ELV, REACH und die Trinkwasserregeln verlangen', d='15. Mai 2025', u='neue-eu-verordnung-zu-blei-in-aluminiumlegierungen-was-bedeutet-das-fuer-unsere-kunden', img='20240606_mw_144.jpg', tags=['REACH','RoHS','ELV','Bleifrei'], x='Welche Fristen gelten für bleihaltiges Messing und Aluminium – und welche bleifreien Werkstoffe kommen in Frage?'),
 dict(t='Bleifreie Aluminium-Automatenlegierungen: EN AW-2033, 2077 und 6026LF im Vergleich', d='28. März 2022', u='die-zukunft-ist-bleifrei', img='mw-header-aluminium.jpg', tags=['Aluminium','Bleifrei','Zerspanbarkeit'], x='Bleifrei zerspanen: Was EN AW-2033, 2077 und 6026LF können – und was sich in der Fertigung ändert.'),
 dict(t='Umarbeitung von Messing', d='28. März 2022', u='UmarbeitungMessing', img='dsc_9855_-3-.jpg', tags=['Umarbeitung','Kosteneffizienz'], x='Späne und Reststücke sinnvoll verwerten: So funktioniert das Umarbeitungskonto bei Müller & Welte.'),
]

def wissen_card(a):
    tags = ''.join(f'<li>{html.escape(t)}</li>' for t in a['tags'][:3])
    return f'''<a class="card rv" href="https://www.mueller-welte.de/blog/{a["u"]}"><img src="img/{a["img"]}" alt="" loading="lazy" decoding="async"><div class="body"><span class="meta">{a["d"]}</span><h3>{html.escape(a["t"])}</h3><ul class="tags">{tags}</ul><p>{html.escape(a["x"])}</p><span class="more">Weiterlesen →</span></div></a>'''

def wissen():
    body = sub_hero([('Start','index.html'),('Wissen',None)], 'Wissen', 'Fachbeiträge rund um Werkstoffe, Zerspanung, Normen und bleifreie Alternativen – aus der täglichen Praxis unserer Beratung.', 'mw-header-branchen.jpg')
    body += f'<section class="s"><div class="wrap"><div class="cards">{"".join(wissen_card(a) for a in ARTICLES)}</div></div></section>' + cta_band('Noch eine Frage zum Werkstoff?', 'Unsere Vertriebsteam berät Sie gerne – kompetent, ehrlich und ohne Umwege.')
    page('wissen.html', 'Wissen | Müller & Welte', 'Fachbeiträge zu Werkstoffzeugnissen, bleifreien Legierungen, Toleranzen und Zerspanbarkeit von NE-Metallen.', 'Wissen', body)

# ---------------------------------------------------------------- Produkte
def clean_table(t):
    t = t.replace('class="table table-sm table-bordered"', 'class="tbl"').replace('mw-group', 'grp')
    t = re.sub(r'<table[^>]*>', '<table class="tbl">', t, 1)
    return t

def product_page(m):
    d = P[m['name']]; secs = d['sections']; c = m['c']
    chips = ''; blocks = ''
    for i, s in enumerate(secs):
        sid = f's{i}'
        short = re.sub(r'^' + m['name'] + r'[- ]?', '', s['title']).strip(' :-')
        short = re.sub(r'^(Werkstoffe: EN- und DIN-Bezeichnungen)$', 'Werkstoffe', short)
        short = short or s['title']
        chips += f'<a class="chip" href="#{sid}">{html.escape(short.replace("physikalische Eigenschaften","Eigenschaften")[:34])}</a>'
        has_stock = bool(s['table'] and 'Lager' in s['table'] and '●' in s['table'])
        tog = f'<label class="stock-toggle"><input type="checkbox" data-stock-toggle="t{i}"> Nur Lagerprogramm anzeigen</label>' if has_stock else ''
        intro = f'<p class="muted" style="max-width:75ch">{s["intro"]}</p>' if s['intro'] else ''
        tbl = f'<div class="tbl-wrap" id="t{i}" tabindex="0" role="region" aria-label="{html.escape(s["title"])}">{clean_table(s["table"])}</div>' if s['table'] else ''
        note = f'<p class="note">{s["note"]}</p>' if s['note'] else ''
        blocks += f'<details class="tsec" id="{sid}" style="--c:{c}"{" open" if i<2 else ""}><summary><h2>{html.escape(s["title"])}</h2></summary><div class="tbody">{intro}{tog}{tbl}{note}</div></details>'
    switch = ''.join(f'<a href="{x["slug"]}.html"{" aria-current=page" if x is m else ""}><span class="dot" style="background:{x["c"]}"></span>{x["name"]}</a>' for x in MATS)
    types = ''.join(f'<li>{html.escape(t)}</li>' for t in d['types'] if t != 'Allgemeines' and t != 'Eigenschaften')
    body = sub_hero([('Start','index.html'),('Produkte','produkte.html'),(m['name'],None)], m['name'], m['lead'], m['hero'], c)
    body += f'<div class="chipbar" aria-label="Abschnitte"><div class="wrap">{chips}</div></div>'
    body += f'''<section class="s" style="padding-top:var(--s7)"><div class="wrap">
<div class="mat-switch" aria-label="Werkstoff wechseln">{switch}</div>
<div class="split" style="margin-bottom:var(--s6);align-items:start"><div><span class="eyebrow">Lieferformen</span><h2 style="font-size:1.8rem">Was wir von {m["name"]} führen</h2><ul class="tags" style="font-size:1rem">{types}</ul><p class="muted">● im Lagerprogramm = sofort verfügbar. Weitere Legierungen, Abmessungen und Zustände liefern wir über Rahmenverträge mit Abrufaufträgen oder im Streckengeschäft.</p></div>{person()}</div>
{blocks}</div></section>''' + cta_band(f'{m["name"]} in Ihrer Abmessung gesucht?', 'Nicht jede Dimension steht in der Tabelle – fragen Sie uns, wir beschaffen auch Sonderformate direkt vom Hersteller.')
    page(f'{m["slug"]}.html', f'{m["name"]} ab Lager Tuningen | Müller & Welte', f'{m["name"]}: Werkstoffe, Eigenschaften und Lieferformen ab Lager. Zuschnitt ab Losgröße 1.', 'Produkte', body)

def produkte():
    cards = ''.join(f'''<a class="mat rv" href="{m["slug"]}.html" style="--c:{m["c"]}"><img src="img/{m["tile"]}" alt="" loading="lazy" decoding="async"><div><h3>{m["name"]}</h3><p>{m["lead"]}</p><span class="go">Zum Sortiment →</span></div></a>''' for m in MATS)
    body = sub_hero([('Start','index.html'),('Produkte',None)], 'Metall ist nicht gleich Metall.', 'Die Qualität macht den Unterschied: Über 3.500 Artikel ab Lager – Aluminium, Messing, Kupfer, Bronze, Neusilber und Bänder. Direkt von den besten Herstellern Westeuropas.', 'mw-header-home-02.jpg')
    body += f'''<section class="s"><div class="wrap"><div class="mat-grid" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">{cards}</div></div></section>
<section class="s soft"><div class="wrap split"><div class="rv"><span class="eyebrow"><span>Bleifrei</span></span><h2>Jetzt schon auf die neue EU-Verordnung vorbereitet.</h2><p class="lead">Bei Messing und Aluminium erhalten Sie auch bleifreie Legierungen – wichtig für die Umwelt und für unsere Kunden.</p><p>Welche Legierung zu welcher Anwendung passt, erklären wir in unseren Fachbeiträgen oder persönlich am Telefon.</p><div class="cta-row"><a class="btn btn-primary" href="https://www.mueller-welte.de/blog/cuzn39pb3-ersetzen-bleifreies-messing">Bleifreie Messinglegierungen</a><a class="btn btn-ghost" href="wissen.html">Alle Fachbeiträge</a></div></div>
<img class="rv" src="img/messing-drehteil-spanbruch.jpg" alt="Drehteil aus Messing beim Zerspanen" loading="lazy" decoding="async"></div></section>''' + cta_band()
    page('produkte.html', 'Produkte | Aluminium, Messing, Kupfer, Bronze, Neusilber | Müller & Welte', 'Alle Werkstoffe im Überblick: Aluminium, Messing, Kupfer, Bronze und Neusilber ab Lager Tuningen.', 'Produkte', body)

# ---------------------------------------------------------------- Service
def dienstleistungen():
    body = sub_hero([('Start','index.html'),('Service',None),('Dienstleistungen',None)], 'Faszination NE-Metalle', 'Rohstoffe sind unser Geschäft – dafür geben wir alles. Wir sind Partner und Dienstleister für Ihre persönlichen Kundenwünsche.', 'mw-dienstleistungen-logistik-lager.jpg')
    body += f'''
<section class="s"><div class="wrap split"><div class="rv"><span class="eyebrow">Zuschnitt</span><h2>Individuelle Zuschnitte – Präzision und Qualität.</h2>
<p class="lead">Wir bringen Platten und Stangen aus unserem Lager für Sie in die richtige Form und Größe.</p>
<p>Plattenzuschnitte für Aluminium, Messing und Kupfer gehören genauso zu unserem Handwerk wie Blech- und Stangenzuschnitte auf unseren leistungsfähigen Maschinen von Mayer und Behringer. Neben handelsüblichen Formaten beschaffen wir auch Sonderformate direkt vom Hersteller.</p></div>
<img class="rv" src="img/mw-dienstleistungen-zuschnitt-blech.jpg" alt="Blechzuschnitt mit Vakuumheber" loading="lazy" decoding="async"></div></section>
<section class="s soft"><div class="wrap"><div class="cards">
<div class="card rv"><div class="body"><div class="icon">{ic("ruler")}</div><h3>Blech- und Plattenzuschnitte</h3><p>Bis zu einer Plattenstärke von 100 mm toleranzgenau, winklig und mit sauberen Schnittkanten. Größere Stärken kurzfristig lieferbar.</p></div></div>
<div class="card rv"><div class="body"><div class="icon">{ic("scissors")}</div><h3>Stangenzuschnitte</h3><p>Bis Ø 400 mm sind alle Stangen in unterschiedlichen Legierungen in Fixlängen ab 11 mm teilbar.</p></div></div>
<div class="card rv"><div class="body"><div class="icon">{ic("box")}</div><h3>Flexible Bedarfsmengen</h3><p>„Der Kunde ist König – und sein Bedarf ist unser Auftrag.“ Auch Abschnitte und Reststücke kurzfristig, zum aktuellen Tagespreis.</p></div></div></div></div></section>
<section class="s"><div class="wrap split rev"><div class="rv"><span class="eyebrow">Selbstabholung</span><h2>Schnell gebraucht? Einfach abholen.</h2>
<p>Bei Müller &amp; Welte können Sie zu den üblichen Geschäftszeiten alle Materialien direkt in Tuningen abholen. Ein Anruf genügt und Ihre Ware wird noch am selben Tag bereitgestellt. Bei Schneidaufträgen nennen wir Ihnen – just-in-time – die Bearbeitungszeit.</p>
<a class="link-arrow" href="kontakt.html#zeiten">Warenannahme- &amp; Abholzeiten</a></div>
<img class="rv" src="img/mw-dienstleistungen-selbstabholung.jpg" alt="Firmengebäude in Tuningen" loading="lazy" decoding="async"></div></section>
<section class="s dark"><div class="wrap"><div class="sec-head"><span class="eyebrow" style="color:#ff6b72">Logistik</span><h2>Wir wollen, dass Ihr Geschäft läuft.</h2><p class="lead">Höchste Flexibilität und kurze Lieferzeiten. Im Durchschnitt 1.000–1.200 Tonnen Rohstoffe im Lager – nicht Vorrätiges liefern wir kurzfristig über unseren großen Lieferantenstamm.</p></div>
<div class="cards c4">
<div class="step rv" style="background:#262e35;border-color:#36414a;color:#e6eaed"><div class="icon" style="background:#36202a;color:#ff6b72">{ic("truck")}</div><h3 style="color:#fff">Frei Haus ab 500 kg</h3><p style="color:#b4bec7">Im Radius von 100 km mit eigenem Fuhrpark (2 Lkw). Darunter 30 € Frachtanteil je Lieferung.</p></div>
<div class="step rv" style="background:#262e35;border-color:#36414a;color:#e6eaed"><div class="icon" style="background:#36202a;color:#ff6b72">{ic("pin")}</div><h3 style="color:#fff">Deutschland &amp; Europa</h3><p style="color:#b4bec7">Überregional mit erfahrenen Speditionen und Paketdiensten – sicher und fachgerecht.</p></div>
<div class="step rv" style="background:#262e35;border-color:#36414a;color:#e6eaed"><div class="icon" style="background:#36202a;color:#ff6b72">{ic("warehouse")}</div><h3 style="color:#fff">2.500 m² Hochregallager</h3><p style="color:#b4bec7">Über 3.500 Artikel jeder Größe, jedes Formats und jeder Legierung sofort verfügbar.</p></div>
<div class="step rv" style="background:#262e35;border-color:#36414a;color:#e6eaed"><div class="icon" style="background:#36202a;color:#ff6b72">{ic("clock")}</div><h3 style="color:#fff">Termintreue</h3><p style="color:#b4bec7">Ein professionell gemanagter Tourenplan und geschulte Fahrer sorgen für reibungslosen Ablauf.</p></div></div></div></section>
<section class="s"><div class="wrap split"><img class="rv" src="img/20240606_mw_218.jpg" alt="Sägezentrum" loading="lazy" decoding="async"><div class="rv"><span class="eyebrow">Nachhaltigkeit</span><h2>Recycling und Umarbeitung.</h2>
<p>Bei Zuschnitt-Arbeiten anfallende Rückstände und Späne sammeln wir und führen sie als Recyclingrohstoffe in den Kreislauf zurück. Ihre Messing-Späne schreiben wir Ihnen auf Ihrem persönlichen <strong>Umarbeitungskonto</strong> gut.</p>
<ul class="checks"><li>Klein-Container (0,5 m³) für Späne und Abfälle kostenfrei – Anlieferung und Abholung ohne Frachtkosten</li><li>Abschließbare Groß-Container (5–8 m³) auf Wunsch</li><li>Verpackungsmaterial wird bei uns wiederverwendet</li><li>Recyclingquote bei NE-Metallen in Deutschland: 90 % – Tendenz steigend</li></ul></div></div></section>
<section class="s soft"><div class="wrap"><div class="sec-head"><h2>Fragen oder Feedback?</h2><p class="lead">Sie erreichen uns telefonisch oder per E-Mail. Ihre Meinung ist uns wichtig – wir freuen uns über Ihre Anregungen.</p></div>{person()}</div></section>''' + cta_band()
    page('dienstleistungen.html', 'Dienstleistungen | Zuschnitt, Logistik, Recycling | Müller & Welte', 'Zuschnitt ab Losgröße 1, Selbstabholung, eigene Lieferung ab 500 kg frei Haus und Späne-Recycling bei Müller & Welte in Tuningen.', 'Service', body)

def branchen():
    items = [
     ('Automotive und Zulieferer-Industrie','mw-branchen-automotive.jpg','Der Mensch braucht Mobilität. Über ein Viertel unserer Rohstoff-Lieferungen werden in der Automobil- und Zulieferindustrie weiterverarbeitet. Besonders wichtig für den Fahrzeugbau: das „Leichtmetall“ Aluminium. Leichte Fahrzeuge mit neuen Technologien (Elektro- oder Brennstoffzellenmotoren) funktionieren nur mit NE-Metallen.'),
     ('Medizintechnik','mw-branchen-medizintechnik.jpg','Rund 15 Prozent aller verkauften NE-Metalle gehen an Hersteller der Medizinbranche. Unsere Kunden fertigen Geräte für die Endoskopie, Sterilisationsbehälter für den OP-Bereich, Instrumente sowie Produkte zum Patiententransport. Zudem finden sich NE-Metalle als Oberflächenschutz in Salbentuben und Tablettenblistern.'),
     ('Werkzeug- und Maschinenbau','mw-branchen-maschinenbau.jpg','In dieser großen und traditionellen Branche geht nichts ohne Buntmetalle. Unsere Kunden benötigen NE-Halbzeuge in jeder Form und Größe – von speziellen Kleinserien bis zu großen Einzel-Zuschnitten.'),
     ('Elektro-Industrie und Energiewirtschaft','mw-branchen-elektroindustrie.jpg','14 Prozent aller NE-Metalle in Deutschland werden in Elektronik und Energiewirtschaft genutzt. Für moderne Solaranlagen werden bis zu 22 NE-Metalle benötigt, eine Windkraftanlage braucht 14, ein modernes Smartphone kommt auf über 40 Metalle. Immer mit dabei – Produkte von Müller &amp; Welte.'),
     ('Drehteile-Hersteller','mw-branchen-drehteile.jpg','Komplexe Drehteile haben aufwendige Formen: Die Konturen innen, außen und an der Rückseite sind im Einsatz erheblichen Kräften ausgesetzt. Auch hier werden Buntmetalle von Müller &amp; Welte bei regionalen Herstellern verbaut – für hohe Qualität und lange Lebensdauer.'),
    ]
    rows = ''.join(f'<section class="s{" soft" if i%2 else ""}" style="padding:var(--s8) 0"><div class="wrap split{" rev" if i%2 else ""}"><img class="rv" src="img/{img}" alt="" loading="lazy" decoding="async"><div class="rv"><span class="eyebrow">Branche {i+1:02d}</span><h2>{t}</h2><p class="lead" style="font-size:1.1rem">{x}</p></div></div></section>' for i,(t,img,x) in enumerate(items))
    body = sub_hero([('Start','index.html'),('Service',None),('Branchen',None)], 'Branchen', 'So vielseitig Buntmetalle in unserem Leben sind, so vielfältig sind auch unsere Kunden. Fünf große Branchen versorgen wir mit unseren Produkten.', 'mw-header-branchen.jpg')
    body += f'<section class="s"><div class="wrap narrow"><p class="lead">Es ist überraschend, wo unsere Rohstoff-Produkte überall sichtbar und manchmal unsichtbar „versteckt“ sind. Wir liefern nicht nur an Global Players aus der Region: <strong>60 bis 70 Prozent unserer Kunden sind – ebenso wie wir – inhabergeführte Familienunternehmen.</strong> Und wir freuen uns genauso über Haushalt, Garten, Hobby-Werkstatt oder Schulunterricht.</p></div></section>{rows}' + cta_band('Ihre Branche, Ihr Material.', 'Sprechen Sie uns an – wir kennen die Anforderungen und finden die passende Legierung.')
    page('branchen.html', 'Branchen | Müller & Welte', 'Automotive, Medizintechnik, Maschinenbau, Elektro-Industrie und Drehteile: Für diese Branchen liefert Müller & Welte NE-Metalle.', 'Service', body)

# ---------------------------------------------------------------- Unternehmen
TEAM = [
 ('Marius Welte','Geschäftsführer','07464 9897-0','20240606_mw_037.jpg'),
 ('Ralf Müller','Geschäftsführer','07464 9897-0','20240606_mw_185.jpg'),
 ('Heiko Müller','Geschäftsführer','07464 9897-0','20240606_mw_097.jpg'),
 ('Iheb Rezgui','Vertrieb Halbzeuge','07464 9897-11','08d3ccc6-54f7-465c-9d85-9bd11b13f324.jpg'),
 ('Maurice Stein','Vertrieb Halbzeuge / Leiter Logistik','07464 9897-14','20240606_mw_099.jpg'),
 ('Peter Ziegenhagen','Vertrieb Halbzeuge','07464 9897-25','peter-ziegenhagen-vertrieb-halbzeuge.jpg'),
 ('Tamara Baumeister','Vertrieb Halbzeuge','07464 9897-19','20240606_mw_175.jpg'),
 ('Andrea Zernikow','Verwaltung','07464 9897-12','20240606_mw_178.jpg'),
 ('Caroline Weinmann','Kundenservice','07464 9897-16','20240606_mw_080.jpg'),
 ('Cornelia Schäfer','Verwaltung','07464 9897-0','img_1441_2.jpg'),
 ('Vivien Müller','Verwaltung','07464 9897-23','img_7981.jpg'),
 ('Lilli Müller','Verwaltung','07464 9897-24','974af1d0-29ac-4552-aaa4-ac000008b867.jpg'),
]
def team_html():
    def tel(t): return '+49' + re.sub(r'[^\d]', '', t)[1:]
    return '<div class="team">' + ''.join(f'<div class="member rv"><img src="img/{i}" alt="{n}" loading="lazy" decoding="async"><h3>{n}</h3><p>{r}</p><a href="tel:{tel(t)}">{t}</a></div>' for n,r,t,i in TEAM) + '</div>'

HIST = [('1987','Gründung der Metall GmbH Müller & Welte in Tuningen, Baden-Württemberg. Geschäftsführende Gesellschafter: Heinz Müller, Horst Müller und Norbert Welte. Ein Facharbeiter.'),
 ('1991','Vergrößerung der Lagerfläche und Ausbau des Hallenkomplexes auf 2.500 Quadratmeter.'),
 ('1995','Zertifizierung nach DIN EN ISO 9001 für ein durchgehendes Qualitätsmanagement aller Unternehmensprozesse.'),
 ('1998','Heinz Müller verabschiedet sich als geschäftsführender Gesellschafter. Ralf Müller wird neuer Geschäftsführer.'),
 ('2003','Horst Müller scheidet aus. Heiko Müller wird neuer Geschäftsführer.'),
 ('2012','25-jähriges Firmenjubiläum. Eintritt von Tamara Baumeister (geb. Welte).'),
 ('2013','Investition in eine hochmoderne Plattenzuschnittsäge der Otto Mayer Maschinenfabrik.'),
 ('2017','30 Jahre Müller & Welte. Das Team wächst auf 15 Kolleginnen und Kollegen.'),
 ('2018','Als Ausbildungsbetrieb für Groß- und Außenhandelskaufleute gratuliert das Unternehmen der zehnten Auszubildenden zum Abschluss. Eintritt von Marius Welte.'),
 ('2020','Norbert Welte verabschiedet sich. Marius Welte wird neuer Geschäftsführer. Neue Website, neue Unternehmenspräsentation und überarbeitetes Kunden-Portal.')]

def unternehmen():
    hist = ''.join(f'<li class="rv"><strong>{y}</strong><p>{html.escape(t)}</p></li>' for y,t in HIST)
    body = sub_hero([('Start','index.html'),('Unternehmen',None)], 'Erstklassige Beratung, Kompetenz und Kundennähe.', 'Seit 1987 sind wir als Händler in der Welt der Nichteisen-Metalle zuhause – familiengeführt, regional verwurzelt und fest an der Seite unserer Kunden.', 'mw-unternehmen-entladen.jpg')
    body += f'''
<section class="s"><div class="wrap split"><div class="rv"><span class="eyebrow">Über uns</span><h2>Ein Partner, der hält, was er verspricht.</h2>
<p class="lead">Hochwertige Produkte zu fairen Preisen, erstklassiges Know-how in allen Belangen der Metallverarbeitung, besten Kundendienst und einen zuverlässigen, schnellen Lieferservice.</p>
<p>Unser Unternehmen gehört zu den führenden Handelshäusern der Metallbranche in Süddeutschland. Das mittelständische, familiengeführte Unternehmen wird bereits in zweiter Generation geführt und ist mit seinen Geschäftspartnern und Mitarbeitern fest in der Region verwurzelt. Unser Qualitätsmanagement nach DIN EN ISO 9001 garantiert gleichbleibend hohe Leistung bei allen relevanten Prozessen.</p>
<p><strong>Wir kennen unsere Kunden noch mit Namen und Gesicht. Und das soll auch in Zukunft so sein!</strong></p></div>
<img class="rv" src="img/20240606_mw_187.jpg" alt="Das Müller-&amp;-Welte-Team" loading="lazy" decoding="async"></div></section>
<section class="s soft"><div class="wrap"><div class="cards">
<div class="card rv"><div class="body"><div class="icon">{ic("users")}</div><h3>Kundennähe &amp; Kompetenz</h3><p>Eine echte, gelebte Partnerschaft aus Vertrauen und Verständnis. Wertschätzung, Offenheit und Transparenz – mit Lieferanten, Kunden und Mitarbeitern. Wir sind persönlich für Sie da.</p></div></div>
<div class="card rv"><div class="body"><div class="icon">{ic("clock")}</div><h3>Einfach, schnell, digital</h3><p>Bestellung, Preise, Zuschnitt-Konfigurator und Logistik – im Kundenportal behalten Sie die volle Kontrolle. Und weiterhin: unser Katalog in Papierform und persönliche telefonische Beratung.</p></div></div>
<div class="card rv"><div class="body"><div class="icon">{ic("warehouse")}</div><h3>Große Auswahl &amp; faire Preise</h3><p>600 bis 800 Tonnen Rohstoff-Metalle auf 2.500 m². Mehr als 3.500 Artikel sofort verfügbar, Zuschnitt auf Maß, eigene Auslieferung im Umkreis von 100 km – kostenfrei ab 500 kg.</p></div></div></div></div></section>
<section class="s" id="team"><div class="wrap"><div class="sec-head"><span class="eyebrow">Das Team</span><h2>20 Menschen, die Metall lieben.</h2><p class="lead">Seit der Gründung 1987 mit einem Angestellten ist das inhabergeführte Familienunternehmen gesund gewachsen. Neben den drei Geschäftsführern beschäftigen wir siebzehn Mitarbeiterinnen und Mitarbeiter mit großem Know-how und technischem Verständnis.</p></div>{team_html()}</div></section>
<section class="s soft"><div class="wrap split"><div class="rv"><span class="eyebrow">Zertifiziert</span><h2>ISO 9001:2015 – seit 1995.</h2>
<p>Bereits in den neunziger Jahren haben wir uns als eines der ersten Metallhandelshäuser in Deutschland für ein durchgehendes Qualitätsmanagement entschieden. Nach einem anspruchsvollen Audit wurde das Unternehmen 1995 nach DIN EN ISO 9001 ausgezeichnet. Diese Zertifizierung ist für viele Geschäftsbeziehungen von großer Bedeutung, da zahlreiche Verträge nur mit auditierten Unternehmen geschlossen werden dürfen.</p>
<p class="muted">Das Zertifikat stellen wir Ihnen auf Anfrage gern zur Verfügung.</p></div>
<img class="rv" src="img/20240606_mw_207.jpg" alt="Beratung im Büro" loading="lazy" decoding="async"></div></section>
<section class="s" id="historie"><div class="wrap"><div class="sec-head"><span class="eyebrow">Historie</span><h2>Qualität mit Tradition.</h2></div><ol class="timeline narrow" style="margin-left:.5rem">{hist}</ol></div></section>''' + cta_band('Wir freuen uns, Sie kennenzulernen.', 'Besuchen Sie uns in Tuningen oder rufen Sie einfach an.')
    page('unternehmen.html', 'Unternehmen | Über Müller & Welte | Metallhandel seit 1987', 'Familiengeführter NE-Metallhändler in Tuningen: Team, Qualitätsmanagement nach ISO 9001 und Historie seit 1987.', 'Unternehmen', body)

# ---------------------------------------------------------------- Kontakt
def kontakt():
    body = sub_hero([('Start','index.html'),('Kontakt',None)], 'Kontakt', 'Sie erreichen uns telefonisch oder per E-Mail. Wenn Ihr Ansprechpartner gerade nicht erreichbar ist, hinterlassen Sie eine kurze Nachricht – wir melden uns schnellstmöglich.', 'mw-kontakt-lager.jpg')
    body += f'''<section class="s"><div class="wrap contact-grid">
<div><h2>Kontaktanfrage</h2>
<form class="f" id="kontaktform" novalidate="false">
<div class="two"><div><label for="anrede">Anrede</label><select id="anrede" name="anrede"><option value="">Bitte wählen …</option><option>Frau</option><option>Herr</option><option>Keine Angabe</option></select></div><div></div></div>
<div class="two"><div><label for="vorname">Vorname*</label><input id="vorname" name="vorname" autocomplete="given-name" required></div><div><label for="nachname">Nachname*</label><input id="nachname" name="nachname" autocomplete="family-name" required></div></div>
<div class="two"><div><label for="email">E-Mail-Adresse*</label><input id="email" name="email" type="email" autocomplete="email" required></div><div><label for="telefon">Telefon*</label><input id="telefon" name="telefon" type="tel" autocomplete="tel" required></div></div>
<div><label for="betreff">Betreff*</label><input id="betreff" name="betreff" required></div>
<div><label for="nachricht">Ihre Nachricht*</label><textarea id="nachricht" name="nachricht" required placeholder="Werkstoff, Abmessung, Menge, gewünschter Zuschnitt …"></textarea></div>
<label class="chk"><input type="checkbox" required> <span>Ich habe die <a href="datenschutz.html">Datenschutzbestimmungen</a> zur Kenntnis genommen und erkenne diese an.*</span></label>
<p class="note">Die mit * markierten Felder sind Pflichtfelder.</p>
<div><button class="btn btn-primary" type="submit">Anfrage senden {ic("arrow")}</button></div></form></div>
<aside><div class="hours" id="zeiten"><h3>Unsere Geschäftszeiten</h3><span class="open-now" id="open-now"><i></i><b>Büro</b></span>
<h4 style="font-size:1rem;margin-bottom:.4rem">Büro</h4><dl><dt>Mo – Do</dt><dd>7.30 – 12.00 · 13.00 – 17.00 Uhr</dd><dt>Freitag</dt><dd>7.30 – 12.00 · 13.00 – 15.00 Uhr</dd></dl>
<h4 style="font-size:1rem;margin-bottom:.4rem">Warenannahme &amp; Selbstabholung</h4><dl><dt>Mo – Do</dt><dd>7.00 – 12.00 · 13.00 – 16.45 Uhr</dd><dt>Freitag</dt><dd>7.00 – 12.00 · 12.45 – 14.00 Uhr</dd><dt>Pause</dt><dd>9.00 – 9.15 Uhr</dd></dl>
<address class="addr"><p style="margin-bottom:.6rem"><strong>Müller &amp; Welte Metall GmbH</strong><br>Gewerbestr. 20, 78609 Tuningen</p><p style="margin:0">Tel. <a href="tel:{TEL_HREF}">{TEL}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p></address>
<p style="margin:var(--s4) 0 0"><a class="link-arrow" href="https://www.google.com/maps/search/?api=1&amp;query=Gewerbestr.+20,+78609+Tuningen" rel="noopener">Route planen</a></p></div></aside></div></section>
<section class="s soft" id="team"><div class="wrap"><div class="sec-head"><span class="eyebrow">Ansprechpartner</span><h2>Direkt zu den Richtigen.</h2><p class="lead">Zentrale: <a href="tel:{TEL_HREF}">{TEL}</a></p></div>{team_html()}</div></section>'''
    page('kontakt.html', 'Kontakt | Müller & Welte Metall GmbH, Tuningen', 'Kontakt, Öffnungszeiten und Ansprechpartner der Müller & Welte Metall GmbH, Gewerbestr. 20, 78609 Tuningen.', 'Kontakt', body)

# ---------------------------------------------------------------- Rechtliches
def impressum():
    body = sub_hero([('Start','index.html'),('Impressum',None)], 'Impressum', '', 'mw-header-branchen.jpg').replace('<p class="lead"></p>','')
    body += f'''<section class="s"><div class="wrap narrow prose"><h2>Metall GmbH Müller &amp; Welte</h2>
<p>Gewerbestr. 20<br>78609 Tuningen<br>Tel. <a href="tel:{TEL_HREF}">{TEL}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p>
<p><strong>Gesellschafter:</strong> Marius Welte, Ralf Müller, Heiko Müller<br><strong>Geschäftsführer:</strong> Marius Welte, Ralf Müller, Heiko Müller<br><strong>Sitz der Gesellschaft:</strong> Gewerbestr. 20, 78609 Tuningen<br><strong>Registergericht Freiburg i. Br.:</strong> HRB 601212<br><strong>USt-IdNr.:</strong> DE142987469<br><strong>Erfüllungsort</strong> für beide Teile ist VS-Schwenningen</p>
<h3>AGB</h3><p>Unsere Geschäftsbedingungen können Sie per Download der PDF-Datei einsehen: <a href="https://www.mueller-welte.de/media/MW_Liefer-und-Zahlungsbedingungen.pdf">Allgemeine Geschäftsbedingungen herunterladen</a></p>
<h3>Haftungsausschluss</h3><p>Die Firma Metall GmbH Müller &amp; Welte übernimmt keine Garantie dafür, dass die auf dieser Website bereitgestellten Informationen vollständig, richtig und in jedem Fall aktuell sind. Dies gilt auch für alle Verbindungen („Links“), auf die diese Website direkt oder indirekt verweist.</p>
<p>Die Firma Metall GmbH Müller &amp; Welte ist für den Inhalt einer Seite, die mit einem solchen Link erreicht wird, nicht verantwortlich.</p>
<p>Die Firma Metall GmbH Müller &amp; Welte behält sich das Recht vor, ohne vorherige Ankündigung Änderungen oder Ergänzungen der bereitgestellten Informationen vorzunehmen.</p>
<h3>Fotografie</h3><p>Nico Pudimat, <a href="https://www.nicopudimat.de">www.nicopudimat.de</a></p></div></section>'''
    page('impressum.html', 'Impressum | Müller & Welte', 'Impressum der Metall GmbH Müller & Welte, Tuningen.', '', body)

def datenschutz():
    lines = open(f'{ROOT}/_src/datenschutz.txt', encoding='utf8').read().split('\n')[2:]
    out = []
    for l in lines:
        e = html.escape(l)
        if re.match(r'^\d+\. ', l): out.append(f'<h2>{e}</h2>')
        elif len(l) < 70 and not re.search(r'[.:;,]$', l): out.append(f'<h3>{e}</h3>')
        else: out.append(f'<p>{e}</p>')
    body = sub_hero([('Start','index.html'),('Datenschutz',None)], 'Datenschutz', '', 'mw-header-branchen.jpg').replace('<p class="lead"></p>','')
    body += f'<section class="s"><div class="wrap narrow prose">{"".join(out)}</div></section>'
    page('datenschutz.html', 'Datenschutz | Müller & Welte', 'Datenschutzerklärung der Metall GmbH Müller & Welte.', '', body)

open(f'{ROOT}/img/favicon.svg', 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#1d2329"/><path d="M6 24V8h3l7 9 7-9h3v16h-3V13l-7 9-7-9v11z" fill="#fff"/><rect x="6" y="26" width="20" height="2" fill="#e41019"/></svg>')

home(); produkte(); [product_page(m) for m in MATS]; dienstleistungen(); branchen(); unternehmen(); wissen(); kontakt(); impressum(); datenschutz()
print('ok')
