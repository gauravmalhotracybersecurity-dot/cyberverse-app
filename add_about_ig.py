import subprocess

p = "backend/templates/about.html"
c = open(p, encoding="utf-8").read()
IG_URL = "https://www.instagram.com/cyberverse.ai.official/"

if "instagram.com" in c:
    print("[SKIP] Instagram already on About page")
else:
    # Find the LinkedIn button line
    lines = c.split("\n")
    idx = None
    for i, l in enumerate(lines):
        if 'href="https://www.linkedin.com/in/gaurav-malhotra-3419124b"' in l:
            idx = i
            break
    
    if idx is None:
        print("[ERROR] LinkedIn button not found")
        raise SystemExit(1)
    
    # Create Instagram button matching LinkedIn style
    ig_btn = lines[idx].replace(
        'href="https://www.linkedin.com/in/gaurav-malhotra-3419124b"',
        f'href="{IG_URL}"'
    ).replace(">LinkedIn<", ">Instagram<").replace('background:#0077b5', 'background:#E1306C')
    
    # Insert after LinkedIn button with same margin-right style
    ig_btn = ig_btn.replace('margin-right:.5rem', 'margin-right:0')
    lines.insert(idx + 1, ig_btn)
    
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    print(f"[INSERTED] Instagram button on About page after line {idx+1}")

c = open(p, encoding="utf-8").read()
print(f"  About page has instagram button: {'YES' if 'instagram.com' in c else 'NO'}")
print(f"  About page has linkedin button: {'YES' if 'linkedin.com/in/gaurav-malhotra-3419124b' in c else 'NO'}")

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "About: add Instagram button next to LinkedIn"], capture_output=True, text=True)
print(f"[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
