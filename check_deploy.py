import subprocess, sys

print("=== 1. GIT STATUS ===")
print(subprocess.run(["git", "status"], capture_output=True, text=True).stdout)

print("\n=== 2. LATEST COMMIT ===")
print(subprocess.run(["git", "log", "--oneline", "-1"], capture_output=True, text=True).stdout)

print("\n=== 3. CHECK IF ARTICLES ARE IN articles.py ===")
content = open("backend/content/articles.py", encoding="utf-8").read()
if "cybersecurity-salary-india-2026" in content:
    print("✓ Salary article found in articles.py")
else:
    print("✗ Salary article NOT in articles.py")
    
if "best-cybersecurity-certifications-beginners-2026" in content:
    print("✓ Certifications article found in articles.py")
else:
    print("✗ Certifications article NOT in articles.py")

print("\n=== 4. LAST 5 LINES OF articles.py ===")
lines = content.split('\n')
for line in lines[-10:]:
    print(line)
