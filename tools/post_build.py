"""Post-build fixes for site/ (safe to re-run; build_site.py calls it at the end).

1. Scrolling: `html, body { overflow-x: hidden }` turned <body> into its own scroll
   container, so the page would not scroll. Only the root element clips horizontal
   overflow now, and the mobile-menu scroll lock targets <html>.
2. Shows scrollbars again (the Stitch screens hid them).
3. About: removes the sticky jump bar and adds "Corrections" to the desktop About
   dropdown; About stays a single page.
4. Adds page titles, then builds the inner pages (tools/inner_pages.py).
"""
import re, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
PAGES = ["index", "article-tariff", "india", "united-states", "europe", "china",
         "tracker", "about"]
TITLES = {"index": "Pharma Corridor", "article-tariff": "The tariff wall goes up this week",
          "india": "India Corridor", "united-states": "United States Corridor",
          "europe": "Europe Corridor", "china": "China Corridor", "tracker": "Live Industry Tracker",
          "about": "About"}

def read(p): return p.read_text(encoding="utf-8")

def common_fixes(html):
    html = html.replace("html, body { overflow-x: hidden; }",
                        "html { overflow-x: hidden; }\r\nbody { overflow-x: clip; }")
    html = html.replace("document.body.style.overflow = open ? 'hidden' : '';",
                        "document.documentElement.style.overflow = open ? 'hidden' : '';")
    html = html.replace("::-webkit-scrollbar{display:none;}", "")
    # About: drop the sticky "01. Mission ... AUDIT GRADE" jump bar under the header
    html = re.sub(r'<!-- Interactive Jump Anchor System -->\s*<div class="sticky top-16.*?</div>\s*</div>\s*</div>\s*(?=<div class="max-w-\[1080px\] mx-auto px-margin w-full)',
                  "", html, count=1, flags=re.S)
    if 'data-path="corrections"' not in html:
        m = re.search(r'(<a class="([^"]*)" data-path="contribute" href="about.html#contribute">Contribute</a>)', html)
        if m:
            html = html.replace(m.group(1), m.group(1) +
                f'<a class="{m.group(2)}" data-path="corrections" href="about.html#corrections">Corrections</a>', 1)
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

def add_title(html, key):
    if "<title" in html: return html
    t = TITLES[key] if key == "index" else f"{TITLES[key]} | Pharma Corridor"
    return html.replace("<head>", f"<head><title>{t}</title>", 1)

def main():
    for p in PAGES:
        f = SITE / f"{p}.html"
        f.write_text(add_title(common_fixes(read(f)), p), encoding="utf-8")
    import inner_pages
    inner_pages.main()

if __name__ == "__main__":
    main()
    print("post_build done")
