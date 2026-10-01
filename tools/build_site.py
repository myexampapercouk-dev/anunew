import re, pathlib
src = pathlib.Path("stitch_faithful_layout_redesign")
out = pathlib.Path("site")
pages = {
 "pharma_corridor_global_intelligence_redesign": "index.html",
 "pharma_corridor_analysis_longread": "analysis.html",
 "pharma_corridor_india_deep_dive": "india.html",
 "pharma_corridor_united_states_deep_dive": "united-states.html",
 "pharma_corridor_europe_deep_dive": "europe.html",
 "pharma_corridor_china_deep_dive": "china.html",
 "pharma_corridor_live_industry_tracker": "tracker.html",
 "pharma_corridor_editorial_standards_mission": "about.html",
 "pharma_corridor_executive_briefing_subscriptions": "briefing.html",
}
paths = {
 "latest": "index.html", "analysis": "analysis.html",
 "corridors-india": "india.html", "corridors-united-states": "united-states.html",
 "corridors-europe": "europe.html", "corridors-china": "china.html",
 # no Rest of World screen was designed yet (MENA page is built by post_build.py)
 "corridors-mena": "mena.html", "corridors-rest-of-world": "index.html#corridors",
 "mission": "about.html#mission", "editorial-standards": "about.html#standards",
 "contribute": "about.html#contribute", "corrections": "about.html#corrections",
 "the-briefing": "briefing.html",
}
text_rules = [
 (r"^home$", "index.html"), (r"^corridors$", "index.html#corridors"),
 (r"back to latest analysis|all trade analyses", "analysis.html"),
 (r"intelligence subscriptions", "briefing.html"),
 (r"^tracker|full tracker|live tracker", "tracker.html"),
 (r"all analysis|read (the )?(full )?analysis", "analysis.html"),
 (r"explore india", "india.html"), (r"explore us|explore united states", "united-states.html"),
 (r"explore europe", "europe.html"), (r"explore china", "china.html"),
 (r"explore mena", "mena.html"), (r"explore global", "index.html#corridors"),
 (r"briefing|subscribe", "briefing.html"),
]
def fix(m):
    attrs, inner = m.group(1), m.group(2)
    if 'href="#"' not in attrs: return m.group(0)
    dp = re.search(r'data-path="([^"]+)"', attrs)
    target = paths.get(dp.group(1)) if dp else None
    if not target:
        text = re.sub(r"<[^>]+>", " ", inner)
        text = re.sub(r"\b(arrow_forward|expand_more|east)\b", "", text)
        text = " ".join(text.split()).lower()
        for pat, t in text_rules:
            if re.search(pat, text): target = t; break
    return m.group(0) if not target else f'<a{attrs.replace(chr(34)+"#"+chr(34), chr(34)+target+chr(34), 1)}>{inner}</a>'
for folder, name in pages.items():
    html = (src/folder/"code.html").read_text(encoding="utf-8")
    html = re.sub(r"<a\b([^>]*)>(.*?)</a>", fix, html, flags=re.S)
    if name == "index.html":
        html = html.replace("<!-- 5. Global 'Corridors' Interactive Hub Grid -->\n<section class=\"", "<!-- 5. Global 'Corridors' Interactive Hub Grid -->\n<section id=\"corridors\" class=\"", 1)
    (out/name).write_text(html, encoding="utf-8")
    print(name, html.count('href="#"'), "unlinked '#' left")

# --- Sitemap footer, shared by every page ---
LOGO = '<svg class="w-6 h-6 shrink-0" fill="none" viewBox="0 0 28 28" xmlns="http://www.w3.org/2000/svg"><rect fill="none" height="24" rx="1" stroke="#FFFFFF" stroke-width="1.75" width="24" x="2" y="2"></rect><path d="M8 7H14.5C17.5 7 19.5 8.7 19.5 11.5C19.5 14.3 17.5 16 14.5 16H8V7Z" stroke="#FFFFFF" stroke-linejoin="round" stroke-width="1.75"></path><path d="M14 16L20 22" stroke="#FFFFFF" stroke-linecap="round" stroke-width="1.75"></path><circle cx="14.5" cy="11.5" fill="#FFFFFF" r="1.25"></circle></svg>'
COLUMNS = [
 ("Coverage", [("Latest", "index.html"), ("Analysis", "analysis.html"), ("Live Industry Tracker", "tracker.html"), ("The Briefing", "briefing.html")]),
 ("Corridors", [("India", "india.html"), ("United States", "united-states.html"), ("Europe", "europe.html"), ("China", "china.html"), ("MENA", "mena.html"), ("Rest of World", "index.html#corridors")]),
 ("About", [("Mission", "about.html#mission"), ("Editorial Standards", "about.html#standards"), ("Contribute", "about.html#contribute"), ("Corrections", "about.html#corrections")]),
]
def footer(current):
    cols = ""
    for title, links in COLUMNS:
        items = ""
        for label, href in links:
            here = href == current
            cls = "text-on-navy-bright font-medium" if here else "text-on-navy-muted hover:text-on-navy-bright"
            aria = ' aria-current="page"' if here else ""
            items += f'<li><a class="font-body-dense text-body-dense {cls} transition-colors" href="{href}"{aria}>{label}</a></li>'
        cols += f'<div><h3 class="font-label-section text-label-section uppercase tracking-wider text-on-navy-bright mb-space-md">{title}</h3><ul class="space-y-space-sm">{items}</ul></div>'
    return f'''<footer class="w-full bg-navy-deep text-on-navy-bright border-t border-navy-soft"><div class="max-w-[1080px] mx-auto px-margin py-space-2xl"><div class="grid grid-cols-2 md:grid-cols-[1.4fr_1fr_1fr_1fr] gap-x-space-xl gap-y-space-xl pb-space-xl border-b border-navy-soft/60"><div class="col-span-2 md:col-span-1 space-y-space-md"><a class="flex items-center gap-space-sm" href="index.html">{LOGO}<span class="font-headline-card text-headline-card font-medium tracking-tight text-on-navy-bright">Pharma Corridor</span></a><p class="font-body-dense text-body-dense text-on-navy-muted max-w-xs">Authoritative biopharmaceutical intelligence, trade corridor flows, and cross-border regulatory analysis.</p><a class="inline-flex items-center gap-1 px-4 py-1.5 rounded-[999px] bg-bg-canvas text-navy-deep font-label-section text-label-section hover:bg-surface-panel transition-colors" href="briefing.html">Get The Briefing <span class="material-symbols-outlined text-[16px]">arrow_forward</span></a></div>{cols}</div><div class="pt-space-md flex flex-col sm:flex-row items-start sm:items-center justify-between gap-space-sm font-label-micro text-label-micro text-on-navy-muted tracking-wider"><p>Pharma Corridor · pharmacorridor.com</p><p class="text-on-navy-muted/80">© 2025 Global Pharmaceutical Intelligence Group. All rights reserved.</p></div></div></footer>'''
for name in pages.values():
    f = out/name
    html = f.read_text(encoding="utf-8")
    html, n = re.subn(r'<footer class="w-full bg-navy-deep.*?</footer>', lambda m: footer(name), html, count=1, flags=re.S)
    assert n == 1, name
    f.write_text(html, encoding="utf-8")
print("footers replaced")

# --- Mobile: hamburger menu + small-screen type and spacing ---
RESPONSIVE_CSS = """<style id="responsive-overrides">
@media (max-width: 639px) {
  .px-margin { padding-left: 1rem !important; padding-right: 1rem !important; }
  .text-display-hero { font-size: 38px !important; line-height: 42px !important; }
  .text-headline-lead { font-size: 34px !important; line-height: 38px !important; }
  .text-headline-section { font-size: 24px !important; line-height: 30px !important; }
  .text-headline-card { font-size: 20px !important; line-height: 26px !important; }
  .text-metric-large { font-size: 26px !important; line-height: 30px !important; }
  .text-body-lead { font-size: 18px !important; line-height: 28px !important; }
  .text-body-reading { font-size: 17px !important; line-height: 28px !important; }
  h1, h2, h3 { overflow-wrap: anywhere; }
}
html, body { overflow-x: hidden; }
img, svg, video { max-width: 100%; }
#mobile-menu a { -webkit-tap-highlight-color: transparent; }
</style>"""

MENU_JS = """<script>
(function () {
  var btn = document.getElementById('mobile-menu-btn'), menu = document.getElementById('mobile-menu');
  if (!btn || !menu) return;
  function set(open) {
    menu.classList.toggle('hidden', !open);
    btn.setAttribute('aria-expanded', open);
    btn.querySelector('span').textContent = open ? 'close' : 'menu';
    document.body.style.overflow = open ? 'hidden' : '';
  }
  btn.addEventListener('click', function () { set(menu.classList.contains('hidden')); });
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) set(false); });
  window.addEventListener('resize', function () { if (window.innerWidth >= 768) set(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
})();
</script>"""

MENU_BTN = '<button id="mobile-menu-btn" class="md:hidden w-10 h-10 -mr-2 flex items-center justify-center rounded-full text-navy-deep hover:bg-surface-panel transition-colors" type="button" aria-label="Open menu" aria-controls="mobile-menu" aria-expanded="false"><span class="material-symbols-outlined text-[24px]">menu</span></button>'

def mobile_menu(current):
    groups = ""
    for title, links in COLUMNS:
        items = ""
        for label, href in links:
            here = href == current
            cls = "text-navy-deep font-semibold bg-surface-panel" if here else "text-ink-primary hover:bg-surface-panel"
            aria = ' aria-current="page"' if here else ""
            items += f'<a class="flex items-center justify-between px-3 py-3 rounded-lg font-body-dense text-[16px] {cls} transition-colors" href="{href}"{aria}><span>{label}</span><span class="material-symbols-outlined text-[18px] text-ink-faint">chevron_right</span></a>'
        groups += f'<div class="py-space-md border-b border-line-hairline last:border-0"><p class="px-3 pb-2 font-label-section text-label-section uppercase tracking-wider text-ink-faint">{title}</p>{items}</div>'
    return (f'<div id="mobile-menu" class="hidden md:hidden border-t border-line-hairline bg-bg-canvas h-[calc(100dvh-4rem)] overflow-y-auto overscroll-contain">'
            f'<nav class="max-w-[1080px] mx-auto px-margin pb-space-xl" aria-label="Mobile">{groups}'
            f'<a class="mt-space-md flex items-center justify-center gap-1 w-full py-3 rounded-[999px] bg-navy-deep text-on-navy-bright font-label-section text-label-section" href="briefing.html">Get The Briefing <span class="material-symbols-outlined text-[16px]">arrow_forward</span></a></nav></div>')

for name in pages.values():
    f = out/name
    html = f.read_text(encoding="utf-8")
    m = re.search(r'<header class="fixed.*?</header>', html, re.S)
    assert m, name
    head = m.group(0)
    # hamburger goes after the avatar, inside the right-hand group; the panel drops below the bar
    assert head.endswith("</div></div></header>"), name
    head = head[:-len("</div></div></header>")] + MENU_BTN + "</div></div>" + mobile_menu(name) + "</header>"
    html = html[:m.start()] + head + html[m.end():]
    html = html.replace("</head>", RESPONSIVE_CSS + "</head>", 1)
    html = html.replace("</body>", MENU_JS + "</body>", 1)
    f.write_text(html, encoding="utf-8")
print("mobile menu added")

# --- Scroll fix, remove "Latest", split About into separate pages ---
import runpy
runpy.run_path(str(pathlib.Path(__file__).with_name("post_build.py")), run_name="__main__")
