import glob
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent

TITLES = {
    "01": "Metaphysics",
    "02": "Epistemology",
    "03": "Logic and Mathematics",
    "04": "Language",
    "05": "Mind",
    "06": "Ethics",
    "07": "Political and Social",
    "08": "Aesthetics",
    "09": "Science",
    "10": "Religion",
    "11": "Continental",
    "12": "Action and Identity",
    "13": "Non-Western",
}

entries = {}
n = 0
for f in sorted(glob.glob(str(root / "src" / "*.txt"))):
    key = Path(f).name[:2]
    for ln in Path(f).read_text(encoding="utf-8").splitlines():
        if " :: " not in ln:
            continue
        name, summary = [s.strip() for s in ln.split(" :: ", 1)]
        n += 1
        entries[name] = {"n": n, "t": name, "s": summary, "b": key}

problems = []
assigned = {}
tree = {k: [] for k in TITLES}
cur = None
for i, ln in enumerate((root / "tools" / "clusters.txt").read_text(encoding="utf-8").splitlines(), 1):
    ln = ln.strip()
    if not ln:
        continue
    if ln.startswith("# "):
        cur = ln[2:].strip()
        if cur not in TITLES:
            problems.append(f"line {i}: unknown branch {cur}")
        continue
    parts = [p.strip() for p in ln.split(" | ")]
    sub, names = parts[0], parts[1:]
    leaves = []
    for nm in names:
        if nm not in entries:
            problems.append(f"line {i} ({sub}): no such concept '{nm}'")
            continue
        if nm in assigned:
            problems.append(f"line {i} ({sub}): '{nm}' already assigned to {assigned[nm]}")
            continue
        if entries[nm]["b"] != cur:
            problems.append(f"line {i} ({sub}): '{nm}' belongs to branch {entries[nm]['b']}, not {cur}")
        assigned[nm] = sub
        leaves.append(entries[nm])
    leaves.sort(key=lambda e: e["n"])
    tree[cur].append({"name": sub, "children": leaves})

missing = [nm for nm in entries if nm not in assigned]
for nm in missing:
    problems.append(f"unassigned: '{nm}' (branch {entries[nm]['b']})")
print("concepts:", len(entries), "assigned:", len(assigned), "subtopics:", sum(len(v) for v in tree.values()))
for p in problems:
    print("PROBLEM:", p)
if problems or len(entries) != 1000:
    sys.exit(1)

data = {"name": "Philosophy", "children": [{"name": TITLES[k], "k": k, "children": tree[k]} for k in sorted(TITLES)]}
template = (root / "tools" / "mindmap_template.html").read_text(encoding="utf-8")
html = template.replace("__TREE__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
(root / "docs" / "mindmap.html").write_text(html, encoding="utf-8")
print("wrote docs/mindmap.html", len(html), "chars")
