import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

old_start = '        ok_api = False\n        if not ok_sig and row and row[1] == user.id and key and sec and payment_id:\n            try:\n                req = _u.Request("https://api.razorpay.com/v1/payments/" + payment_id)'
new_block = '        ok_api = False\n        api_err = ""\n        if not ok_sig and row and row[1] == user.id and key and sec:\n            try:\n                pid = payment_id\n                if not pid:\n                    req0 = _u.Request("https://api.razorpay.com/v1/orders/" + order_id + "/payments")\n                    req0.add_header("Authorization", "Basic " + base64.b64encode((key + ":" + sec).encode()).decode())\n                    with _u.urlopen(req0, timeout=15) as r0:\n                        lst = _j.loads(r0.read())\n                    caps = [x for x in (lst.get("items") or []) if x.get("status") == "captured"]\n                    if caps:\n                        pid = caps[0].get("id")\n                if pid:\n                    req = _u.Request("https://api.razorpay.com/v1/payments/" + pid)'
if old_start in c:
    c = c.replace(old_start, new_block, 1)
    c = c.replace('                if pay.get("status") == "captured" and pay.get("order_id") == order_id:\n                    ok_api = True\n            except Exception:\n                ok_api = False',
                  '                if pay.get("status") == "captured" and pay.get("order_id") == order_id:\n                    ok_api = True\n                    payment_id = pid\n            except Exception as _ae:\n                ok_api = False\n                api_err = repr(_ae)[:200]', 1)
    c = c.replace('"order_owned": bool(row and row[1] == user.id)}',
                  '"order_owned": bool(row and row[1] == user.id), "api_err": api_err}', 1)
    open(ar, "w", encoding="utf-8").write(c)
    print("[BACKEND] verify v4 installed")
else:
    print("[ERROR] fallback block not found")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Payments: verify v4 self-resolving payment fallback"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
