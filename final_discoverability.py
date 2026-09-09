import re, subprocess

base_html = "backend/templates/base.html"
c = open(base_html, encoding="utf-8").read()

# Target the exact footer structure from the live fetch
old_footer_links = """<div class="footer-links">
            <a href="/privacy">Privacy Policy</a>
            <a href="/terms">Terms of Service</a>
            <a href="/disclaimer">Disclaimer</a>
            <a href="/b2b">For Businesses</a>

        </div>"""

new_footer_links = """<div class="footer-links">
            <a href="/privacy">Privacy Policy</a>
            <a href="/terms">Terms of Service</a>
            <a href="/disclaimer">Disclaimer</a>
            <a href="/b2b">For Businesses</a>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
            <a href="/faq">FAQ</a>
        </div>
        <div style="display:flex;gap:1rem;justify-content:center;margin:1.5rem 0">
            <a href="https://linkedin.com/in/gauravmalhotracybersecurity" target="_blank" rel="noopener" title="LinkedIn" style="color:var(--muted);font-size:1.5rem">
                <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
            </a>
            <a href="https://twitter.com/gauravmalhotra" target="_blank" rel="noopener" title="Twitter / X" style="color:var(--muted);font-size:1.5rem">
                <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
            </a>
            <a href="https://youtube.com/@grcwithgaurav" target="_blank" rel="noopener" title="YouTube" style="color:var(--muted);font-size:1.5rem">
                <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
            </a>
        </div>"""

if old_footer_links in c:
    c = c.replace(old_footer_links, new_footer_links, 1)
    open(base_html, "w", encoding="utf-8").write(c)
    print("[UPDATED] Footer: added /about, /contact, /faq links + social icons")
else:
    print("[WARN] Footer pattern mismatch - checking current state")
    # Show what we have
    if 'href="/about"' in c:
        print("  /about link: already present")
    if 'linkedin.com' in c:
        print("  LinkedIn icon: already present")
    if 'youtube.com' in c:
        print("  YouTube icon: already present")

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Discoverability: footer links to About/Contact/FAQ + social icons"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout if r.returncode == 0 else r.stderr}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
