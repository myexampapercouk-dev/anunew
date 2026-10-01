"""Inner pages from the original single-page site (the-pharma-corridor-site.html),
redrawn in the Stitch redesign's design language:

  analysis.html          Analysis listing with beat filters
  article-<id>.html      one longread page per article (article-tariff.html is the
                         Stitch-designed longread, so it is left as built)
  mena.html, rest-of-world.html   corridor pages
  404.html               not-found page (Netlify serves it for any missing URL)

Content comes from tools/spa_content.json (run tools/extract_spa.py to refresh it).
Called at the end of post_build.py; safe to re-run.
"""
import html as H, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from post_build import SITE, read, unmark_current, mark_current

DATA = json.loads((pathlib.Path(__file__).with_name("spa_content.json")).read_text(encoding="utf-8"))
ARTICLES, NEWS, CORRIDORS = DATA["articles"], DATA["news"], DATA["corridors"]
BEATS = ["Policy & Trade", "Manufacturing & Operations", "Quality & Regulatory", "Supply Chain & Sourcing", "Deals & Capacity"]
CORRIDOR_PAGE = {"India": "india.html", "United States": "united-states.html", "Europe": "europe.html",
                 "China": "china.html", "MENA": "mena.html", "Rest of World": "rest-of-world.html"}

def e(s): return H.escape(s, quote=False)
def article_href(a): return f"article-{a['id']}.html"

def write_page(fname, title, main, root_links=False):
    """Reuse europe.html's head/header/footer/scripts around new <main> content.
    root_links: make page links absolute (/x.html), for 404.html, which is served at any path."""
    page = unmark_current(read(SITE / "europe.html"))
    i, j = page.find("<main"), page.find("</main>") + len("</main>")
    page = page[:i] + main + page[j:]
    page = re.sub(r"<title>.*?</title>", f"<title>{e(title)} | Pharma Corridor</title>", page, count=1, flags=re.S)
    page = mark_current(page, fname)
    if root_links:
        page = re.sub(r'href="(?!https?:|mailto:|#|/)([^"]+)"', r'href="/\1"', page)
    (SITE / fname).write_text(page, encoding="utf-8")

def corridor_chips(cors, cls="px-2 py-0.5 rounded-[999px] bg-surface-panel text-ink-muted hover:text-navy-deep"):
    return "".join(f'<a class="{cls} font-label-micro text-label-micro uppercase font-medium transition-colors" href="{CORRIDOR_PAGE[c]}">{e(c)}</a>' for c in cors)

def crumb(*items):
    out = []
    for label, href in items:
        out.append(f'<a class="hover:text-navy-deep transition-colors" href="{href}">{e(label)}</a>' if href else f'<span class="text-navy-deep font-medium">{e(label)}</span>')
    return '<nav class="flex flex-wrap items-center gap-2 font-label-meta text-label-meta text-ink-faint">' + '<span class="text-line-subtle">/</span>'.join(out) + "</nav>"

def briefing_box():
    return ('<div class="bg-navy-deep rounded-xl p-space-lg text-on-navy-bright flex flex-col gap-space-sm">'
            '<span class="font-label-section text-label-section uppercase tracking-wider text-on-navy-muted">The Corridor Briefing</span>'
            '<p class="font-body-dense text-body-dense text-on-navy-muted">One read that matters, assembled for your corridor and function. Free, most weekday mornings.</p>'
            '<a class="self-start mt-1 inline-flex items-center gap-1 px-4 py-2 rounded-[999px] bg-bg-canvas text-navy-deep font-label-section text-label-section hover:bg-surface-panel transition-colors" href="index.html#briefing">Subscribe <span class="material-symbols-outlined text-[16px]">arrow_forward</span></a></div>')

# ---------------------------------------------------------------- articles
def article_main(a):
    others = [x for x in ARTICLES if x["id"] != a["id"]]
    nxt = ARTICLES[(ARTICLES.index(a) + 1) % len(ARTICLES)]
    paras = "".join(
        f'<p class="{"first-letter:float-left first-letter:font-medium first-letter:text-[64px] first-letter:leading-[56px] first-letter:mr-2 first-letter:text-navy-deep " if k == 0 else ""}">{e(p)}</p>'
        for k, p in enumerate(a["body"]))
    more = "".join(
        f'<a class="block py-space-md border-b border-line-hairline last:border-0 group" href="{article_href(o)}">'
        f'<span class="block font-label-micro text-label-micro uppercase text-navy-deep font-semibold mb-1">{e(o["beat"])}</span>'
        f'<span class="block font-body-dense text-body-dense text-ink-primary font-medium leading-snug group-hover:text-navy-soft transition-colors">{e(o["head"])}</span></a>'
        for o in others[:3])
    return f'''<main class="w-full pt-16 bg-bg-canvas"><div class="flex flex-col w-full">
<header class="w-full bg-surface-panel py-space-md"><div class="max-w-[1080px] mx-auto px-margin flex flex-wrap items-center justify-between gap-space-sm">
<a class="inline-flex items-center gap-space-xs text-navy-deep hover:text-navy-soft font-label-section text-label-section group" href="analysis.html"><span class="material-symbols-outlined text-[18px] transition-transform group-hover:-translate-x-0.5">arrow_left_alt</span><span>All analysis</span></a>
<div class="flex items-center gap-space-sm flex-wrap"><span class="px-2.5 py-0.5 rounded-full bg-surface-container-highest text-navy-deep font-label-micro text-label-micro font-semibold">Analysis · {e(a["beat"])}</span>{corridor_chips(a["corridors"])}</div>
</div></header>
<article class="w-full pb-space-3xl">
<div class="max-w-[1080px] mx-auto px-margin pt-space-xl"><div class="max-w-[840px]">
<h1 class="font-headline-lead text-headline-lead text-navy-deep tracking-tight text-balance mb-space-lg">{e(a["head"])}</h1>
<p class="font-body-lead text-body-lead text-ink-muted leading-relaxed mb-space-lg">{e(a["sf"])}</p>
<div class="bg-surface-panel p-space-md rounded-xl flex flex-wrap items-center gap-x-space-md gap-y-1 font-label-meta text-label-meta text-ink-muted">
<span class="text-navy-deep font-semibold">By {e(a["byline"])}</span><span class="text-ink-faint">·</span><span>Dateline {e(a["dateline"])}</span><span class="text-ink-faint">·</span><span class="inline-flex items-center gap-1"><span class="material-symbols-outlined text-[15px]">schedule</span>{e(a["read"])} read</span></div>
</div></div>
<div class="max-w-[1080px] mx-auto px-margin mt-space-2xl"><div class="grid grid-cols-1 lg:grid-cols-12 gap-space-2xl">
<div class="lg:col-span-8 font-body-reading text-body-reading text-ink-primary space-y-space-lg">{paras}
<div class="pt-space-lg border-t border-line-hairline flex flex-wrap items-center gap-space-sm"><span class="font-label-section text-label-section text-navy-deep font-semibold">{e(a["beat"])}</span>{corridor_chips(a["corridors"])}</div>
<a class="block mt-space-lg p-space-lg rounded-xl bg-surface-panel hover:bg-surface-variant transition-colors group" href="{article_href(nxt)}">
<span class="block font-label-section text-label-section uppercase tracking-wider text-ink-muted mb-1">Next analysis</span>
<span class="flex items-start justify-between gap-space-md"><span class="font-headline-card text-headline-card text-navy-deep">{e(nxt["head"])}</span><span class="material-symbols-outlined text-navy-deep group-hover:translate-x-1 transition-transform">arrow_forward</span></span></a>
</div>
<aside class="lg:col-span-4 flex flex-col gap-space-lg lg:sticky lg:top-24 self-start w-full">
<div class="bg-surface-panel rounded-xl p-space-lg"><h2 class="font-label-section text-label-section uppercase tracking-wider text-navy-deep font-semibold mb-1">More analysis</h2>{more}</div>
{briefing_box()}
</aside></div></div>
</article></div></main>'''

# ---------------------------------------------------------------- analysis listing
def listing_main():
    lead = next(a for a in ARTICLES if a.get("lead"))
    rows = "".join(
        f'<a class="analysis-row py-space-lg flex flex-col md:flex-row md:items-start justify-between gap-space-md group border-b border-line-hairline" data-beat="{e(a["beat"])}" href="{article_href(a)}">'
        f'<div class="flex-1 flex flex-col gap-space-xs"><div class="flex flex-wrap items-center gap-space-sm font-label-micro text-label-micro text-ink-faint uppercase font-medium"><span class="text-navy-deep font-semibold">{e(a["beat"])}</span><span>·</span><span class="text-ink-muted">{e(" · ".join(a["corridors"]))}</span></div>'
        f'<h3 class="font-headline-card text-headline-card text-ink-primary font-medium group-hover:text-navy-soft transition-colors leading-snug">{e(a["head"])}</h3>'
        f'<p class="font-body-dense text-body-dense text-ink-muted leading-relaxed">{e(a["sf"])}</p></div>'
        f'<div class="md:w-40 shrink-0 flex md:flex-col md:items-end gap-2 font-label-meta text-label-meta text-ink-faint"><span class="text-ink-primary font-medium">{e(a["dateline"])}</span><span class="inline-flex items-center gap-1"><span class="material-symbols-outlined text-[14px]">schedule</span>{e(a["read"])} read</span></div></a>'
        for a in ARTICLES if a is not lead)
    chip = "beat-chip px-3.5 py-1.5 rounded-full font-label-section text-label-section transition-colors whitespace-nowrap"
    chips = f'<button class="{chip} bg-navy-deep text-on-navy-bright" data-beat="" type="button">All</button>' + "".join(
        f'<button class="{chip} bg-surface-container text-ink-muted hover:text-navy-deep" data-beat="{e(b)}" type="button">{e(b)}</button>' for b in BEATS)
    return f'''<main class="w-full pt-16 bg-bg-canvas"><div class="max-w-[1080px] w-full mx-auto px-margin py-space-xl flex flex-col gap-space-xl">
<div class="flex flex-col gap-space-md">{crumb(("Home", "index.html"), ("Analysis", None))}
<h1 class="font-headline-lead text-headline-lead text-navy-deep tracking-tight">Analysis</h1>
<p class="font-body-lead text-body-lead text-ink-muted max-w-[60ch]">Long-form, bylined corridor analysis, the premium read.</p></div>
<a class="analysis-row grid grid-cols-1 lg:grid-cols-[1.4fr_0.6fr] gap-space-xl p-space-xl bg-surface-panel rounded-xl hover:bg-surface-variant transition-colors group" data-beat="{e(lead["beat"])}" href="{article_href(lead)}">
<div class="flex flex-col gap-space-md"><span class="self-start px-2.5 py-1 rounded-[999px] bg-navy-deep text-on-navy-bright font-label-micro text-label-micro uppercase font-semibold tracking-wider">Lead analysis · {e(lead["beat"])}</span>
<h2 class="font-headline-section text-headline-section sm:text-[36px] sm:leading-[42px] text-navy-deep font-normal tracking-tight group-hover:text-navy-soft transition-colors">{e(lead["head"])}</h2>
<p class="font-body-dense text-body-dense text-ink-muted leading-relaxed">{e(lead["sf"])}</p></div>
<div class="flex lg:flex-col lg:items-end lg:justify-end gap-space-sm font-label-meta text-label-meta text-ink-muted"><span class="text-navy-deep font-semibold">{e(lead["byline"])}</span><span>{e(lead["dateline"])} · {e(lead["read"])} read</span><span class="hidden lg:inline-flex items-center gap-1 text-navy-deep font-semibold mt-space-md">Read the analysis <span class="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span></span></div></a>
<div class="flex flex-col gap-space-md"><div class="flex items-center justify-between pb-space-sm border-b border-line-hairline"><h2 class="font-label-section text-label-section uppercase tracking-wider text-navy-deep font-semibold">All analysis</h2><span id="analysis-count" class="font-label-meta text-label-meta text-ink-faint"></span></div>
<div class="flex items-center gap-space-xs overflow-x-auto pb-1">{chips}</div>
<div id="analysis-list" class="flex flex-col">{rows}</div>
<p id="analysis-empty" class="hidden py-space-xl font-body-dense text-body-dense text-ink-muted">No analysis on this beat yet. The wire tracks it in the <a class="text-navy-deep underline" href="tracker.html">Live Industry Tracker</a>.</p></div>
</div>
<script>
(function () {{
  var chips = document.querySelectorAll('.beat-chip'), rows = document.querySelectorAll('.analysis-row');
  function show(beat) {{
    var n = 0;
    rows.forEach(function (r) {{ var on = !beat || r.dataset.beat === beat; r.classList.toggle('hidden', !on); if (on) n++; }});
    chips.forEach(function (c) {{
      var on = c.dataset.beat === beat;
      c.classList.toggle('bg-navy-deep', on); c.classList.toggle('text-on-navy-bright', on);
      c.classList.toggle('bg-surface-container', !on); c.classList.toggle('text-ink-muted', !on);
    }});
    document.getElementById('analysis-count').textContent = n + (n === 1 ? ' piece' : ' pieces');
    document.getElementById('analysis-empty').classList.toggle('hidden', n > 0);
  }}
  chips.forEach(function (c) {{ c.addEventListener('click', function () {{ show(c.dataset.beat); }}); }});
  show('');
}})();
</script></main>'''

# ---------------------------------------------------------------- MENA / Rest of World
def corridor_main(name):
    ROW = CORRIDORS[name]
    numbers = "".join(
        f'<div class="bg-navy-deep p-space-lg flex flex-col gap-2"><span class="font-metric-large text-metric-large text-on-navy-bright">{e(n["big"])}</span>'
        f'<span class="font-body-dense text-body-dense text-on-navy-muted">{e(n["lbl"])}</span><span class="font-label-micro text-label-micro text-on-navy-muted/70">{e(n["src"])}</span></div>'
        for n in ROW["numbers"])
    hubs = "".join(
        f'<div class="p-space-lg rounded-xl {"bg-navy-deep text-on-navy-bright" if r.get("lead") else "bg-surface-panel"} flex flex-col gap-space-sm">'
        f'<div class="flex flex-wrap items-baseline justify-between gap-2"><h3 class="font-headline-card text-headline-card {"text-on-navy-bright" if r.get("lead") else "text-navy-deep"}">{e(r["name"])}</h3>'
        f'<span class="font-label-meta text-label-meta {"text-on-navy-muted" if r.get("lead") else "text-ink-muted"}">{e(r["val"])}</span></div>'
        + (f'<span class="self-start px-2 py-0.5 rounded-[999px] {"bg-navy-soft text-primary-fixed" if r.get("lead") else "bg-surface-container-high text-navy-deep"} font-label-micro text-label-micro uppercase font-semibold">{e(r["role"])}</span>' if r.get("role") else "")
        + (f'<p class="font-body-dense text-body-dense {"text-on-navy-muted" if r.get("lead") else "text-ink-muted"} leading-relaxed">{e(r["detail"])}</p>' if r.get("detail") else "")
        + "</div>"
        for r in ROW["hubs"]["rows"])
    def items(lst):
        return "".join(f'<div class="py-space-sm border-b border-line-hairline last:border-0"><div class="font-body-dense text-body-dense text-ink-primary font-semibold">{e(x["nm"])}</div><div class="font-label-meta text-label-meta text-ink-muted mt-0.5">{e(x["d"])}</div></div>' for x in lst)
    tone = {"risk": "text-amber-risk", "struct": "text-navy-deep"}
    profile = "".join(
        f'<div class="grid grid-cols-1 md:grid-cols-[200px_1fr] gap-1 md:gap-space-xl py-space-md border-b border-line-hairline">'
        f'<div class="font-label-section text-label-section uppercase tracking-wider {tone.get(p.get("cls"), "text-ink-faint")}">{e(p["k"])}</div>'
        f'<div class="font-body-reading text-[16.5px] leading-relaxed text-ink-primary [&_b]:font-semibold [&_b]:text-navy-deep">{p["v"]}</div></div>'
        for p in ROW["profile"])
    wire = [n for n in NEWS if name in n["corridors"]]
    wire_rows = "".join(
        f'<div class="grid grid-cols-[64px_1fr] gap-space-md py-space-md border-b border-line-hairline"><span class="font-label-meta text-label-meta text-ink-faint tabular-nums">{e(n["date"])}</span>'
        f'<div><div class="font-body-dense text-body-dense text-ink-primary font-medium">{e(n["head"])}</div><div class="font-label-micro text-label-micro text-ink-faint mt-1">{e(n["source"])} · {e(n["beat"])}</div></div></div>'
        for n in wire)
    arts = [a for a in ARTICLES if name in a["corridors"]]
    art_rows = "".join(
        f'<a class="block p-space-lg rounded-xl bg-surface-panel hover:bg-surface-variant transition-colors group" href="{article_href(a)}"><span class="block font-label-micro text-label-micro uppercase text-navy-deep font-semibold mb-1">Analysis · {e(a["beat"])}</span>'
        f'<span class="block font-headline-card text-headline-card text-ink-primary group-hover:text-navy-soft transition-colors">{e(a["head"])}</span><span class="block font-body-dense text-body-dense text-ink-muted mt-1">{e(a["sf"])}</span></a>'
        for a in arts)
    return f'''<main class="w-full pt-16 bg-bg-canvas"><div class="max-w-[1080px] w-full mx-auto px-margin py-space-xl flex flex-col gap-space-2xl">
<div class="flex flex-col gap-space-md">{crumb(("Home", "index.html"), ("Corridors", "index.html#corridors"), (name, None))}
<span class="font-label-section text-label-section uppercase tracking-wider text-ink-muted">Trade corridor intelligence deck</span>
<h1 class="font-headline-lead text-headline-lead text-navy-deep tracking-tight">{name}</h1>
<p class="font-body-lead text-body-lead text-ink-muted max-w-[62ch]">{e(ROW["stand"])}</p></div>
<section class="flex flex-col gap-space-md"><h2 class="font-label-section text-label-section uppercase tracking-wider text-navy-deep font-semibold">The region in numbers</h2>
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-px bg-navy-soft rounded-xl overflow-hidden">{numbers}</div></section>
<section class="flex flex-col gap-space-md"><div><span class="font-label-section text-label-section uppercase tracking-wider text-ink-muted">The hubs</span>
<h2 class="font-headline-section text-headline-section text-navy-deep">A corridor made of several, not one</h2></div>
<div class="grid grid-cols-1 md:grid-cols-2 gap-space-md">{hubs}</div>
<p class="font-label-micro text-label-micro text-ink-faint">{e(ROW["hubs"]["src"])}</p></section>
<section class="grid grid-cols-1 md:grid-cols-2 gap-space-md">
<div class="bg-surface-panel rounded-xl p-space-lg"><h2 class="font-label-section text-label-section uppercase tracking-wider text-navy-deep font-semibold mb-space-sm">Where it's made</h2>{items(ROW["madeIn"])}</div>
<div class="bg-surface-panel rounded-xl p-space-lg"><h2 class="font-label-section text-label-section uppercase tracking-wider text-navy-deep font-semibold mb-space-sm">{e(ROW["whoTitle"])}</h2>{items(ROW["who"])}</div></section>
<section class="border-t-2 border-navy-deep pt-space-md"><h2 class="font-label-section text-label-section uppercase tracking-wider text-navy-deep font-semibold mb-space-sm">How the corridor works</h2>{profile}</section>
<section class="grid grid-cols-1 lg:grid-cols-[1.2fr_0.8fr] gap-space-xl">
<div class="flex flex-col gap-space-md"><h2 class="font-headline-section text-headline-section text-navy-deep">Latest from the {name} corridor</h2>{art_rows}</div>
<div class="flex flex-col"><div class="flex items-center justify-between pb-space-sm border-b border-line-hairline"><h2 class="font-label-section text-label-section uppercase tracking-wider text-navy-deep font-semibold">From the tracker</h2><a class="font-label-section text-label-section text-navy-deep hover:text-navy-soft inline-flex items-center gap-1" href="tracker.html">Tracker <span class="material-symbols-outlined text-[16px]">arrow_forward</span></a></div>{wire_rows}</div></section>
<div class="p-space-lg bg-surface-panel rounded-xl font-label-meta text-label-meta text-ink-muted leading-relaxed"><span class="flex items-center gap-2 mb-2 text-navy-deep font-label-section text-label-section uppercase tracking-wider font-semibold"><span class="material-symbols-outlined text-[18px]">verified</span>Sources</span>{e(ROW["sources"])}</div>
</div></main>'''

# ---------------------------------------------------------------- Latest (the source site's tracker view)
def latest_main():
    chip = "beat-chip px-3.5 py-1.5 rounded-full font-label-section text-label-section transition-colors whitespace-nowrap"
    chips = f'<button class="{chip} bg-navy-deep text-on-navy-bright" data-beat="" type="button">All</button>' + "".join(
        f'<button class="{chip} bg-surface-container text-ink-muted hover:text-navy-deep" data-beat="{e(b)}" type="button">{e(b)}</button>' for b in BEATS)
    rows = "".join(
        f'<div class="analysis-row grid grid-cols-[56px_1fr] sm:grid-cols-[72px_1fr] gap-space-md py-space-md border-b border-line-hairline" data-beat="{e(n["beat"])}">'
        f'<span class="font-label-meta text-label-meta text-ink-faint tabular-nums pt-0.5">{e(n["date"])}</span>'
        f'<div><div class="font-headline-row text-headline-row text-ink-primary">{e(n["head"])}</div>'
        f'<div class="font-label-meta text-label-meta text-ink-faint mt-1">{e(n["source"])} · {e(n["beat"])} · '
        + " · ".join(f'<a class="hover:text-navy-deep" href="{CORRIDOR_PAGE[c]}">{e(c)}</a>' for c in n["corridors"]) + '</div></div></div>'
        for n in NEWS)
    return f'''<main class="w-full pt-16 bg-bg-canvas"><div class="max-w-[1080px] w-full mx-auto px-margin py-space-xl flex flex-col gap-space-xl">
<div class="flex flex-col gap-space-md">{crumb(("Home", "index.html"), ("Latest", None))}
<h1 class="font-headline-lead text-headline-lead text-navy-deep tracking-tight">Industry Tracker</h1>
<p class="font-body-lead text-body-lead text-ink-muted max-w-[60ch]">The corridor's daily wire, selected from 300-400 sources worldwide. We track everything; we publish what matters, and every item is tagged, so it flows to its corridor and beat automatically.</p>
<div class="flex items-center gap-space-xs overflow-x-auto pb-1">{chips}</div></div>
<div class="flex flex-col"><div id="analysis-list">{rows}</div>
<p class="pt-space-lg font-label-meta text-label-meta text-ink-faint">Showing <span id="analysis-count"></span>, drawn from a much wider feed we filter down before it reaches the page.</p>
<p id="analysis-empty" class="hidden py-space-xl font-body-dense text-body-dense text-ink-muted">Nothing on this beat yet.</p></div>
</div>
<script>
(function () {{
  var chips = document.querySelectorAll('.beat-chip'), rows = document.querySelectorAll('.analysis-row');
  function show(beat) {{
    var n = 0;
    rows.forEach(function (r) {{ var on = !beat || r.dataset.beat === beat; r.classList.toggle('hidden', !on); if (on) n++; }});
    chips.forEach(function (c) {{
      var on = c.dataset.beat === beat;
      c.classList.toggle('bg-navy-deep', on); c.classList.toggle('text-on-navy-bright', on);
      c.classList.toggle('bg-surface-container', !on); c.classList.toggle('text-ink-muted', !on);
    }});
    document.getElementById('analysis-count').textContent = n + (n === 1 ? ' item' : ' items');
    document.getElementById('analysis-empty').classList.toggle('hidden', n > 0);
  }}
  chips.forEach(function (c) {{ c.addEventListener('click', function () {{ show(c.dataset.beat); }}); }});
  show('');
}})();
</script></main>'''

# ---------------------------------------------------------------- 404
def not_found_main():
    links = [("Latest", "latest.html", "home"), ("Analysis", "analysis.html", "article"),
             ("Live Industry Tracker", "tracker.html", "monitoring"), ("Corridors", "index.html#corridors", "public")]
    cards = "".join(
        f'<a class="flex items-center gap-space-md p-space-lg rounded-xl bg-surface-panel hover:bg-surface-variant transition-colors group" href="{h}">'
        f'<span class="material-symbols-outlined text-navy-deep text-[22px]">{icon}</span>'
        f'<span class="flex-1 font-body-dense text-body-dense text-ink-primary font-semibold">{label}</span>'
        f'<span class="material-symbols-outlined text-ink-faint group-hover:text-navy-deep group-hover:translate-x-1 transition-all">arrow_forward</span></a>'
        for label, h, icon in links)
    return f'''<main class="w-full pt-16 bg-bg-canvas"><div class="max-w-[1080px] w-full mx-auto px-margin py-space-3xl flex flex-col gap-space-xl">
<div class="flex flex-col gap-space-md max-w-[640px]">
<span class="self-start px-2.5 py-1 rounded-[999px] bg-surface-container-high text-navy-deep font-label-section text-label-section font-semibold">Error 404</span>
<h1 class="font-headline-lead text-headline-lead text-navy-deep tracking-tight">This page isn't on the corridor map.</h1>
<p class="font-body-lead text-body-lead text-ink-muted">The link may be old, or the page may have moved. Pick up the trail from one of these.</p></div>
<div class="grid grid-cols-1 sm:grid-cols-2 gap-space-md max-w-[760px]">{cards}</div>
</div></main>'''

# ---------------------------------------------------------------- links into the new pages
GENERATED = {"latest.html", "analysis.html", "mena.html", "rest-of-world.html", "404.html"}

def link_headlines(html):
    """Make article headlines on existing pages (home lead, latest-analysis rows) open the article."""
    for a in ARTICLES:
        pat = re.compile(r'(<h[123][^>]*>)\s*(' + re.escape(e(a["head"])).replace("'", "['’]") + r')\s*(</h[123]>)')
        html = pat.sub(lambda m: f'{m.group(1)}<a class="hover:text-navy-soft transition-colors" href="{article_href(a)}">{m.group(2)}</a>{m.group(3)}', html)
    return html

def main():
    for a in ARTICLES:
        if a["id"] != "tariff":  # article-tariff.html is the Stitch longread
            write_page(article_href(a), a["head"], article_main(a))
    write_page("analysis.html", "Analysis", listing_main())
    write_page("rest-of-world.html", "Rest of World Corridor", corridor_main("Rest of World"))
    write_page("mena.html", "MENA Corridor", corridor_main("MENA"))
    write_page("latest.html", "Latest", latest_main())
    write_page("404.html", "Page not found", not_found_main(), root_links=True)
    for f in SITE.glob("*.html"):
        # generated pages already link their headlines; wrapping again would nest <a> tags
        if f.name in GENERATED or (f.name.startswith("article-") and f.name != "article-tariff.html"):
            continue
        f.write_text(link_headlines(read(f)), encoding="utf-8")
    print("wrote analysis.html, mena.html, rest-of-world.html and", len(ARTICLES) - 1, "article pages")

if __name__ == "__main__":
    main()
