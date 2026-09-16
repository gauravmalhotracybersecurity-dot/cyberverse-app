import subprocess, re, os

print("=== FIXING TRAILING SLASHES ON TOOL PAGES ===\n")

tools_dir = "backend/templates/tools"
tool_files = [f for f in os.listdir(tools_dir) if f.endswith(".html") and f != "index.html"]

fixed = 0
for filename in tool_files:
    filepath = os.path.join(tools_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find canonical with trailing slash
    pattern = r'(<link[^>]*rel="canonical"[^>]*href="https://grcwithgaurav\.com/tools/[^"]+)/("[^>]*>)'
    
    if re.search(pattern, content):
        new_content = re.sub(pattern, r'\1\2', content)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[FIXED] {filename}")
        fixed += 1
    else:
        print(f"[OK] {filename} (no trailing slash)")

print(f"\nFixed {fixed} tool pages")

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "SEO: remove trailing slashes from tool page canonicals"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
