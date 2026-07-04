#!/usr/bin/env python3
"""Static-site generator for the Ackermann Spülmaschinen recreation.
Runs top-to-bottom, writing every page with a shared header/footer so the
navigation stays consistent. Re-run after editing content: `python3 build.py`.
"""
import os, html

ROOT = os.path.dirname(os.path.abspath(__file__))

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
    ("Die Andersmacher", "/die-andersmacher/", []),
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
<link rel="icon" href="/assets/img/ackermann-logo-mobile.png">
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
      <img src="/assets/img/ackermann-biene-footer.png" alt="" class="footer__bee">
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
    <nav class="footer__col" aria-label="Kontakt und Rechtliches">
      <h4>Kontakt</h4>
      <a href="tel:+4975029779100">+49 (0)7502 97791 00</a>
      <a href="mailto:info@ackermann-spuelmaschinen.de">info@ackermann-spuelmaschinen.de</a>
      <div class="footer__social">
        <a href="https://www.facebook.com/ackermann.spuelmaschinen/" target="_blank" rel="noopener">Facebook</a>
        <a href="https://www.instagram.com/" target="_blank" rel="noopener">Instagram</a>
      </div>
      <a href="/impressum/">Impressum</a>
      <a href="/datenschutz/">Datenschutz</a>
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
    ("🍽️", "Gastronomie und Hotellerie", "/gastronomie-und-hotellerie/",
     "Zuverlässige Technik für Cafés, Bars, Restaurants und Hotels – einfach zu bedienen und wartungsarm."),
    ("🥗", "Gemeinschaftsverpflegung und Catering", "/gemeinschaftsverpflegung-und-catering/",
     "Spültechnik, mit der man rechnen kann – robuste Geräte für hohe Durchsätze und faire Betriebskosten."),
    ("🥖", "Bäckereien und Metzgereien", "/baeckereien-und-metzgereien/",
     "Heiß und fettig? Mit uns bleibst Du cool. Meister der Vielfalt für Bleche, Geschirr und Behälter."),
    ("🎪", "Außer Haus und mobiles Spülen", "/ausser-haus-und-mobiles-spuelen/",
     "Mit dem Spülmobil erfüllst Du alle Vorschriften und gewinnst maximale Flexibilität für jeden Einsatzort."),
]

MACHINES = {
    "Untertischspülmaschinen": [
        ("U 440", "Gläser", "U-440.png"),
        ("U 540 Bistro", "Gläser", "U-540-Bistro.png"),
        ("U 540E", "Gläser / Geschirr", "U-540E.png"),
        ("U 640E", "Gläser / Geschirr / Gerätschaften", "U-640E.png"),
    ],
    "Haubenspülmaschinen": [
        ("H 540E", "Gläser / Geschirr", "H-540E.png"),
        ("H 540E Klima+", "Gläser / Geschirr", "H-540E-Klima-Plus.png"),
        ("H 640", "Gläser / Geschirr / Gerätschaften", "H-640.png"),
        ("H 640 Klima+", "Gläser / Geschirr / Gerätschaften", "H-640-Klima-Plus.png"),
    ],
    "Gerätespülmaschinen": [
        ("F 720", "Gerätschaften", "F-720.png"),
        ("F 920", "Gerätschaften", "F-920.png"),
    ],
    "Korbtransportspülmaschinen": [
        ("KT-1", "Gläser / Geschirr / Gerätschaften", "KT1.png"),
        ("KT-1 PLUS", "Gläser / Geschirr / Gerätschaften", "KT1-Plus.png"),
        ("KT-2", "Gläser / Geschirr / Gerätschaften", "KT2.png"),
        ("KT-2 PLUS", "Gläser / Geschirr / Gerätschaften", "KT2-Plus.png"),
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

CHEMIE = {
    "Reiniger": ["F 440 Bistro", "F 450 green", "F 500 GS", "P 500 GS", "F 540 Power", "F 600 GR"],
    "Spezialreiniger": ["Gläsergrundreiniger"],
    "Klarspüler": ["KLAR GS", "KLAR GG sauer"],
    "Weitere": ["Entkalker", "Regeneriersalz"],
}

# ---------------------------------------------------------------- builders
def cards_solutions():
    c = "".join(f"""<a class="card" href="{u}">
  <div class="card__icon">{ic}</div>
  <h3>{html.escape(t)}</h3>
  <p>{html.escape(d)}</p>
  <span class="card__link">Mehr erfahren &rarr;</span>
</a>""" for ic, t, u, d in SOLUTIONS)
    return f'<div class="cards cards--4">{c}</div>'

def machine_grid():
    out = []
    for cat, items in MACHINES.items():
        cards = "".join(f"""<div class="machine">
  <div class="machine__media"><img src="/assets/img/machines/{img}" alt="{html.escape(name)}" loading="lazy"></div>
  <h4>{html.escape(name)}</h4>
  <p>{html.escape(use)}</p>
</div>""" for name, use, img in items)
        out.append(f'<h3 class="machine-cat">{html.escape(cat)}</h3><div class="cards cards--4 machine-row">{cards}</div>')
    return "\n".join(out)

def andersmacher_grid():
    c = ""
    for name, img, url in ANDERSMACHER:
        media = (f'<img src="/assets/img/{img}" alt="{html.escape(name)}" loading="lazy">'
                 if img else f'<div class="ref__placeholder">{html.escape(name)}</div>')
        c += f'<a class="ref" href="{url}"><div class="ref__media">{media}</div><span class="ref__name">{html.escape(name)}</span></a>'
    return f'<div class="cards cards--4 refs">{c}</div>'

def stats_strip():
    stats = [("Top 5", "Systemanbieter der Branche"),
             ("min.", "Wasser- &amp; Energieverbrauch"),
             ("1.", "Preis-Leistung im Premiumbereich"),
             ("100%", "Service &amp; Beratung aus einer Hand")]
    return '<section class="stats"><div class="container stats__grid">' + "".join(
        f'<div class="stat"><strong>{s}</strong><span>{t}</span></div>' for s, t in stats) + '</div></section>'

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
 hero("Die Alternative im Premiumbereich",
      "Dein Partner für gewerbliche Spültechnik",
      "Ob Gastronomie, Hotellerie, Gemeinschaftsverpflegung, Bäckereien und Metzgereien oder mobiles Spülen auf Feiern und Festen – wir liefern das beste Preis-Leistungs-Verhältnis im Premiumbereich, erstklassigen Service und nachhaltige Lösungen mit extrem niedrigem Wasserverbrauch.",
      cta=[("Entdecke unsere Lösungen", "/#loesungen", "btn--primary"),
           ("Warum Ackermann?", "/ueber-uns/", "btn--ghost")],
      img="/assets/img/machines/H-640.png")
 + stats_strip()
 + f'<section class="section" id="loesungen"><div class="container">'
   + section_head("Lösungen für Deine Branche", "Für jeden Einsatz die passende Spültechnik",
       "Entdecke unsere Lösungen für Deine Branche – individuell abgestimmt auf Deine Anforderungen, Deine Abläufe und Dein Spülgut.")
   + cards_solutions() + '</div></section>'
 + f'<section class="section section--muted"><div class="container">'
   + section_head("Produkte", "Alles fürs perfekte Spülergebnis")
   + f"""<div class="cards cards--2">
      <a class="product" href="/produkte/spuelmaschinen/">
        <div class="product__media"><img src="/assets/img/machines/U-540E.png" alt="Spülmaschinen"></div>
        <div class="product__body"><h3>Spülmaschinen</h3>
          <p>Vom Gläser- und Bistrospüler über Hauben- und Gerätespülmaschinen bis zur Korbtransport-Spülmaschine – zuverlässige Technik für jede Betriebsgröße.</p>
          <span class="card__link">Zu den Spülmaschinen &rarr;</span></div>
      </a>
      <a class="product" href="/produkte/spuelchemie/">
        <div class="product__media product__media--chem">🧪</div>
        <div class="product__body"><h3>Spülchemie</h3>
          <p>Passgenau abgestimmte Reiniger, Klarspüler und Pflegemittel für glänzend saubere Ergebnisse bei minimalem Verbrauch.</p>
          <span class="card__link">Zur Spülchemie &rarr;</span></div>
      </a></div></div></section>"""
 + f'<section class="section"><div class="container">'
   + section_head("Über uns", "Qualität und Service: Entdecke die Alternative!",
       "Als familiengeführter Systemanbieter für gewerbliche Spültechnik zählen wir zu den Top 5 der Branche – mit schlanken Abläufen, fairen Preisen und klarem Fokus auf das optimale Spülergebnis.")
   + '<div class="pillars">'
   + "".join(f'<a class="pillar" href="{u}"><span class="pillar__no">{n:02d}</span><h3>{t}</h3><p>{d}</p></a>'
       for n,(t,u,d) in enumerate([
         ("Unser Team","/ueber-uns/","Menschen, die Spültechnik leben und Dich persönlich beraten."),
         ("Qualität","/ueber-uns/qualitaet/","Premium-Technik, die im harten Alltag zuverlässig läuft."),
         ("Service","/ueber-uns/service/","Schnell erreichbar, kompetent vor Ort – aus einer Hand."),
         ("Innovationen","/ueber-uns/innovationen/","Durchdachte Technik für bessere Ergebnisse und Effizienz."),
         ("Nachhaltigkeit","/ueber-uns/nachhaltigkeit/","Extrem niedriger Wasser- und Energieverbrauch."),
       ],1)) + '</div></div></section>'
 + f'<section class="section section--dark"><div class="container">'
   + section_head("Die Andersmacher", "Betriebe, die anders spülen",
       "Vom Hofcafé bis zur Metzgerei: Diese Andersmacher setzen auf Ackermann.", light=True)
   + andersmacher_grid() + '</div></section>'
 + cta_band("Bereit für die Alternative im Premiumbereich?",
     "Sprich mit uns – wir finden die passende Spüllösung für Deinen Betrieb."),
 "Ackermann Spülmaschinen GmbH aus Baindt: gewerbliche Spülmaschinen und Spülchemie für Gastronomie, Hotellerie, Catering, Bäckereien, Metzgereien und mobiles Spülen."))

def solution_page(url, filename, eyebrow, h1, lead, body_extra=""):
    b = (hero(eyebrow, h1, lead, cta=[("Jetzt beraten lassen", "/kontakt/", "btn--primary")], cls="hero--sub")
         + f'<section class="section"><div class="container prose">{body_extra}</div></section>'
         + '<section class="section section--muted"><div class="container">'
         + section_head("Passende Produkte", "Unsere Spülmaschinen")
         + cards_solutions().replace("cards--4","cards--4") + '</div></section>'
         + cta_band("Fragen zu Deiner Branche?", "Wir beraten Dich persönlich und unverbindlich.", "Kontakt aufnehmen"))
    PAGES[url] = (filename, h1, page(url, h1, b, lead[:150]))

solution_page("/gastronomie-und-hotellerie/", "gastronomie-und-hotellerie/index.html",
    "Lösungen für", "Gastronomie &amp; Hotellerie",
    "Wir machen das Spülen einfach.",
    "<p>Spülmaschinen für die Gastronomie müssen zuverlässig laufen, hervorragende Ergebnisse liefern und dabei intuitiv und wartungsarm sein. Als Partner innovativer Cafés, Bars, Restaurants und Hotels schätzen unsere Kunden entweder unseren unschlagbaren Preis oder unseren außergewöhnlichen Service – und meistens beides.</p><p>Auch kleinere Betriebe erhalten bei uns die volle Aufmerksamkeit und Unterstützung. Denn wir sind einfach näher dran.</p>")

solution_page("/gemeinschaftsverpflegung-und-catering/", "gemeinschaftsverpflegung-und-catering/index.html",
    "Lösungen für", "Catering und Gemeinschaftsverpflegung",
    "Spültechnik, mit der man rechnen kann.",
    "<p>Von der Kita-Küche bis zum großen Hochzeits-Event: So unterschiedlich die Einsätze, so vielseitig muss die Spültechnik sein – und in kurzer Zeit ganz verschiedenes Spülgut bewältigen.</p><p>Profis rechnen mit den kompletten Lebenszykluskosten: Anschaffungspreis, Wartung, Verbrauch und Ersatzteile. Genau hier punkten wir mit robuster Premium-Qualität zu fairen Preisen und starkem Service.</p>")

solution_page("/baeckereien-und-metzgereien/", "baeckereien-und-metzgereien/index.html",
    "Lösungen für", "Heiß und fettig? Mit uns bleibst Du cool",
    "Meister der Vielfalt für Bäckereien und Metzgereien.",
    "<p>Bäckereien und Metzgereien sind heute oft fast schon kleine Bistros. Die heiße Theke hat Konjunktur. Damit steigen auch die Anforderungen an die Spültechnik. Die Hygiene bleibt das A und O, zudem aber müssen Spülmaschinen in diesen Branchen Meister der Vielfalt sein.</p><p>Von fettigen Blechen über empfindliches Geschirr bis zu Behältern – und das alles auf begrenztem Raum. Unsere Geräte überzeugen bei Leistung und Wirtschaftlichkeit gleichermaßen.</p>")

solution_page("/ausser-haus-und-mobiles-spuelen/", "ausser-haus-und-mobiles-spuelen/index.html",
    "Lösungen für", "Außer Haus und mobiles Spülen",
    "So einfach war mobiles Spülen noch nie.",
    "<p>Beim Außerhaus-Catering, auf Festen oder auf Marktplätzen: Die Ansprüche an die Bewirtung und Logistik steigen, und auch die Hygienevorschriften werden immer anspruchsvoller.</p><p>Mit dem Spülmobil erfüllst Du nicht nur alle Vorschriften, sondern gewinnst maximale Flexibilität für unterschiedliche Einsatzorte. Anschluss an Strom und Wasser genügt – und los geht's.</p>")

# PRODUCTS – Spülmaschinen
PAGES["/produkte/spuelmaschinen/"] = ("produkte/spuelmaschinen/index.html", "Spülmaschinen", page(
 "/produkte/spuelmaschinen/", "Spülmaschinen",
 hero("Produkte", "Unsere Spülmaschinen",
      "Untertisch-, Hauben-, Geräte- und Korbtransportspülmaschinen – zuverlässige Premium-Technik für jede Betriebsgröße und jedes Spülgut.",
      cta=[("Beratung anfragen","/kontakt/","btn--primary")], cls="hero--sub")
 + '<section class="section"><div class="container">' + machine_grid() + '</div></section>'
 + cta_band("Welche Maschine passt zu Deinem Betrieb?", "Wir beraten Dich gern und finden die passende Lösung."),
 "Untertisch-, Hauben-, Geräte- und Korbtransportspülmaschinen von Ackermann."))

# PRODUCTS – Spülchemie
chem_cards = "".join(
    f'<div class="card"><h3>{html.escape(cat)}</h3><ul class="chem-list">' +
    "".join(f'<li>{html.escape(x)}</li>' for x in items) + '</ul></div>'
    for cat, items in CHEMIE.items())
PAGES["/produkte/spuelchemie/"] = ("produkte/spuelchemie/index.html", "Spülchemie", page(
 "/produkte/spuelchemie/", "Spülchemie",
 hero("Produkte", "Unsere Spülchemie",
      "Reiniger, Klarspüler und Pflegemittel – passgenau abgestimmt auf unsere Maschinen für glänzende Ergebnisse bei minimalem Verbrauch.",
      cta=[("Beratung anfragen","/kontakt/","btn--primary")], cls="hero--sub")
 + '<section class="section"><div class="container">'
   + section_head("Sortiment", "Für jedes Spülgut die richtige Chemie",
       "Unsere Reiniger sind zur Anwendung in gewerblichen Gläser- und Geschirrspülmaschinen formuliert. Klarspüler mit gutem Benetzungsvermögen und schaumreduzierender Wirkung sorgen für streifenfreien Glanz.")
   + f'<div class="cards cards--4">{chem_cards}</div></div></section>'
 + cta_band("Fragen zur richtigen Dosierung?", "Wir helfen Dir, Verbrauch und Ergebnis optimal einzustellen."),
 "Reiniger, Klarspüler, Entkalker und Regeneriersalz von Ackermann Spülmaschinen."))

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
       for n,(t,u,d) in enumerate([
         ("Qualität","/ueber-uns/qualitaet/","Premium-Technik, die im harten Alltag zuverlässig läuft."),
         ("Service","/ueber-uns/service/","Schnell erreichbar, kompetent vor Ort – aus einer Hand."),
         ("Innovationen","/ueber-uns/innovationen/","Durchdachte Technik für bessere Ergebnisse und Effizienz."),
         ("Nachhaltigkeit","/ueber-uns/nachhaltigkeit/","Extrem niedriger Wasser- und Energieverbrauch."),
       ],1)) + '</div></div></section>'
 + cta_band("Werde ein Andersmacher", "Sprich mit uns über die Alternative im Premiumbereich."),
 "Familiengeführter Systemanbieter für gewerbliche Spültechnik aus Baindt – Top 5 der Branche."))

def about_sub(url, filename, title, eyebrow, lead, paras):
    body = (hero(eyebrow, html.escape(title), lead, cta=[("Kontakt","/kontakt/","btn--primary")], cls="hero--sub")
      + '<section class="section"><div class="container prose">'
      + "".join(f"<p>{p}</p>" for p in paras) + '</div></section>'
      + cta_band("Mehr erfahren?", "Wir beraten Dich gern persönlich."))
    PAGES[url] = (filename, title, page(url, title, body, lead))

about_sub("/ueber-uns/qualitaet/", "ueber-uns/qualitaet/index.html", "Qualität", "Über uns",
    "Premium-Qualität, die sich im Alltag beweist.",
    ["Unsere Maschinen sind für den harten Dauereinsatz gebaut – langlebige Komponenten, durchdachte Technik und hervorragende Spülergebnisse.",
     "Premium bedeutet für uns nicht überteuert, sondern verlässlich: Qualität, auf die Du Dich Tag für Tag verlassen kannst."])
about_sub("/ueber-uns/service/", "ueber-uns/service/index.html", "Service", "Über uns",
    "Service aus einer Hand – schnell und kompetent.",
    ["Beratung, Installation, Wartung und Ersatzteile: Bei uns kommt alles aus einer Hand. Wir sind schnell erreichbar und dann vor Ort, wenn es darauf ankommt.",
     "So minimierst Du Ausfallzeiten und hast einen Partner, der Deinen Betrieb wirklich kennt."])
about_sub("/ueber-uns/innovationen/", "ueber-uns/innovationen/index.html", "Innovationen", "Über uns",
    "Durchdachte Technik für bessere Ergebnisse.",
    ["Wir entwickeln unsere Spültechnik konsequent weiter – für bessere Ergebnisse, einfachere Bedienung und mehr Effizienz.",
     "Jede Innovation muss sich im Praxisalltag beweisen. Nur was den Betrieb spürbar besser macht, kommt in unsere Maschinen."])
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
legal("/datenschutz/", "datenschutz/index.html", "Datenschutz", [
  "<p>Der Schutz Deiner persönlichen Daten ist uns wichtig. Wir verarbeiten personenbezogene Daten ausschließlich im Rahmen der gesetzlichen Bestimmungen (DSGVO, BDSG).</p>",
  "<h2>Verantwortlicher</h2><p>Ackermann Spülmaschinen GmbH, Am Umspannwerk 18, 88255 Baindt, info@ackermann-spuelmaschinen.de</p>",
  "<h2>Deine Rechte</h2><p>Du hast das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch.</p>",
  "<p class='muted-note'>Hinweis: Platzhalter-Datenschutzerklärung für die Nachbildung. Vor Veröffentlichung durch die vollständige, rechtssichere Fassung ersetzen.</p>",
])

# ---------------------------------------------------------------- write
# BASE_PATH lets the same source deploy at a sub-path (GitHub Pages project site)
# or at root (local server). All internal refs start with ="/ ; external ones
# start with ="http, ="tel:, ="mailto:, ="# and are left untouched.
BASE = os.environ.get("BASE_PATH", "").rstrip("/")

count = 0
for url, (filename, title, content) in PAGES.items():
    if BASE:
        content = content.replace('="/', f'="{BASE}/')
    path = os.path.join(ROOT, filename)
    os.makedirs(os.path.dirname(path) or ROOT, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    count += 1
print(f"Wrote {count} pages (BASE_PATH='{BASE}').")
