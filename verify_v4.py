import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

old_start = "        ok_api = False\n        if not ok_sig and row and row[1] == user.id and key and sec and payment_id:\n            try:\n                req = _u.Request(\"https://api.razorpay.com/v1/payments/\" + payment_id)"
new_block = """        ok_api = False
        api_err = ""
        if not ok_sig and row and row[1] == user.id and key and sec:
            try:
                pid = payment_id
                if not pid:
                    req0 = _u.Request("https://api.razorpay.com/v1/orders/" + order_id + "/payments")
                    req0.add_header("Authorization", "Basic " + base64.b64encode((key + ":" + sec).encode()).decode())
                    with _u.urlopen(req0, timeout=15) as r0:
                        lst = _j.loads(r0.read())
                    caps = [x for x in (lst.get("items") or []) if x.get("status") == "captured"]
                    if caps:
                        pid = caps[0].get("id")
                if pid:
                    req = _u.Request("https://api.razorpay.com/v1/payments/" + pid)"""
if old_start in c:
    c = c.replace(old_start, new_block, 1)
    # after successful capture check, remember resolved pid
    c = c.replace("""                if pay.get("status") == "captured" and pay.get("order_id") == order_id:
                    ok_api = True
            except Exception:
                ok_api = False""",
                  """                if pay.get("status") == "captured" and pay.get("order_id") == order_id:
                    ok_api = True
                    payment_id = pid
            except Exception as _ae:
                ok_api = False
                api_err = repr(_ae)[:200]""", 1)
    c = c.replace('"diag": {"sec_len": len(sec), "has_sig": bool(signature), "order_owned": bool(row and row[1] == user.id)}',
                  '"diag": {"sec_len": len(sec), "has_sig": bool(signature), "order_owned": bool(row and row[1] == user.id), "api_err": api_err}', 1)
    open(ar, "w", encoding="utf-8").write(c)
    print("[BACKEND] verify v4: fallback auto-resolves payment from order")
else:
    print("[ERROR] v3 fallback block not found - paste output")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Payments: verify v4 self-resolving payment fallback"])
