"""Builds the <main> markup for mena.html in the same design language as the other
corridor pages. Content is structural/qualitative on purpose: no trade-value or growth
statistics are stated here, so nothing unsourced is published. Add sourced figures where
the 'Quantified flows' notes are."""

def esc(s):
    return s.replace("&", "&amp;")

def status_card(label, title, sub, amber=False):
    color = "text-amber-risk" if amber else "text-navy-deep"
    return (f'<div class="p-space-sm bg-bg-canvas rounded-lg shadow-sm">'
            f'<div class="font-label-micro text-label-micro text-ink-faint uppercase tracking-wider mb-1">{esc(label)}</div>'
            f'<div class="font-headline-row text-headline-row {color} font-medium">{esc(title)}</div>'
            f'<div class="font-label-meta text-label-meta text-ink-muted mt-1">{esc(sub)}</div></div>')

def deck_tile(big, label, note):
    return (f'<div class="space-y-1"><div class="font-metric-large text-metric-large text-on-navy-bright tracking-tight">{esc(big)}</div>'
            f'<div class="font-label-meta text-label-meta text-on-navy-muted uppercase tracking-wide">{esc(label)}</div>'
            f'<p class="font-label-meta text-label-meta text-primary-fixed-dim pt-1">{esc(note)}</p></div>')

def lane(name, chip, desc, dark=True):
    bar = "bg-navy-deep" if dark else "bg-bar-secondary"
    return (f'<div><div class="flex justify-between gap-3 font-label-meta text-label-meta text-ink-primary mb-1.5">'
            f'<span class="font-medium text-navy-deep">{esc(name)}</span>'
            f'<span class="font-semibold text-navy-deep shrink-0">{esc(chip)}</span></div>'
            f'<div class="w-full bg-surface-container h-1.5 rounded-full overflow-hidden"><div class="{bar} h-full rounded-full w-full"></div></div>'
            f'<p class="font-label-micro text-label-micro text-ink-muted mt-1.5">{esc(desc)}</p></div>')

def lane_card(title, sub, tag, lanes):
    body = "".join(lane(*l) for l in lanes)
    return (f'<div class="bg-surface-panel p-space-lg rounded-xl shadow-sm space-y-space-md">'
            f'<div class="flex items-center justify-between pb-space-sm border-b border-line-hairline"><div>'
            f'<div class="font-headline-card text-headline-card text-navy-deep font-normal">{esc(title)}</div>'
            f'<div class="font-label-meta text-label-meta text-ink-muted">{esc(sub)}</div></div>'
            f'<span class="font-label-section text-label-section text-navy-deep bg-surface-container px-2.5 py-1 rounded-full shrink-0">{esc(tag)}</span></div>'
            f'<div class="space-y-space-md">{body}</div></div>')

def hub(country, chip, title, body, operators, tag):
    return (f'<div class="p-space-lg bg-surface-panel rounded-xl shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow"><div>'
            f'<div class="flex items-center justify-between mb-2"><span class="font-label-section text-label-section text-navy-deep uppercase tracking-wider font-semibold">{esc(country)}</span>'
            f'<span class="font-label-micro text-label-micro bg-bg-canvas px-2 py-0.5 rounded text-ink-muted">{esc(chip)}</span></div>'
            f'<h3 class="font-headline-card text-headline-card text-navy-deep mb-2 font-normal">{esc(title)}</h3>'
            f'<p class="font-body-dense text-body-dense text-ink-muted mb-space-md">{esc(body)}</p></div>'
            f'<div class="pt-space-sm border-t border-line-hairline flex items-center justify-between gap-3 text-ink-faint font-label-micro text-label-micro">'
            f'<span>Anchor Operators: {esc(operators)}</span><span class="font-medium text-navy-deep shrink-0">{esc(tag)}</span></div></div>')

def operator(name, country, focus):
    return (f'<div class="p-space-sm bg-bg-canvas rounded-lg text-center shadow-xs">'
            f'<div class="font-headline-row text-headline-row text-navy-deep font-semibold">{esc(name)}</div>'
            f'<div class="font-label-meta text-label-meta text-ink-muted">{esc(country)}</div>'
            f'<div class="font-label-micro text-label-micro text-primary-container mt-1 font-medium">{esc(focus)}</div></div>')

def ledger_row(dim, status, impl):
    return (f'<tr class="hover:bg-surface-container-low transition-colors"><td class="p-space-md font-medium text-navy-deep">{esc(dim)}</td>'
            f'<td class="p-space-md">{esc(status)}</td><td class="p-space-md text-ink-muted">{esc(impl)}</td></tr>')

def watch(tag, title, body):
    return (f'<article class="p-space-md bg-surface-panel hover:bg-surface-container-low transition-colors rounded-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-space-md">'
            f'<div class="space-y-1 max-w-3xl"><div class="flex items-center gap-2"><span class="px-2 py-0.5 bg-bg-canvas text-navy-deep font-label-micro text-label-micro uppercase font-semibold rounded">{esc(tag)}</span>'
            f'<span class="font-label-meta text-label-meta text-ink-faint">Standing theme</span></div>'
            f'<h3 class="font-headline-row text-headline-row text-navy-deep font-medium">{esc(title)}</h3>'
            f'<p class="font-body-dense text-body-dense text-ink-muted">{esc(body)}</p></div>'
            f'<a class="shrink-0 px-4 py-2 bg-bg-canvas text-navy-deep font-label-section text-label-section rounded-full shadow-xs hover:bg-navy-deep hover:text-on-navy-bright transition-colors" href="tracker.html">Follow in Tracker</a></article>')

def heading(eyebrow, title, tag="h2", cls="font-headline-section text-headline-section"):
    return (f'<div class="mb-space-lg"><div class="font-label-section text-label-section uppercase text-ink-muted tracking-wider">{esc(eyebrow)}</div>'
            f'<{tag} class="{cls} text-navy-deep font-normal">{esc(title)}</{tag}></div>')

def build_main():
    status = "".join([
        status_card("Dominant Function", "Import Market & Localization Drive",
                    "Large branded and generic import demand, with state-backed local manufacturing growing alongside it"),
        status_card("Regulatory Architecture", "SFDA, EDE & EDA Anchors",
                    "National authorities in Saudi Arabia, the UAE and Egypt, plus GCC central registration"),
        status_card("Systemic Strategic Exposure", "Red Sea Routing & Cold-Chain Heat Load",
                    "Chokepoint disruption and high ambient temperatures stress temperature-controlled supply", amber=True),
    ])
    deck = "".join([
        deck_tile("6", "GCC Member States", "Saudi Arabia, UAE, Kuwait, Qatar, Bahrain and Oman share a central drug-registration route."),
        deck_tile("3", "Maritime Chokepoints", "Suez Canal, Bab el-Mandeb and the Strait of Hormuz carry the corridor's sea freight."),
        deck_tile("2", "Gulf Air-Cargo Hubs", "Dubai and Doha anchor temperature-controlled air freight into and through the region."),
    ])
    inbound = lane_card("Inbound Supply Lanes", "Where MENA's finished medicine and inputs come from", "Import Dependence", [
        ("India (generics, vaccines, formulations)", "Volume lane",
         "High-volume, price-competitive generics for tender-driven public and private markets across the Gulf, Levant and North Africa."),
        ("Europe (branded drugs & biologics)", "Value lane",
         "Patented medicines and specialty biologics for Gulf private and insured markets and for national reference lists."),
        ("United States (innovator brands & biologics)", "Value lane",
         "Innovator launches and specialty lines, increasingly routed through Gulf regional headquarters."),
        ("China (active ingredients & key starting materials)", "Input lane",
         "The ingredient base behind regional generics makers, from Cairo to Amman to Casablanca.", False),
    ])
    outbound = lane_card("Outbound & Intra-Regional Flows", "Where MENA-made and MENA-routed medicine goes", "Hub & Export", [
        ("Egypt & Jordan to Gulf, Levant and Africa", "Generics lane",
         "Established manufacturers supply neighbouring tenders and distributors with oral solids, injectables and specialty generics."),
        ("Gulf free zones to Africa and Central Asia", "Re-export lane",
         "Dubai and Abu Dhabi free zones, Jebel Ali and the air hubs act as regional stocking and re-export gateways."),
        ("Morocco and the Maghreb to Europe and West Africa", "Nearshore lane",
         "A growing manufacturing base positioned close to European demand and francophone African markets.", False),
    ])
    hubs = "".join([
        hub("Saudi Arabia", "Localization Anchor", "The Procurement Giant",
            "The Gulf's largest market, using Vision 2030 localization goals and centralized government purchasing through NUPCO to pull manufacturing onshore.",
            "Tabuk, Jamjoom, SPIMACO", "Rank #1 Gulf Market"),
        hub("United Arab Emirates", "Hub Gateway", "Dubai & Abu Dhabi Gateway",
            "Free zones, world-class air and sea logistics and a federal regulator (EDE) make the UAE the region's stocking, distribution and re-export hub.",
            "Julphar, regional HQs", "Logistics Hub"),
        hub("Egypt", "Volume Base", "The Manufacturing Workhorse",
            "One of the region's deepest domestic manufacturing bases, with state procurement through the Unified Procurement Authority and exposure to currency swings on imported inputs.",
            "Pharco, EVA Pharma, EIPICO", "Volume Leader"),
        hub("Jordan", "Generics Exporter", "The Regional Generics Exporter",
            "A small domestic market with an export-oriented generics industry that supplies buyers across the Levant, Gulf and North Africa.",
            "Hikma, Dar Al Dawa", "Export Specialist"),
        hub("Morocco", "Nearshore Gateway", "The Maghreb Gateway",
            "A growing manufacturing base positioned close to Europe and reaching toward West and Central Africa through regional distribution links.",
            "Sothema, Cooper Pharma", "Rising Hub"),
        hub("Algeria", "Import Substitution", "The Localization Mandate",
            "A policy of favouring domestic production restricts imports where local equivalents exist, pushing multinationals toward local partnerships.",
            "Saidal", "Policy-Driven"),
    ])
    ops = "".join([
        operator("Hikma", "Jordan", "Generics / Injectables"),
        operator("Julphar", "United Arab Emirates", "Insulin / Generics"),
        operator("Tabuk Pharmaceuticals", "Saudi Arabia", "Generics"),
        operator("Pharco", "Egypt", "Generics / Antivirals"),
        operator("Sothema", "Morocco", "Generics"),
        operator("Saidal", "Algeria", "Public-Sector Generics"),
    ])
    ledger = "".join([
        ledger_row("Market Role", "Large importer with a rising local-manufacturing share",
                   "Demand is secure; the contest is over who supplies it, imported or locally made."),
        ledger_row("Procurement Model", "Centralized state buyers, such as NUPCO and Egypt's Unified Procurement Authority",
                   "Tender terms, local-content preferences and payment timing decide market access and margins."),
        ledger_row("Regulatory Pathway", "National authorities (SFDA, EDE, EDA, JFDA) plus GCC central registration",
                   "Registration strategy and use of reference-authority approvals set launch timelines."),
        ledger_row("Logistics Backbone", "Jebel Ali, Dubai and Doha air hubs, Suez Canal transit",
                   "Gulf hubs shorten lead times to the wider region, but depend on a few strategic passages."),
        ledger_row("Cold-Chain Pressure", "High ambient temperatures and long last-mile distances",
                   "Biologics and vaccines need validated temperature-controlled handling from airport to pharmacy."),
        ledger_row("Primary Risks", "Red Sea routing, currency pressure in import-dependent economies, tender price compression",
                   "Supply continuity and pricing power vary sharply from the Gulf to North Africa."),
    ])
    watches = "".join([
        watch("Policy & Trade", "Localization mandates are reshaping tender eligibility across the Gulf",
              "Governments are tying market access to local manufacturing, technology transfer and regional-headquarters commitments."),
        watch("Logistics", "Red Sea routing keeps transit times and cold-chain risk in focus",
              "Disruption around Bab el-Mandeb has pushed carriers onto longer routes, tightening schedules for temperature-sensitive cargo."),
        watch("Supply Security", "Currency pressure tests import-dependent supply in North Africa",
              "Foreign-exchange availability shapes how reliably importers can pay for finished medicine and ingredients."),
        watch("Regulatory", "Regional regulators lean further on reference-authority approvals",
              "Reliance pathways can shorten review times for products already approved by major regulators."),
    ])
    return f'''<main class="w-full pt-16 bg-bg-canvas"><div class="flex flex-col w-full">
<div class="max-w-[1080px] mx-auto px-margin py-space-xl w-full">
<!-- Breadcrumb & Classification Bar -->
<div class="flex flex-wrap items-center justify-between gap-space-sm mb-space-md">
<div class="flex items-center gap-2 font-label-meta text-label-meta text-ink-muted">
<a class="hover:text-navy-deep transition-colors" href="index.html">Home</a>
<span class="text-ink-faint">/</span>
<a class="hover:text-navy-deep transition-colors" href="index.html#corridors">Corridors</a>
<span class="text-ink-faint">/</span>
<span class="text-navy-deep font-medium">MENA</span>
</div>
<div class="inline-flex items-center gap-2 px-3 py-1 bg-surface-container rounded-full text-navy-deep font-label-section text-label-section uppercase tracking-wider">
<span class="w-2 h-2 rounded-full bg-navy-deep"></span>
<span>Strategic Corridor Dossier · Ref: COR-MENA-2025</span>
</div>
</div>
<!-- Editorial Header & Standfirst -->
<div class="mb-space-xl">
<div class="inline-block mb-space-xs font-label-section text-label-section uppercase text-ink-muted tracking-widest">Trade Corridor Intelligence Deck</div>
<h1 class="font-headline-lead text-headline-lead text-navy-deep mb-space-md tracking-tight">MENA</h1>
<p class="font-body-lead text-body-lead text-ink-muted max-w-[900px] leading-relaxed">A large import market and a hard localization drive, from Riyadh to Cairo. The Middle East and North Africa buy branded medicine from Europe and the United States and generics from India, while governments push manufacturing onshore and Gulf hubs route stock to the wider region.</p>
</div>
<!-- Top Corridor Matrix / Status Strip -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-space-sm bg-surface-panel p-space-md rounded-xl mb-space-2xl">{status}</div>
<!-- Navy Structural Deck -->
<div class="bg-navy-deep text-on-navy-bright rounded-xl p-space-lg shadow-md mb-space-2xl">
<div class="flex flex-wrap items-center justify-between gap-2 pb-space-md mb-space-lg border-b border-navy-soft">
<div class="flex items-center gap-space-sm"><span class="material-symbols-outlined text-[20px] text-primary-fixed">hub</span>
<span class="font-label-section text-label-section text-on-navy-muted uppercase tracking-wider">Corridor Structure at a Glance</span></div>
<span class="font-label-meta text-label-meta text-primary-fixed-dim">Quantified trade flows to follow at next re-index</span></div>
<div class="grid grid-cols-1 sm:grid-cols-3 gap-space-lg">{deck}</div>
</div>
<!-- Trade Flow Lanes -->
<div class="mb-space-2xl">
{heading("Trade Flow Breakdown", "Supply Lanes In, Hub Lanes Out")}
<div class="grid grid-cols-1 lg:grid-cols-2 gap-space-lg">{inbound}{outbound}</div>
<div class="mt-space-lg p-space-md bg-surface-container-low rounded-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-space-md shadow-sm">
<div class="flex items-start gap-space-sm"><span class="material-symbols-outlined text-[24px] text-amber-risk shrink-0 mt-0.5">warning</span>
<div><div class="font-label-section text-label-section text-navy-deep uppercase tracking-wider">Corridor Vulnerability Assessment</div>
<p class="font-body-dense text-body-dense text-ink-muted max-w-3xl">MENA depends on imports for much of its finished medicine and on a handful of strategic passages and hubs to receive them. Red Sea disruption, heat-stressed cold chains and currency pressure in some importing economies are the pressure points to watch.</p></div></div>
<a class="inline-flex items-center gap-1 font-label-section text-label-section text-navy-deep hover:text-navy-soft font-semibold shrink-0" href="briefing.html"><span>Get the MENA Hub &amp; Red Sea Briefing</span><span class="material-symbols-outlined text-[16px]">arrow_forward</span></a>
</div>
</div>
<!-- Geographic Epicenters Grid -->
<div class="mb-space-2xl">
{heading("Market Cartography", "MENA Epicenters of Demand, Production & Transit")}
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-space-md">{hubs}</div>
</div>
<!-- Operators -->
<div class="bg-surface-panel p-space-lg rounded-xl mb-space-2xl shadow-sm">
<div class="mb-space-md"><div class="font-label-section text-label-section uppercase text-ink-muted tracking-wider">Corporate Operators</div>
<h2 class="font-headline-card text-headline-card text-navy-deep font-medium">Regional Operators to Watch</h2></div>
<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-space-sm">{ops}</div>
</div>
<!-- Operational Ledger -->
<div class="mb-space-2xl">
{heading("Institutional Overview", "Corridor Operational Ledger")}
<div class="bg-bg-canvas rounded-xl shadow-sm overflow-hidden"><div class="overflow-x-auto">
<table class="w-full text-left"><thead class="bg-surface-panel text-ink-muted font-label-section text-label-section uppercase tracking-wider"><tr>
<th class="p-space-md">Strategic Dimension</th><th class="p-space-md">Corridor Status</th><th class="p-space-md">Analytical Implications</th></tr></thead>
<tbody class="divide-y divide-line-hairline font-body-dense text-body-dense text-ink-primary">{ledger}</tbody></table>
</div></div>
</div>
<!-- Watchlist -->
<div class="mb-space-2xl">
<div class="flex items-center justify-between gap-3 mb-space-lg"><div><div class="font-label-section text-label-section uppercase text-ink-muted tracking-wider">Corridor Watchlist</div>
<h2 class="font-headline-section text-headline-section text-navy-deep font-normal">What We Are Tracking in MENA</h2></div>
<a class="font-label-section text-label-section text-navy-deep hover:text-navy-soft flex items-center gap-1 font-semibold shrink-0" href="tracker.html"><span>Open Live Tracker</span><span class="material-symbols-outlined text-[16px]">chevron_right</span></a></div>
<div class="space-y-space-sm">{watches}</div>
</div>
<!-- Methodology -->
<div class="p-space-lg bg-surface-panel rounded-xl text-ink-muted font-body-dense text-body-dense mb-space-xl">
<div class="flex items-center gap-2 mb-2 text-navy-deep font-label-section text-label-section uppercase tracking-wider font-semibold"><span class="material-symbols-outlined text-[18px]">verified</span><span>Methodology &amp; Verification Ledger</span></div>
<p class="mb-space-sm leading-relaxed">This dossier is a structural profile of the corridor, compiled from public regulator, procurement-authority and customs publications. It deliberately states no trade values or growth rates until they are verified against primary customs and national-statistics datasets; quantified flows will be added at the next corridor re-index.</p>
<div class="flex flex-wrap items-center gap-x-space-lg gap-y-2 pt-space-sm border-t border-line-hairline font-label-micro text-label-micro text-ink-faint">
<span>Regulators: SFDA, EDE, EDA, JFDA</span><span>GCC Central Registration</span><span>Quantified flows: pending re-index</span></div>
</div>
</div>
</div>
</main>'''
