import subprocess, sys
from collections import Counter

# 0. REAL duplicate check (top-level article entries only)
sys.path.insert(0, "backend")
from content import articles
slugs = [a["slug"] for a in articles.ARTICLES]
real_dups = [s for s, n in Counter(slugs).items() if n > 1]
print(f"ARTICLES entries: {len(slugs)}, unique: {len(set(slugs))}, real dups: {real_dups if real_dups else 'none'}")

# 1. Append slug-dedupe to articles.py (fixes hub listings + sitemap + route collisions)
ap = "backend/content/articles.py"
c = open(ap, encoding="utf-8").read()
if "_deduped" not in c:
    c += '''

# De-duplicate articles by slug (keeps first occurrence)
_seen = set()
_deduped = []
for _a in ARTICLES:
    if _a["slug"] not in _seen:
        _seen.add(_a["slug"])
        _deduped.append(_a)
ARTICLES = _deduped
'''
    open(ap, "w", encoding="utf-8").write(c)
    print("[UPDATED] articles.py - slug dedupe appended")
else:
    print("[SKIP] dedupe already present")

# 2. Sitemap: add /careers + /faq
sr = "backend/routers/site_routes.py"
c = open(sr, encoding="utf-8").read()

old_paths = '    paths = ["/", "/tools", "/learn", "/about", "/resources", "/contact", "/b2b"] + TOOL_PATHS + ["/learn/" + a["slug"] for a in ARTICLES]'
new_paths = '    paths = ["/", "/tools", "/learn", "/about", "/resources", "/contact", "/b2b", "/careers", "/faq"] + TOOL_PATHS + ["/learn/" + a["slug"] for a in ARTICLES]'
if old_paths in c:
    c = c.replace(old_paths, new_paths, 1)
    print("[UPDATED] sitemap paths + /careers + /faq")
else:
    print("[WARN] paths line not matched")

# 3. Sitemap: dedupe + per-article lastmod
old_loop = '''    items = ""
    for p in paths:
        items += "<url><loc>" + BASE_URL + p + "</loc><lastmod>2026-09-03</lastmod><changefreq>weekly</changefreq></url>"'''
new_loop = '''    seen = set()
    items = ""
    for p in paths:
        if p in seen:
            continue
        seen.add(p)
        lm = "2026-09-11"
        for a in ARTICLES:
            if p == "/learn/" + a["slug"]:
                lm = a.get("date", "2026-09-11")
                break
        items += "<url><loc>" + BASE_URL + p + "</loc><lastmod>" + lm + "</lastmod><changefreq>weekly</changefreq></url>"'''
if old_loop in c:
    c = c.replace(old_loop, new_loop, 1)
    print("[UPDATED] sitemap loop - dedupe + fresh lastmod per article")
else:
    print("[WARN] loop not matched")

# 4. Robots: block admin routes
old_robots = r'    txt = "User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /admin.html\nDisallow: /app.html\n\nSitemap: " + BASE_URL + "/sitemap.xml\n"'
new_robots = r'    txt = "User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /admin.html\nDisallow: /app.html\nDisallow: /admin-payments\nDisallow: /admin-leads\n\nSitemap: " + BASE_URL + "/sitemap.xml\n"'
if old_robots in c:
    c = c.replace(old_robots, new_robots, 1)
    print("[UPDATED] robots.txt - admin routes blocked")
else:
    print("[WARN] robots line not matched")

# 5. Compile check
try:
    compile(c, sr, "exec")
    compile(open(ap, encoding="utf-8").read(), ap, "exec")
    print("[COMPILE] both files clean")
except SyntaxError as e:
    print(f"[ABORT] {e}")
    raise SystemExit(1)

open(sr, "w", encoding="utf-8").write(c)

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "SEO: sitemap +careers +faq, dedupe, fresh lastmod; robots blocks admin"], capture_output=True, text=True)
print(f"[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
