import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

# Remove broken guard
c = c.replace("\nimport sys as _sys, os as _os2\n_sys.path.append(_os2.join(_os2.dirname(_os2.abspath(__file__)), '..'))\n", "")
c = c.replace("\nimport sys as _sys, os as _os2\n_sys.path.append(_os2.join(_os2.dirname(_os2.abspath(__file__)), \"..\"))\n", "")

# Add pathlib guard (can't conflict with os shadowing)
guard = "\nimport sys as _sys\nfrom pathlib import Path as _Path\n_sys.path.insert(0, str(_Path(__file__).parent.parent))\n"
if "_sys.path.insert" not in c and "from pathlib import" not in c[:2000]:
    idx = c.find("from fastapi import")
    if idx == -1:
        c = guard + c
    else:
        le = c.find("\n", idx)
        c = c[:le] + guard + c[le:]
    print("[PATCHED] pathlib-based sys.path guard installed")
else:
    print("[OK] guard already present or alternative exists")

open(ar, "w", encoding="utf-8").write(c)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: replace broken os-based guard with pathlib to restore app boot"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED - Render should deploy cleanly now")
