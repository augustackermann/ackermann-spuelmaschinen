#!/usr/bin/env python3
"""Static-site generator for the Ackermann Spülmaschinen recreation.
Runs top-to-bottom, writing every page with a shared header/footer so the
navigation stays consistent. Re-run after editing content: `python3 build.py`.
"""
import os, html, json, re

ROOT = os.path.dirname(os.path.abspath(__file__))
OFFICIAL_PAGES_PATH = os.path.join(ROOT, "official_pages.json")

def load_official_pages():
    if not os.path.exists(OFFICIAL_PAGES_PATH):
        return {}
    with open(OFFICIAL_PAGES_PATH, encoding="utf-8") as f:
        return json.load(f)

OFFICIAL_PAGES = load_official_pages()

# ---------------------------------------------------------------- navigation
NAV = [
    ("Willkommen", "/", []),
    ("Lösungen für", None, [
        ("Gastronomie und Hotellerie", "/gastronomie-und-hotellerie/"),
        ("Gemeinschaftsverpflegung und Catering", "/gemeinschaftsverpflegung-und-catering/"),
        ("Bäckereien und Metzgereien", "/baeckereien-und-metzgereien/"),
        ("Außer Haus und mobiles Spülen", "/ausser-haus-und-mobiles-spuelen/"),
    ]),
    ("Produkte", None, [
        ("Spülmaschinen", "/produkte/spuelmaschinen/"),
        ("Spülchemie", "/produkte/spuelchemie/"),
    ]),
    ("Über uns", "/ueber-uns/", [
        ("Unser Team", "/ueber-uns/"),
        ("Qualität", "/ueber-uns/qualitaet/"),
        ("Service", "/ueber-uns/service/"),
        ("Innovationen", "/ueber-uns/innovationen/"),
        ("Nachhaltigkeit", "/ueber-uns/nachhaltigkeit/"),
    ]),
    ("Die Andersmacher", None, [
        ("Max.Café", "/die-andersmacher/max-cafe/"),
        ("Härle‘s Hofcafé", "/die-andersmacher/haerles-hofcafe/"),
        ("Pier 40", "/die-andersmacher/pier-40/"),
        ("Haus Nazareth", "/die-andersmacher/haus-nazareth/"),
        ("Stotz Hof", "/die-andersmacher/stotz-hof/"),
        ("Biolandhof Kelly", "/die-andersmacher/biolandhof-kelly/"),
        ("Metzgerei Kutter", "/die-andersmacher/metzgerei-kutter/"),
        ("Culina", "/die-andersmacher/culina/"),
        ("Hirscheck", "/die-andersmacher/hirscheck/"),
        ("Ellgass", "/die-andersmacher/ellgass/"),
    ]),
    ("Karriere", "/karriere/", []),
    ("News", "/news/", []),
    ("Kontakt", "/kontakt/", []),
]

def nav_html(active):
    items = []
    for label, url, kids in NAV:
        if kids:
            sub = "".join(
                f'<a href="{k_url}"{" class=\'active\'" if k_url==active else ""}>{html.escape(k_label)}</a>'
                for k_label, k_url in kids)
            top = f'<a href="{url}">{html.escape(label)}</a>' if url else f'<span>{html.escape(label)}</span>'
            items.append(
                f'<li class="has-sub">{top}<span class="caret">▾</span><div class="submenu">{sub}</div></li>')
        else:
            cls = ' class="active"' if url == active else ""
            items.append(f'<li><a href="{url}"{cls}>{html.escape(label)}</a></li>')
    return "\n".join(items)

# ------------------------------------------------------------ page shell
def page(active, title, body, description=""):
    year = 2026
    nav = nav_html(active)
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} | Ackermann Spülmaschinen</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" type="image/x-icon" href="/assets/img/favicon.ico">
<link rel="apple-touch-icon" href="/assets/img/bee-teal.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
</head>
<body>

<div class="topbar">
  <div class="container topbar__inner">
    <div class="topbar__contact">
      <a href="tel:+4975029779100">&#9742; +49 (0)7502 97791&nbsp;00</a>
      <a href="mailto:info@ackermann-spuelmaschinen.de">&#9993; info@ackermann-spuelmaschinen.de</a>
    </div>
    <a class="topbar__shop" href="/kontakt/">Zum Händlershop &rarr;</a>
  </div>
</div>

<header class="header" id="top">
  <div class="container header__inner">
    <a href="/" class="brand" aria-label="Ackermann Spülmaschinen Startseite">
      <img src="/assets/img/ackermann-logo-web-3.png" alt="Ackermann Spülmaschinen" class="brand__logo">
    </a>
    <nav class="nav" aria-label="Hauptnavigation">
      <ul>{nav}</ul>
    </nav>
    <button class="nav-toggle" aria-label="Menü umschalten" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>

<main>
{body}
</main>

<footer class="footer">
  <div class="container footer__inner">
    <div class="footer__brand">
      <img src="/assets/img/bee-light.png" alt="Ackermann Biene" class="footer__bee">
      <p class="footer__claim">Einfach näher dran:<br>Spülmaschinen für Andersmacher.</p>
      <p class="footer__addr">Ackermann Spülmaschinen GmbH<br>Am Umspannwerk 18<br>88255 Baindt</p>
    </div>
    <nav class="footer__col" aria-label="Lösungen">
      <h4>Lösungen für</h4>
      <a href="/gastronomie-und-hotellerie/">Gastronomie &amp; Hotellerie</a>
      <a href="/gemeinschaftsverpflegung-und-catering/">Gemeinschaftsverpflegung &amp; Catering</a>
      <a href="/baeckereien-und-metzgereien/">Bäckereien &amp; Metzgereien</a>
      <a href="/ausser-haus-und-mobiles-spuelen/">Außer Haus &amp; mobiles Spülen</a>
    </nav>
    <nav class="footer__col" aria-label="Produkte und Unternehmen">
      <h4>Entdecken</h4>
      <a href="/produkte/spuelmaschinen/">Spülmaschinen</a>
      <a href="/produkte/spuelchemie/">Spülchemie</a>
      <a href="/ueber-uns/">Über uns</a>
      <a href="/die-andersmacher/">Die Andersmacher</a>
      <a href="/karriere/">Karriere</a>
      <a href="/news/">News</a>
    </nav>
    <nav class="footer__col" aria-label="Kontakt und Links">
      <h4>Links</h4>
      <a href="tel:+4975029779100">+49 (0)7502 97791 00</a>
      <a href="mailto:info@ackermann-spuelmaschinen.de">info@ackermann-spuelmaschinen.de</a>
      <div class="footer__social">
        <a href="https://www.facebook.com/ackermann.spuelmaschinen/?locale=de_DE" target="_blank" rel="noopener">Facebook</a>
        <a href="https://www.instagram.com/ackermann_spuelmaschinen/" target="_blank" rel="noopener">Instagram</a>
      </div>
      <a href="/impressum/">Impressum</a>
      <a href="/datenschutz/">Datenschutz</a>
      <a href="/cookie-richtlinie-eu/">Cookie-Richtlinie (EU)</a>
      <a href="/downloadbereich/">Downloadbereich</a>
    </nav>
  </div>
  <div class="footer__bottom"><div class="container">© {year} Ackermann Spülmaschinen GmbH · Baindt · Näher dran sein.</div></div>
</footer>

<script src="/script.js"></script>
</body>
</html>
"""

def hero(eyebrow, h1, lead, cta=None, img=None, cls=""):
    actions = ""
    if cta:
        actions = '<div class="hero__actions">' + "".join(
            f'<a href="{u}" class="btn {c}">{html.escape(t)}</a>' for t, u, c in cta) + '</div>'
    figure = f'<div class="hero__media"><img src="{img}" alt=""></div>' if img else ""
    grid = " hero--split" if img else ""
    return f"""<section class="hero {cls}{grid}">
  <div class="container hero__inner">
    <div class="hero__content">
      <p class="eyebrow eyebrow--light">{html.escape(eyebrow)}</p>
      <h1>{h1}</h1>
      <p class="hero__lead">{lead}</p>
      {actions}
    </div>
    {figure}
  </div>
</section>"""

def section_head(eyebrow, h2, sub="", light=False):
    lc = " section__head--light" if light else ""
    ec = " eyebrow--light" if light else ""
    subhtml = f'<p class="section__sub">{sub}</p>' if sub else ""
    return f'<div class="section__head{lc}"><p class="eyebrow{ec}">{html.escape(eyebrow)}</p><h2>{h2}</h2>{subhtml}</div>'

# ---------------------------------------------------------------- data
SOLUTIONS = [
    ("U-540-Bistro.png", "Gastronomie und Hotellerie", "/gastronomie-und-hotellerie/",
     "Zuverlässige Technik für Cafés, Bars, Restaurants und Hotels – einfach zu bedienen und wartungsarm."),
    ("H-640.png", "Gemeinschaftsverpflegung und Catering", "/gemeinschaftsverpflegung-und-catering/",
     "Spültechnik, mit der man rechnen kann – robuste Geräte für hohe Durchsätze und faire Betriebskosten."),
    ("F-920.png", "Bäckereien und Metzgereien", "/baeckereien-und-metzgereien/",
     "Heiß und fettig? Mit uns bleibst Du cool. Meister der Vielfalt für Bleche, Geschirr und Behälter."),
    ("spuelmobil.jpg", "Außer Haus und mobiles Spülen", "/ausser-haus-und-mobiles-spuelen/",
     "Mit dem Spülmobil erfüllst Du alle Vorschriften und gewinnst maximale Flexibilität für jeden Einsatzort."),
]

MACHINES = {
    "Untertischspülmaschinen": [
        ("U 430-2", "Gläser", "U-430-2.png", "u-430-2"),
        ("U 440", "Gläser", "U-440.png", "u-440"),
        ("U 540 Bistro", "Gläser", "U-540-Bistro.png", "u-540-bistro"),
        ("U 530-2 / U 530-2E", "Gläser / Geschirr", "U-530-2.png", "u-530-2"),
        ("U 540 / U 540E", "Gläser / Geschirr", "U-540E.png", "u-540e"),
        ("U 640 / U 640E", "Gläser / Geschirr / Gerätschaften", "U-640E.png", "u-640e"),
    ],
    "Haubenspülmaschinen": [
        ("H 530-2 / H 530-2E", "Gläser / Geschirr", "H-530-2.png", "h-530-2"),
        ("H 540 / H 540E", "Gläser / Geschirr", "H-540E.png", "h-540e"),
        ("H 540 Klima+ / H 540E Klima+", "Gläser / Geschirr", "H-540E-Klima-Plus.png", "h-540e-klima-plus"),
        ("H 640", "Gläser / Geschirr / Gerätschaften", "H-640.png", "h-640"),
        ("H 640 Klima+", "Gläser / Geschirr / Gerätschaften", "H-640-Klima-Plus.png", "h-640-klima-plus"),
    ],
    "Gerätespülmaschinen": [
        ("F 720", "Gerätschaften", "F-720.png", "f-720"),
        ("F 920", "Gerätschaften", "F-920.png", "f-920"),
    ],
    "Korbtransportspülmaschinen": [
        ("KT-1", "Gläser / Geschirr / Gerätschaften", "KT1.png", "kt-1"),
        ("KT-1 PLUS", "Gläser / Geschirr / Gerätschaften", "KT1-Plus.png", "kt-1-plus"),
        ("KT-2", "Gläser / Geschirr / Gerätschaften", "KT2.png", "kt-2"),
        ("KT-2 PLUS", "Gläser / Geschirr / Gerätschaften", "KT2-Plus.png", "kt-2-plus"),
    ],
}

ANDERSMACHER = [
    ("Max.Café", "Ackermann_Max_Cafe_2.jpg", "/die-andersmacher/max-cafe/"),
    ("Härle's Hofcafé", "Ackermann_Haerle_Slider-3.jpg", "/die-andersmacher/haerles-hofcafe/"),
    ("Pier 40", "Ackermann-Spuelmaschinen-Pier40-Slider.jpg", "/die-andersmacher/pier-40/"),
    ("Haus Nazareth", "HausNazareth_Ackermann_Spuelmaschinen-Slider.jpg", "/die-andersmacher/haus-nazareth/"),
    ("Stotz Hof", "ackermann-slider-stotzhof.jpg", "/die-andersmacher/stotz-hof/"),
    ("Metzgerei Kutter", "metzgerei-kutter-slider.jpg", "/die-andersmacher/metzgerei-kutter/"),
    ("Culina", "ackermann-andersmacher-culina-slider.jpg", "/die-andersmacher/culina/"),
    ("Hirscheck", "Hirscheck_12.jpg", "/die-andersmacher/hirscheck/"),
    ("Biolandhof Kelly", None, "/die-andersmacher/biolandhof-kelly/"),
    ("Ellgass", None, "/die-andersmacher/ellgass/"),
]

# (name, group, description, image, datasheet-pdf-or-None)
CHEMIE_PRODUCTS = [
    ("F 440 Bistro", "Reiniger", "Flüssigreiniger zur Anwendung in gewerblichen Gläser- und Geschirrspülmaschinen.",
     "F_440_Bistro.jpg", "F440_Bistro.pdf"),
    ("F 450 green", "Reiniger", "Umweltschonender Flüssigreiniger für gewerbliche Gläser- und Geschirrspülmaschinen.",
     "F_450_Green.jpg", "F450-Green.pdf"),
    ("F 500 GS", "Reiniger", "Flüssigreiniger zur Anwendung in gewerblichen Geschirrspülmaschinen.",
     "F_500_GS.jpg", "F500-GS.pdf"),
    ("P 500 GS", "Reiniger", "Pulverreiniger zur Anwendung in gewerblichen Geschirrspülmaschinen.",
     "P_500_GS-3.jpg", "Pulverreiniger-P-500-GS.pdf"),
    ("F 540 Power", "Reiniger", "Kraftvoller Flüssigreiniger für gewerbliche Geschirrspülmaschinen.",
     "F_540_Power.jpg", "F540-Power.pdf"),
    ("F 600 GR", "Reiniger", "Flüssigreiniger für gewerbliche Geschirr- und Gerätespülmaschinen.",
     "F_600_GR.jpg", "F600-GR.pdf"),
    ("Gläsergrundreiniger", "Spezialreiniger", "Flüssiger Spezialreiniger zur Grundreinigung von Gläsern vor dem ersten maschinellen Spülen.",
     "Glaesergrundreiniger.jpg", "Grundreiniger.pdf"),
    ("KLAR GS", "Klarspüler", "Universeller, leicht saurer Klarspüler mit gutem Benetzungsvermögen und schaumreduzierender Wirkung.",
     "Klar_GS.jpg", "Klar-GS.pdf"),
    ("KLAR GG sauer", "Klarspüler", "Saurer Klarspüler, besonders geeignet für Gläser sowie Edelstahl- und Kunststoffgeschirr.",
     "Klar_GG_sauer.jpg", "Klar-GG-sauer.pdf"),
    ("Entkalker F", "Pflege", "Flüssiger Entkalker gegen Kalkablagerungen – für Spülmaschinen, Kaffeemaschinen, Heißluftdämpfer und Heißwasseraufbereiter.",
     "Entkalker.jpg", "Entkalker-F.pdf"),
    ("Regeneriersalz 2/6", "Pflege", "Regeneriersalz für Spülmaschinen mit eingebautem Enthärter.",
     "Geschirrspuelsalz.jpg", None),
]

ACKERMANN_REASONS = [
    ("Unser Team", "/ueber-uns/", "Bodenständig, persönlich und nah dran an den Menschen, die täglich mit unserer Technik arbeiten."),
    ("Qualität", "/ueber-uns/qualitaet/", "Robuste Maschinen, gebaut für den harten Alltag in Küche, Betrieb und Dauereinsatz."),
    ("Service", "/ueber-uns/service/", "Flächendeckend in ganz Deutschland erreichbar, damit Hilfe schnell dort ist, wo sie gebraucht wird."),
    ("Innovation", "/ueber-uns/innovationen/", "Wirklich brauchbare Innovationen für Einfachheit, Bedienfreundlichkeit und weniger Schnickschnack."),
    ("Nachhaltigkeit", "/ueber-uns/nachhaltigkeit/", "Extrem niedriger Wasser- und Energieverbrauch."),
]

# ---------------------------------------------------------------- builders
def cards_solutions():
    c = "".join(f"""<a class="card" href="{u}">
  <div class="card__media"><img src="/assets/img/{'machines/' if img != 'spuelmobil.jpg' else ''}{img}" alt="{html.escape(t)}"></div>
  <h3>{html.escape(t)}</h3>
  <p>{html.escape(d)}</p>
  <span class="card__link">Mehr erfahren &rarr;</span>
</a>""" for img, t, u, d in SOLUTIONS)
    return f'<div class="cards cards--4">{c}</div>'

def machine_grid():
    out = []
    for cat, items in MACHINES.items():
        cards = "".join(f"""<a class="machine" href="/produkte/spuelmaschinen/{slug}/">
  <div class="machine__media"><img src="/assets/img/machines/{img}" alt="{html.escape(name)}" loading="lazy"></div>
  <h4>{html.escape(name)}</h4>
  <p>{html.escape(use)}</p>
  <span class="machine__link">Details &amp; Datenblatt &rarr;</span>
</a>""" for name, use, img, slug in items)
        out.append(f'<h3 class="machine-cat">{html.escape(cat)}</h3><div class="cards cards--4 machine-row">{cards}</div>')
    return "\n".join(out)

def andersmacher_grid():
    c = ""
    for name, img, url in ANDERSMACHER:
        media = (f'<img src="/assets/img/{img}" alt="{html.escape(name)}" loading="lazy">'
                 if img else f'<div class="ref__placeholder">{html.escape(name)}</div>')
        c += f'<a class="ref" href="{url}"><div class="ref__media">{media}</div><span class="ref__name">{html.escape(name)}</span></a>'
    return f'<div class="cards cards--4 refs">{c}</div>'

# Real quotes + people from the official homepage slider (own company content)
STORY_SLIDES = [
    ("Mit so wenig Wasser so sauber spülen", "Bruno Stotz", "Der Stotz Hof, Markdorf",
     "ackermann-slider-stotzhof.jpg", "/die-andersmacher/stotz-hof/"),
    ("Die stehen zu ihrem Produkt", "Michael Habereder", "Haus Nazareth, Sigmaringen",
     "HausNazareth_Ackermann_Spuelmaschinen-Slider.jpg", "/die-andersmacher/haus-nazareth/"),
    ("Unschlagbar in Preis/Leistung", "Anna Härle-Löffler", "Härle's Hofcafé, Ostrach",
     "Ackermann_Haerle_Slider-3.jpg", "/die-andersmacher/haerles-hofcafe/"),
    ("Beim Service meilenweit voraus", "Maximilian Sedelmayr", "Max.Café, Weingarten",
     "Ackermann_Max_Cafe_2.jpg", "/die-andersmacher/max-cafe/"),
    ("Lieber einfach und länger haltbar als Schnickschnack", "Laila Klinger", "Pier 40, Friedrichshafen",
     "Ackermann-Spuelmaschinen-Pier40-Slider.jpg", "/die-andersmacher/pier-40/"),
    ("Wir sind nach wie vor begeistert", "Gerhard Kutter", "Metzgerei Kutter, Bermatingen",
     "metzgerei-kutter-slider.jpg", "/die-andersmacher/metzgerei-kutter/"),
    ("Bei Ackermann stimmt die DNA", "Dr. Reinhard Klumpp", "Culina GmbH & Co. KG, Friedrichshafen",
     "ackermann-andersmacher-culina-slider.jpg", "/die-andersmacher/culina/"),
    ("Wir geben 5 von 5 Sternen", "Kim Fleck und Florian Lorenz", "Hirscheck, Ravensburg",
     "Hirscheck_12.jpg", "/die-andersmacher/hirscheck/"),
    ("Ein Unternehmen mit Haltung", "Felix Ellgass", "Ellgass Allgäu-Hotel",
     "ellgass-hotel.jpg", "/die-andersmacher/ellgass/"),
]

def story_slider():
    photos = ""
    dots = ""
    for i, (quote, person, firm, img, url) in enumerate(STORY_SLIDES):
        active = " is-active" if i == 0 else ""
        photos += f"""<img class="story-photo{active}" src="/assets/img/{img}" alt="{html.escape(firm)}"
          data-quote="{html.escape(quote)}" data-person="{html.escape(person)}"
          data-firm="{html.escape(firm)}" data-url="{url}" loading="{'eager' if i == 0 else 'lazy'}">"""
        dots += f'<button class="story-dot{active}" data-go="{i}" aria-label="Story {i+1}"></button>'
    first = STORY_SLIDES[0]
    return f"""<section class="story" id="stories" aria-label="Die Andersmacher – Kundenstimmen">
  <div class="as-grid">
    <div class="as-panel">
      <img src="/assets/img/bee-teal.png" alt="" class="as-panel__bee" aria-hidden="true">
      <p class="eyebrow eyebrow--light">Die Andersmacher</p>
      <blockquote id="story-quote">&bdquo;{html.escape(first[0])}&ldquo;</blockquote>
      <div class="as-person">
        <strong id="story-person">{html.escape(first[1])}</strong>
        <span id="story-firm">{html.escape(first[2])}</span>
      </div>
      <a id="story-link" href="{first[4]}" class="btn btn--ghost btn--sm">Zur Story &rarr;</a>
      <div class="story-dots">{dots}</div>
    </div>
    <div class="as-media">
      {photos}
      <button class="story-arrow story-arrow--prev" aria-label="Vorherige Story">&#8249;</button>
      <button class="story-arrow story-arrow--next" aria-label="Nächste Story">&#8250;</button>
    </div>
  </div>
</section>"""

def cta_band(title, text, btn_text="Kontakt aufnehmen", btn_url="/kontakt/"):
    return f"""<section class="cta"><div class="container cta__inner">
  <div><h2>{title}</h2><p>{text}</p></div>
  <a href="{btn_url}" class="btn btn--dark">{html.escape(btn_text)}</a>
</div></section>"""

# ---------------------------------------------------------------- pages
PAGES = {}

# HOME
PAGES["/"] = ("index.html", "Dein Partner für gewerbliche Spültechnik", page(
 "/", "Dein Partner für gewerbliche Spültechnik",
story_slider()
 + """<section class="section partner">
  <div class="container partner__inner">
    <div class="partner__copy">
      <h1>Dein Partner für gewerbliche Spültechnik</h1>
      <p class="partner__text">Ackermann Spülmaschinen ist Dein Partner für gewerbliche Spülmaschinen:
      ob in der <a href="/gastronomie-und-hotellerie/">Gastronomie und Hotellerie</a>, der
      <a href="/gemeinschaftsverpflegung-und-catering/">Gemeinschaftsverpflegung</a>, für
      <a href="/baeckereien-und-metzgereien/">Bäckereien und Metzgereien</a> oder beim
      <a href="/ausser-haus-und-mobiles-spuelen/">mobilen Spülen</a> auf Feiern und Festen.
      Wir bieten Dir das beste Preis-Leistungs-Verhältnis im Premiumbereich und darüber hinaus einen
      erstklassigen <a href="/ueber-uns/service/">Service</a>, sinnvolle
      <a href="/ueber-uns/innovationen/">Innovationen</a> und
      <a href="/ueber-uns/nachhaltigkeit/">nachhaltige Lösungen</a> – zum Beispiel durch einen
      extrem niedrigen Wasserverbrauch.</p>
      <a href="#loesungen" class="btn btn--primary">Entdecke unsere Lösungen für Deine Branche!</a>
    </div>
    <div class="partner__team">
      <img src="/assets/img/Gruppenbild-2.png" alt="Das Ackermann Spülmaschinen Team">
    </div>
  </div>
</section>"""
 + """<section class="section section--dark alt-sec">
  <div class="container alt-sec__inner">
    <div class="alt-sec__text">
      <p class="eyebrow eyebrow--light">Warum Ackermann?</p>
      <h2>Die Alternative im Premiumbereich</h2>
      <p>Als Systemanbieter für gewerbliche Spültechnik haben wir uns in den Top 5 der Branche
      etabliert. Das macht uns stolz. Wir wollen näher dran sein an Deinen Bedürfnissen – und
      Dinge anders machen, damit Du es einfach hast.</p>
      <p>Das beginnt bei den Kosten: Wir sind extrem schlank aufgestellt, kalkulieren scharf und
      konzentrieren uns auf alles, was für ein optimales Spülergebnis nötig ist. Deshalb sind
      unsere Maschinen so überraschend günstig. Und das gilt genauso für den Service: Unsere
      Techniker stehen Dir rund um die Uhr zur Verfügung – auch am Wochenende.</p>
      <a href="/ueber-uns/" class="btn btn--primary">Qualität und Service: Entdecke die Alternative!</a>
    </div>
    <div class="alt-sec__media">
      <img src="/assets/img/Ackmann_Techniker.jpg" alt="Ackermann Servicetechniker im Einsatz" loading="lazy">
    </div>
  </div>
</section>"""
 + f'<section class="section" id="loesungen"><div class="container">'
   + section_head("Lösungen für Deine Branche", "Für jeden Einsatz die passende Spültechnik",
       "Entdecke unsere Lösungen für Deine Branche – individuell abgestimmt auf Deine Anforderungen, Deine Abläufe und Dein Spülgut.")
   + cards_solutions() + '</div></section>'
 + f'<section class="section section--dark"><div class="container">'
   + section_head("Produkte", "Alles fürs perfekte Spülergebnis", light=True)
   + f"""<div class="cards cards--2">
      <a class="product" href="/produkte/spuelmaschinen/">
        <div class="product__media"><img src="/assets/img/machines/U-540E.png" alt="Spülmaschinen"></div>
        <div class="product__body"><h3>Spülmaschinen</h3>
          <p>Vom Gläser- und Bistrospüler über Hauben- und Gerätespülmaschinen bis zur Korbtransport-Spülmaschine – zuverlässige Technik für jede Betriebsgröße.</p>
          <span class="card__link">Zu den Spülmaschinen &rarr;</span></div>
      </a>
      <a class="product" href="/produkte/spuelchemie/">
        <div class="product__media product__media--chem">
          <img src="/assets/img/chemie/Klar_GS.jpg" alt="KLAR GS Klarspüler">
        </div>
        <div class="product__body"><h3>Spülchemie</h3>
          <p>Passgenau abgestimmte Reiniger, Klarspüler und Pflegemittel für glänzend saubere Ergebnisse bei minimalem Verbrauch.</p>
          <span class="card__link">Zur Spülchemie &rarr;</span></div>
      </a></div></div></section>"""
 + f'<section class="section"><div class="container">'
   + section_head("Über uns", "5 Gründe für Ackermann",
       "Unsere Stärke liegt nicht in lauten Versprechen, sondern in Technik, Service und Haltung, die im Alltag zuverlässig funktionieren.")
   + '<div class="pillars">'
   + "".join(f'<a class="pillar" href="{u}"><span class="pillar__no">{n:02d}</span><h3>{t}</h3><p>{d}</p></a>'
       for n,(t,u,d) in enumerate(ACKERMANN_REASONS,1)) + '</div></div></section>'
 + """<section class="band-cta">
  <div class="container band-cta__inner">
    <img src="/assets/img/bee-light.png" alt="" class="band-cta__bee" aria-hidden="true">
    <h2>Spülmaschinen für Andersmacher</h2>
    <a href="/die-andersmacher/" class="btn btn--dark">Mehr erfahren</a>
  </div>
</section>
<section class="section newsletter" id="newsletter">
  <div class="container newsletter__inner">
    <div class="newsletter__text">
      <p class="eyebrow">Newsletter</p>
      <h2>Bleib auf dem Laufenden</h2>
      <p>Unser kostenloser Newsletter informiert Dich regelmäßig per E-Mail über Produktneuheiten
      und Sonderaktionen. Deine Daten werden nur zur Personalisierung des Newsletters verwendet
      und nicht an Dritte weitergegeben.</p>
    </div>
    <form class="newsletter__form" onsubmit="alert('Danke! Dies ist eine Demo-Anmeldung.');return false;">
      <input type="email" placeholder="E-Mail" aria-label="E-Mail" required>
      <div class="row">
        <input type="text" placeholder="Vorname" aria-label="Vorname">
        <input type="text" placeholder="Nachname" aria-label="Nachname">
      </div>
      <select aria-label="Betriebsart">
        <option>Gastronomischer Betrieb</option>
        <option>Fachhandel</option>
        <option>Sonstiges</option>
      </select>
      <button type="submit" class="btn btn--primary">Anmelden</button>
    </form>
  </div>
</section>""",
 "Ackermann Spülmaschinen GmbH aus Baindt: gewerbliche Spülmaschinen und Spülchemie für Gastronomie, Hotellerie, Catering, Bäckereien, Metzgereien und mobiles Spülen."))

# flat lookup: slug -> (display name, use, image)
MACHINE_BY_SLUG = {slug: (name, use, img)
                   for items in MACHINES.values() for name, use, img, slug in items}

def machine_cards(slugs):
    cards = ""
    for slug in slugs:
        name, use, img = MACHINE_BY_SLUG[slug]
        cards += f"""<a class="machine" href="/produkte/spuelmaschinen/{slug}/">
  <div class="machine__media"><img src="/assets/img/machines/{img}" alt="{html.escape(name)}" loading="lazy"></div>
  <h4>{html.escape(name)}</h4>
  <p>{html.escape(use)}</p>
  <span class="machine__link">Details &amp; Datenblatt &rarr;</span>
</a>"""
    return f'<div class="cards cards--4 machine-row">{cards}</div>'

def solution_page(url, filename, eyebrow, h1, lead, body_extra="", machines=None, extra_section=""):
    if machines:
        rec = ('<section class="section section--muted"><div class="container">'
               + section_head("Passende Maschinen", "Unsere Empfehlung für Deine Branche",
                   "Diese Modelle haben sich in Betrieben wie Deinem bewährt.")
               + machine_cards(machines)
               + '<div style="text-align:center;margin-top:2rem"><a class="btn btn--primary" href="/produkte/spuelmaschinen/">Alle Spülmaschinen ansehen</a></div>'
               + '</div></section>')
    else:
        rec = ""
    b = (hero(eyebrow, h1, lead, cta=[("Jetzt beraten lassen", "/kontakt/", "btn--primary")], cls="hero--sub")
         + f'<section class="section"><div class="container prose">{body_extra}</div></section>'
         + extra_section
         + rec
         + cta_band("Fragen zu Deiner Branche?", "Wir beraten Dich persönlich und unverbindlich.", "Kontakt aufnehmen"))
    PAGES[url] = (filename, h1, page(url, h1, b, lead[:150]))

solution_page("/gastronomie-und-hotellerie/", "gastronomie-und-hotellerie/index.html",
    "Lösungen für", "Gastronomie &amp; Hotellerie",
    "Wir machen das Spülen einfach.",
    "<p>Spülmaschinen für die Gastronomie müssen zuverlässig laufen, hervorragende Ergebnisse liefern und dabei intuitiv und wartungsarm sein. Als Partner innovativer Cafés, Bars, Restaurants und Hotels schätzen unsere Kunden entweder unseren unschlagbaren Preis oder unseren außergewöhnlichen Service – und meistens beides.</p><p>Auch kleinere Betriebe erhalten bei uns die volle Aufmerksamkeit und Unterstützung. Denn wir sind einfach näher dran.</p>",
    machines=["u-440", "u-540-bistro", "u-540e", "h-540e", "h-540e-klima-plus", "h-640", "h-640-klima-plus", "f-720"])

solution_page("/gemeinschaftsverpflegung-und-catering/", "gemeinschaftsverpflegung-und-catering/index.html",
    "Lösungen für", "Catering und Gemeinschaftsverpflegung",
    "Spültechnik, mit der man rechnen kann.",
    "<p>Von der Kita-Küche bis zum großen Hochzeits-Event: So unterschiedlich die Einsätze, so vielseitig muss die Spültechnik sein – und in kurzer Zeit ganz verschiedenes Spülgut bewältigen.</p><p>Profis rechnen mit den kompletten Lebenszykluskosten: Anschaffungspreis, Wartung, Verbrauch und Ersatzteile. Genau hier punkten wir mit robuster Premium-Qualität zu fairen Preisen und starkem Service.</p>",
    machines=["h-640", "kt-1", "kt-2", "kt-2-plus"])

solution_page("/baeckereien-und-metzgereien/", "baeckereien-und-metzgereien/index.html",
    "Lösungen für", "Heiß und fettig? Mit uns bleibst Du cool",
    "Meister der Vielfalt für Bäckereien und Metzgereien.",
    "<p>Bäckereien und Metzgereien sind heute oft fast schon kleine Bistros. Die heiße Theke hat Konjunktur. Damit steigen auch die Anforderungen an die Spültechnik. Die Hygiene bleibt das A und O, zudem aber müssen Spülmaschinen in diesen Branchen Meister der Vielfalt sein.</p><p>Von fettigen Blechen über empfindliches Geschirr bis zu Behältern – und das alles auf begrenztem Raum. Unsere Geräte überzeugen bei Leistung und Wirtschaftlichkeit gleichermaßen.</p>",
    machines=["u-640e", "h-640", "f-920"])

solution_page("/ausser-haus-und-mobiles-spuelen/", "ausser-haus-und-mobiles-spuelen/index.html",
    "Lösungen für", "Außer Haus und mobiles Spülen",
    "So einfach war mobiles Spülen noch nie.",
    "<p>Beim Außerhaus-Catering, auf Festen oder auf Marktplätzen: Die Ansprüche an die Bewirtung und Logistik steigen, und auch die Hygienevorschriften werden immer anspruchsvoller.</p><p>Mit dem Spülmobil erfüllst Du nicht nur alle Vorschriften, sondern gewinnst maximale Flexibilität für unterschiedliche Einsatzorte. Anschluss an Strom und Wasser genügt – und los geht's.</p>",
    extra_section="""<section class="section section--dark alt-sec">
  <div class="container alt-sec__inner">
    <div class="alt-sec__text">
      <p class="eyebrow eyebrow--light">Unsere Lösung</p>
      <h2>Das Spülmobil</h2>
      <p>Die komplette Spülküche auf Rädern: Das Spülmobil bringt professionelle Spültechnik
      dorthin, wo gefeiert wird. Strom- und Wasseranschluss genügen – und schon spülst Du
      auch draußen auf Profi-Niveau, hygienisch einwandfrei und vorschriftenkonform.</p>
      <a href="/kontakt/" class="btn btn--primary">Spülmobil anfragen</a>
    </div>
    <div class="alt-sec__media">
      <img src="/assets/img/spuelmobil.jpg" alt="Das Ackermann Spülmobil im Einsatz" loading="lazy">
    </div>
  </div>
</section>""")

# PRODUCTS – Spülmaschinen
PAGES["/produkte/spuelmaschinen/"] = ("produkte/spuelmaschinen/index.html", "Spülmaschinen", page(
 "/produkte/spuelmaschinen/", "Spülmaschinen",
 hero("Produkte", "Unsere Spülmaschinen",
      "Untertisch-, Hauben-, Geräte- und Korbtransportspülmaschinen – zuverlässige Premium-Technik für jede Betriebsgröße und jedes Spülgut.",
      cta=[("Beratung anfragen","/kontakt/","btn--primary")], cls="hero--sub")
 + '<section class="section"><div class="container">' + machine_grid() + '</div></section>'
 + cta_band("Welche Maschine passt zu Deinem Betrieb?", "Wir beraten Dich gern und finden die passende Lösung."),
 "Untertisch-, Hauben-, Geräte- und Korbtransportspülmaschinen von Ackermann."))

# PRODUCTS – Spülchemie (full product cards with image + datasheet)
def chemie_grid():
    out = []
    groups = []
    for name, group, desc, img, pdf in CHEMIE_PRODUCTS:
        if group not in groups:
            groups.append(group)
    for g in groups:
        cards = ""
        for name, group, desc, img, pdf in CHEMIE_PRODUCTS:
            if group != g:
                continue
            btn = (f'<a class="chem-card__pdf" href="/assets/datasheets/{pdf}" target="_blank" rel="noopener">Datenblatt (PDF)</a>'
                   if pdf else '<span class="chem-card__pdf chem-card__pdf--none">Datenblatt auf Anfrage</span>')
            cards += f"""<div class="chem-card">
  <div class="chem-card__media"><img src="/assets/img/chemie/{img}" alt="{html.escape(name)}" loading="lazy"></div>
  <h4>{html.escape(name)}</h4>
  <p>{html.escape(desc)}</p>
  {btn}
</div>"""
        out.append(f'<h3 class="machine-cat">{html.escape(g)}</h3><div class="cards cards--4 machine-row">{cards}</div>')
    return "\n".join(out)

PAGES["/produkte/spuelchemie/"] = ("produkte/spuelchemie/index.html", "Spülchemie", page(
 "/produkte/spuelchemie/", "Spülchemie",
 hero("Produkte", "Unsere Spülchemie",
      "Reiniger, Klarspüler und Pflegemittel – passgenau abgestimmt auf unsere Maschinen für glänzende Ergebnisse bei minimalem Verbrauch.",
      cta=[("Beratung anfragen","/kontakt/","btn--primary")], cls="hero--sub")
 + '<section class="section"><div class="container">' + chemie_grid() + '</div></section>'
 + cta_band("Fragen zur richtigen Dosierung?", "Wir helfen Dir, Verbrauch und Ergebnis optimal einzustellen."),
 "Reiniger, Klarspüler, Entkalker und Regeneriersalz von Ackermann Spülmaschinen – mit Datenblättern."))

# ÜBER UNS
PAGES["/ueber-uns/"] = ("ueber-uns/index.html", "Über uns", page(
 "/ueber-uns/", "Über uns",
 hero("Über uns", "Einfach näher dran: Spülmaschinen für Andersmacher",
      "Wer morgen noch erfolgreich sein will, muss heute etwas anders machen.",
      cta=[("Lern uns kennen","/kontakt/","btn--primary")],
      img="/assets/img/Gruppenbild-2.png", cls="hero--sub")
 + '<section class="section"><div class="container prose">'
   + "<p>Wir sind für alle da, die Traditionen hinterfragen und keine überteuerten Markennamen bezahlen wollen, sondern eine praxistaugliche Alternative suchen. Wir wollen das gewerbliche Spülen so ressourceneffizient, unkompliziert und kostengünstig wie möglich gestalten – in echter Partnerschaft mit Händlern und Gastronomen.</p>"
   + "<p>Ackermann Spülmaschinen ist ein echter Familienbetrieb: Gründer Stefan Ackermann führt die Geschäfte, seine Frau Emma kümmert sich um die Buchhaltung, Sohn August bringt neue Ideen ein und Tochter Clara ist ebenfalls mit an Bord. Uns liegt am Herzen, dass sich alle im Team wohlfühlen.</p>"
   + "<p>Beheimatet in der Region Bodensee-Oberschwaben-Allgäu sind wir bundesweit und international aktiv. Unser Motto: näher dran sein.</p>"
   + '</div></section>'
 + '<section class="section section--muted"><div class="container">'
   + section_head("Wofür wir stehen", "Fünf Gründe für Ackermann")
   + '<div class="pillars">'
   + "".join(f'<a class="pillar" href="{u}"><span class="pillar__no">{n:02d}</span><h3>{t}</h3><p>{d}</p></a>'
       for n,(t,u,d) in enumerate(ACKERMANN_REASONS,1)) + '</div></div></section>'
 + cta_band("Werde ein Andersmacher", "Sprich mit uns über die Alternative im Premiumbereich."),
 "Familiengeführter Systemanbieter für gewerbliche Spültechnik aus Baindt – Top 5 der Branche."))

def about_sub(url, filename, title, eyebrow, lead, paras):
    body = (hero(eyebrow, html.escape(title), lead, cta=[("Kontakt","/kontakt/","btn--primary")], cls="hero--sub")
      + '<section class="section"><div class="container prose">'
      + "".join(f"<p>{p}</p>" for p in paras) + '</div></section>'
      + cta_band("Mehr erfahren?", "Wir beraten Dich gern persönlich."))
    PAGES[url] = (filename, title, page(url, title, body, lead))

about_sub("/ueber-uns/qualitaet/", "ueber-uns/qualitaet/index.html", "Qualität", "Über uns",
    "Robuste Qualität, die sich im Alltag beweist.",
    ["Unsere Maschinen sind für den harten Dauereinsatz gebaut – mit langlebigen Komponenten, solider Konstruktion und Technik, die nicht empfindlich sein darf.",
     "Qualität heißt für uns: zuverlässig laufen, einfach zu warten sein und auch dann sauber spülen, wenn es im Betrieb richtig zur Sache geht."])
about_sub("/ueber-uns/service/", "ueber-uns/service/index.html", "Service", "Über uns",
    "Service flächendeckend in ganz Deutschland.",
    ["Beratung, Installation, Wartung und Ersatzteile: Bei uns kommt alles aus einer Hand. Unser Service ist flächendeckend in ganz Deutschland erreichbar und dann vor Ort, wenn es darauf ankommt.",
     "So minimierst Du Ausfallzeiten und hast einen Partner, der Deinen Betrieb wirklich kennt."])
about_sub("/ueber-uns/innovationen/", "ueber-uns/innovationen/index.html", "Innovation", "Über uns",
    "Wirklich brauchbare Innovation statt Schnickschnack.",
    ["Wir entwickeln unsere Spültechnik konsequent weiter – für einfachere Bedienung, klarere Abläufe und mehr Effizienz im Alltag.",
     "Jede Innovation muss sich im Praxisalltag beweisen. Nur was den Betrieb spürbar einfacher macht, kommt in unsere Maschinen."])
about_sub("/ueber-uns/nachhaltigkeit/", "ueber-uns/nachhaltigkeit/index.html", "Nachhaltigkeit", "Über uns",
    "Spülen mit gutem Gewissen.",
    ["Extrem niedriger Wasser- und Energieverbrauch ist bei uns kein Extra, sondern Standard. Ressourcenschonende Technik spart Kosten und schont die Umwelt.",
     "Mit unserer Spülchemie – etwa dem F 450 green – runden wir das nachhaltige Gesamtpaket ab."])

# DIE ANDERSMACHER
PAGES["/die-andersmacher/"] = ("die-andersmacher/index.html", "Die Andersmacher", page(
 "/die-andersmacher/", "Die Andersmacher",
 hero("Referenzen", "Die Andersmacher",
      "Betriebe, die Traditionen hinterfragen und anders spülen – und dabei auf Ackermann setzen. Lern sie kennen.",
      cls="hero--sub")
 + '<section class="section"><div class="container">' + andersmacher_grid() + '</div></section>'
 + cta_band("Auch ein Andersmacher?", "Erzähl uns von Deinem Betrieb.", "Kontakt aufnehmen"),
 "Referenzen von Ackermann Spülmaschinen – Betriebe, die anders spülen."))

# DIE ANDERSMACHER – detail pages
ANDERSMACHER_INFO = {
    "/die-andersmacher/max-cafe/": ("Max.Café", "Gastronomie",
        "Ein Café, das Wert auf Qualität legt – vom Kaffee bis zum Spülergebnis."),
    "/die-andersmacher/haerles-hofcafe/": ("Härle's Hofcafé", "Hofcafé",
        "Regional, ehrlich und mit einem klaren Blick auf Ressourcen: so wenig Wasser, so sauber spülen."),
    "/die-andersmacher/pier-40/": ("Pier 40", "Gastronomie",
        "Am Wasser gelegen, mit hohem Anspruch an Service und Verlässlichkeit."),
    "/die-andersmacher/haus-nazareth/": ("Haus Nazareth", "Gemeinschaftsverpflegung",
        "Große Küche, viele Essen am Tag – Spültechnik, auf die Verlass ist."),
    "/die-andersmacher/stotz-hof/": ("Stotz Hof", "Hofgastronomie",
        "Bodenständig und nachhaltig – ein Betrieb, der Dinge anders anpackt."),
    "/die-andersmacher/metzgerei-kutter/": ("Metzgerei Kutter", "Metzgerei",
        "Heiß und fettig? Kein Problem. Unschlagbar in Preis und Leistung."),
    "/die-andersmacher/culina/": ("Culina", "Catering",
        "Vielfältige Einsätze, hohe Durchsätze – Spültechnik, mit der man rechnen kann."),
    "/die-andersmacher/hirscheck/": ("Hirscheck", "Gastronomie",
        "Neu dabei und überzeugt von der Alternative im Premiumbereich."),
    "/die-andersmacher/biolandhof-kelly/": ("Biolandhof Kelly", "Biolandhof",
        "Bio von Grund auf – nachhaltige Spültechnik passt da perfekt ins Bild."),
    "/die-andersmacher/ellgass/": ("Ellgass", "Landwirtschaft & Direktvermarktung",
        "Ein Andersmacher, der auf Qualität und faire Kosten setzt."),
}
_ander_img = {name: img for name, img, url in ANDERSMACHER}
for url, (name, branche, blurb) in ANDERSMACHER_INFO.items():
    slug = url.strip("/").split("/")[-1]
    filename = f"die-andersmacher/{slug}/index.html"
    img = _ander_img.get(name)
    media = (f'<div class="ref-detail__media"><img src="/assets/img/{img}" alt="{html.escape(name)}"></div>'
             if img else "")
    body = (hero("Ein Andersmacher", html.escape(name), html.escape(blurb),
                 cta=[("Zurück zur Übersicht","/die-andersmacher/","btn--ghost")], cls="hero--sub")
        + '<section class="section"><div class="container ref-detail">'
        + media
        + f'<div class="prose"><p class="eyebrow">{html.escape(branche)}</p>'
          f'<p>{html.escape(name)} zählt zu den Andersmachern – Betrieben, die Traditionen hinterfragen '
          f'und auf eine praxistaugliche, ressourceneffiziente Alternative im Premiumbereich setzen. '
          f'Gemeinsam mit Ackermann sorgt {html.escape(name)} für einwandfreie Hygiene bei minimalem '
          f'Wasser- und Energieverbrauch.</p>'
          f'<p><a href="/kontakt/">Auch ein Andersmacher werden &rarr;</a></p></div>'
        + '</div></section>'
        + cta_band("Auch ein Andersmacher?", "Erzähl uns von Deinem Betrieb.", "Kontakt aufnehmen"))
    PAGES[url] = (filename, name, page("/die-andersmacher/", name, body,
        f"{name} – ein Andersmacher, der auf Ackermann Spülmaschinen setzt."))

# KARRIERE
PAGES["/karriere/"] = ("karriere/index.html", "Karriere", page(
 "/karriere/", "Karriere",
 hero("Karriere", "Werde ein Andersmacher",
      "Wir suchen Menschen, die mit anpacken – in Vertrieb, Service und Technik. Als Familienbetrieb legen wir Wert darauf, dass sich alle im Team wohlfühlen.",
      cta=[("Initiativ bewerben","/kontakt/","btn--primary")], cls="hero--sub")
 + '<section class="section"><div class="container prose">'
   + "<p>Bei Ackermann arbeitest Du in einem echten Familienbetrieb mit kurzen Wegen, flachen Hierarchien und viel Gestaltungsspielraum. Ob im Außendienst, in der Werkstatt oder im Innendienst – bei uns zählt, was Du bewegst.</p>"
   + "<p>Aktuell keine passende Stelle dabei? Schick uns einfach eine Initiativbewerbung an <a href='mailto:info@ackermann-spuelmaschinen.de'>info@ackermann-spuelmaschinen.de</a>.</p>"
   + '</div></section>'
 + cta_band("Lust auf etwas anderes?", "Wir freuen uns auf Deine Bewerbung."),
 "Karriere bei Ackermann Spülmaschinen in Baindt – Jobs in Vertrieb, Service und Technik."))

# NEWS
news_items = [
 ("Innovationen","Weniger Wasser, bessere Ergebnisse","Wie unsere neueste Maschinengeneration den Verbrauch weiter senkt."),
 ("Nachhaltigkeit","Spülen mit gutem Gewissen","Unser Weg zu ressourcenschonender Spültechnik im Premiumbereich."),
 ("Andersmacher","Neu dabei: Hirscheck","Warum immer mehr Betriebe auf die Alternative im Premiumbereich setzen."),
]
PAGES["/news/"] = ("news/index.html", "News", page(
 "/news/", "News",
 hero("News", "Neues aus Baindt",
      "Neuigkeiten, Innovationen und Geschichten rund um gewerbliche Spültechnik.", cls="hero--sub")
 + '<section class="section"><div class="container"><div class="cards cards--3">'
   + "".join(f'<article class="news"><div class="news__tag">{html.escape(t)}</div><h3>{html.escape(h)}</h3><p>{html.escape(d)}</p><a class="card__link" href="/kontakt/">Weiterlesen &rarr;</a></article>' for t,h,d in news_items)
   + '</div></div></section>'
 + cta_band("Immer auf dem Laufenden bleiben?", "Frag nach unserem Newsletter."),
 "Neuigkeiten von Ackermann Spülmaschinen aus Baindt."))

# KONTAKT
PAGES["/kontakt/"] = ("kontakt/index.html", "Kontakt", page(
 "/kontakt/", "Kontakt",
 hero("Kontakt", "Wir freuen uns, von Dir zu hören!",
      "Hast Du Fragen, Ideen, Anregungen? Wir beraten Dich gern persönlich und finden die passende Spüllösung für Deinen Betrieb.", cls="hero--sub")
 + '<section class="section"><div class="container contact">'
   + """<div class="contact__info">
     <h2>Ackermann Spülmaschinen GmbH</h2>
     <ul class="contact__list">
       <li><span>Adresse</span><a href="https://maps.google.com/?q=Am+Umspannwerk+18,+88255+Baindt" target="_blank" rel="noopener">Am Umspannwerk 18, 88255 Baindt</a></li>
       <li><span>Telefon</span><a href="tel:+4975029779100">+49 (0)7502 97791&nbsp;00</a></li>
       <li><span>Fax</span><span>+49 (0)7502 97791&nbsp;190</span></li>
       <li><span>E-Mail</span><a href="mailto:info@ackermann-spuelmaschinen.de">info@ackermann-spuelmaschinen.de</a></li>
       <li><span>Öffnungszeiten</span><span>Mo–Do 08:00–17:00 Uhr<br>Fr 08:00–15:00 Uhr</span></li>
     </ul>
     <a href="/kontakt/" class="btn btn--primary">Zum Händlershop</a>
   </div>
   <form class="contact__form" onsubmit="alert('Danke! Dies ist eine Demo – bitte kontaktiere uns per Telefon oder E-Mail.');return false;">
     <div class="row"><input type="text" placeholder="Vorname" aria-label="Vorname" required><input type="text" placeholder="Nachname" aria-label="Nachname" required></div>
     <input type="email" placeholder="E-Mail-Adresse" aria-label="E-Mail" required>
     <input type="text" placeholder="Betrieb / Branche" aria-label="Betrieb">
     <textarea placeholder="Deine Nachricht" rows="5" aria-label="Nachricht"></textarea>
     <button type="submit" class="btn btn--primary">Nachricht senden</button>
   </form>"""
   + '</div></section>'
 + '<section class="section section--muted"><div class="container"><div class="mapbox"><iframe title="Standort Baindt" src="https://www.openstreetmap.org/export/embed.html?bbox=9.63%2C47.83%2C9.70%2C47.87&layer=mapnik&marker=47.851%2C9.667" loading="lazy"></iframe></div></div></section>',
 "Kontakt zu Ackermann Spülmaschinen GmbH, Am Umspannwerk 18, 88255 Baindt."))

# LEGAL
def legal(url, filename, title, paras):
    body = (hero(title, html.escape(title), "", cls="hero--sub hero--slim")
      + '<section class="section"><div class="container prose prose--legal">'
      + "".join(p for p in paras) + '</div></section>')
    PAGES[url] = (filename, title, page(url, title, body, title))

legal("/impressum/", "impressum/index.html", "Impressum", [
  "<h2>Angaben gemäß § 5 TMG</h2><p>Ackermann Spülmaschinen GmbH<br>Am Umspannwerk 18<br>88255 Baindt<br>Deutschland</p>",
  "<h2>Kontakt</h2><p>Telefon: +49 (0)7502 97791 00<br>Fax: +49 (0)7502 97791 190<br>E-Mail: info@ackermann-spuelmaschinen.de</p>",
  "<h2>Vertretungsberechtigter Geschäftsführer</h2><p>Stefan Ackermann</p>",
  "<h2>Registereintrag</h2><p>Amtsgericht Ulm, HRB 632024</p>",
  "<p class='muted-note'>Hinweis: Dies ist eine originalgetreue Nachbildung. Bitte die vollständigen Pflichtangaben (USt-IdNr., verantwortlich i.S.d. Presserechts u.&nbsp;a.) vor Veröffentlichung ergänzen.</p>",
])
# DOWNLOADBEREICH – all datasheets in one place (like the official site)
MACHINE_DOWNLOADS = [
    ("U 430-2", "Datenblatt-U-430-1.pdf"), ("U 440", "Datenblatt-U-440.pdf"),
    ("U 530-2 / U 530-2E", "Datenblatt-U-530-1-U-530-1E.pdf"), ("U 540 Bistro", "Datenblatt-U-540-Bistro.pdf"),
    ("U 540 / U 540E", "Datenblatt-U-540-U-540E.pdf"), ("U 640 / U 640E", "Datenblatt-U-640-U-640E.pdf"),
    ("H 530-2 / H 530-2E", "Datenblatt-H530-1-und-H530-1E.pdf"), ("H 540 / H 540E", "Datenblatt-H-540-H-540E.pdf"),
    ("H 540 Klima+ / H 540E Klima+", "Datenblatt-H540KlimaPlus-H540EKlimaPlus.pdf"),
    ("H 640", "Datenblatt-H640.pdf"), ("H 640 Klima+", "Datenblatt-H640KlimaPlus.pdf"),
    ("F 720", "Datenblatt-F720.pdf"), ("F 920", "Datenblatt-F-920.pdf"),
    ("KT-1 / KT-2", "Datenblatt_KT_1_KT_2_2024.pdf"),
    ("KT-1 Plus / KT-2 Plus", "Datenblatt-KT_1-Plus-und_KT_2_Plus_2024.pdf"),
]
CHEMIE_DOWNLOADS = [(n, p) for n, g, d, i, p in CHEMIE_PRODUCTS if p]

def dl_list(items):
    rows = "".join(
        f'<li><span>{html.escape(n)}</span>'
        f'<a class="btn btn--primary btn--sm" href="/assets/datasheets/{p}" target="_blank" rel="noopener">⭳ PDF</a></li>'
        for n, p in items)
    return f'<ul class="dl-list">{rows}</ul>'

PAGES["/downloadbereich/"] = ("downloadbereich/index.html", "Downloadbereich", page(
 "/downloadbereich/", "Downloadbereich",
 hero("Service", "Downloadbereich",
      "Alle Datenblätter unserer Spülmaschinen und Spülchemie als PDF – zum Ansehen und Herunterladen.",
      cls="hero--sub")
 + '<section class="section"><div class="container dl-cols">'
   + f'<div><h3 class="machine-cat">Spülmaschinen</h3>{dl_list(MACHINE_DOWNLOADS)}</div>'
   + f'<div><h3 class="machine-cat">Spülchemie</h3>{dl_list(CHEMIE_DOWNLOADS)}</div>'
 + '</div></section>'
 + cta_band("Fehlt Dir ein Dokument?", "Schreib uns – wir schicken Dir alles Nötige zu.", "Kontakt aufnehmen"),
 "Datenblätter aller Ackermann Spülmaschinen und Spülchemie-Produkte als PDF-Download."))

legal("/cookie-richtlinie-eu/", "cookie-richtlinie-eu/index.html", "Cookie-Richtlinie (EU)", [
  "<p>Diese Website verwendet Cookies und ähnliche Technologien, um grundlegende Funktionen bereitzustellen und – nur mit Deiner Einwilligung – Statistik- und Marketingzwecke zu unterstützen.</p>",
  "<h2>Kategorien</h2><p><strong>Funktional:</strong> für den Betrieb der Website erforderlich.<br><strong>Vorlieben:</strong> speichern Deine Einstellungen.<br><strong>Statistiken:</strong> anonyme Auswertung der Nutzung.<br><strong>Marketing:</strong> nur mit ausdrücklicher Zustimmung.</p>",
  "<h2>Einwilligung verwalten</h2><p>Du kannst Deine Einwilligung jederzeit anpassen oder widerrufen. Details zur Verarbeitung findest Du in unserer <a href='/datenschutz/'>Datenschutzerklärung</a>.</p>",
  "<p class='muted-note'>Hinweis: Platzhalter-Richtlinie für die Nachbildung. Vor Veröffentlichung durch die vollständige, rechtssichere Fassung ersetzen.</p>",
])

legal("/datenschutz/", "datenschutz/index.html", "Datenschutz", [
  "<p>Der Schutz Deiner persönlichen Daten ist uns wichtig. Wir verarbeiten personenbezogene Daten ausschließlich im Rahmen der gesetzlichen Bestimmungen (DSGVO, BDSG).</p>",
  "<h2>Verantwortlicher</h2><p>Ackermann Spülmaschinen GmbH, Am Umspannwerk 18, 88255 Baindt, info@ackermann-spuelmaschinen.de</p>",
  "<h2>Deine Rechte</h2><p>Du hast das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch.</p>",
  "<p class='muted-note'>Hinweis: Platzhalter-Datenschutzerklärung für die Nachbildung. Vor Veröffentlichung durch die vollständige, rechtssichere Fassung ersetzen.</p>",
])

# ---------------------------------------------------------------- write
# ---------------------------------------------------------------- machine detail pages
# Values are the factual specifications from the official Ackermann datasheets,
# re-presented in a fresh layout. Each page links the original PDF as the
# authoritative source ("Alle Angaben laut offiziellem Datenblatt").
_F = "Doppelwandige Edelstahl-Konstruktion für leisen, langlebigen Betrieb"
MACHINE_DETAIL = {
 "u-430-2": dict(name="U 430-2", series="Untertisch · Gläser & Bistro", img="U-430-2.png",
   pdf="/assets/datasheets/Datenblatt-U-430-1.pdf",
   tagline="Die kompakte Gläser- und Bistrospülmaschine für Körbe 400 × 400 mm.",
   intro=["Die U 430-2 ist der platzsparende Einstieg in die Ackermann-Welt: gebaut für Bars und Cafés, in denen jeder Zentimeter zählt.",
          "Einfach zu bedienen, robust im Alltag und sparsam im Verbrauch – ganz ohne Schnickschnack."],
   highlights=[("400 × 400 mm","Korbgröße"),("40","Körbe / Stunde"),("230 V","Stromanschluss"),("3,4 kW","Anschlusswert")],
   specs=[("Korbgröße","400 × 400 mm"),("Theor. Stundenleistung","40 Körbe/h"),("Einfahrhöhe","300 mm"),
          ("Max. Glashöhe","275 mm"),("Höhe mit geöffneter Türe","885 mm"),("Stromanschluss","230 V / 50 Hz"),
          ("Gesamtanschlusswert","3,4 kW"),("Absicherung","16 A"),("Tanktemperatur","60–65 °C")],
   features=[_F,"Extrem kompakte Stellfläche","Anschluss an normale 230-V-Steckdose","Ideal für Gläser und Bistrogeschirr","Einfachste Bedienung – robust statt Schnickschnack"]),
 "u-530-2": dict(name="U 530-2 / U 530-2E", series="Untertisch-Geschirrspülmaschine", img="U-530-2.png",
   pdf="/assets/datasheets/Datenblatt-U-530-1-U-530-1E.pdf",
   tagline="Untertischspülmaschine für Gläser und Geschirr – Körbe 500 × 500 mm.",
   intro=["Die U 530-2 ist die vielseitige Untertischmaschine für Gläser und Geschirr. Mit 330 mm Glashöhe nimmt sie auch hohe Gläser problemlos auf.",
          "Der umschaltbare Anschlusswert macht sie flexibel: volle Leistung am 400-V-Anschluss oder reduzierter Betrieb, wo nur 230 V verfügbar sind. Als E-Modell mit eingebautem Wasserenthärter."],
   highlights=[("500 × 500 mm","Korbgröße"),("40","Körbe / Stunde"),("330 mm","max. Glashöhe"),("6,8 kW","Anschlusswert")],
   specs=[("Korbgröße","500 × 500 mm"),("Theor. Stundenleistung","40 Körbe/h"),("Max. Glashöhe","330 mm"),
          ("Höhe mit geöffneter Türe","1.005 mm"),("Stromanschluss","400 V / 3 / 50 Hz"),
          ("Gesamtanschlusswert","6,8 kW (umschaltbar 3,4 kW)"),("Absicherung","16 A"),
          ("Tanktemperatur","60–65 °C"),("Boilertemperatur","80–85 °C")],
   e_note="E-Modell: mit eingebautem Wasserenthärter",
   features=[_F,"Umschaltbarer Anschlusswert (400 V / 230 V)","330 mm Glashöhe für hohe Gläser","Große 500 × 500 mm Körbe","E-Variante mit eingebautem Wasserenthärter"]),
 "h-530-2": dict(name="H 530-2 / H 530-2E", series="Haubenspülmaschine", img="H-530-2.png",
   pdf="/assets/datasheets/Datenblatt-H530-1-und-H530-1E.pdf",
   tagline="Die kompakte Haubenspülmaschine für den Einstieg ins Durchschub-Spülen.",
   intro=["Die H 530-2 bringt das Hauben-Prinzip in kompakter Form in Deine Küche: aufrechtes Arbeiten, schnelle Korbwechsel und konstante Ergebnisse.",
          "Ideal für Betriebe, die vom Untertisch-Format aufsteigen wollen – als E-Modell mit eingebautem Wasserenthärter."],
   highlights=[("500 × 500 mm","Korbgröße"),("40","Körbe / Stunde"),("440 mm","Einfahrhöhe"),("2.010 mm","Höhe offene Haube")],
   specs=[("Korbgröße","500 × 500 mm"),("Theor. Stundenleistung","40 Körbe/h"),("Einfahrhöhe","440 mm"),
          ("Höhe mit geöffneter Haube","2.010 mm"),("Stromanschluss","400 V / 3 / 50 Hz"),
          ("Boilerleistung","7.000 W"),("Tanktemperatur","60–65 °C"),("Boilertemperatur","80–85 °C")],
   e_note="E-Modell: mit eingebautem Wasserenthärter",
   features=[_F,"Kompaktes Hauben-Format – aufrechtes Arbeiten","440 mm Einfahrhöhe","Ideal für den Einstieg ins Durchschub-Spülen","E-Variante mit eingebautem Wasserenthärter"]),
 "u-440": dict(name="U 440", series="Untertisch · Gläser & Bistro", img="U-440.png",
   pdf="/assets/datasheets/Datenblatt-U-440.pdf",
   tagline="Kompakte Gläser- und Bistrospülmaschine für Körbe 400 × 400 mm.",
   intro=["Die U 440 ist die kompakte Einstiegsmaschine für Bars, Cafés und kleine Bistros. Sie passt unter jede Theke und liefert bei minimalem Platzbedarf glasklare Ergebnisse.",
          "Einfache Bedienung, ein doppelwandiges Gehäuse für leisen Betrieb und geringer Verbrauch machen sie zur idealen Wahl für den täglichen Einsatz."],
   highlights=[("400 × 400 mm","Korbgröße"),("40","Körbe / Stunde"),("230 V","Stromanschluss"),("3,4 kW","Anschlusswert")],
   specs=[("Korbgröße","400 × 400 mm"),("Theor. Stundenleistung","40 Körbe/h"),("Stromanschluss","230 V / 50 Hz"),
          ("Gesamtanschlusswert","3,4 kW"),("Absicherung","16 A"),("Tankinhalt","8 l"),("Tanktemperatur","60–65 °C"),
          ("Boilerinhalt","6 l"),("Leistung Umwälzpumpe","200 W"),("Gehäuse doppelwandig","ja")],
   features=[_F,"Kompakte Stellfläche – passt unter jede Theke","Anschluss an normale 230-V-Steckdose","Intuitive Bedienung, wartungsarm","Ideal für Gläser, Tassen und Bistrogeschirr"]),
 "u-540-bistro": dict(name="U 540 Bistro", series="Untertisch · Gläser & Bistro", img="U-540-Bistro.png",
   pdf="/assets/datasheets/Datenblatt-U-540-Bistro.pdf",
   tagline="Bistrospülmaschine mit großem 500 × 500 mm Korb für gemischtes Spülgut.",
   intro=["Die U 540 Bistro kombiniert den kompakten Untertisch-Formfaktor mit einem großen 500 × 500 mm Korb – so lassen sich Gläser und Bistrogeschirr flexibel gemeinsam spülen.",
          "Der große Tank und die kräftige Umwälzpumpe sorgen für gleichbleibend gute Ergebnisse, auch im Dauereinsatz."],
   highlights=[("500 × 500 mm","Korbgröße"),("40","Körbe / Stunde"),("400 V","Stromanschluss"),("7,9 kW","Anschlusswert")],
   specs=[("Korbgröße","500 × 500 mm"),("Theor. Stundenleistung","40 Körbe/h"),("Stromanschluss","400 V / 3 / 50 Hz (opt. 230 V, 3,4 kW)"),
          ("Gesamtanschlusswert","7,9 kW"),("Absicherung","16 A"),("Tankinhalt","15 l"),("Tanktemperatur","60–65 °C"),
          ("Boilerinhalt","6 l"),("Leistung Umwälzpumpe","470 W"),("Gehäuse doppelwandig","ja")],
   features=[_F,"Großer 500 × 500 mm Korb für Gläser und Geschirr","Wahlweise 400-V- oder 230-V-Anschluss","Kräftige Umwälzpumpe für konstante Ergebnisse","Geringer Wasser- und Energieverbrauch"]),
 "u-540e": dict(name="U 540 / U 540E", series="Untertisch-Geschirrspülmaschine", img="U-540E.png",
   pdf="/assets/datasheets/Datenblatt-U-540-U-540E.pdf",
   tagline="Untertisch-Geschirrspülmaschine für Körbe 500 × 500 mm – mit eingebautem Wasserenthärter.",
   intro=["Die U 540E ist die Geschirrspülmaschine für den anspruchsvollen Alltag. Mit 385 mm Einfahrhöhe nimmt sie auch höheres Geschirr auf.",
          "Das E-Modell bringt einen eingebauten Wasserenthärter mit – für kalkfreie, streifenlose Ergebnisse ohne separate Enthärtungsanlage."],
   highlights=[("500 × 500 mm","Korbgröße"),("40","Körbe / Stunde"),("385 mm","Einfahrhöhe"),("7,9 kW","Anschlusswert")],
   specs=[("Korbgröße","500 × 500 mm"),("Einfahrhöhe","385 mm"),("Theor. Stundenleistung","40 Körbe/h"),
          ("Stromanschluss","400 V / 3 / 50 Hz"),("Gesamtanschlusswert","7,9 kW"),("Absicherung","16 A"),
          ("Tankinhalt","15 l"),("Tanktemperatur","60–65 °C"),("Boilerinhalt","6 l"),("Leistung Umwälzpumpe","470 W")],
   e_note="E-Modell: mit eingebautem Wasserenthärter",
   features=[_F,"Eingebauter Wasserenthärter für kalkfreie Ergebnisse","385 mm Einfahrhöhe – auch für höheres Geschirr","Große 500 × 500 mm Körbe","Effizient bei Wasser und Energie"]),
 "u-640e": dict(name="U 640 / U 640E", series="Untertisch · Geschirr & Gerätschaften", img="U-640E.png",
   pdf="/assets/datasheets/Datenblatt-U-640-U-640E.pdf",
   tagline="Die größte Untertisch – auch für Tabletts und Gerätschaften.",
   intro=["Die U 640E ist unsere leistungsstärkste Untertischmaschine: Sie bewältigt Geschirr, Tabletts (bis 600 × 400 mm / EN 4) und Gerätschaften gleichermaßen.",
          "Mit größerem Tank und höherer Stundenleistung ist sie ideal für Betriebe, die aus dem Untertisch-Format herauswachsen – inklusive eingebautem Wasserenthärter."],
   highlights=[("bis 600 × 400 mm","Tabletts / EN 4"),("48","Körbe / Stunde"),("9,8 kW","Anschlusswert"),("25 l","Tankinhalt")],
   specs=[("Korbgröße","500 × 500 mm"),("Passend für Tabletts","600 × 400 mm (EN 4)"),("Theor. Stundenleistung","48 Körbe/h"),
          ("Stromanschluss","400 V / 3 / 50 Hz"),("Gesamtanschlusswert","9,8 kW"),("Absicherung","16 A"),
          ("Tankinhalt","25 l"),("Tanktemperatur","60–65 °C"),("Boilertemperatur","80–85 °C"),("Leistung Umwälzpumpe","700 W")],
   e_note="E-Modell: mit eingebautem Wasserenthärter",
   features=[_F,"Auch für Tabletts (EN 4) und Gerätschaften","Eingebauter Wasserenthärter","Großer 25-l-Tank für konstante Leistung","Höchste Kapazität im Untertisch-Format"]),
 "h-540e": dict(name="H 540 / H 540E", series="Haubenspülmaschine", img="H-540E.png",
   pdf="/assets/datasheets/Datenblatt-H-540-H-540E.pdf",
   tagline="Durchschub-Haubenmaschine mit hoher Leistung für den Dauerbetrieb.",
   intro=["Die H 540E ist die klassische Haubenspülmaschine für mittlere bis große Betriebe. Bis zu 60 Körbe pro Stunde und 460 mm Einfahrhöhe meistern jeden Ansturm.",
          "Als Durchschubmaschine lässt sie sich perfekt in Spülstraßen integrieren – das E-Modell mit eingebautem Wasserenthärter."],
   highlights=[("500 × 500 mm","Korbgröße"),("60","Körbe / Stunde"),("460 mm","Einfahrhöhe"),("2.070 mm","Höhe offene Haube")],
   specs=[("Korbgröße","500 × 500 mm"),("Einfahrhöhe","460 mm"),("Höhe mit geöffneter Haube","2.070 mm"),
          ("Theor. Stundenleistung","60 Körbe/h"),("Stromanschluss","400 V / 3 / 50 Hz"),("Boilerleistung","7.000 W"),
          ("Tankinhalt","22 l"),("Tanktemperatur","60–65 °C"),("Boilertemperatur","80–85 °C")],
   e_note="E-Modell: mit eingebautem Wasserenthärter",
   features=[_F,"Bis 60 Körbe/h – für den Dauerbetrieb","460 mm Einfahrhöhe für hohes Spülgut","Ideal für Spülstraßen (Durchschub)","Eingebauter Wasserenthärter"]),
 "h-540e-klima-plus": dict(name="H 540 Klima+ / H 540E Klima+", series="Haubenspülmaschine · Klima+", img="H-540E-Klima-Plus.png",
   pdf="/assets/datasheets/Datenblatt-H540KlimaPlus-H540EKlimaPlus.pdf",
   tagline="Haubenmaschine mit Wärmerückgewinnung – weniger Energie, weniger Wrasen.",
   intro=["Die Klima+-Variante der H 540E bringt eine integrierte Wärmerückgewinnung mit: Die Abwärme wird genutzt, um Frischwasser vorzuwärmen. Das spart Energie und reduziert den Wrasen beim Öffnen der Haube deutlich.",
          "So bleibt das Arbeitsklima angenehm – bei gleicher Spülleistung von bis zu 60 Körben pro Stunde."],
   highlights=[("500 × 500 mm","Korbgröße"),("60","Körbe / Stunde"),("Klima+","Wärmerückgewinnung"),("460 mm","Einfahrhöhe")],
   specs=[("Korbgröße","500 × 500 mm"),("Einfahrhöhe","460 mm"),("Theor. Stundenleistung","60 Körbe/h"),
          ("Wärmerückgewinnung","ja (Klima+)"),("Stromanschluss","400 V / 3 / 50 Hz"),("Boilerleistung","7.000 W"),
          ("Tankinhalt","22 l"),("Tanktemperatur","60–65 °C"),("Boilertemperatur","80–85 °C")],
   e_note="E-Modell: mit eingebautem Wasserenthärter",
   features=["Klima+: integrierte Wärmerückgewinnung senkt den Energieverbrauch","Deutlich weniger Wrasen beim Haubenöffnen","Angenehmes Arbeitsklima am Spülplatz",_F,"Eingebauter Wasserenthärter"]),
 "h-640": dict(name="H 640", series="Haubenspülmaschine · Geschirr & Gerätschaften", img="H-640.png",
   pdf="/assets/datasheets/Datenblatt-H640.pdf",
   tagline="Große Haubenmaschine – auch für Tabletts und Gerätschaften.",
   intro=["Die H 640 ist die leistungsstarke Haubenmaschine für gemischtes Spülgut: Geschirr, Tabletts (600 × 400 mm / EN 4) und Gerätschaften in einem Durchgang.",
          "Robuste Technik und hohe Kapazität machen sie zur ersten Wahl für Kantinen, Hotels und Gemeinschaftsverpflegung."],
   highlights=[("500 × 500 mm","Korbgröße"),("60","Körbe / Stunde"),("9,5 kW","Anschlusswert"),("600 × 400 mm","Tabletts / EN 4")],
   specs=[("Korbgröße","500 × 500 mm"),("Passend für Tabletts","600 × 400 mm (EN 4)"),("Theor. Stundenleistung","60 Körbe/h"),
          ("Stromanschluss","400 V / 3 / 50 Hz"),("Gesamtanschlusswert","9,5 kW"),("Tanktemperatur","60–65 °C"),
          ("Boilertemperatur","80–85 °C")],
   features=[_F,"Auch für Tabletts (EN 4) und Gerätschaften","Hohe Kapazität für Kantine & Hotel","Bis 60 Körbe/h","Robuste Durchschub-Konstruktion"]),
 "h-640-klima-plus": dict(name="H 640 Klima+", series="Haubenspülmaschine · Klima+", img="H-640-Klima-Plus.png",
   pdf="/assets/datasheets/Datenblatt-H640KlimaPlus.pdf",
   tagline="Die H 640 mit integrierter Wärmerückgewinnung.",
   intro=["Die H 640 Klima+ vereint die hohe Kapazität der H 640 mit integrierter Wärmerückgewinnung. Die genutzte Abwärme senkt den Energieverbrauch und reduziert den Wrasen spürbar.",
          "Ideal für Betriebe mit hohem Spülaufkommen, die zugleich auf Effizienz und ein angenehmes Arbeitsklima achten."],
   highlights=[("500 × 500 mm","Korbgröße"),("60","Körbe / Stunde"),("Klima+","Wärmerückgewinnung"),("9,5 kW","Anschlusswert")],
   specs=[("Korbgröße","500 × 500 mm"),("Passend für Tabletts","600 × 400 mm (EN 4)"),("Theor. Stundenleistung","60 Körbe/h"),
          ("Wärmerückgewinnung","ja (Klima+)"),("Stromanschluss","400 V / 3 / 50 Hz"),("Gesamtanschlusswert","9,5 kW"),
          ("Tanktemperatur","60–65 °C"),("Boilertemperatur","80–85 °C")],
   features=["Klima+: integrierte Wärmerückgewinnung","Weniger Wrasen, angenehmeres Arbeitsklima","Auch für Tabletts (EN 4) und Gerätschaften",_F,"Hohe Kapazität für Großbetriebe"]),
 "f-720": dict(name="F 720", series="Gerätespülmaschine", img="F-720.png",
   pdf="/assets/datasheets/Datenblatt-F720.pdf",
   tagline="Gerätespülmaschine für Bleche, Töpfe und großes Spülgut.",
   intro=["Die F 720 ist auf sperriges Spülgut spezialisiert: Bleche, Töpfe, Behälter und Gerätschaften bis 800 × 600 mm. Mit 850 mm Einfahrhöhe nimmt sie auch hohe Teile auf.",
          "Kräftige Umwälzpumpe und leistungsstarker Boiler sorgen für hygienisch saubere Ergebnisse – ideal für Bäckereien, Metzgereien und Großküchen."],
   highlights=[("bis 800 × 600 mm","Spülgut"),("850 mm","Einfahrhöhe"),("68 l","Tankinhalt"),("2.700 W","Umwälzleistung")],
   specs=[("Passend für Bleche/Tabletts","800 × 600 mm"),("Einfahrhöhe","850 mm"),("Theor. Stundenleistung","30 Körbe/h"),
          ("Stromanschluss","400 V / 3 / 50 Hz"),("Boilerleistung","10.500 W"),("Tankinhalt","68 l"),
          ("Leistung Umwälzpumpe","2.700 W"),("Boilertemperatur","80–85 °C")],
   features=[_F,"Für Bleche, Töpfe und Gerätschaften bis 800 × 600 mm","850 mm Einfahrhöhe für sperriges Spülgut","Kräftige Umwälzpumpe (2.700 W)","Ideal für Bäckerei, Metzgerei & Großküche"]),
 "f-920": dict(name="F 920", series="Gerätespülmaschine XL", img="F-920.png",
   pdf="/assets/datasheets/Datenblatt-F-920.pdf",
   tagline="Die große Gerätespülmaschine für Bäckereien und Großküchen.",
   intro=["Die F 920 ist unsere größte Gerätespülmaschine – ausgelegt auf Bleche und Tabletts bis 1.200 × 600 mm. Zwei kräftige Umwälzpumpen bewältigen selbst stark verschmutztes Spülgut.",
          "Wo täglich viele Bleche und Behälter anfallen, spielt die F 920 ihre Stärke aus: maximale Kapazität bei zuverlässiger Hygiene."],
   highlights=[("bis 1.200 × 600 mm","Spülgut"),("850 mm","Einfahrhöhe"),("2 × 2.700 W","Umwälzleistung"),("30","Körbe / Stunde")],
   specs=[("Passend für Bleche/Tabletts","1.200 × 600 mm"),("Einfahrhöhe","850 mm"),("Theor. Stundenleistung","30 Körbe/h"),
          ("Stromanschluss","400 V / 3 / 50 Hz"),("Boilerleistung","10.500 W"),("Leistung Umwälzpumpe","2 × 2.700 W"),
          ("Boilertemperatur","80–85 °C")],
   features=[_F,"Für Bleche und Tabletts bis 1.200 × 600 mm","Zwei kräftige Umwälzpumpen","Maximale Kapazität für hohe Aufkommen","Ideal für Großbäckereien & Großküchen"]),
 "kt-1": dict(name="KT-1", series="Korbtransportspülmaschine", img="KT1.png",
   pdf="/assets/datasheets/Datenblatt_KT_1_KT_2_2024.pdf",
   tagline="Korbtransport-Spülmaschine für hohe, kontinuierliche Durchsätze.",
   intro=["Die KT-1 transportiert die Körbe automatisch durch die Maschine – für kontinuierliches Spülen ohne Handgriffe. Bis zu 160 Körbe pro Stunde bewältigen auch großes Aufkommen.",
          "Robuste Edelstahl-Konstruktion und durchdachte Zonen sorgen für zuverlässige Hygiene bei wirtschaftlichem Verbrauch."],
   highlights=[("80–160","Körbe / Stunde"),("500 × 500 mm","Korbgröße"),("22,2 kW","Anschlusswert (55 °C)"),("170 l/h","max. Wasserverbrauch")],
   specs=[("Abmessung (B × T × H)","1.450 × 770 × 1.565 mm"),("Einfahrhöhe","450 mm"),("Korbabmessung","500 × 500 mm"),
          ("Theor. Stundenleistung","80–160 Körbe/h"),("Stromanschluss","400 V / 3 / 50 Hz"),
          ("Gesamtanschlusswert (55 °C)","22,2 kW"),("Gesamtanschlusswert (15 °C)","28,7 kW"),
          ("Tankinhalt Waschzone","70 l"),("Tanktemperatur","55–60 °C"),("Boilertemperatur","80–85 °C"),
          ("Wasserverbrauch max.","170 l/h"),("Gewicht netto","240 kg")],
   features=["Automatischer Korbtransport – kontinuierliches Spülen","Bis 160 Körbe/h für hohes Aufkommen","Robuste Edelstahl-Konstruktion","Wirtschaftlicher Wasser- und Energieverbrauch"]),
 "kt-2": dict(name="KT-2", series="Korbtransportspülmaschine", img="KT2.png",
   pdf="/assets/datasheets/Datenblatt_KT_1_KT_2_2024.pdf",
   tagline="Die größere Korbtransportmaschine mit Vorspül- und Waschzone.",
   intro=["Die KT-2 erweitert das Korbtransport-Prinzip um eine separate Vorspülzone. So werden bis zu 270 Körbe pro Stunde bei bester Reinigung möglich.",
          "Ideal für Kantinen, Caterer und Großküchen mit hohem, konstantem Spülaufkommen."],
   highlights=[("130–270","Körbe / Stunde"),("500 × 500 mm","Korbgröße"),("29,7 kW","Anschlusswert (55 °C)"),("280 l/h","max. Wasserverbrauch")],
   specs=[("Abmessung (B × T × H)","2.268 × 770 × 1.565 mm"),("Einfahrhöhe","450 mm"),("Korbabmessung","500 × 500 mm"),
          ("Theor. Stundenleistung","130–270 Körbe/h"),("Stromanschluss","400 V / 3 / 50 Hz"),
          ("Gesamtanschlusswert (55 °C)","29,7 kW"),("Gesamtanschlusswert (15 °C)","41,2 kW"),
          ("Tankinhalt Vorspül-/Waschzone","70 / 70 l"),("Tanktemperatur","55–60 °C"),("Boilertemperatur","80–85 °C"),
          ("Wasserverbrauch max.","280 l/h"),("Gewicht netto","340 kg")],
   features=["Separate Vorspül- und Waschzone","Bis 270 Körbe/h für höchste Durchsätze","Automatischer Korbtransport","Für Kantine, Catering & Großküche"]),
 "kt-1-plus": dict(name="KT-1 Plus", series="Korbtransportspülmaschine · Plus", img="KT1-Plus.png",
   pdf="/assets/datasheets/Datenblatt-KT_1-Plus-und_KT_2_Plus_2024.pdf",
   tagline="KT 1 Plus – noch effizienter dank optimierter Zonen.",
   intro=["Die KT-1 Plus optimiert das bewährte KT-1-Konzept: Bei bis zu 200 Körben pro Stunde sinkt der Wasserverbrauch auf nur 160 l/h.",
          "Höhere Bauhöhe und verfeinerte Technik machen sie zur effizienten Wahl für anspruchsvolle Dauereinsätze."],
   highlights=[("100–200","Körbe / Stunde"),("500 × 500 mm","Korbgröße"),("23,7 kW","Anschlusswert (55 °C)"),("160 l/h","max. Wasserverbrauch")],
   specs=[("Abmessung (B × T × H)","2.001 × 770 × 1.880 mm"),("Einfahrhöhe","450 mm"),("Korbabmessung","500 × 500 mm"),
          ("Theor. Stundenleistung","100–200 Körbe/h"),("Stromanschluss","400 V / 3 / 50 Hz"),
          ("Gesamtanschlusswert (55 °C)","23,7 kW"),("Gesamtanschlusswert (15 °C)","30,2 kW"),
          ("Tankinhalt Waschzone","70 l"),("Tanktemperatur","55–60 °C"),("Boilertemperatur","80–85 °C"),
          ("Wasserverbrauch max.","160 l/h"),("Gewicht netto","300 kg")],
   features=["Optimierte Zonen für höhere Effizienz","Nur 160 l/h bei bis zu 200 Körben/h","Automatischer Korbtransport","Robuste Edelstahl-Konstruktion"]),
 "kt-2-plus": dict(name="KT-2 Plus", series="Korbtransportspülmaschine · Plus", img="KT2-Plus.png",
   pdf="/assets/datasheets/Datenblatt-KT_1-Plus-und_KT_2_Plus_2024.pdf",
   tagline="Das Flaggschiff: höchste Durchsätze mit Vorspül- und Waschzone.",
   intro=["Die KT-2 Plus ist unsere leistungsstärkste Korbtransportmaschine: Vorspül- und Waschzone, bis zu 270 Körbe pro Stunde und dennoch nur 220 l/h Wasserverbrauch.",
          "Für Großküchen und Caterer, bei denen kontinuierlich große Mengen anfallen – maximale Leistung bei kontrolliertem Verbrauch."],
   highlights=[("135–270","Körbe / Stunde"),("500 × 500 mm","Korbgröße"),("28,2 kW","Anschlusswert (55 °C)"),("220 l/h","max. Wasserverbrauch")],
   specs=[("Abmessung (B × T × H)","2.819 × 770 × 1.880 mm"),("Einfahrhöhe","450 mm"),("Korbabmessung","500 × 500 mm"),
          ("Theor. Stundenleistung","135–270 Körbe/h"),("Stromanschluss","400 V / 3 / 50 Hz"),
          ("Gesamtanschlusswert (55 °C)","28,2 kW"),("Gesamtanschlusswert (15 °C)","37,7 kW"),
          ("Tankinhalt Vorspül-/Waschzone","70 / 70 l"),("Tanktemperatur","55–60 °C"),("Boilertemperatur","80–85 °C"),
          ("Wasserverbrauch max.","220 l/h"),("Gewicht netto","440 kg")],
   features=["Separate Vorspül- und Waschzone","Bis 270 Körbe/h bei nur 220 l/h","Automatischer Korbtransport","Für Großküche & Catering mit Höchstlast"]),
}

for slug, d in MACHINE_DETAIL.items():
    url = f"/produkte/spuelmaschinen/{slug}/"
    filename = f"produkte/spuelmaschinen/{slug}/index.html"
    highs = "".join(f'<div class="spec-hi"><strong>{v}</strong><span>{html.escape(l)}</span></div>' for v, l in d["highlights"])
    feats = "".join(f'<li>{html.escape(x)}</li>' for x in d["features"])
    rows = "".join(f'<tr><th>{html.escape(l)}</th><td>{html.escape(v)}</td></tr>' for l, v in d["specs"])
    intro = "".join(f"<p>{html.escape(p)}</p>" for p in d["intro"])
    enote = f'<p class="enote">✚ {html.escape(d["e_note"])}</p>' if d.get("e_note") else ""
    body = (
      f'<div class="crumb"><div class="container"><a href="/produkte/spuelmaschinen/">Spülmaschinen</a> '
      f'<span>›</span> {html.escape(d["name"])}</div></div>'
      + hero(f'Spülmaschinen · {d["series"]}', html.escape(d["name"]), html.escape(d["tagline"]),
             cta=[("Anfrage senden", "/kontakt/", "btn--primary"),
                  ("Datenblatt (PDF)", d["pdf"], "btn--ghost")],
             img=f'/assets/img/machines/{d["img"]}', cls="hero--sub")
      + f'<section class="spec-hi-band"><div class="container spec-hi-grid">{highs}</div></section>'
      + '<section class="section"><div class="container spec-layout">'
        + f'<div class="spec-intro"><p class="eyebrow">Überblick</p><h2>{html.escape(d["name"])} im Detail</h2>'
          f'{intro}{enote}<ul class="feature-list">{feats}</ul></div>'
        + f'<aside class="spec-card"><h3>Technische Daten</h3><table class="spec-table"><tbody>{rows}</tbody></table>'
          f'<a class="btn btn--primary datasheet-btn" href="{d["pdf"]}" target="_blank" rel="noopener">⭳ Original-Datenblatt (PDF)</a>'
          f'<p class="spec-note">Alle Angaben laut offiziellem Datenblatt. Änderungen und Irrtümer vorbehalten.</p></aside>'
      + '</div></section>'
      + cta_band(f'Passt die {html.escape(d["name"])} zu Deinem Betrieb?',
                 "Wir beraten Dich persönlich und unverbindlich – und finden die richtige Maschine.",
                 "Beratung anfragen")
      + '<section class="section section--muted"><div class="container">'
        + section_head("Weitere Modelle", "Alle Spülmaschinen im Überblick")
        + '<div style="text-align:center"><a class="btn btn--primary" href="/produkte/spuelmaschinen/">Zur Produktübersicht</a></div>'
      + '</div></section>')
    PAGES[url] = (filename, d["name"], page("/produkte/spuelmaschinen/", d["name"], body,
        f'{d["name"]} – {d["tagline"]} Technische Daten und Datenblatt.'))

def official_filename(url):
    return "index.html" if url == "/" else f"{url.strip('/')}/index.html"

def official_text_length(content):
    text = re.sub(r"<[^>]+>", " ", content)
    text = html.unescape(re.sub(r"\s+", " ", text)).strip()
    return len(text)

def official_page_body(data):
    source = html.escape(data.get("source", ""))
    return (
        f'<section class="official-page" data-source="{source}">'
        f'{data.get("content_html", "")}'
        '</section>'
    )

for official_url, official_data in OFFICIAL_PAGES.items():
    if official_url == "/":
        continue
    content_html = official_data.get("content_html", "")
    # Some WordPress parent pages are only menu containers. Keep the local
    # overview pages instead of replacing them with near-empty content.
    if official_text_length(content_html) < 80:
        continue
    title = official_data.get("title") or official_url.strip("/").replace("-", " ").title()
    description = official_data.get("description", "")
    filename = official_filename(official_url)
    PAGES[official_url] = (
        filename,
        title,
        page(official_url, title, official_page_body(official_data), description),
    )

# BASE_PATH lets the same source deploy at a sub-path (GitHub Pages project site)
# or at root (local server). All internal refs start with ="/ ; external ones
# start with ="http, ="tel:, ="mailto:, ="# and are left untouched.
BASE = os.environ.get("BASE_PATH", "").rstrip("/")

count = 0
for url, (filename, title, content) in PAGES.items():
    if BASE:
        content = content.replace('="/', f'="{BASE}/')
        content = content.replace("='/", f"='{BASE}/")
        content = content.replace("url(/", f"url({BASE}/")
    path = os.path.join(ROOT, filename)
    os.makedirs(os.path.dirname(path) or ROOT, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    count += 1
print(f"Wrote {count} pages (BASE_PATH='{BASE}').")
