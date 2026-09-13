import re, subprocess

print("=== FIXING DUPLICATE OG TAGS ===\n")

# === 1. FIX /learn/index.html ===
learn_path = "backend/templates/learn/index.html"
learn = open(learn_path, encoding="utf-8").read()

print("BEFORE /learn:")
print(f"  og:image tags in template: {learn.count('og:image')}")
print(f"  og:url tags in template: {learn.count('og:url')}")

# Remove any {% block head %} sections that add duplicate tags
head_block_pattern = r'{% block head %}.*?{% endblock %}'
head_blocks = re.findall(head_block_pattern, learn, re.DOTALL)
if head_blocks:
    print(f"  Found {len(head_blocks)} head block(s) - removing")
    learn = re.sub(head_block_pattern, '', learn, flags=re.DOTALL)
else:
    print("  No head blocks found")

# Add proper block overrides (after title block)
title_block_end = learn.find('{% endblock %}', learn.find('{% block title %}'))
if title_block_end > 0:
    insert_pos = title_block_end + 14  # After {% endblock %}
    og_overrides = """

{% block og_url %}https://grcwithgaurav.com/learn{% endblock %}
{% block og_image %}https://grcwithgaurav.com/static/og-default.jpg{% endblock %}
"""
    learn = learn[:insert_pos] + og_overrides + learn[insert_pos:]
    print("  Added og_url and og_image block overrides")

open(learn_path, "w", encoding="utf-8").write(learn)

print("\nAFTER /learn:")
print(f"  og:image tags in template: {learn.count('og:image')}")
print(f"  og:url tags in template: {learn.count('og:url')}")

# === 2. FIX /resources.html ===
resources_path = "backend/templates/resources.html"
resources = open(resources_path, encoding="utf-8").read()

print("\nBEFORE /resources:")
print(f"  og:image tags in template: {resources.count('og:image')}")
print(f"  og:url tags in template: {resources.count('og:url')}")

# Remove any {% block head %} sections
head_blocks = re.findall(head_block_pattern, resources, re.DOTALL)
if head_blocks:
    print(f"  Found {len(head_blocks)} head block(s) - removing")
    resources = re.sub(head_block_pattern, '', resources, flags=re.DOTALL)
else:
    print("  No head blocks found")

# Add proper block overrides
title_block_end = resources.find('{% endblock %}', resources.find('{% block title %}'))
if title_block_end > 0:
    insert_pos = title_block_end + 14
    og_overrides = """

{% block og_url %}https://grcwithgaurav.com/resources{% endblock %}
{% block og_image %}https://grcwithgaurav.com/static/og-default.jpg{% endblock %}
"""
    resources = resources[:insert_pos] + og_overrides + resources[insert_pos:]
    print("  Added og_url and og_image block overrides")

open(resources_path, "w", encoding="utf-8").write(resources)

print("\nAFTER /resources:")
print(f"  og:image tags in template: {resources.count('og:image')}")
print(f"  og:url tags in template: {resources.count('og:url')}")

# === 3. COMMIT + PUSH ===
print("\n=== COMMIT + PUSH ===")
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "FIX: remove duplicate OG tags, use proper block overrides for /learn and /resources"], capture_output=True, text=True)
print(r.stdout.strip() if r.returncode == 0 else r.stderr.strip())
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
