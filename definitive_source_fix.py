import re, subprocess, os

print("=== DEFINITIVE DIAGNOSIS + SOURCE FIX ===\n")

# 1. Check what's actually in base.html right now
print("1. CHECKING LOCAL base.html:")
with open("backend/templates/base.html", "r", encoding="utf-8") as f:
    base = f.read()

m = re.search(r'{% block canonical %}.*?{% endblock %}', base, re.DOTALL)
if m:
    print(f"   Current block: {m.group(0)}")
    has_rstrip = 'rstrip' in m.group(0)
    print(f"   Has rstrip fix: {'YES' if has_rstrip else 'NO'}")
    
    if not has_rstrip:
        # Apply the fix
        old_block = m.group(0)
        new_block = old_block.replace('{{ request.url.path }}', '{{ request.url.path.rstrip("/") }}')
        base = base.replace(old_block, new_block)
        with open("backend/templates/base.html", "w", encoding="utf-8") as f:
            f.write(base)
        print("   [FIXED] Applied rstrip to base.html")
else:
    print("   [ERROR] No canonical block found!")

# 2. Check for trailing slashes in tool route definitions
print("\n2. CHECKING main.py FOR TOOL ROUTES:")
with open("backend/main.py", "r", encoding="utf-8") as f:
    main = f.read()

# Look for any route definition with /tools/ that has a trailing slash
route_pattern = r'@app\.(get|post)\s*\(\s*["\'](/tools/[^"\']*/?)["\']'
matches = list(re.finditer(route_pattern, main))

print(f"   Found {len(matches)} tool route definitions")
fixed_routes = 0
for match in matches:
    route_path = match.group(2)
    if route_path.endswith('/'):
        print(f"   [FOUND] Route with trailing slash: {route_path}")
        # Remove the trailing slash from the route definition
        new_path = route_path.rstrip('/')
        main = main.replace(f'"{route_path}"', f'"{new_path}"')
        main = main.replace(f"'{route_path}'", f"'{new_path}'")
        fixed_routes += 1

if fixed_routes > 0:
    with open("backend/main.py", "w", encoding="utf-8") as f:
        f.write(main)
    print(f"   [FIXED] Removed trailing slashes from {fixed_routes} route definitions")
else:
    print("   [OK] No trailing slashes found in route definitions")

# 3. Check for Mount or generic tool serving
if "Mount" in main and "/tools" in main:
    print("\n3. CHECKING FOR MOUNT:")
    mount_lines = [line for line in main.split('\n') if 'Mount' in line and 'tools' in line]
    for line in mount_lines:
        print(f"   {line.strip()}")

# 4. Commit and push
print("\n4. COMMIT + PUSH:")
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "SEO: definitive fix - strip trailing slashes from base.html canonical and tool routes"], capture_output=True, text=True)
print(f"   {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print(f"   {'[PUSHED]' if r.returncode == 0 else '[PUSH FAILED]'}")

print("\n" + "="*70)
print("⚠️  CRITICAL NEXT STEP: MANUAL DEPLOY REQUIRED")
print("="*70)
print("1. Go to Render Dashboard → your web service → Deploys tab")
print("2. Click 'Manual Deploy' → 'Deploy latest commit'")
print("3. Wait for status to show 'Live' (green)")
print("4. Then run the verify script below")
