import subprocess, os

# Generate og-default.jpg using Pillow
script = """
from PIL import Image, ImageDraw, ImageFont
import os

# Create 1200x630 image (Open Graph standard)
width, height = 1200, 630
img = Image.new('RGB', (width, height), color='#0a0a0a')
draw = ImageDraw.Draw(img)

# Add gradient effect (simple vertical gradient)
for y in range(height):
    # Dark blue to dark purple gradient
    r = int(10 + (y / height) * 20)
    g = int(10 + (y / height) * 15)
    b = int(10 + (y / height) * 40)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# Add logo text "GRC"
try:
    # Try to use a default font
    font_large = ImageFont.truetype("arial.ttf", 120)
    font_medium = ImageFont.truetype("arial.ttf", 48)
    font_small = ImageFont.truetype("arial.ttf", 32)
except:
    # Fallback to default font
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Draw "GRCWithGaurav"
text = "GRCWithGaurav"
bbox = draw.textbbox((0, 0), text, font=font_large)
text_width = bbox[2] - bbox[0]
x = (width - text_width) // 2
y = 150
draw.text((x, y), text, fill='#00ffcc', font=font_large)

# Draw tagline
tagline = "Cybersecurity & GRC Career Platform"
bbox = draw.textbbox((0, 0), tagline, font=font_medium)
text_width = bbox[2] - bbox[0]
x = (width - text_width) // 2
y = 320
draw.text((x, y), tagline, fill='#e0e0e0', font=font_medium)

# Draw features
features = "10 Free Tools + AI Mock Interviews"
bbox = draw.textbbox((0, 0), features, font=font_small)
text_width = bbox[2] - bbox[0]
x = (width - text_width) // 2
y = 420
# Draw rounded rectangle background for badge
padding = 20
draw.rounded_rectangle(
    [(x - padding, y - padding//2), (x + text_width + padding, y + 40 + padding//2)],
    radius=25,
    fill='#00ffcc'
)
draw.text((x, y), features, fill='#000000', font=font_small)

# Save
os.makedirs('backend/static', exist_ok=True)
img.save('backend/static/og-default.jpg', 'JPEG', quality=95)
print('[CREATED] og-default.jpg (1200x630)')
"""

# Write the generation script
with open('generate_og.py', 'w', encoding='utf-8') as f:
    f.write(script)

# Run it
result = subprocess.run(['python', 'generate_og.py'], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("[ERROR] Pillow generation failed:", result.stderr)
    print("Creating minimal placeholder instead...")
    
    # Create a minimal 1x1 transparent PNG as fallback
    # (Base64 encoded minimal PNG)
    import base64
    minimal_png = base64.b64decode(
        'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
    )
    os.makedirs('backend/static', exist_ok=True)
    with open('backend/static/og-default.jpg', 'wb') as f:
        f.write(minimal_png)
    print("[CREATED] Minimal placeholder og-default.jpg")

# Clean up
os.remove('generate_og.py')

# Now check if we need to mount /static
c = open('backend/main.py', encoding='utf-8').read()
if 'mount("/static"' not in c and "mount('/static'" not in c:
    print("\n[ADD] Mounting /static to serve backend/static files")
    # Find where to insert the mount
    lines = c.split('\n')
    insert_idx = None
    for i, line in enumerate(lines):
        if 'app.mount("/"' in line or "app.mount('/" in line:
            insert_idx = i
            break
    
    if insert_idx:
        # Insert before the frontend mount
        lines.insert(insert_idx, 'app.mount("/static", StaticFiles(directory="backend/static"), name="static")')
        c = '\n'.join(lines)
        open('backend/main.py', 'w', encoding='utf-8').write(c)
        print("[ADDED] /static mount before line", insert_idx + 1)
else:
    print("\n[OK] /static already mounted")

# Commit and push
subprocess.run(['git', 'add', '-A'])
result = subprocess.run(['git', 'commit', '-m', 'SEO: add og-default.jpg image + mount /static'], 
                       capture_output=True, text=True)
print("\n[COMMIT]", result.stdout if result.returncode == 0 else result.stderr)

result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
if result.returncode == 0:
    print("[PUSHED] Deploying to Render")
else:
    print("[PUSH FAILED]", result.stderr)
