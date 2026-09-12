import subprocess, re

print("=== ADDING CLARITY TRACKING ===\n")

# === 1. Add Clarity to base.html (main site) ===
base_path = "backend/templates/base.html"
base = open(base_path, encoding="utf-8").read()

if "clarity.ms/tag" not in base:
    clarity_snippet = '''    <!-- Microsoft Clarity -->
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){
            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        })(window, document, "clarity", "script", "xl9b4c7mdv");
    </script>
'''
    # Insert before </head>
    head_end = base.find("</head>")
    if head_end > 0:
        base = base[:head_end] + clarity_snippet + base[head_end:]
        open(base_path, "w", encoding="utf-8").write(base)
        print("[ADDED] Clarity to base.html")
    else:
        print("[ERROR] Could not find </head> in base.html")
else:
    print("[SKIP] Clarity already in base.html")

# === 2. Add Clarity to app.html (app subdomain) ===
app_path = "frontend/app.html"
app = open(app_path, encoding="utf-8").read()

if "clarity.ms/tag" not in app:
    clarity_snippet = '''
    <!-- Microsoft Clarity -->
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){
            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        })(window, document, "clarity", "script", "xl9b4c7mdv");
    </script>
'''
    # Insert before </head>
    head_end = app.find("</head>")
    if head_end > 0:
        app = app[:head_end] + clarity_snippet + app[head_end:]
        open(app_path, "w", encoding="utf-8").write(app)
        print("[ADDED] Clarity to app.html")
    else:
        print("[ERROR] Could not find </head> in app.html")
else:
    print("[SKIP] Clarity already in app.html")

# === 3. Check for CSP in backend code ===
print("\n=== CHECKING CSP CONFIGURATION ===")

# Check main.py or app.py for CSP headers
import os
for root, dirs, files in os.walk("backend"):
    for f in files:
        if f.endswith(".py"):
            filepath = os.path.join(root, f)
            try:
                content = open(filepath, encoding="utf-8").read()
                if "Content-Security-Policy" in content or "CSP" in content.upper():
                    print(f"Found CSP in: {filepath}")
                    # Show context
                    idx = content.find("Content-Security-Policy")
                    if idx < 0:
                        idx = content.find("CSP")
                    if idx >= 0:
                        print(content[max(0, idx-100):idx+300])
            except:
                pass

print("\n=== COMMIT + PUSH ===")
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Add Microsoft Clarity tracking to main site and app"], capture_output=True, text=True)
print(r.stdout.strip() if r.returncode == 0 else r.stderr.strip())
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
