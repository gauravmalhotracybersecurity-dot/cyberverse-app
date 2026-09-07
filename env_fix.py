import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

old_key = 'key = os.environ.get("RAZORPAY_KEY_ID", "")'
new_key = 'key = os.environ.get("RAZORPAY_KEY_ID") or os.environ.get("RAZORPAY_KEY") or os.environ.get("RZP_KEY_ID") or ""'
old_sec = 'sec = os.environ.get("RAZORPAY_KEY_SECRET", "")'
new_sec = 'sec = os.environ.get("RAZORPAY_KEY_SECRET") or os.environ.get("RAZORPAY_SECRET") or os.environ.get("RZP_KEY_SECRET") or ""'

n = 0
if old_key in c:
    c = c.replace(old_key, new_key); n += 1
if old_sec in c:
    c = c.replace(old_sec, new_sec); n += 1
open(ar, "w", encoding="utf-8").write(c)
print("[PATCHED] env-name variants:", n)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: accept Razorpay env key name variants"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
