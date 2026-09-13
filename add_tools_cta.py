import subprocess

p = "backend/templates/tools/index.html"
c = open(p, encoding="utf-8").read()

print("=== ADDING BOTTOM CTA BANNER TO /tools ===\n")

if "tools-cta-banner" in c:
    print("[SKIP] CTA banner already present")
else:
    # Find the last {% endblock %}
    end_idx = c.rfind("{% endblock %}")
    if end_idx < 0:
        print("[ERROR] no {% endblock %} found")
        raise SystemExit(1)
    
    # CTA banner with inline styles matching dark theme
    cta_html = '''
<style>
.tools-cta-banner {
  margin: 3rem auto 1rem;
  padding: 2rem;
  background: linear-gradient(135deg, #0d1a16, #0a0a0a);
  border: 1px solid var(--accent, #00ffcc);
  border-radius: 16px;
  text-align: center;
  max-width: 700px;
}
.tools-cta-banner h3 {
  color: #fff;
  margin: 0 0 0.75rem;
  font-size: 1.5rem;
}
.tools-cta-banner p {
  color: var(--muted, #a0a0a0);
  line-height: 1.6;
  margin: 0 0 1.5rem;
}
.tools-cta-banner .cta-primary {
  display: inline-block;
  background: var(--accent, #00ffcc);
  color: #000;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: transform 0.2s;
}
.tools-cta-banner .cta-primary:hover { transform: translateY(-2px); }
.tools-cta-banner .cta-secondary {
  display: block;
  margin-top: 1rem;
  color: var(--muted, #a0a0a0);
  font-size: 0.9rem;
  text-decoration: none;
}
.tools-cta-banner .cta-secondary:hover { color: var(--accent, #00ffcc); }
</style>

<div class="tools-cta-banner">
  <h3>Used these tools to build something real?</h3>
  <p>Practice explaining it out loud. CyberVerse AI runs mock interviews on exactly this material and grades your answers like a hiring manager.</p>
  <a href="/app.html" class="cta-primary">Practice with CyberVerse AI &rarr;</a>
  <a href="/books" class="cta-secondary">Want it all written down? See the playbooks &rarr;</a>
</div>

'''
    
    c = c[:end_idx] + cta_html + c[end_idx:]
    open(p, "w", encoding="utf-8").write(c)
    print("[ADDED] Bottom CTA banner to /tools/index.html")

print("\n=== COMMIT + PUSH ===")
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Monetization: add bottom CTA banner to /tools page"], capture_output=True, text=True)
print(r.stdout.strip() if r.returncode == 0 else r.stderr.strip())
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
