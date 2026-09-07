import re, glob, subprocess
skip = ("venv", "node_modules", ".git")
n = 0
for f in [x for x in glob.glob("**/*.py", recursive=True) if not any(t in x for t in skip)]:
    c = open(f, encoding="utf-8").read()
    c2 = re.sub(r'(@router\.post\("/event"\)[^\n]*\n(?:async )?def \w+\(\w+: )\w+', r'\1dict', c)
    if c2 != c:
        open(f, "w", encoding="utf-8").write(c2)
        n += 1
        print("[PATCHED]", f)
print("files patched:", n)
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: /event accepts any payload shape (param-agnostic)"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
