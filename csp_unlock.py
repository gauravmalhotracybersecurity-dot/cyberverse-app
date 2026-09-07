import re, glob, subprocess
skip = ("venv", "node_modules", ".git")

def fix_csp(c):
    c = re.sub(r"(script-src)([^ https://checkout.razorpay.com;]*)", lambda m: m.group(1) + m.group(2) + ("" if "checkout.razorpay.com" in m.group(2) else " https://checkout.razorpay.com"), c)
    if "frame-src" in c:
        c = re.sub(r"(frame-src)([^ https://api.razorpay.com https://checkout.razorpay.com;]*)", lambda m: m.group(1) + m.group(2) + ("" if "api.razorpay.com" in m.group(2) else " https://api.razorpay.com https://checkout.razorpay.com"), c)
    else:
        c = c.replace("script-src", "frame-src https://api.razorpay.com https://checkout.razorpay.com; script-src", 1)
    if "connect-src" in c:
        c = re.sub(r"(connect-src)([^ https://checkout.razorpay.com;]*)", lambda m: m.group(1) + m.group(2) + ("" if "razorpay.com" in m.group(2) else " https://api.razorpay.com https://checkout.razorpay.com"), c)
    return c

n = 0
for f in [x for x in glob.glob("**/*.py", recursive=True) if not any(t in x for t in skip)] + \
         [x for x in glob.glob("**/*.html", recursive=True) if not any(t in x for t in skip)]:
    c = open(f, encoding="utf-8").read()
    if "Content-Security-Policy" not in c:
        continue
    c2 = fix_csp(c)
    if c2 != c:
        open(f, "w", encoding="utf-8").write(c2)
        n += 1
        print("[CSP] razorpay domains allowed in", f)
print("csp files patched:", n)

# 422 fix v3: multiline-safe param replacement on /event
m2 = 0
for f in [x for x in glob.glob("**/*.py", recursive=True) if not any(t in x for t in skip)]:
    c = open(f, encoding="utf-8").read()
    c2 = re.sub(r'(@router\.post\("/event"\)[\s\S]{0,200}?def \w+\([\s]*\w+[\s]*:[\s]*)\w+', r'\1dict', c)
    if c2 != c:
        open(f, "w", encoding="utf-8").write(c2)
        m2 += 1
        print("[EVENT] payload relaxed in", f)
print("event files patched:", m2)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: CSP allows Razorpay checkout script/frames + /event payload"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
