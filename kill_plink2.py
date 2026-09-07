import re, glob, subprocess
skip = ("venv", "node_modules", ".git")
pat = r'https?://[^\s"\'<>)]*(?:plink_|payment-link|rzp\.io)[^\s"\'<>)]*'
total = 0
files = [x for x in glob.glob("**/*.html", recursive=True) if not any(t in x for t in skip)]
files += [x for x in glob.glob("**/*.js", recursive=True) if not any(t in x for t in skip)]
for f in files:
    c = open(f, encoding="utf-8").read()
    found = re.findall(pat, c)
    if found:
        print("[FOUND] in", f, "->", found)
    c2 = re.sub(pat, "#", c)
    if c2 != c:
        open(f, "w", encoding="utf-8").write(c2)
        total += 1
        print("[CLEANED]", f)
print("files cleaned:", total)
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: catch-all removal of legacy razorpay payment-link URLs"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
