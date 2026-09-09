import subprocess, glob, re

OLD_URLS = [
    "https://linkedin.com/in/gauravmalhotracybersecurity",
    "http://linkedin.com/in/gauravmalhotracybersecurity",
    "linkedin.com/in/gauravmalhotracybersecurity"
]
NEW_URL = "https://www.linkedin.com/in/gaurav-malhotra-3419124b"

changed_files = []
for f in glob.glob("backend/templates/**/*.html", recursive=True):
    c = open(f, encoding="utf-8").read()
    orig = c
    for old in OLD_URLS:
        if old in c:
            c = c.replace(old, NEW_URL)
    if c != orig:
        open(f, "w", encoding="utf-8").write(c)
        changed_files.append(f)
        print(f"[UPDATED] {f}")

if not changed_files:
    print("[NOTE] Old LinkedIn URL not found in templates.")

# Final local verification
print("\n=== LOCAL CHECK ===")
count_old = 0
count_new = 0
for f in glob.glob("backend/templates/**/*.html", recursive=True):
    c = open(f, encoding="utf-8").read()
    if "gauravmalhotracybersecurity" in c: count_old += 1
    if "gaurav-malhotra-3419124b" in c: count_new += 1
print(f"  Files with OLD URL: {count_old}")
print(f"  Files with NEW URL: {count_new}")

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Update LinkedIn profile URL to correct handle"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
