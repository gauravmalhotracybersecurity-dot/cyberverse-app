import glob, re, subprocess
skip = ("venv", "node_modules", ".git")

# 1. Remove public Admin link(s) from footer
bh = [x for x in glob.glob("**/base.html", recursive=True) if not any(t in x for t in skip)][0]
b = open(bh, encoding="utf-8").read()
b2 = re.sub(r'<a[^>]*href="/admin-leads"[^>]*>[^<]*</a>', '', b)
b2 = re.sub(r'<a[^>]*href="/admin-payments"[^>]*>[^<]*</a>', '', b2)
if b2 != b:
    open(bh, "w", encoding="utf-8").write(b2)
    print("[FOOTER] public Admin link removed")

# 2. Add admin-only authorization to admin APIs
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

helper = '''def _is_admin(user):
    import os
    raw = os.environ.get("ADMIN_EMAIL", "")
    if raw:
        allowed = {x.strip().lower() for x in raw.replace(";", ",").split(",") if x.strip()}
    else:
        allowed = {"gauravmalhotra.cybersecurity@gmail.com", "gaurav_malhotra86@yahoo.com", "gauravmalhotra86@yahoo.com"}
    em = getattr(user, "email", "") or ""
    return em.lower() in allowed


'''
guard = '\n    if not _is_admin(user):\n        raise HTTPException(status_code=403, detail="Admin only")'

if "_is_admin" not in c:
    anchor = '@router.get("/b2b/leads")'
    if anchor in c:
        c = c.replace(anchor, helper + anchor, 1)
        print("[BACKEND] _is_admin helper added")

targets = [
    'def b2b_leads(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):',
    'def b2b_lead_update(lead_id: int, payload: dict, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):',
    'def b2b_lead_delete(lead_id: int, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):',
    'def admin_payments(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):',
]
n = 0
for t in targets:
    if t in c and (t + guard) not in c:
        c = c.replace(t, t + guard, 1)
        n += 1
print("[BACKEND] admin guards applied to", n, "endpoints")

open(ar, "w", encoding="utf-8").write(c)
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Security: hide admin link + restrict admin APIs to owner email"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
