import subprocess

print("=== FIXING MOBILE PRICING LAYOUT ===\n")

# === 1. Homepage: replace inline grid styles with responsive classes ===
idx_path = "backend/templates/index.html"
idx = open(idx_path, encoding="utf-8").read()

old_grid = '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;max-width:950px;margin:0 auto">'
new_grid = '<div class="pricing-grid">'
if old_grid in idx:
    idx = idx.replace(old_grid, new_grid, 1)
    print("[FIX] homepage: 3-col inline grid -> .pricing-grid class")
else:
    print("[CHECK] homepage grid pattern not found")

old_wrap = '<div style="max-width:900px;margin:2.5rem auto 0;padding:2rem;background:linear-gradient(135deg,#0d1a16,#0a0a0a);border:1px solid var(--accent);border-radius:16px">'
new_wrap = '<div class="pricing-wrap">'
if old_wrap in idx:
    idx = idx.replace(old_wrap, new_wrap, 1)
    print("[FIX] homepage: wrapper inline style -> .pricing-wrap class")

open(idx_path, "w", encoding="utf-8").write(idx)

# === 2. base.html: responsive CSS (stacks columns on mobile) ===
base_path = "backend/templates/base.html"
base = open(base_path, encoding="utf-8").read()
if "/*pricing-responsive*/" not in base:
    css = '''
<style>
/*pricing-responsive*/
.pricing-wrap { max-width:900px; margin:2.5rem auto 0; padding:2rem; background:linear-gradient(135deg,#0d1a16,#0a0a0a); border:1px solid var(--accent); border-radius:16px; }
.pricing-grid { display:grid; grid-template-columns:1fr 1fr 1fr; gap:1rem; max-width:950px; margin:0 auto; }
@media (max-width: 900px) {
  .pricing-wrap { padding:1.2rem; margin:2rem .8rem 0; }
  .pricing-grid { grid-template-columns:1fr; max-width:520px; margin:0 auto; gap:1.4rem; }
}
</style>
'''
    h = base.find("</head>")
    base = base[:h] + css + base[h:]
    open(base_path, "w", encoding="utf-8").write(base)
    print("[ADDED] responsive pricing CSS to base.html")
else:
    print("[SKIP] pricing CSS already in base.html")

# === 3. app.html: same fix for the 2-col pricing grid ===
app_path = "frontend/app.html"
app = open(app_path, encoding="utf-8").read()

old_app_grid = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;max-width:750px;margin:0 auto">'
new_app_grid = '<div class="app-pricing-grid">'
if old_app_grid in app:
    app = app.replace(old_app_grid, new_app_grid, 1)
    print("[FIX] app.html: 2-col inline grid -> .app-pricing-grid class")

if "/*app-pricing-responsive*/" not in app:
    css2 = '''
<style>
/*app-pricing-responsive*/
.app-pricing-grid { display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; max-width:750px; margin:0 auto; }
@media (max-width: 860px) {
  .app-pricing-grid { grid-template-columns:1fr; max-width:520px; margin:0 auto; }
}
</style>
'''
    h = app.find("</head>")
    app = app[:h] + css2 + app[h:]
    print("[ADDED] responsive app pricing CSS")

open(app_path, "w", encoding="utf-8").write(app)

# === 4. Commit + push ===
print("\n=== COMMIT + PUSH ===")
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Mobile: responsive pricing grids (stack Free/Pro/Premium on small screens)"], capture_output=True, text=True)
print(r.stdout.strip() if r.returncode == 0 else r.stderr.strip())
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
