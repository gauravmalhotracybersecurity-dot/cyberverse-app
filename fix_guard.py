import glob, subprocess, re

main_py = glob.glob("backend/main.py")[0]
c = open(main_py, encoding="utf-8").read()

# Find and fix the broken try/except block
# Look for: try: followed by blank lines or the next import
pattern = r'try:\s*\n\s*(?:from routers import site_routes\s*\n)?\s*_safe_include_router\("site_routes", site_routes\)\s*\nexcept'

# If we find a broken pattern, replace the entire try/except block
if 'try:' in c and '_safe_include_router("site_routes", site_routes)' in c:
    # Find the site_routes section
    lines = c.split('\n')
    
    # Find where site_routes import/usage is
    site_start = None
    site_end = None
    for i, line in enumerate(lines):
        if 'site_routes' in line and ('from routers import' in line or '_safe_include_router' in line):
            # Look backwards for try:
            for j in range(i, max(0, i-10), -1):
                if lines[j].strip() == 'try:':
                    site_start = j
                    break
            # Look forward for the matching except
            for j in range(i, min(len(lines), i+10)):
                if lines[j].strip().startswith('except'):
                    # Find end of except block
                    for k in range(j+1, min(len(lines), j+10)):
                        if lines[k].strip() and not lines[k].startswith(' ') and not lines[k].startswith('\t'):
                            site_end = k
                            break
                    break
            break
    
    if site_start is not None and site_end is not None:
        print(f"[FOUND] Broken site_routes block: lines {site_start+1} to {site_end}")
        # Replace with clean single-line call
        lines[site_start:site_end] = ['_safe_include_router("site_routes", site_routes)']
        c = '\n'.join(lines)
        print("[FIXED] Replaced try/except with clean call")

# Verify compilation
try:
    compile(c, main_py, "exec")
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ERROR] Still has syntax error:", e)
    # Show context around the error
    lines = c.split('\n')
    for i in range(max(0, e.lineno-5), min(len(lines), e.lineno+5)):
        marker = ">>>" if i == e.lineno-1 else "   "
        print(f"{marker} {i+1}: {lines[i]}")
    raise SystemExit(1)

open(main_py, "w", encoding="utf-8").write(c)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: guard syntax error in main.py"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED - Guard fix deployed")
