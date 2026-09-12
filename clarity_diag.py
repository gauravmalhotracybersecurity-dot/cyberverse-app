import urllib.request, subprocess

# 1. Verify the Clarity tag endpoint is alive (project active?)
try:
    r = urllib.request.urlopen("https://www.clarity.ms/tag/xl9b4c7mdv", timeout=20)
    body = r.read()
    print(f"[TAG] status={r.status}, bytes={len(body)} -> project is {'ACTIVE' if r.status == 200 and len(body) > 100 else 'SUSPECT'}")
except Exception as e:
    print(f"[TAG] ERROR: {e}  <-- project ID may be wrong/paused")

# 2. Verify main site snippet is well-formed on live HTML
req = urllib.request.Request("https://grcwithgaurav.com/", headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
i = html.find("clarity.ms")
print(f"\n[MAIN SITE] snippet found: {'YES' if i >= 0 else 'NO'}")
if i >= 0:
    print(html[i-250:i+150].replace("\n", " | ")[:400])

# 3. Check CSP header blocking inline scripts
r = urllib.request.urlopen(req, timeout=20)
csp = r.headers.get("Content-Security-Policy")
print(f"\n[CSP] header: {csp if csp else 'none (good)'}")

# 4. THE GAP: add Clarity to frontend/app.html
app = "frontend/app.html"
c = open(app, encoding="utf-8").read()
if "clarity.ms" not in c:
    snippet = '''
    <!-- Microsoft Clarity -->
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){
            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        })(window, document, "clarity", "script", "xl9b4c7mdv");
    </script>
'''
    idx = c.find("</head>")
    if idx > 0:
        c = c[:idx] + snippet + c[idx:]
        open(app, "w", encoding="utf-8").write(c)
        print("\n[ADDED] Clarity to frontend/app.html (product analytics now live)")
        subprocess.run(["git", "add", "-A"])
        r = subprocess.run(["git", "commit", "-m", "Analytics: add Clarity to app.html (product usage tracking)"], capture_output=True, text=True)
        print(f"[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
        r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
        print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
    else:
        print("\n[ERROR] </head> not found in app.html")
else:
    print("\n[SKIP] app.html already has Clarity")
