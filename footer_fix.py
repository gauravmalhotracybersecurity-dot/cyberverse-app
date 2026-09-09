import subprocess

p = "backend/templates/base.html"
lines = open(p, encoding="utf-8").read().split("\n")

if any('href="/about"' in l for l in lines):
    print("[SKIP] About link already in footer")
else:
    # 1. Find the /b2b footer link line
    idx = None
    for i, l in enumerate(lines):
        if 'href="/b2b"' in l and l.strip().startswith("<a"):
            idx = i
            break
    if idx is None:
        print("[ERROR] /b2b footer link not found")
        raise SystemExit(1)

    ind = lines[idx][:len(lines[idx]) - len(lines[idx].lstrip())]
    print(f"[FOUND] /b2b link at line {idx+1}, indent={len(ind)}")

    # 2. Insert About/Contact/FAQ right after it
    new_links = [
        ind + '<a href="/about">About</a>',
        ind + '<a href="/contact">Contact</a>',
        ind + '<a href="/faq">FAQ</a>',
    ]
    lines[idx+1:idx+1] = new_links
    print("[INSERTED] About / Contact / FAQ links")

    # 3. Find the closing </div> of footer-links after insertion point
    j = idx + 4
    while j < len(lines) and lines[j].strip() != "</div>":
        j += 1
    print(f"[FOUND] footer-links closing div at line {j+1}")

    # 4. Insert social icons block after it
    icons = [
        '        <div style="display:flex;gap:1.2rem;justify-content:center;align-items:center;margin:1.5rem 0">',
        '            <a href="https://linkedin.com/in/gauravmalhotracybersecurity" target="_blank" rel="noopener" title="LinkedIn" style="color:var(--muted)"><svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>',
        '            <a href="https://twitter.com/gauravmalhotra" target="_blank" rel="noopener" title="Twitter / X" style="color:var(--muted)"><svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>',
        '            <a href="https://youtube.com/@grcwithgaurav" target="_blank" rel="noopener" title="YouTube" style="color:var(--muted)"><svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a>',
        '        </div>',
    ]
    lines[j+1:j+1] = icons
    print("[INSERTED] LinkedIn / Twitter / YouTube icons")

    open(p, "w", encoding="utf-8").write("\n".join(lines))
    print("[SAVED] base.html")

# Verify locally BEFORE pushing
c = open(p, encoding="utf-8").read()
for k in ['href="/about"', 'href="/contact"', 'href="/faq"', 'youtube.com']:
    print(f"  local check {k}: {'YES' if k in c else 'NO'}")

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Footer: line-based insert of About/Contact/FAQ links + social icons"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
