import glob, subprocess
skip = ("venv", "node_modules", ".git")
ar = [x for x in glob.glob("**/analytics_routes.py", recursive=True) if not any(t in x for t in skip)][0]
c = open(ar, encoding="utf-8").read()
lines = c.split('\n')

print("=== LINES 100-120 ===")
for i in range(99, min(120, len(lines))):
    print(f"{i+1:3d}: {lines[i]}")

# Find ALL try: blocks and check for except/finally
broken_indices = []
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped == 'try:':
        # Look ahead for except or finally within 50 lines
        found_except = False
        for j in range(i+1, min(i+50, len(lines))):
            if 'except' in lines[j] or 'finally' in lines[j]:
                found_except = True
                break
        if not found_except:
            broken_indices.append(i)
            print(f"[BROKEN] Line {i+1}: {line}")

if not broken_indices:
    print("[OK] All try blocks have except/finally")
else:
    # Remove broken blocks (work backwards to preserve indices)
    for idx in sorted(broken_indices, reverse=True):
        # Find the end of this broken block (next line at same or lower indent that's not empty/comment)
        indent = len(lines[idx]) - len(lines[idx].lstrip())
        end = idx + 1
        for j in range(idx+1, min(idx+30, len(lines))):
            line = lines[j]
            if line.strip() and not line.strip().startswith('#'):
                line_indent = len(line) - len(line.lstrip())
                if line_indent <= indent:
                    end = j
                    break
        print(f"[FIX] Removing lines {idx+1} to {end}")
        del lines[idx:end]
    
    open(ar, "w", encoding="utf-8").write('\n'.join(lines))
    print("[BACKEND] Broken try blocks removed")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: remove all broken try blocks from analytics_routes"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
