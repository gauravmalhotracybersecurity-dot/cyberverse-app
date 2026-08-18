import os, re, glob, subprocess

print("=== 1. PATCHING BACKEND (Disabling Email Verification) ===")

# Find all python files in the backend
py_files = glob.glob("backend/**/*.py", recursive=True) + ["backend/main.py"]
patched_files = []

for filepath in py_files:
    if not os.path.exists(filepath): continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    original_content = content
    
    # Fix 1: Auto-verify new users on signup
    # Changes is_verified=False to is_verified=True
    content = re.sub(r'is_verified\s*=\s*False', 'is_verified=True', content)
    
    # Fix 2: Comment out email sending functions
    # Targets common variations of send_email / send_verification
    content = re.sub(r'^(\s*)(send_verification_email\(.*\))', r'\1# \2  # DISABLED FOR LAUNCH', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)(send_email\(.*\))', r'\1# \2  # DISABLED FOR LAUNCH', content, flags=re.MULTILINE)
    
    # Fix 3: Bypass verification check on login
    # Comments out the "if not user.is_verified" raise blocks
    content = re.sub(r'^(\s*)(if\s+not\s+user\.is_verified:)', r'\1# \2  # BYPASSED FOR LAUNCH', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)(raise\s+HTTPException\([^)]*verify[^)]*\))', r'\1# \2  # BYPASSED FOR LAUNCH', content, flags=re.MULTILINE | re.IGNORECASE)
    
    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        patched_files.append(filepath)
        print(f"[PATCHED] {filepath}")

if not patched_files:
    print("[INFO] No standard verification patterns found. You may need to manually check your auth route.")

print("\n=== 2. COMMIT & PUSH TO RENDER ===")
subprocess.run(["git", "add", "."])
status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)

if status.stdout.strip():
    commit_msg = "Launch fix: disable email verification for instant signup"
    subprocess.run(["git", "commit", "-m", commit_msg])
    print(f"[COMMITTED] {commit_msg}")
    
    push_res = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    print(push_res.stdout or push_res.stderr)
else:
    print("[INFO] No changes detected to commit.")

print("\n=== 3. DEPLOY STATUS ===")
print("Render is now deploying. Wait ~60 seconds, then test a fresh signup in an Incognito window!")
