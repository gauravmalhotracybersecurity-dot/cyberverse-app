import subprocess
p = "backend/routers/analytics_routes.py"
log = subprocess.run(["git", "log", "--format=%h", "--", p], capture_output=True, text=True).stdout.split()
good = None
for h in log:
    src = subprocess.run(["git", "show", h + ":" + p], capture_output=True, text=True).stdout
    try:
        compile(src, p, "exec")
        good = h
        break
    except Exception:
        pass
print("GOOD COMMIT: " + str(good))
if good:
    src = subprocess.run(["git", "show", good + ":" + p], capture_output=True, text=True).stdout
    open(p, "w", encoding="utf-8").write(src)
    subprocess.run(["git", "add", "-A"])
    subprocess.run(["git", "commit", "-m", "Restore last compiling analytics_routes.py"])
    subprocess.run(["git", "push", "origin", "main"])
    print("PUSHED")
else:
    print("NO COMPILING VERSION IN HISTORY")
