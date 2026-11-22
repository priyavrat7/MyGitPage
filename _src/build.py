"""Build EN pages (parts/) and FR pages (parts_fr/ -> fr/) with shared header/footer.

Run from anywhere:  python3 _src/build.py
"""
import re, sys, pathlib
S = pathlib.Path(__file__).resolve().parent; site = S.parent
BASE = "https://priyavrat7.github.io/MyGitPage/"
H = (S/"tpl/header.html").read_text(); F = (S/"tpl/footer.html").read_text()
JL = (S/"tpl/jsonld.json").read_text()

FR_NAV = {">Home<": ">Accueil<", ">About<": ">À propos<", ">Resume<": ">CV<", ">Open Source<": ">Open source<",
          ">Projects<": ">Projets<", ">Academics<": ">Formation<"}
FR_HDR = {"Skip to content": "Aller au contenu", 'aria-label="Main"': 'aria-label="Principal"',
          'aria-label="Toggle theme"': 'aria-label="Changer de thème"', 'aria-label="Menu"': 'aria-label="Menu"'}
FR_FTR = {
  "Research software, distributed systems, machine learning, and IoT. Based in Canada.": "Logiciels de recherche, systèmes distribués, apprentissage automatique et IdO. Basé au Canada.",
  ">Explore<": ">Explorer<", ">More<": ">Plus<", "IEEE ICC 2025 paper": "Article IEEE ICC 2025",
  'aria-label="Email"': 'aria-label="Courriel"', 'aria-label="Techamana profile"': 'aria-label="Profil Techamana"',
  "© Priyavrat Dev Sharma. All rights reserved.": "© Priyavrat Dev Sharma. Tous droits réservés.",
  "Last updated November 2026": "Dernière mise à jour : novembre 2026"}

def tr(s, table):
    for a, b in table.items(): s = s.replace(a, b)
    return s

def page(name, raw, lang):
    meta_block, body = raw.split("\n---\n", 1)
    meta = dict(l.split(": ", 1) for l in meta_block.strip().splitlines())
    fr = lang == "fr"
    hdr, ftr = H, F
    if fr:
        hdr = tr(tr(hdr, FR_NAV), FR_HDR); ftr = tr(tr(ftr, FR_NAV), FR_FTR)
        sw = f'<a class="icon-btn lang-btn" href="../{name}" hreflang="en" lang="en" aria-label="View this page in English">EN</a>'
    else:
        sw = f'<a class="icon-btn lang-btn" href="fr/{name}" hreflang="fr" lang="fr" aria-label="Voir cette page en français">FR</a>'
    hdr = hdr.replace("{{LANGSWITCH}}", sw)
    hdr = hdr.replace(f'<a href="{name}">', f'<a href="{name}" aria-current="page">')
    url = BASE + ("fr/" if fr else "") + (name if name != "index.html" else "")
    en_url = BASE + (name if name != "index.html" else ""); fr_url = BASE + "fr/" + (name if name != "index.html" else "")
    img = BASE + "assets/img/" + meta.get("image", "priv6.jpg")
    pre = "../" if fr else ""
    jl = ""
    if name == "index.html":
        j = JL.replace('"jobTitle": "Research Software Developer"', '"jobTitle": "Développeur de logiciels de recherche"') if fr else JL
        jl = f'\n  <script type="application/ld+json">{j}</script>'
    d, k, ti = meta["description"], meta["keywords"], meta["title"]
    out = f"""<!DOCTYPE html>
<html lang="{lang}" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{ti}</title>
  <meta name="description" content="{d}">
  <meta name="keywords" content="{k}">
  <meta name="author" content="Priyavrat Dev Sharma">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="en" href="{en_url}">
  <link rel="alternate" hreflang="fr" href="{fr_url}">
  <link rel="alternate" hreflang="x-default" href="{en_url}">

  <meta property="og:type" content="website">
  <meta property="og:locale" content="{'fr_CA' if fr else 'en_CA'}">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{ti}">
  <meta property="og:description" content="{d}">
  <meta property="og:image" content="{img}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{ti}">
  <meta name="twitter:description" content="{d}">
  <meta name="twitter:image" content="{img}">

  <link rel="icon" type="image/png" href="{pre}assets/img/apple-touch-icon.png?v=3">
  <link rel="apple-touch-icon" href="{pre}assets/img/apple-touch-icon.png?v=3">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link href="{pre}assets/vendor/bootstrap-icons/bootstrap-icons.css" rel="stylesheet">
  <link href="{pre}assets/css/site.css" rel="stylesheet">
  <script>(function(){{var t;try{{t=localStorage.getItem('theme')}}catch(e){{}}if(t)document.documentElement.setAttribute('data-theme',t);}})();</script>{jl}
</head>

<body>
{hdr}

  <main id="main">
{body.rstrip()}
  </main>

{ftr}

  <script src="{pre}assets/js/site.js"></script>
</body>
</html>
"""
    if fr:
        out = re.sub(r'(href|src)="assets/', r'\1="../assets/', out)
        out = out.replace('href="index.html"', 'href="index.html"')
    dest = site / ("fr" if fr else "") / name
    dest.parent.mkdir(exist_ok=True); dest.write_text(out); print("built", ("fr/" if fr else "") + name)

for p in sorted((S/"parts").glob("*.html")): page(p.name, p.read_text(), "en")
for p in sorted((S/"parts_fr").glob("*.html")): page(p.name, p.read_text(), "fr")
