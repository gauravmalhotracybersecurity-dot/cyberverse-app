import subprocess

print("=== FIXING CSP AND ADDING CLARITY ===\n")

# === 1. Update CSP in main.py to allow Clarity ===
main_py = "backend/main.py"
c = open(main_py, encoding="utf-8").read()

old_csp = '''response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "frame-src https://api.razorpay.com https://checkout.razorpay.com; script-src 'self' 'unsafe-inline' https://checkout.razorpay.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "'''

new_csp = '''response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "frame-src https://api.razorpay.com https://checkout.razorpay.com; script-src 'self' 'unsafe-inline' https://checkout.razorpay.com https://www.clarity.ms https://*.clarity.ms; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "connect-src 'self' https://www.clarity.ms https://*.clarity.ms; "'''

if old_csp in c:
    c = c.replace(old_csp, new_csp)
    open(main_py, "w", encoding="utf-8").write(c)
    print("[FIX] Updated CSP to allow Clarity domains")
else:
    print("[SKIP] CSP already updated or pattern not found")

# === 2. Add Clarity snippet to base.html ===
base_html = "backend/templates/base.html"
b = open(base_html, encoding="utf-8").read()

if "clarity.ms/tag/xl9b4c7mdv" not in b:
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
    head_end = b.find("</head>")
    if head_end > 0:
        b = b[:head_end] + clarity_snippet + b[head_end:]
        open(base_html, "w", encoding="utf-8").write(b)
        print("[ADDED] Clarity to base.html")
    else:
        print("[ERROR] Could not find </head> in base.html")
else:
    print("[SKIP] Clarity already in base.html")

# === 3. Add Clarity snippet to app.html ===
app_html = "frontend/app.html"
a = open(app_html, encoding="utf-8").read()

if "clarity.ms/tag/xl9b4c7mdv" not in a:
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
    head_end = a.find("</head>")
    if head_end > 0:
        a = a[:head_end] + clarity_snippet + a[head_end:]
        open(app_html, "w", encoding="utf-8").write(a)
        print("[ADDED] Clarity to app.html")
    else:
        print("[ERROR] Could not find </head> in app.html")
else:
    print("[SKIP] Clarity already in app.html")

# === 4. Commit and push ===
print("\n=== COMMIT + PUSH ===")
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Fix CSP to allow Clarity + add Clarity tracking to all pages"], capture_output=True, text=True)
print(r.stdout.strip() if r.returncode == 0 else r.stderr.strip())
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
