import subprocess, os

src_photo = r"C:\Users\hp\Downloads\Confident Executive Portrait with Watch.png"
dest = "backend/static/gaurav.jpg"

if not os.path.exists(src_photo):
    print(f"[ERROR] Source photo not found: {src_photo}")
    raise SystemExit(1)
print(f"[FOUND] source photo ({os.path.getsize(src_photo)} bytes)")

os.makedirs("backend/static", exist_ok=True)

# Convert PNG -> optimized JPG
try:
    from PIL import Image
    img = Image.open(src_photo)
    if img.mode != "RGB":
        img = img.convert("RGB")
    if img.width > 900:
        ratio = 900 / img.width
        img = img.resize((900, int(img.height * ratio)), Image.LANCZOS)
    img.save(dest, "JPEG", quality=85, optimize=True)
    print(f"[CONVERTED] {dest} - {img.width}px wide, {os.path.getsize(dest)} bytes")
except ImportError:
    # Fallback: raw copy (PNG served as .jpg still renders in browsers, but Pillow path is preferred)
    import shutil
    shutil.copyfile(src_photo, dest)
    print(f"[COPIED] raw file to {dest}")

# Replace GM placeholder in about.html
p = "backend/templates/about.html"
lines = open(p, encoding="utf-8").read().split("\n")
idx = None
for i, l in enumerate(lines):
    if ">GM</span>" in l:
        idx = i
        break

if idx is None:
    print("[SKIP] GM placeholder not found - already replaced?")
else:
    img_line = '   <img src="/static/gaurav.jpg" alt="Gaurav Malhotra - Cybersecurity & GRC Professional" style="width:100%;aspect-ratio:1;object-fit:cover;object-position:center 20%;border-radius:12px;border:2px solid var(--accent)">'
    lines[idx-1:idx+2] = [img_line]
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    print("[UPDATED] about.html - real photo replaces GM placeholder")

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "About: add founder photo (optimized JPG) replacing GM placeholder"], capture_output=True, text=True)
print(f"[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
