import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

print("[CHECK] debug checkout present:", "plans import failed" in c)

guard = '\nimport sys as _sys, os as _os2\n_sys.path.append(_os2.join(_os2.dirname(_os2.abspath(__file__)), ".."))\n'
if "_sys.path.append" not in c:
    idx = c.find("from fastapi import")
    if idx == -1:
        c = guard + c
    else:
        le = c.find("\n", idx)
        c = c[:le] + guard + c[le:]
    open(ar, "w", encoding="utf-8").write(c)
    print("[PATCHED] sys.path guard added to analytics_routes")
else:
    print("[OK] guard already present")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: sys.path guard for plans import in analytics_routes"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
