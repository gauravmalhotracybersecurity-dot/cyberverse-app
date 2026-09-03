import subprocess

# 1. Repoint homepage cards to real content
p = "backend/templates/index.html"
c = open(p, encoding="utf-8").read()
c = c.replace('href="/learn/soc"', 'href="/learn"')
c = c.replace('href="/learn/grc"', 'href="/learn/what-is-iso-27001"')
open(p, "w", encoding="utf-8").write(c)
print("[FIXED] homepage Learn cards repointed")

# 2. Soft-redirect unknown /learn slugs to the hub (no more dead ends)
sr = "backend/routers/site_routes.py"
r = open(sr, encoding="utf-8").read()
r = r.replace("from fastapi.responses import HTMLResponse, Response",
              "from fastapi.responses import HTMLResponse, Response, RedirectResponse")
r = r.replace('raise HTTPException(status_code=404, detail="Article not found")',
              'return RedirectResponse(url="/learn", status_code=302)')
open(sr, "w", encoding="utf-8").write(r)
print("[FIXED] unknown /learn slugs now redirect to /learn")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: repoint learn links + soft-redirect unknown slugs"])
subprocess.run(["git", "push", "origin", "main"])
print("Pushed. Live in ~60s.")
