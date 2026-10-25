import glob
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent

TITLES = {
    "01": "Metaphysics and Ontology",
    "02": "Epistemology",
    "03": "Logic and Mathematics",
    "04": "Language",
    "05": "Mind",
    "06": "Ethics",
    "07": "Political and Social",
    "08": "Aesthetics",
    "09": "Science",
    "10": "Religion",
    "11": "Existential and Continental",
    "12": "Action and Identity",
    "13": "Non-Western",
}

entries = []
n = 0
for f in sorted(glob.glob(str(root / "src" / "*.txt"))):
    key = Path(f).name[:2]
    for ln in Path(f).read_text(encoding="utf-8").splitlines():
        if " :: " not in ln:
            continue
        name, summary = [s.strip() for s in ln.split(" :: ", 1)]
        n += 1
        entries.append({"n": n, "b": key, "t": name, "s": summary})

if n != 1000:
    print("expected 1000 entries, got", n)
    sys.exit(1)

template = (root / "tools" / "site_template.html").read_text(encoding="utf-8")
html = template.replace("__DATA__", json.dumps(entries, ensure_ascii=False).replace("</", "<\\/"))
html = html.replace("__BRANCHES__", json.dumps(TITLES, ensure_ascii=False))
out = root / "docs" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding="utf-8")
print("wrote", out, len(html), "bytes")
