import glob

main_py = glob.glob("backend/main.py")[0]
c = open(main_py, encoding="utf-8").read()
lines = c.split('\n')

print("=== CURRENT ROUTER INCLUSION PATTERN ===")
for i, line in enumerate(lines):
    if 'include_router' in line:
        start = max(0, i-5)
        end = min(len(lines), i+5)
        for j in range(start, end):
            print(f"{j+1:3d}: {lines[j]}")
        print()

print("\n=== CURRENT HEALTH ENDPOINT ===")
for i, line in enumerate(lines):
    if '"/api/health"' in line and 'def ' in line:
        start = max(0, i-2)
        end = min(len(lines), i+15)
        for j in range(start, end):
            print(f"{j+1:3d}: {lines[j]}")
        break
