import glob, subprocess, re
sr = glob.glob("backend/routers/site_routes.py")[0]
c = open(sr, encoding="utf-8").read()
lines = c.split('\n')

# Find all undefined names used in function signatures
print("=== SCANNING FOR MISSING IMPORTS ===")

# Check for get_db usage
if 'get_db' in c and 'get_db' not in '\n'.join(lines[:20]):
    print("✗ get_db is used but not imported")
    
# Check for Session usage
if 'Session' in c and 'from sqlalchemy.orm' not in c:
    print("✗ Session is used but not imported")
    
# Check for models usage
if 'models.' in c and 'import models' not in c and 'from models' not in c:
    print("✗ models is used but not imported")

# Add missing imports after line 4 (after the fastapi.responses import)
insert_pos = 4  # After "from fastapi.responses import HTMLResponse, Response, RedirectResponse"

new_imports = [
    "from sqlalchemy.orm import Session",
    "from database import get_db",
    "import models"
]

# Check what's already imported
existing_imports = '\n'.join(lines[:20])
to_add = []

if 'from sqlalchemy.orm' not in existing_imports and 'Session' in c:
    to_add.append("from sqlalchemy.orm import Session")
    
if 'get_db' not in existing_imports and 'get_db' in c:
    to_add.append("from database import get_db")
    
if 'import models' not in existing_imports and 'models.' in c:
    to_add.append("import models")

if to_add:
    print(f"\nAdding {len(to_add)} missing imports:")
    for imp in to_add:
        print(f"  + {imp}")
    
    # Insert after line 4
    for imp in reversed(to_add):
        lines.insert(insert_pos + 1, imp)
    
    c = '\n'.join(lines)
    open(sr, "w", encoding="utf-8").write(c)
    print("\n[ADDED] Missing imports")
else:
    print("\n[SKIP] All imports present")

# Verify it compiles
try:
    compile(c, sr, "exec")
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: add get_db, Session, and models imports to site_routes"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED - Render will redeploy in ~60s")
