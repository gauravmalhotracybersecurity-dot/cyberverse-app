import glob, subprocess

skip = ("venv", "node_modules", ".git")

# 1) CSP: allow buildlist.io wherever img-src is defined (backend header OR html meta)
files = [x for x in glob.glob("**/*.py", recursive=True) if not any(t in x for t in skip)]
files += [x for x in glob.glob("**/*.html", recursive=True) if not any(t in x for t in skip)]
for f in files:
    c = open(f, encoding="utf-8").read()
    if "img-src 'self' data:" in c and "buildlist.io" not in c:
        c = c.replace("img-src 'self' data:", "img-src 'self' data: https://buildlist.io")
        open(f, "w", encoding="utf-8").write(c)
        print("[CSP] buildlist.io allowed in", f)

# 2) Pricing v2: literal, count-guarded replacements (no regex anywhere)
htmls = [x for x in glob.glob("**/app.html", recursive=True) if not any(t in x for t in skip)]
for f in htmls:
    c = open(f, encoding="utf-8").read()
    reps = [
        ("499 lifetime", "&#8377;499 lifetime <span style='color:#9aa4b2;font-size:.8rem'>&middot; &#8776; $6 USD one-time</span>"),
        ("999 lifetime", "&#8377;999 lifetime <span style='color:#9aa4b2;font-size:.8rem'>&middot; &#8776; $12 USD one-time</span>"),
        ("Access activates", "Prices in Indian Rupees (INR): Pro &#8776; $6 USD, Premium &#8776; $12 USD one-time.<br>Access activates"),
    ]
    changed = False
    for old, new in reps:
        n = c.count(old)
        if n == 1:
            c = c.replace(old, new)
            changed = True
            print("[PRICING] updated:", old)
        else:
            print("[PRICING][WARN] skipped '%s' (found %d times)" % (old, n))
    if changed:
        open(f, "w", encoding="utf-8").write(c)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Polish: CSP badge allowlist + dual-currency paywall (guarded literals)"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
