import subprocess, re, os

print("=== DEFINITIVE DIAGNOSIS + FIX ===\n")

# 1. Check what's actually in base.html right now
print("1. CHECKING base.html CANONICAL BLOCK:")
with open("backend/templates/base.html", "r", encoding="utf-8") as f:
    base = f.read()

m = re.search(r'{% block canonical %}.*?{% endblock %}', base, re.DOTALL)
if m:
    print(f"   Current: {m.group(0)}")
    has_rstrip = 'rstrip' in m.group(0)
    print(f"   Has rstrip fix: {'YES ✅' if has_rstrip else 'NO ❌'}")
else:
    print("   NO CANONICAL BLOCK FOUND")

# 2. Check how tool routes are defined in main.py
print("\n2. CHECKING TOOL ROUTE DEFINITIONS:")
with open("backend/main.py", "r", encoding="utf-8") as f:
    main = f.read()

tool_routes = re.findall(r'@app\.get\(["\']\/tools\/[^"\']+["\']', main)
print(f"   Found {len(tool_routes)} tool route definitions:")
for route in tool_routes[:5]:
    has_slash = route.endswith('/"') or route.endswith("/'")
    print(f"   {route}  {'❌ HAS SLASH' if has_slash else '✅ no slash'}")

# 3. Apply the fix to base.html if not already done
print("\n3. APPLYING BASE.HTML FIX:")
old_canon = '{% block canonical %}https://grcwithgaurav.com{{ request.url.path }}{% endblock %}'
new_canon = '{% block canonical %}https://grcwithgaurav.com{{ request.url.path.rstrip("/") }}{% endblock %}'

if old_canon in base:
    base = base.replace(old_canon, new_canon)
    with open("backend/templates/base.html", "w", encoding="utf-8") as f:
        f.write(base)
    print("   [FIXED] Added rstrip to canonical block")
elif new_canon in base:
    print("   [SKIP] Fix already applied")
else:
    print("   [CHECK] Pattern not found - manual review needed")

# 4. Commit and push
print("\n4. COMMIT + PUSH:")
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "SEO: ensure base.html canonical strips trailing slashes"], capture_output=True, text=True)
print(f"   {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print(f"   {'[PUSHED]' if r.returncode == 0 else f'[PUSH FAILED] {r.stderr}'}")

print("\n" + "="*70)
print("⚠️  CRITICAL NEXT STEP: MANUAL DEPLOY REQUIRED")
print("="*70)
print("1. Go to Render Dashboard → your web service → Deploys tab")
print("2. Click 'Manual Deploy' → 'Deploy latest commit'")
print("3. Wait for status to show 'Live' (green)")
print("4. Then run the verify script below")
