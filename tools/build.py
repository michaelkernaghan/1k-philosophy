import glob
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
TARGET = 1000

TITLES = {
    "01": "Metaphysics and Ontology",
    "02": "Epistemology",
    "03": "Logic and Philosophy of Mathematics",
    "04": "Philosophy of Language",
    "05": "Philosophy of Mind",
    "06": "Ethics",
    "07": "Political, Legal and Social Philosophy",
    "08": "Aesthetics",
    "09": "Philosophy of Science",
    "10": "Philosophy of Religion",
    "11": "Existentialism, Phenomenology and Continental Philosophy",
    "12": "Action, Free Will, Identity and the Examined Life",
    "13": "Non-Western Traditions",
}

entries = []  # (number, section_key, name, summary)
problems = []
seen = {}
n = 0
for f in sorted(glob.glob(str(root / "src" / "*.txt"))):
    key = Path(f).name[:2]
    for i, ln in enumerate(Path(f).read_text(encoding="utf-8").splitlines(), 1):
        if not ln.strip():
            continue
        if " :: " not in ln:
            problems.append(f"{Path(f).name}:{i} malformed: {ln[:60]}")
            continue
        name, summary = [s.strip() for s in ln.split(" :: ", 1)]
        low = name.lower()
        if low in seen:
            problems.append(f"duplicate '{name}' in {Path(f).name}:{i} and {seen[low]}")
        seen[low] = f"{Path(f).name}:{i}"
        if not summary or len(summary.split()) < 8:
            problems.append(f"{Path(f).name}:{i} short summary for '{name}'")
        n += 1
        entries.append((n, key, name, summary))

print("entries:", n)
if n != TARGET:
    problems.append(f"count is {n}, target {TARGET}")
for p in problems:
    print("PROBLEM:", p)
if problems:
    sys.exit(1)

out = []
out.append("# The 1,000 Most Important Philosophical Concepts\n")
out.append("Indexed, ordered and summarized. Part I groups the concepts by branch of philosophy, "
           "and within each branch they run from the most to the less central. Part II is an "
           "alphabetical index giving each concept's entry number.\n")
out.append("The selection and the within-branch order are editorial judgments, not a measured ranking. "
           "Concepts that belong to several branches appear once, in the branch where they are most at home.\n")
out.append("## Contents\n")
counts = {}
for num, key, name, summary in entries:
    counts[key] = counts.get(key, 0) + 1
first = {}
for num, key, name, summary in entries:
    first.setdefault(key, num)
for key in sorted(counts):
    last = first[key] + counts[key] - 1
    out.append(f"- Part I.{int(key)}: {TITLES[key]} (entries {first[key]}-{last})")
out.append("- Part II: Alphabetical index\n")
out.append("# Part I: Concepts by Branch\n")
cur = None
for num, key, name, summary in entries:
    if key != cur:
        out.append(f"\n## {int(key)}. {TITLES[key]}\n")
        cur = key
    out.append(f"**{num}. {name}.** {summary}\n")
out.append("\n# Part II: Alphabetical Index\n")


def sortkey(name):
    return re.sub(r"[^a-z0-9 ]", "", name.lower().replace("é", "e").replace("ā", "a").replace("ū", "u").replace("ö", "o").replace("ü", "u").replace("ł", "l").replace("É", "e"))


letter = None
for num, key, name, summary in sorted(entries, key=lambda e: sortkey(e[2])):
    first_char = sortkey(name)[:1].upper() or "#"
    if first_char != letter:
        out.append(f"\n### {first_char}\n")
        letter = first_char
    out.append(f"- {name} ({num})")
(root / "philosophical-concepts.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("wrote philosophical-concepts.md")
