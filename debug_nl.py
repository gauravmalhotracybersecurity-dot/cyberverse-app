import glob, subprocess, os
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

# Add diagnostic endpoint
endpoint = '''

@router.get("/newsletter/debug")
async def nl_debug(request: Request):
    import os as _os
    secret = request.headers.get("x-admin-secret", "")
    if secret != _os.environ.get("ADMIN_SECRET", ""):
        raise HTTPException(status_code=403, detail="Forbidden")
    return {
        "RESEND_API_KEY_set": bool(_os.environ.get("RESEND_API_KEY")),
        "RESEND_API_KEY_prefix": (_os.environ.get("RESEND_API_KEY") or "")[:8] + "...",
        "RESEND_FROM_EMAIL": _os.environ.get("RESEND_FROM_EMAIL"),
        "NL_FROM_constant": NL_FROM,
        "grcwithgaurav.com_domain_verified": "Check Resend dashboard"
    }
'''

if '"/newsletter/debug"' not in c:
    c += endpoint
    try:
        compile(c, ar, "exec")
        open(ar, "w", encoding="utf-8").write(c)
        print("[BACKEND] Debug endpoint added")
    except SyntaxError as e:
        print("[ABORT] Syntax error:", e)
        raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Debug: newsletter config diagnostic endpoint"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
