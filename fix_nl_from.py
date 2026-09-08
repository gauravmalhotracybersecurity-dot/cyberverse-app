import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()

# Replace the hardcoded NL_FROM with env var reading
import re

# Pattern: NL_FROM = "..."
pattern = r'NL_FROM\s*=\s*["\'][^"\']+["\']'
replacement = 'NL_FROM = _os.environ.get("RESEND_FROM_EMAIL", "onboarding@resend.dev")'

c_new = re.sub(pattern, replacement, c, count=1)

if c_new != c:
    print("[FIX] NL_FROM constant replaced with env var reading")
    # Ensure 'import os as _os' is present
    if 'import os as _os' not in c_new and 'import os' not in c_new:
        c_new = 'import os as _os\n' + c_new
        print("[FIX] Added 'import os as _os'")
else:
    print("[WARN] Pattern not found, trying manual replacement")
    # Manual fallback
    old_lines = c.split('\n')
    new_lines = []
    for line in old_lines:
        if line.strip().startswith('NL_FROM =') and 'Gaurav Malhotra' in line:
            new_lines.append('NL_FROM = _os.environ.get("RESEND_FROM_EMAIL", "onboarding@resend.dev")')
            print("[FIX] Manual replacement done")
        else:
            new_lines.append(line)
    c_new = '\n'.join(new_lines)

try:
    compile(c_new, ar, "exec")
    open(ar, "w", encoding="utf-8").write(c_new)
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print("[ABORT] Syntax error:", e)
    raise SystemExit(1)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: NL_FROM reads from RESEND_FROM_EMAIL env var instead of hardcoded domain"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
