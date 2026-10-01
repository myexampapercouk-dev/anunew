"""Pull article, news, MENA and Rest of World data out of the-pharma-corridor-site.html
(the original single-page site) into tools/spa_content.json for inner_pages.py."""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "the-pharma-corridor-site.html"
s = SRC.read_text(encoding="utf-8")

def grab(start, end):
    i = s.index(start) + len(start)
    return s[i:s.index(end, i)]

STRING = re.compile(r'("(?:[^"\\]|\\.)*")')
BARE_KEY = re.compile(r'([{,]\s*)([A-Za-z_]\w*)\s*:')

def js2json(text):
    """JS object literal -> JSON: quote bare keys, but only outside string literals."""
    parts = STRING.split(text)
    for k in range(0, len(parts), 2):
        parts[k] = BARE_KEY.sub(r'\1"\2":', parts[k])
    return json.loads("".join(parts))

data = {
    "articles": js2json(grab("const ARTICLES=", "];\n") + "]"),
    "news": js2json(grab("const NEWS=", "];\n") + "]"),
    "corridors": {name: js2json(grab(f'CP["{name}"]=', "};\n") + "}") for name in ("MENA", "Rest of World")},
}
(ROOT / "tools" / "spa_content.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print("articles:", [a["id"] for a in data["articles"]], "| news:", len(data["news"]), "| corridors:", list(data["corridors"]))
