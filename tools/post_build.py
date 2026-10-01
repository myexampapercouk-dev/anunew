"""Post-build fixes for site/ (safe to re-run; build_site.py calls it at the end).

1. Scrolling: `html, body { overflow-x: hidden }` turned <body> into its own scroll
   container (and broke the sticky bar), so the page would not scroll. Only the root
   element clips horizontal overflow now, and the mobile-menu scroll lock targets <html>.
2. Removes "Latest" from the header menu, the mobile menu and the footer.
3. Splits the About page into one page per About sub-menu item:
   mission.html, editorial-standards.html, contribute.html, corrections.html
4. Creates mena.html (content in tools/mena_page.py) and points every MENA link at it.
"""
import re, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
PAGES = ["index", "analysis", "india", "united-states", "europe", "china",
         "tracker", "briefing", "about"]
NEW = {  # file -> (section ids to keep, breadcrumb label, eyebrow, h1, lead)
    "mission.html": (["mission"], "Mission", "Our Mission", "Mission",
        "Why Pharma Corridor exists, who it serves, and the principles behind every corridor we cover."),
    "editorial-standards.html": (["standards", "methodology"], "Editorial Standards", "Charter of Global Editorial Protocol",
        "Editorial Standards",
        "How we keep our reporting independent, and how every data point is sourced and verified before it is published."),
    "contribute.html": (["contribute"], "Contribute", "Field Submissions & Commissions", "Contribute",
        "How to pitch, submit and be commissioned for analysis from the Corridor Desk."),
    "corrections.html": (["corrections"], "Corrections", "Public Accountability", "Corrections",
        "Our public ledger of corrections and clarifications."),
}
ABOUT_LINKS = {"about.html#mission": "mission.html", "about.html#standards": "editorial-standards.html",
               "about.html#contribute": "contribute.html", "about.html#corrections": "corrections.html"}
ABOUT_TABS = [("mission.html", "01. Mission"), ("editorial-standards.html", "02. Editorial Standards"),
              ("contribute.html", "03. Contribute"), ("corrections.html", "04. Corrections")]

def read(p): return p.read_text(encoding="utf-8")

def common_fixes(html):
    # 1. scroll fix
    html = html.replace("html, body { overflow-x: hidden; }",
                        "html { overflow-x: hidden; }\r\nbody { overflow-x: clip; }")
    html = html.replace("document.body.style.overflow = open ? 'hidden' : '';",
                        "document.documentElement.style.overflow = open ? 'hidden' : '';")
    # 2. remove "Latest" (header, mobile menu, footer)
    html = re.sub(r'<a [^>]*data-path="latest"[^>]*>Latest</a>', "", html)
    html = re.sub(r'<a [^>]*><span>Latest</span><span[^>]*>chevron_right</span></a>', "", html)
    html = re.sub(r'<li><a [^>]*>Latest</a></li>', "", html)
    # 3. About links -> separate pages
    for old, new in ABOUT_LINKS.items():
        html = html.replace(f'href="{old}"', f'href="{new}"')
    # 4. MENA -> its own page (header dropdown, mobile menu, footer, homepage card)
    html = html.replace('data-path="corridors-mena" href="index.html#corridors"', 'data-path="corridors-mena" href="mena.html"')
    html = html.replace('href="index.html#corridors"><span>MENA</span>', 'href="mena.html"><span>MENA</span>')
    html = html.replace('href="index.html#corridors">MENA</a>', 'href="mena.html">MENA</a>')
    html = html.replace('<!-- Corridor 5: MENA -->\n<a class="flex flex-col justify-between p-space-lg bg-surface-panel rounded-lg hover:bg-surface-variant transition-colors group" href="index.html#corridors">',
                        '<!-- Corridor 5: MENA -->\n<a class="flex flex-col justify-between p-space-lg bg-surface-panel rounded-lg hover:bg-surface-variant transition-colors group" href="mena.html">')
    # Corrections was missing from the desktop About dropdown
    if 'data-path="corrections"' not in html:
        m = re.search(r'(<a class="([^"]*)" data-path="contribute" href="contribute.html">Contribute</a>)', html)
        if m:
            html = html.replace(m.group(1), m.group(1) +
                f'<a class="{m.group(2)}" data-path="corrections" href="corrections.html">Corrections</a>', 1)
    return html

def mark_current(html, fname):
    """Highlight the current page in the mobile menu and footer."""
    def mob(m):
        a = m.group(0)
        if f'href="{fname}"' not in a or "aria-current" in a: return a
        a = a.replace("text-ink-primary hover:bg-surface-panel", "text-navy-deep font-semibold bg-surface-panel")
        return a.replace(f'href="{fname}"', f'href="{fname}" aria-current="page"', 1)
    html = re.sub(r'<a class="flex items-center justify-between[^>]*>', mob, html)
    def foot(m):
        a = m.group(0)
        if f'href="{fname}"' not in a or "aria-current" in a: return a
        a = a.replace("text-on-navy-muted hover:text-on-navy-bright", "text-on-navy-bright font-medium")
        return a.replace(f'href="{fname}"', f'href="{fname}" aria-current="page"', 1)
    return re.sub(r'<a class="font-body-dense text-body-dense text-on-navy[^>]*>', foot, html)

def unmark_current(html):
    """Strip the 'current page' highlight so a copied shell can be re-marked for another page."""
    html = html.replace("text-navy-deep font-semibold bg-surface-panel transition-colors\" href=", "text-ink-primary hover:bg-surface-panel transition-colors\" href=")
    html = html.replace("text-on-navy-bright font-medium transition-colors\" href=", "text-on-navy-muted hover:text-on-navy-bright transition-colors\" href=")
    return html.replace(' aria-current="page"', "")

def make_mena():
    """mena.html = Europe page shell (head, header, footer, scripts) + MENA main content."""
    import mena_page
    html = unmark_current(read(SITE / "europe.html"))
    i, j = html.find("<main"), html.find("</main>") + len("</main>")
    assert i > 0 and j > i, "europe.html shell not found"
    html = html[:i] + mena_page.build_main() + html[j:]
    html = re.sub(r"<title>.*?</title>", "", html, count=1, flags=re.S)
    html = add_title(html, "mena")
    html = mark_current(html, "mena.html")
    (SITE / "mena.html").write_text(html, encoding="utf-8")
    print("wrote mena.html")

def tabs(current):
    on = "px-3.5 py-1.5 rounded-full bg-navy-deep text-on-navy-bright font-label-section text-label-section tracking-wide transition-all shadow-sm hover:bg-navy-soft"
    off = "px-3.5 py-1.5 rounded-full bg-surface-container text-ink-muted font-label-section text-label-section hover:bg-surface-variant hover:text-navy-deep transition-all"
    links = "\n".join(
        f'<a class="{on if h == current else off}" href="{h}"' + (' aria-current="page"' if h == current else "") + f'>{t}</a>'
        for h, t in ABOUT_TABS)
    return f'<div class="flex items-center gap-1.5 shrink-0">\n{links}\n</div>'

def split_about(about_html):
    i, j = about_html.find("<main"), about_html.find("</main>")
    head, main, tail = about_html[:i], about_html[i:j], about_html[j:]
    secs = {m.group(1): m.start() for m in re.finditer(r'<section class="py-12 scroll-mt-28" id="([^"]+)">', main)}
    order = sorted(secs.items(), key=lambda kv: kv[1])
    ends = {}
    for n, (sid, start) in enumerate(order):
        nxt = order[n + 1][1] if n + 1 < len(order) else main.find('<section class="mt-8 p-6')
        ends[sid] = main[start:nxt]
    contact_start = main.find('<section class="mt-8 p-6')
    contact_end = main.rfind("</div>\n</div>")
    contact = main[contact_start:contact_end]
    # intro = everything before the first section, split into tab bar / page header
    intro = main[:order[0][1]]
    bar_a = intro.find('<div class="flex items-center gap-1.5 shrink-0">')
    bar_b = intro.find('<div class="hidden lg:flex')
    for fname, (keep, crumb, eyebrow, h1, lead) in NEW.items():
        pi = intro[:bar_a] + tabs(fname) + "\n" + intro[bar_b:]
        pi = pi.replace('<span class="text-navy-deep font-medium">Institutional Mission &amp; Standards</span>',
                        '<a class="hover:text-navy-deep transition-colors" href="mission.html">About</a>'
                        '<span class="text-ink-faint">/</span>'
                        f'<span class="text-navy-deep font-medium">{crumb}</span>', 1)
        pi = pi.replace("Charter of Global Editorial Protocol", eyebrow.replace("&", "&amp;"), 1)
        pi = pi.replace("Editorial Standards &amp; Institutional Mission", h1, 1)
        pi = re.sub(r'(<p class="font-body-lead[^>]*>)\s*.*?\s*(</p>)', lambda m: m.group(1) + lead + m.group(2), pi, count=1, flags=re.S)
        if fname != "mission.html":  # keep the trust-signifier tiles on Mission only
            pi = re.sub(r'<!-- Quick Trust Signifiers Bar -->.*?</div>\n</div>\n(?=</header>)', "", pi, count=1, flags=re.S)
        body = "".join(ends[k] for k in keep)
        page_main = pi + body + contact + "</div>\n</div>\n"
        page = head + page_main + tail
        # page <title>
        page = re.sub(r"<title>.*?</title>", "", page, count=1, flags=re.S)
        page = add_title(page, fname[:-5])
        page = mark_current(common_fixes(page), fname)
        (SITE / fname).write_text(page, encoding="utf-8")
        print("wrote", fname)

TITLES = {"index": "Pharma Corridor", "analysis": "Analysis", "india": "India Corridor", "united-states": "United States Corridor",
          "europe": "Europe Corridor", "china": "China Corridor", "tracker": "Live Industry Tracker",
          "briefing": "The Briefing", "about": "About", "mena": "MENA Corridor", "mission": "Mission",
          "editorial-standards": "Editorial Standards", "contribute": "Contribute", "corrections": "Corrections"}

def add_title(html, key):
    if "<title" in html: return html
    t = TITLES[key] if key == "index" else f"{TITLES[key]} | Pharma Corridor"
    return html.replace("<head>", f"<head><title>{t}</title>", 1)

def main():
    for p in PAGES:
        f = SITE / f"{p}.html"
        f.write_text(add_title(common_fixes(read(f)), p), encoding="utf-8")
    about = read(SITE / "about.html")
    split_about(about)
    make_mena()

if __name__ == "__main__":
    main()
    print("post_build done")
