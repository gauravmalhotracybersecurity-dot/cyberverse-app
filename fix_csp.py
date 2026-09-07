import glob, subprocess
n = 0
for f in [x for x in glob.glob("**/*.html", recursive=True) if not any(t in x for t in ("venv","node_modules",".git"))]:
    c = open(f, encoding="utf-8").read()
    if "img-src 'self' data:" in c and "buildlist.io" not in c.split("img-src 'self' data:")[1][:40]:
        c = c.replace("img-src 'self' data:", "img-src 'self' data: https://buildlist.io")
        open(f, "w", encoding="utf-8").write(c)
        n += 1
        print("[CSP] buildlist.io allowed in", f)
print("files patched:", n)
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: allow buildlist.io badge via CSP img-src"])
subprocess.run(["git", "push", "origin", "main"])
