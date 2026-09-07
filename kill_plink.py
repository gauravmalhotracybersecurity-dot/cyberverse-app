import re, glob, subprocess
skip = ("venv", "node_modules", ".git")
pat = r'(?:rzp\.io|payment-link|plink_)'
total = 0
files = [x for x in glob.glob("**/*.html", recursive=True) if not any(t in x for t in skip)]
files += [x for x in glob.glob("**/*.js", recursive=True) if not any(t in x for t in skip)]
for f in files:
    c = open(f, encoding="utf-8").read()
    c2 = re.sub(r'href="[^"]*' + pat + r'[^"]*"', 'href="#"', c)
    c2 = re.sub(r"href='[^']*" + pat + r"[^']*'", "href='#'", c2)
    c2 = re.sub(r'onclick="[^"]*(?:' + pat + r'|razorpay)[^"]*"', '', c2)
    c2 = re.sub(r'window\.open\(\s*["\'][^"\']*' + pat + r'[^"\']*["\'][^)]*\)', 'void(0)', c2)
    c2 = re.sub(r'location\.href\s*=\s*["\'][^"\']*' + pat + r'[^"\']*["\']', 'void(0)', c2)
    if c2 != c:
        open(f, "w", encoding="utf-8").write(c2)
        total += 1
        print("[CLEANED] old razorpay payment-link references removed from", f)
print("files cleaned:", total)
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: remove legacy Razorpay payment-link hijack from paywall"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
