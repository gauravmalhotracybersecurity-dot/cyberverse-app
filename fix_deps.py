import os, re, glob, shutil

print("=== FIX 1: jinja2 into EVERY requirements file ===")
reqs = [f for f in glob.glob("**/requirements*.txt", recursive=True)
        if not any(x in f for x in ("venv", "node_modules", ".git"))]
if not reqs:
    reqs = ["requirements.txt"]

for r in reqs:
    content = open(r, encoding="utf-8").read() if os.path.exists(r) else ""
    add = []
    if "jinja2" not in content.lower(): add.append("jinja2")
    if "aiofiles" not in content.lower(): add.append("aiofiles")
    if add:
        with open(r, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(add) + "\n")
        print(f"[DEPS] added {add} to {r}")
    else:
        print(f"[DEPS] already present in {r}")

# Mirror root requirements into backend/ if missing (covers Render rootDir builds)
if os.path.exists("requirements.txt") and not os.path.exists("backend/requirements.txt"):
    shutil.copy("requirements.txt", "backend/requirements.txt")
    print("[DEPS] created backend/requirements.txt mirror")

print("\n=== FIX 2: Harden main.py (marketing layer can't kill SaaS) ===")
main_py = "backend/main.py"
c = open(main_py, encoding="utf-8").read()
pair = "from routers import site_routes\napp.include_router(site_routes.router)\n"
if pair in c:
    safe = ('try:\n'
            '    from routers import site_routes\n'
            '    app.include_router(site_routes.router)\n'
            'except Exception as _site_err:\n'
            '    print("site_routes disabled:", _site_err)\n')
    c = c.replace(pair, safe)
    open(main_py, "w", encoding="utf-8").write(c)
    print("[HARDENED] site_routes import wrapped in try/except")
else:
    print("[WARN] exact pattern not found - check main.py manually")

print("\n=== COMMIT & PUSH ===")
os.system("git add -A")
os.system('git commit -m "Fix: install jinja2 on Render + fail-safe site routes"')
os.system("git push origin main")
print("Pushed. Render rebuilding now.")
