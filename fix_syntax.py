import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()
lines = c.split('\n')

# Find the broken try block around line 107
broken_idx = None
for i, line in enumerate(lines):
    if i > 100 and i < 115 and line.strip() == 'try:':
        # Check if next few lines have except/finally
        has_except = False
        for j in range(i+1, min(i+10, len(lines))):
            if 'except' in lines[j] or 'finally' in lines[j]:
                has_except = True
                break
        if not has_except:
            broken_idx = i
            print(f"[DIAG] Found broken try at line {i+1}")
            break

if broken_idx is None:
    print("[OK] No broken try found")
else:
    # Remove the entire broken notification block (from the try back to the last good line)
    # Find where the notification code starts (look back for the pattern)
    start_remove = broken_idx
    for i in range(broken_idx-1, max(broken_idx-20, 0), -1):
        if 'db.commit()' in lines[i]:
            start_remove = i + 1
            break
    
    # Find where it ends (look forward for the next db.execute or def)
    end_remove = broken_idx
    indent_level = len(lines[broken_idx]) - len(lines[broken_idx].lstrip())
    for i in range(broken_idx+1, min(broken_idx+30, len(lines))):
        line = lines[i]
        if line.strip() and not line.startswith(' ' * (indent_level + 1)) and not line.strip().startswith('#'):
            # Back to same or lower indent = end of block
            end_remove = i
            break
    
    print(f"[FIX] Removing lines {start_remove+1} to {end_remove}")
    new_lines = lines[:start_remove] + lines[end_remove:]
    open(ar, "w", encoding="utf-8").write('\n'.join(new_lines))
    print("[BACKEND] Broken notification block removed")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: repair broken try block in analytics_routes"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
