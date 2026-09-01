import os, glob

print("=== 1. HIDING LEAGUE IN FRONTEND (CSS) ===")
html_files = glob.glob("**/app.html", recursive=True)
html_files = [f for f in html_files if "venv" not in f and "node_modules" not in f]

css_block = """
<style id="disable-league">
/* Remove League/Leaderboard from UI completely */
[data-goto="league"], [data-view="league"], #league-view, #league-tab, 
[id*="league" i], [class*="league" i], a[href*="league" i], button:has(> *:[data-goto="league"]) {
    display: none !important;
}
</style>
"""

for hf in html_files:
    with open(hf, "r", encoding="utf-8") as f:
        content = f.read()
    if "disable-league" not in content:
        content = content.replace("</head>", css_block + "\n</head>")
        with open(hf, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[HIDDEN] League UI removed from {hf}")

print("\n=== 2. NEUTERING LEAGUE BACKEND QUERIES ===")
py_files = glob.glob("backend/routers/*.py", recursive=True)
for pf in py_files:
    with open(pf, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Look for the exact leaderboard queries we found in the X-Ray
    if "order_by(models.User.xp.desc())" in content:
        content = content.replace("rows = db.query(models.User).order_by(models.User.xp.desc()).limit(10).all()", "rows = [] # League disabled")
        content = content.replace("rows = db.query(models.User).order_by(models.User.xp.desc()).limit(20).all()", "rows = [] # League disabled")
        with open(pf, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[NEUTERED] Leaderboard query disabled in {pf}")

print("\n=== 3. COMMIT & PUSH ===")
os.system("git add .")
os.system('git commit -m "Feature: Remove League/Leaderboard to streamline UX"')
os.system("git push origin main")
print("\nPushed! Render will deploy in ~60s.")
