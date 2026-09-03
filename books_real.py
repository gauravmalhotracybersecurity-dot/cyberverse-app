import subprocess

books = '''[
  {
    "title": "Breaking Into GRC",
    "desc": "A career-changer's guide to cybersecurity Governance, Risk & Compliance. No coding, no IT degree - a real, sequential transition path.",
    "price": "$9",
    "link": "https://malhotra72.gumroad.com/l/GRC"
  },
  {
    "title": "AI Workflows for Cybersecurity Professionals",
    "desc": "Practitioner playbook: human-in-the-loop AI workflows for triage, threat intel, compliance, offensive security and reporting.",
    "price": "$9",
    "link": "https://malhotra72.gumroad.com/l/cyberhustle"
  },
  {
    "title": "The AI Governance Playbook",
    "desc": "Practical frameworks, NIST AI RMF mapping and done-for-you AI risk assessment templates. Neither academic nor fluff.",
    "price": "$9",
    "link": "https://malhotra72.gumroad.com/l/wxhxoo"
  }
]
'''
open("backend/content/books.json", "w", encoding="utf-8").write(books)
print("[UPDATED] books.json with your 3 real Gumroad ebooks")

# Upgrade the resources page book cards with price badge + external link
rp = "backend/templates/resources.html"
c = open(rp, encoding="utf-8").read()
old = '<div class="card"><h3 style="font-size:1rem">{{ b.title }}</h3><p style="font-size:.85rem">{{ b.desc }}</p><a href="{{ b.link }}">Get the book &rarr;</a></div>'
new = '<div class="card"><h3 style="font-size:1rem">{{ b.title }}</h3><p style="font-size:.85rem">{{ b.desc }}</p><p style="margin:.4rem 0 .6rem"><span style="background:var(--accent);color:#000;font-weight:700;border-radius:12px;padding:.15rem .7rem;font-size:.8rem">{{ b.price }}</span> <span style="color:var(--muted);font-size:.75rem">by Gaurav Malhotra</span></p><a href="{{ b.link }}" target="_blank" rel="noopener">Get the book &rarr;</a></div>'
if old in c:
    open(rp, "w", encoding="utf-8").write(c.replace(old, new))
    print("[UPDATED] resources.html book cards with price badges")
else:
    print("[WARN] book card pattern not found - check resources.html")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Resources: real Gumroad ebooks (GRC, AI Workflows, AI Governance) with pricing"])
subprocess.run(["git", "push", "origin", "main"])
print("Pushed. Live in ~60s.")
