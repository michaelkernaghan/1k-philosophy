import glob
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
cuts = [c.strip() for c in (root / "tools" / "cuts.txt").read_text(encoding="utf-8").splitlines() if c.strip()]
remaining = set(cuts)
removed = 0
for f in sorted(glob.glob(str(root / "src" / "*.txt"))):
    p = Path(f)
    lines = p.read_text(encoding="utf-8").splitlines()
    keep = []
    for ln in lines:
        name = ln.split(" :: ", 1)[0].strip()
        if name in remaining:
            remaining.discard(name)
            removed += 1
        else:
            keep.append(ln)
    p.write_text("\n".join(keep) + "\n", encoding="utf-8")
print("removed", removed, "of", len(cuts))
if remaining:
    print("NOT FOUND:", sorted(remaining))
    sys.exit(1)
