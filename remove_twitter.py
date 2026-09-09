import subprocess, glob, re

TARGET = "twitter.com/gauravmalhotra"
changed = []

for f in glob.glob("backend/templates/**/*.html", recursive=True):
    c = open(f, encoding="utf-8").read()
    if TARGET not in c:
        continue
    orig = c
    lines = c.split("\n")
    out = []
    for l in lines:
        # Remove whole-line twitter profile links (footer icon, about button, schema line)
        if TARGET in l and ("twitter.com/intent" not in l):
            stripped = l.strip()
            if stripped.startswith("<a ") or stripped.startswith('"http'):
                print(f"[REMOVE LINE] {f}: {stripped[:80]}")
                continue
        out.append(l)
    c = "\n".join(out)

    # Inline removal (e.g. contact.html sentence: "...on LinkedIn or Twitter.")
    c = re.sub(r'\s*or\s*<a href="https?://' + re.escape(TARGET) + r'"[^>]*>Twitter</a>', '', c)
    c = re.sub(r'<a href="https?://' + re.escape(TARGET) + r'"[^>]*>Twitter</a>\s*or\s*', '', c)

    # Fix JSON trailing comma in sameAs array after twitter line removal
    c = re.sub(r',(\s*\n\s*\])', r'\1', c)

    if c != orig:
        open(f, "w", encoding="utf-8").write(c)
        changed.append(f)
        print(f"[UPDATED] {f}")

if not changed:
    print("[NOTE] No twitter profile links found")

# Final local verification
print("\n=== LOCAL CHECK ===")
for f in glob.glob("backend/templates/**/*.html", recursive=True):
    c = open(f, encoding="utf-8").read()
    if TARGET in c:
        print(f"  STILL PRESENT in {f}")
print("  twitter profile links remaining: ", sum(1 for f in glob.glob("backend/templates/**/*.html", recursive=True) if TARGET in open(f, encoding="utf-8").read()))
print("  share-intent buttons kept: ", sum(1 for f in glob.glob("backend/templates/**/*.html", recursive=True) if "twitter.com/intent" in open(f, encoding="utf-8").read()))

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Remove wrong Twitter/X profile links (footer, about, contact, schema)"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
