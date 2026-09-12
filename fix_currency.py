import subprocess

def upd(path, pairs, label):
    c = open(path, encoding="utf-8").read()
    hits = 0
    for old, new in pairs:
        if old in c:
            c = c.replace(old, new)
            hits += 1
    if hits:
        open(path, "w", encoding="utf-8").write(c)
        print(f"[UPDATED] {label} ({hits} replacements)")
    else:
        print(f"[SKIP] {label} (no matches)")

# === 1. Homepage pricing: add USD equivalents + international note ===
upd("backend/templates/index.html", [
    ("499", "499 (≈ $6)"),
    ("999", "999 (≈ $12)"),
    ("7-day money-back guarantee. One-time payment, lifetime access.",
     "7-day money-back guarantee. One-time payment, lifetime access. Priced in INR — international cards accepted (499 ≈ $6, 999 ≈ $12 USD at checkout)."),
], "homepage pricing")

# === 2. App: modal button, nudge, pricing header, guarantee line ===
upd("frontend/app.html", [
    ("Upgrade to Pro — 499", "Upgrade to Pro — 499 (≈ $6)"),
    ("Pro (499 lifetime)", "Pro (499 ≈ $6, lifetime)"),
    ('<h4 style="color:var(--accent);margin:0 0 .5rem">Pro</h4>',
     '<h4 style="color:var(--accent);margin:0 0 .5rem">Pro — 499 (≈ $6)</h4>'),
    ("7-day money-back guarantee. Cancel anytime.",
     "7-day money-back guarantee. One-time payment, lifetime access."),
], "app pricing + freemium modal")

# === 3. FAQ: add USD equivalents wherever prices appear ===
upd("backend/templates/faq.html", [
    ("499", "499 (≈ $6 USD)"),
    ("999", "999 (≈ $12 USD)"),
], "FAQ pricing")

# === 4. Commit + push ===
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Pricing: add USD equivalents for international buyers (499 ≈ $6, 999 ≈ $12)"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
