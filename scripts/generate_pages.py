#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère publications.html et talks.html (format AcademicPages) à partir de own-bib.bib.

Usage :  python3 generate_pages.py own-bib.bib
Produit : _pages/publications.html et _pages/talks.html (ici : ./output/)

Classification par le champ `hceres` :
  os                  -> monographies (IGNORÉES : bloc statique conservé tel quel)
  do                  -> Edited Works
  acl                 -> Journal Articles
  cos                 -> Book Chapters
  C-INV, C-COM,
  C-ACTI, C-ACTN      -> Conference Presentations & Invited Talks
  pv (howpublished in PUBLIC_ENGAGEMENT_KINDS ou clé dans EXTRA_PUBLIC_KEYS)
                      -> Public Engagement
  RE, autres pv, PV   -> ignorés

Entrées dont le titre contient [Accepté] : ignorées (à paraître).
Liens : champ `doi` prioritaire, sinon `url`.
Champ optionnel `video = {https://...}` sur un talk -> lien "▶ video" dans la note.
"""

import re
import sys
import html
from pathlib import Path

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

PUBLIC_ENGAGEMENT_KINDS = {
    "Conférence", "Workshop", "Présentation du livre", "Présentation orale",
}
# Clés d'entrées pv à inclure dans Public Engagement malgré un howpublished
# hors liste (ex. le débat sur le pape François, encodé comme Interview) :
EXTRA_PUBLIC_KEYS = {"Feneuilpape2014"}

TALK_HCERES = {"C-INV", "C-COM", "C-ACTI", "C-ACTN"}

MEDIA_RADIO_KINDS = {"Émission de radio", "Émission de télévision", "Podcast"}
MEDIA_PRESS_KINDS = {"Interview", "Article", "Tribune", "Interviews, articles"}

SKIP_TITLE_MARKERS = ("[Accepté]", "[A paraître]", "[À paraître]", "[Sous presse]")

# ----------------------------------------------------------------------------
# Parseur BibTeX minimal (gère les accolades imbriquées)
# ----------------------------------------------------------------------------

def parse_bib(text):
    entries = []
    i = 0
    n = len(text)
    while i < n:
        at = text.find("@", i)
        if at == -1:
            break
        # ignorer les @ dans les commentaires de ligne (%)
        line_start = text.rfind("\n", 0, at) + 1
        if text[line_start:at].lstrip().startswith("%"):
            i = at + 1
            continue
        m = re.match(r"@(\w+)\s*\{", text[at:])
        if not m:
            i = at + 1
            continue
        typ = m.group(1).lower()
        j = at + m.end()  # après '{'
        # clé
        comma = text.find(",", j)
        key = text[j:comma].strip()
        # corps : lire jusqu'à l'accolade fermante correspondante
        depth = 1
        k = comma + 1
        while k < n and depth > 0:
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
            k += 1
        body = text[comma + 1 : k - 1]
        entries.append({"type": typ, "key": key,
                        "fields": parse_fields(body), "order": len(entries)})
        i = k
    return entries


def parse_fields(body):
    fields = {}
    i = 0
    n = len(body)
    while i < n:
        m = re.compile(r"\s*([A-Za-z]+)\s*=\s*").match(body, i)
        if not m:
            i += 1
            continue
        name = m.group(1).lower()
        i = m.end()
        if i < n and body[i] == "{":
            depth = 1
            j = i + 1
            while j < n and depth > 0:
                if body[j] == "{":
                    depth += 1
                elif body[j] == "}":
                    depth -= 1
                j += 1
            value = body[i + 1 : j - 1]
            i = j
        elif i < n and body[i] == '"':
            j = body.find('"', i + 1)
            value = body[i + 1 : j]
            i = j + 1
        else:
            m2 = re.compile(r"[^,]*").match(body, i)
            value = m2.group(0)
            i = m2.end()
        fields[name] = value.strip()
        comma = body.find(",", i)
        i = n if comma == -1 else comma + 1
    return fields

# ----------------------------------------------------------------------------
# LaTeX -> HTML
# ----------------------------------------------------------------------------

def latex_to_html(s):
    if not s:
        return ""
    s = s.replace("\\normalfont", "")
    # \href{url}{texte} -> <a>
    def _href(m):
        return f'<a href="{html.escape(m.group(1), quote=True)}">{m.group(2)}</a>'
    s = re.sub(r"\\href\{([^}]*)\}\{([^}]*)\}", _href, s)
    s = re.sub(r"\\(?:textit|emph)\{([^}]*)\}", r"<em>\1</em>", s)
    s = s.replace("\\\\", " ")
    s = s.replace("\\&", "&amp;").replace("\\%", "%").replace("\\_", "_")
    s = s.replace("~", "\u00a0")          # espace insécable
    s = s.replace("\\,", "\u202f")
    s = re.sub(r"\{([^{}]*)\}", r"\1", s)  # accolades de protection {Aaron}
    s = re.sub(r"\{([^{}]*)\}", r"\1", s)  # deuxième passe (imbrication)
    s = re.sub(r"\[([A-ZÀ-Þ])\]", r"\1", s)  # crochets de protection [C]oncile
    s = re.sub(r"\s+", " ", s).strip()
    # tirets de pages
    s = s.replace("--", "\u2013")
    return s


def clean_pages(p):
    if not p or "?" in p:
        return ""
    return re.sub(r"\s*[-–]+\s*", "\u2013", p.strip())


def extract_year(y):
    m = re.search(r"(\d{4})", y or "")
    return int(m.group(1)) if m else 0

# ----------------------------------------------------------------------------
# Noms
# ----------------------------------------------------------------------------

def split_names(field):
    return [n.strip() for n in re.split(r"\s+and\s+", field or "") if n.strip()]


def is_feneuil(name):
    return "feneuil" in name.lower()


def name_full(name):
    """'Feneuil, Anthony' -> 'Feneuil, Anthony' ; 'Albert Piette' -> 'Piette, Albert'."""
    if "," in name:
        return name
    parts = name.split()
    return f"{parts[-1]}, {' '.join(parts[:-1])}" if len(parts) > 1 else name


def name_abbrev(name):
    """'Bouriau, Christophe' -> 'Bouriau, C.' ; 'Askani, Hans-Christoph' -> 'Askani, H.-C.'
    Les particules minuscules (de, du, van...) sont conservées telles quelles."""
    full = name_full(name)
    if "," not in full:
        return full
    last, first = [p.strip() for p in full.split(",", 1)]
    out = []
    for token, sep in re.findall(r"([^\s-]+)([\s-]*)", first):
        if token[0].islower():
            out.append(token + (" " if sep else ""))
        else:
            out.append(token[0] + "." + ("-" if sep.strip() == "-" else " " if sep else ""))
    return f"{last}, {''.join(out).strip()}"


def join_et(names):
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " et " + names[-1]

# ----------------------------------------------------------------------------
# Blocs HTML
# ----------------------------------------------------------------------------

def link_for(f):
    doi = (f.get("doi") or "").strip()
    url = (f.get("url") or "").strip()
    if doi:
        return doi if doi.startswith("http") else "https://doi.org/" + doi
    return url or ""


def title_html(f, quotes=False):
    t = latex_to_html(f.get("title", ""))
    sub = latex_to_html(f.get("subtitle", ""))
    if sub:
        t = f"{t}\u00a0: {sub}"
    if quotes:
        t = f"«\u00a0{t}\u00a0»"
    return t


def translation_span(f, css="pub-translation"):
    tr = latex_to_html(f.get("engtransl", ""))
    return f'<span class="{css}">{tr}</span>' if tr else ""


def pub_entry(year, body):
    return (f'<div class="pub-entry"><div class="pub-year">{year}</div>'
            f'<div class="pub-body">{body}</div></div>')


def talk_entry(year, body):
    return (f'<div class="talk-entry"><div class="talk-year">{year}</div>'
            f'<div class="talk-body">{body}</div></div>')


def wrap_link(text, url):
    return f'<a href="{html.escape(url, quote=True)}">{text}</a>' if url else text


def fmt_edited_work(e):
    f = e["fields"]
    t = f"<em>{title_html(f)}</em>"
    t = wrap_link(t, link_for(f))
    parts = [t]
    others = [name_full(n) for n in split_names(f.get("editor")) if not is_feneuil(n)]
    if others:
        parts.append(f". Dir. avec {join_et(others)}")
    series = latex_to_html(f.get("series", ""))
    if series:  # numéro de revue dirigé
        num = latex_to_html(f.get("number", ""))
        if "|" in num:  # forme "21|2024" -> "21(2024)"
            num = num.replace("|", "(") + ")"
        parts.append(f". <em>{series}</em> {num}".rstrip())
    else:
        pub = latex_to_html(f.get("publisher", ""))
        addr = latex_to_html(f.get("address", ""))
        if addr and pub:
            parts.append(f". {addr}: {pub}")
        elif pub:
            parts.append(f". {pub}")
    return pub_entry(extract_year(f.get("year")), "".join(parts) + translation_span(f))


def fmt_article(e):
    f = e["fields"]
    t = wrap_link(title_html(f, quotes=True), link_for(f))
    ref = f"<em>{latex_to_html(f.get('journal',''))}</em>"
    vol = latex_to_html(f.get("volume", ""))
    num = latex_to_html(f.get("number", ""))
    if vol and num:
        ref += f" {vol}({num})"
    elif vol:
        ref += f" {vol}"
    elif num:
        ref += f" ({num})"
    pages = clean_pages(f.get("pages"))
    if pages:
        ref += f", {pages}"
    return pub_entry(extract_year(f.get("year")), f"{t}. {ref}" + translation_span(f))


def fmt_chapter(e):
    f = e["fields"]
    t = wrap_link(title_html(f, quotes=True), link_for(f))
    book = f"<em>{latex_to_html(f.get('booktitle',''))}</em>"
    eds = split_names(f.get("editor"))
    ed_str = ""
    if eds:
        if len(eds) > 3:
            ed_str = f", dir. {name_abbrev(eds[0])} et al."
        else:
            ed_str = f", dir. {join_et([name_abbrev(n) for n in eds])}"
    pub = latex_to_html(f.get("publisher", ""))
    addr = latex_to_html(f.get("address", ""))
    place = f"{addr}: {pub}" if addr and pub else (pub or addr)
    pages = clean_pages(f.get("pages"))
    tail = f". In {book}{ed_str}"
    if place:
        sep = " " if tail.rstrip().endswith(".") else ". "
        tail = tail.rstrip() + sep + place
    if pages:
        tail += f", {pages}"
    return pub_entry(extract_year(f.get("year")), t + tail + translation_span(f))


def fmt_talk(e):
    f = e["fields"]
    t = title_html(f, quotes=True)
    t = wrap_link(t, (f.get("url") or "").strip())
    if (f.get("howpublished") or "").strip().lower().startswith("round table"):
        t += " — round table"
    note = latex_to_html(f.get("note", ""))
    video = (f.get("video") or "").strip()
    if video:
        note += (f' — <a href="{html.escape(video, quote=True)}" '
                 f'class="talk-video-link">▶ video</a>')
    note_html = f'<span class="talk-note">{note}</span>' if note else ""
    return talk_entry(extract_year(f.get("year")), t + note_html)

def fmt_media(e):
    f = e["fields"]
    t = title_html(f, quotes=True)
    t = wrap_link(t, (f.get("url") or "").strip())
    note = latex_to_html(f.get("note", ""))
    note_html = f'<span class="med-note">{note}</span>' if note else ""
    return (f'<div class="med-entry"><div class="med-year">{extract_year(f.get("year"))}</div>'
            f'<div class="med-body">{t}{note_html}</div></div>')


# ----------------------------------------------------------------------------
# Sélection et tri
# ----------------------------------------------------------------------------

def skip_entry(e):
    title = e["fields"].get("title", "")
    return any(m in title for m in SKIP_TITLE_MARKERS)


def select(entries, pred):
    out = [e for e in entries if pred(e) and not skip_entry(e)]
    out.sort(key=lambda e: (-extract_year(e["fields"].get("year")), e["order"]))
    return out


def main():
    bib_path = sys.argv[1] if len(sys.argv) > 1 else "own-bib.bib"
    text = Path(bib_path).read_text(encoding="utf-8")
    entries = parse_bib(text)

    h = lambda e: (e["fields"].get("hceres") or "").strip()
    hp = lambda e: (e["fields"].get("howpublished") or "").strip()

    edited = select(entries, lambda e: h(e) == "do")
    articles = select(entries, lambda e: h(e) == "acl")
    chapters = select(entries, lambda e: h(e) == "cos")
    talks = select(entries, lambda e: h(e) in TALK_HCERES)
    public = select(entries, lambda e: h(e) == "pv" and (
        hp(e) in PUBLIC_ENGAGEMENT_KINDS or e["key"] in EXTRA_PUBLIC_KEYS))

    out = Path("output")
    out.mkdir(exist_ok=True)

    pubs_html = (
        PUB_HEADER
        + "\n\n".join(fmt_edited_work(e) for e in edited)
        + '\n\n<p class="pub-section-title">Journal Articles</p>\n\n'
        + "\n\n".join(fmt_article(e) for e in articles)
        + '\n\n<p class="pub-section-title">Book Chapters</p>\n\n'
        + "\n\n".join(fmt_chapter(e) for e in chapters)
        + PUB_FOOTER
    )
    (out / "publications.html").write_text(pubs_html, encoding="utf-8")

    talks_html = (
        TALK_HEADER
        + "\n\n".join(fmt_talk(e) for e in talks)
        + '\n\n<p class="talk-section-title">Public Engagement</p>\n\n'
        + "\n\n".join(fmt_talk(e) for e in public)
        + "\n\n</div>\n"
    )
    (out / "talks.html").write_text(talks_html, encoding="utf-8")

    radio = select(entries, lambda e: h(e) == "pv" and hp(e) in MEDIA_RADIO_KINDS
                   and e["key"] not in EXTRA_PUBLIC_KEYS)
    press = select(entries, lambda e: h(e) == "pv" and hp(e) in MEDIA_PRESS_KINDS
                   and e["key"] not in EXTRA_PUBLIC_KEYS)

    media_html = (
        MED_HEADER
        + "\n\n".join(fmt_media(e) for e in radio)
        + '\n\n<p class="med-section-title">Press Articles &amp; Interviews</p>\n\n'
        + "\n\n".join(fmt_media(e) for e in press)
        + "\n\n</div>\n"
    )
    (out / "media.html").write_text(media_html, encoding="utf-8")

    # --- Encart "publications récentes" pour la page d'accueil ---
    # Même structure HTML que le bloc next-events (classes event-date, etc.)
    RECENT_N = 4
    recent = sorted(edited + articles + chapters,
                    key=lambda e: (-extract_year(e["fields"].get("year")), e["order"]))[:RECENT_N]
    items = []
    for e in recent:
        f = e["fields"]
        year = extract_year(f.get("year"))
        url = link_for(f)
        label = title_html(f)  # titre original uniquement, pas de traduction
        if url:
            label = f'<a href="{html.escape(url, quote=True)}">{label}</a>'
        hh = h(e)
        if hh == "acl":
            venue = f"<em>{latex_to_html(f.get('journal',''))}</em>"
        elif hh == "cos":
            venue = f"in <em>{latex_to_html(f.get('booktitle',''))}</em>"
        else:
            venue = latex_to_html(f.get("publisher", "") or f.get("series", ""))
        items.append(
            '    <li>\n'
            f'      <span class="event-date">{year}</span>\n'
            '      <span class="event-desc">\n'
            f'        {label}\n'
            f'        <span class="event-location">{venue}</span>\n'
            '      </span>\n'
            '    </li>')
    recent_html = (
        '<div class="next-events recent-pubs">\n'
        '  <h2>{% if page.lang == "fr" %}Publications récentes'
        '{% else %}Recent Publications{% endif %}</h2>\n'
        '  <ul>\n' + "\n".join(items) + "\n  </ul>\n</div>\n")
    (out / "recent-pubs.html").write_text(recent_html, encoding="utf-8")

    print(f"Edited Works: {len(edited)} | Articles: {len(articles)} | "
          f"Chapters: {len(chapters)} | Talks: {len(talks)} | Public: {len(public)} | "
          f"Media: {len(radio)} radio+TV, {len(press)} presse")


# ----------------------------------------------------------------------------
# Gabarits statiques (repris tels quels des pages actuelles)
# ----------------------------------------------------------------------------

PUB_HEADER = """---
layout: refonte
title: "Anthony Feneuil — Publications"
description: "Publications of Anthony Feneuil in philosophy and theology, including books, journal articles, and book chapters."
permalink: /publications/
lang: en
---

<style>
.pub-wrap{max-width:760px}
.pub-section-title{font-family:var(--disp);font-weight:700;font-size:1.15rem;color:var(--ink);margin:2.4rem 0 .5rem;padding-top:1.4rem;border-top:1px solid var(--line)}
.pub-section-title:first-child{margin-top:.4rem;border-top:none;padding-top:0}
.pub-entry{display:grid;grid-template-columns:1fr;gap:.15rem;padding:1rem 0;border-bottom:1px solid var(--line)}
.pub-year{font-weight:700;font-size:.72rem;letter-spacing:.1em;color:var(--pop);text-transform:uppercase}
.pub-body{font-size:1.02rem;line-height:1.4;color:var(--ink)}
.pub-body a{border-bottom:1.5px solid var(--line);transition:.15s}
.pub-body a:hover{border-color:var(--pop);color:var(--pop)}
.pub-body em{font-style:italic}
.pub-translation{display:block;margin-top:.25rem;color:var(--soft);font-size:.9rem;font-style:italic}
.pub-books{display:flex;flex-wrap:wrap;gap:1.4rem;margin:.6rem 0 1rem}
.pub-book{width:110px;text-align:center}
.pub-book img{width:100%;box-shadow:0 10px 22px -10px rgba(0,0,0,.4);margin-bottom:.5rem}
.pub-book-title{font-size:.78rem;line-height:1.35;font-style:italic;color:var(--ink)}
.pub-book-title a{color:var(--ink)}
.pub-book-editor{font-size:.7rem;color:var(--soft);margin-top:.15rem}
@media(min-width:720px){.pub-entry{grid-template-columns:auto 1fr;gap:.2rem 1.6rem;align-items:baseline}.pub-year{padding-top:.15rem}}
</style>

<div class="pub-wrap">
<div class="pagehead"><div class="eyebrow">Research</div><h2>Publications</h2></div>

<p class="pub-section-title">Monographs</p>
  <div class="pub-books">
  <div class="pub-book">
    <a href="https://www.laboretfides.com/product/un-lexique-theologique/"><img src="/images/images_livres/lexique.png" alt="Lexique de théologie"></a>
    <div class="pub-book-title"><a href="https://www.laboretfides.com/product/un-lexique-theologique/">Lexique de théologie</a></div>
    <div class="pub-book-editor">Labor et Fides</div>
  </div>
  <div class="pub-book">
    <a href="https://www.laboretfides.com/product/l-evidence-de-dieu/"><img src="/images/images_livres/evidence.png" alt="L'évidence de Dieu"></a>
    <div class="pub-book-title"><a href="https://www.laboretfides.com/product/l-evidence-de-dieu/">L'évidence de Dieu</a></div>
    <div class="pub-book-editor">Labor et Fides</div>
  </div>
  <div class="pub-book">
    <a href="https://www.cnrseditions.fr/catalogue/philosophie-et-histoire-des-idees/l-individu-impossible/"><img src="/images/images_livres/individu.png" alt="L'individu impossible"></a>
    <div class="pub-book-title"><a href="https://www.cnrseditions.fr/catalogue/philosophie-et-histoire-des-idees/l-individu-impossible/">L'individu impossible</a></div>
    <div class="pub-book-editor">CNRS Éditions</div>
  </div>
  <div class="pub-book">
    <a href="https://www.lagedhomme.com/ouvrages/anthony+feneuil/le+serpent+d%27aaron/4058"><img src="/images/images_livres/serpent.png" alt="Le serpent d'Aaron"></a>
    <div class="pub-book-title"><a href="https://www.lagedhomme.com/ouvrages/anthony+feneuil/le+serpent+d%27aaron/4058">Le serpent d'Aaron</a></div>
    <div class="pub-book-editor">L'Âge d'Homme</div>
  </div>
  <div class="pub-book">
    <a href="https://www.puf.com/bergson-mystique-et-philosophie"><img src="/images/images_livres/bergson.png" alt="Bergson, mystique et philosophie"></a>
    <div class="pub-book-title"><a href="https://www.puf.com/bergson-mystique-et-philosophie">Bergson, mystique et philosophie</a></div>
    <div class="pub-book-editor">PUF</div>
  </div>
</div>

<p class="pub-section-title">Edited Works</p>

"""

PUB_FOOTER = """

<p style="margin-top:2.4rem;padding-top:1.5rem;border-top:1px solid var(--line);font-size:.9rem;color:var(--soft)">Voir aussi : <a href="/rien-de-cache/" style="color:var(--pop);border-bottom:1px solid var(--line)"><em>Rien de caché</em></a> (Bayard, 2026) — récit littéraire</p>

</div>
"""

TALK_HEADER = """---
layout: refonte
title: "Anthony Feneuil — Talks"
description: "Oral presentations and public engagement by Anthony Feneuil, philosopher and theologian at the Université de Lorraine."
permalink: /talks/
lang: en
---

<style>
.talk-wrap{max-width:760px}
.talk-section-title{font-family:var(--disp);font-weight:700;font-size:1.15rem;color:var(--ink);margin:2.4rem 0 .5rem;padding-top:1.4rem;border-top:1px solid var(--line)}
.talk-section-title:first-of-type{margin-top:.4rem;border-top:none;padding-top:0}
.talk-entry{display:grid;grid-template-columns:1fr;gap:.15rem;padding:1rem 0;border-bottom:1px solid var(--line)}
.talk-year{font-weight:700;font-size:.72rem;letter-spacing:.1em;color:var(--pop);text-transform:uppercase}
.talk-body{font-size:1.02rem;line-height:1.4;color:var(--ink)}
.talk-body a{border-bottom:1.5px solid var(--line);transition:.15s}
.talk-body a:hover{border-color:var(--pop);color:var(--pop)}
.talk-body em{font-style:italic}
.talk-note{display:block;margin-top:.25rem;color:var(--soft);font-size:.9rem;font-style:italic}
.talk-video-link{font-style:normal;color:var(--pop);margin-left:.4rem;border-bottom:1px solid var(--line)}
.talk-video-link:hover{border-color:var(--pop)}
@media(min-width:720px){.talk-entry{grid-template-columns:auto 1fr;gap:.2rem 1.6rem;align-items:baseline}.talk-year{padding-top:.15rem}}
</style>

<div class="talk-wrap">
<div class="pagehead"><div class="eyebrow">Presentations</div><h2>Talks</h2></div>

<p class="talk-section-title">Conference Presentations &amp; Invited Talks</p>

"""

MED_HEADER = """---
layout: refonte
title: "Anthony Feneuil — Media"
description: "media and public interventions by Anthony Feneuil, theology and philosophy."
permalink: /media/
lang: en
---

<style>
.med-wrap{max-width:760px}
.med-rdc{color:var(--soft);font-size:1rem;margin-bottom:1.4rem;padding-bottom:1.2rem;border-bottom:1px solid var(--line)}
.med-rdc a{color:var(--pop);border-bottom:1px solid var(--line)}
.med-section-title{font-family:var(--disp);font-weight:700;font-size:1.15rem;color:var(--ink);margin:2.4rem 0 .5rem;padding-top:1.4rem;border-top:1px solid var(--line)}
.med-section-title:first-of-type{margin-top:.4rem;border-top:none;padding-top:0}
.med-entry{display:grid;grid-template-columns:1fr;gap:.15rem;padding:1rem 0;border-bottom:1px solid var(--line)}
.med-year{font-weight:700;font-size:.72rem;letter-spacing:.1em;color:var(--pop);text-transform:uppercase}
.med-body{font-size:1.02rem;line-height:1.4;color:var(--ink)}
.med-body a{border-bottom:1.5px solid var(--line);transition:.15s}
.med-body a:hover{border-color:var(--pop);color:var(--pop)}
.med-body em{font-style:italic}
.med-note{display:block;margin-top:.25rem;color:var(--soft);font-size:.9rem;font-style:italic}
@media(min-width:720px){.med-entry{grid-template-columns:auto 1fr;gap:.2rem 1.6rem;align-items:baseline}.med-year{padding-top:.15rem}}
</style>

<div class="med-wrap">
<div class="pagehead"><div class="eyebrow">Rien de caché</div><h2>Media</h2></div>

<p class="med-rdc">Presse et médias autour de <a href="/rien-de-cache/"><em>Rien de caché</em></a> (Bayard, 2026) — <a href="/rien-de-cache/">voir la page dédiée</a></p>

<p class="med-section-title">Radio, TV &amp; Podcasts</p>

"""

if __name__ == "__main__":
    main()
