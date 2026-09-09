import re, subprocess, os

main_py = "backend/main.py"
c = open(main_py, encoding="utf-8").read()
lines = c.split("\n")

BAD = 'app.mount("/static", StaticFiles(directory="backend/static"), name="static")'

# 1. Remove the badly-inserted line(s)
new_lines, removed = [], 0
for l in lines:
    if l.strip() == BAD:
        removed += 1
        continue
    new_lines.append(l)
lines = new_lines
print(f"[REMOVED] {removed} bad mount line(s)")

# 2. Ensure import os exists near top
head = "\n".join(lines[:40])
if not re.search(r"^\s*import os\b", head, re.M):
    lines.insert(0, "import os")
    print("[ADDED] import os")

# 3. Find frontend mount and walk back to the column-0 statement that owns its block
idx_fe = None
for i, l in enumerate(lines):
    if 'app.mount("/", StaticFiles(' in l:
        idx_fe = i
        break
if idx_fe is None:
    for i, l in enumerate(lines):
        if "app = FastAPI(" in l:
            idx_fe = i + 1
            break

k = idx_fe
while k >= 0 and (lines[k][:1] in (" ", "\t") or lines[k].strip() == ""):
    k -= 1
insert_at = k
print(f"[INSERT] before line {insert_at+1}: {lines[insert_at].strip()[:60]}")

# 4. Insert guarded static mount at column 0 (crash-proof: skips if dir missing)
block = [
    '_static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")',
    'if os.path.isdir(_static_dir):',
    '    app.mount("/static", StaticFiles(directory=_static_dir), name="static")',
    '',
]
lines[insert_at:insert_at] = block

c = "\n".join(lines)

# 5. Compile check BEFORE writing
try:
    compile(c, main_py, "exec")
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error:", e)
    raise SystemExit(1)

open(main_py, "w", encoding="utf-8").write(c)
print("[SAVED] main.py fixed")

# 6. Try regenerating proper og image (only if Pillow installed)
try:
    from PIL import Image, ImageDraw, ImageFont
    width, height = 1200, 630
    img = Image.new("RGB", (width, height), (10, 10, 10))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        draw.line([(0, y), (width, y)], fill=(int(10 + y/height*20), int(10 + y/height*15), int(10 + y/height*40)))
    try:
        f1 = ImageFont.truetype("arial.ttf", 100); f2 = ImageFont.truetype("arial.ttf", 40); f3 = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        f1 = f2 = f3 = ImageFont.load_default()
    for text, font, fill, y in [("GRCWithGaurav", f1, (0,255,204), 150), ("Cybersecurity & GRC Career Platform", f2, (224,224,224), 320)]:
        bb = draw.textbbox((0,0), text, font=font); draw.text(((width-(bb[2]-bb[0]))//2, y), text, fill=fill, font=font)
    t = "10 Free Tools + AI Mock Interviews"; bb = draw.textbbox((0,0), t, font=f3); tw = bb[2]-bb[0]; x = (width-tw)//2
    draw.rounded_rectangle([(x-20, 410), (x+tw+20, 470)], radius=25, fill=(0,255,204))
    draw.text((x, 420), t, fill=(0,0,0), font=f3)
    img.save("backend/static/og-default.jpg", "JPEG", quality=95)
    print("[CREATED] proper og-default.jpg (1200x630)")
except ImportError:
    print("[NOTE] Pillow not installed - keeping placeholder image (fine for now)")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: indentation-safe /static mount (guarded, absolute path)"])
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else "[PUSH FAILED] " + r.stderr)
