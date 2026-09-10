import subprocess

p = "backend/templates/base.html"
lines = open(p, encoding="utf-8").read().split("\n")

if any("clarity.ms" in l for l in lines):
    print("[SKIP] Clarity already installed")
else:
    # Find </head> and insert Clarity script before it
    idx = None
    for i, l in enumerate(lines):
        if "</head>" in l:
            idx = i
            break
    
    if idx is None:
        print("[ERROR] </head> not found")
        raise SystemExit(1)
    
    clarity_script = [
        '',
        '    <!-- Microsoft Clarity -->',
        '    <script type="text/javascript">',
        '        (function(c,l,a,r,i,t,y){',
        '            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};',
        '            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;',
        '            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);',
        '        })(window, document, "clarity", "script", "xl9b4c7mdv");',
        '    </script>',
    ]
    
    lines[idx:idx] = clarity_script
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    print(f"[INSERTED] Clarity script before </head> at line {idx}")

c = open(p, encoding="utf-8").read()
print(f"  local clarity script: {'YES' if 'clarity.ms' in c else 'NO'}")
print(f"  project ID xl9b4c7mdv: {'YES' if 'xl9b4c7mdv' in c else 'NO'}")

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Analytics: add Microsoft Clarity tracking (project xl9b4c7mdv)"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
