import subprocess, re

print("=== ADDING PER-TOOL INLINE CTAs ===\n")

# 1. Add shared CSS to base.html (once)
base_path = "backend/templates/base.html"
base = open(base_path, encoding="utf-8").read()
if "/*tool-result-cta*/" not in base:
    css = '''
<style>
/*tool-result-cta*/
.tool-result-cta { margin:1.25rem 0; padding:1rem 1.25rem; background:#0d1a16; border:1px solid var(--accent,#00ffcc); border-radius:12px; }
.tool-result-cta p { color:var(--muted,#a0a0a0); margin:0 0 .6rem; line-height:1.5; font-size:.92rem; }
.tool-result-cta p strong { color:#fff; }
.tool-result-cta .cta-secondary { color:var(--accent,#00ffcc); font-weight:600; text-decoration:none; font-size:.92rem; }
.tool-result-cta .cta-secondary:hover { text-decoration:underline; }
</style>
'''
    h = base.find("</head>")
    base = base[:h] + css + base[h:]
    open(base_path, "w", encoding="utf-8").write(base)
    print("[ADDED] .tool-result-cta CSS to base.html\n")

# 2. Per-tool CTA copy
tools = {
    "iso_risk_calculator.html":        '<p>Nice work. Now try explaining <strong>risk scoring</strong> out loud &mdash; CyberVerse AI asks you this in a mock interview and scores your answer.</p><a href="/app.html" class="cta-secondary">Try a Mock Interview &rarr;</a>',
    "cvss_calculator.html":            '<p>Nice work. Now try explaining <strong>CVSS scoring</strong> out loud &mdash; CyberVerse AI asks you this in a mock interview and scores your answer.</p><a href="/app.html" class="cta-secondary">Try a Mock Interview &rarr;</a>',
    "iso_gap_assessment.html":         '<p>Nice work. Now try explaining <strong>gap assessment findings</strong> out loud &mdash; CyberVerse AI asks you this in a mock interview and scores your answer.</p><a href="/app.html" class="cta-secondary">Try a Mock Interview &rarr;</a>',
    "incident_severity_calculator.html":'<p>Nice work. Now try explaining <strong>incident severity classification</strong> out loud &mdash; CyberVerse AI asks you this in a mock interview and scores your answer.</p><a href="/app.html" class="cta-secondary">Try a Mock Interview &rarr;</a>',
    "vendor_risk_assessment.html":     '<p>Nice work. Now try explaining <strong>vendor risk scoring</strong> out loud &mdash; CyberVerse AI asks you this in a mock interview and scores your answer.</p><a href="/app.html" class="cta-secondary">Try a Mock Interview &rarr;</a>',
    "security_policy_generator.html":  '<p>Nice work. Now try explaining <strong>security policy drafting</strong> out loud &mdash; CyberVerse AI asks you this in a mock interview and scores your answer.</p><a href="/app.html" class="cta-secondary">Try a Mock Interview &rarr;</a>',
    "iso27001_control_finder.html":    '<p>Nice work. Now try explaining <strong>ISO 27001 control selection</strong> out loud &mdash; CyberVerse AI asks you this in a mock interview and scores your answer.</p><a href="/app.html" class="cta-secondary">Try a Mock Interview &rarr;</a>',
    "ats_resume_checker.html":         '<p>Your resume just passed the bots. Next: pass the human. Practice your interview answers with CyberVerse AI before you apply.</p><a href="/app.html" class="cta-secondary">Try a Mock Interview &rarr;</a>',
    "risk_register_generator.html":    '<p>You just built a real risk register. Want the complete playbook on how to present this in interviews?</p><a href="/books" class="cta-secondary">See Breaking Into GRC &rarr;</a>',
}

for fname, inner in tools.items():
    path = "backend/templates/tools/" + fname
    c = open(path, encoding="utf-8").read()
    if "tool-result-cta" in c:
        print(f"[SKIP] {fname} already has CTA")
        continue
    
    div = '\n<div class="tool-result-cta">' + inner + '</div>\n'
    
    # Insert before first Download/Export/Copy button (i.e., inside result area)
    m = re.search(r'<(?:button|a)\b[^>]*>\s*(?:Download|Export|Copy)', c, re.I)
    if m:
        idx = m.start()
        where = "before Download/Export button (inside result area)"
    else:
        idx = c.rfind("{% endblock %}")
        where = "end of content block (no export button found)"
    
    c = c[:idx] + div + c[idx:]
    open(path, "w", encoding="utf-8").write(c)
    print(f"[ADDED] {fname}: {where}")

# 3. Commit + push
print("\n=== COMMIT + PUSH ===")
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Monetization: per-tool inline CTAs on all 9 tool result pages"], capture_output=True, text=True)
print(r.stdout.strip() if r.returncode == 0 else r.stderr.strip())
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
