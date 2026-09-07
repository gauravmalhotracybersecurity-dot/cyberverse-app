import subprocess

ap = "backend/content/articles.py"
a = open(ap, encoding="utf-8").read()

# Cross-link FIRST (count=1 keeps replacements surgical)
old1 = '{"slug": "what-is-grc", "title": "What is GRC? Governance, Risk and Compliance Explained"}'
new1 = old1 + ',\n            {"slug": "grc-interview-questions", "title": "GRC Interview Questions and Answers (2026): 15 Real Questions with Frameworks"},\n            {"slug": "how-to-start-grc-career", "title": "How to Start a GRC Career in 2026 (Even Without an IT Background)"}'
a = a.replace(old1, new1, 1)
old2 = '{"slug": "grc-analyst-career-roadmap", "title": "GRC Analyst Career Roadmap (2026): Zero to Job-Ready"}'
new2 = old2 + ',\n            {"slug": "how-to-start-grc-career", "title": "How to Start a GRC Career in 2026 (Even Without an IT Background)"}'
a = a.replace(old2, new2, 1)

new_articles = ''',
    {
        "slug": "how-to-start-grc-career",
        "title": "How to Start a GRC Career in 2026 (Even Without an IT Background)",
        "category": "Careers",
        "description": "The exact 4-step path into Governance, Risk & Compliance for career changers: frameworks to learn, 3 artifacts to build, one credibility signal, and the job engine.",
        "author": "Gaurav Malhotra",
        "date": "2026-09-07",
        "read": "7 min read",
        "tools": [
            {"href": "/tools/risk-register-generator", "label": "Risk Register Generator"},
            {"href": "/tools/iso-gap-assessment", "label": "Gap Assessment"},
            {"href": "/tools/ats-resume-checker", "label": "Resume ATS Checker"}
        ],
        "related": [
            {"slug": "what-is-grc", "title": "What is GRC? Governance, Risk and Compliance Explained"},
            {"slug": "grc-analyst-career-roadmap", "title": "GRC Analyst Career Roadmap (2026): Zero to Job-Ready"}
        ],
        "faq": [
            ["Can I get a GRC job with no certifications?", "Yes, but slower. One foundation credential plus three real artifacts (risk register, gap assessment, a policy you wrote) beats five certificates with nothing to show."],
            ["How long does it take to land the first GRC role?", "Commonly 6-12 months part-time. People with adjacent experience - audit, finance, operations, teaching - often move faster because their stories already sound like GRC."],
            ["Is GRC non-technical forever?", "No. Day one needs technical literacy, not coding. Senior GRC goes deep into cloud, AI governance and architecture reviews - but you grow into that, you do not start there."]
        ],
        "body": """
<p>GRC is one of the few cybersecurity paths where a non-technical background is an <strong>advantage</strong>. Operations managers, teachers, finance analysts and customer-service leads already possess the three skills GRC runs on: process thinking, documentation discipline, and stakeholder management. Here is the honest entry path.</p>
<h2>Why GRC hires career changers</h2>
<ul>
<li>Risk is a business language before it is a technical one - you already speak business.</li>
<li>Auditors and control owners respond to people who can write clearly and chase evidence politely.</li>
<li>Most technical engineers hate writing policies and registers. You will not.</li>
</ul>
<h2>The 4-step entry path</h2>
<ol>
<li><strong>Learn the language (weeks 1-6):</strong> ISO 27001 clauses 4-10 and the four Annex A themes; NIST CSF functions; how SOC 2 differs. Start with the <a href="/learn/what-is-grc">GRC explainer</a>.</li>
<li><strong>Build three artifacts (weeks 6-14):</strong> a 15-row <a href="/tools/risk-register-generator">risk register</a> for a fictional company, a completed <a href="/tools/iso-gap-assessment">gap assessment</a>, and one policy you drafted and edited by hand. These become your portfolio.</li>
<li><strong>One credibility signal (weeks 12-20):</strong> CompTIA Security+ or ISO 27001 foundation training - or a structured book like <a href="https://malhotra72.gumroad.com/l/GRC" rel="noopener">Breaking Into GRC</a> if you learn faster by reading.</li>
<li><strong>Run the job engine (weeks 18-26):</strong> keyword-map your resume, pass it through the <a href="/tools/ats-resume-checker">ATS checker</a>, then practice interviews out loud until your answers are crisp.</li>
</ol>
<h2>What "no IT background" actually requires</h2>
<p>Technical literacy, not coding: what identity and MFA do, how cloud responsibility splits, what a network segment is, why logs matter. Enough to ask sharp questions in a risk workshop - not enough to configure the firewall yourself.</p>
<h2>Where GRC roles hide on job boards</h2>
<ul>
<li>GRC Analyst, IT Risk Analyst, Compliance Analyst</li>
<li>ISMS Coordinator, Information Security Officer (junior)</li>
<li>Third-Party / Vendor Risk Analyst, IT Auditor (internal)</li>
</ul>
<h2>Timeline expectations</h2>
<p>Plan for 6-12 months of part-time effort. The people who quit early are the ones who collected certificates but never built artifacts - hiring managers can tell the difference in one interview question.</p>
"""
    },
    {
        "slug": "grc-interview-questions",
        "title": "GRC Interview Questions and Answers (2026): 15 Real Questions with Frameworks",
        "category": "Careers",
        "description": "15 real GRC interview questions grouped by fundamentals, risk, ISO 27001 controls and scenarios - each with what the interviewer is testing and a strong answer framework.",
        "author": "Gaurav Malhotra",
        "date": "2026-09-07",
        "read": "9 min read",
        "tools": [
            {"href": "/app.html", "label": "AI Mock Interview Coach"},
            {"href": "/tools/iso27001-control-finder", "label": "Annex A Control Finder"}
        ],
        "related": [
            {"slug": "grc-analyst-career-roadmap", "title": "GRC Analyst Career Roadmap (2026): Zero to Job-Ready"},
            {"slug": "how-to-start-grc-career", "title": "How to Start a GRC Career in 2026 (Even Without an IT Background)"}
        ],
        "faq": [
            ["How do I answer GRC questions with no direct experience?", "Use transfer stories plus artifacts. Describe a process you owned in your old role using GRC vocabulary, then show the risk register or policy you built. Honest method beats fake experience every time."],
            ["Should I memorize answers?", "No. Memorize frameworks and five STAR stories. Interviewers change the wording; frameworks survive any wording."]
        ],
        "body": """
<p>GRC interviewers rarely want definitions - they want to hear <strong>how you think</strong>. For each question below: what is really being tested, and a framework you can adapt. Then practice it out loud, because silent knowledge fails in rooms.</p>
<h2>Fundamentals</h2>
<ol>
<li><strong>"What is GRC and why does it matter?"</strong> Testing: can you connect governance to business outcomes? Framework: name the three pillars, then one concrete business consequence of getting it wrong (lost enterprise deal, regulatory fine, breach).</li>
<li><strong>"Explain the CIA triad with a real example."</strong> Testing: applied basics. Framework: define each pillar, then one breach example per pillar (exfiltration = confidentiality, tampered logs = integrity, ransomware downtime = availability).</li>
<li><strong>"Threat vs vulnerability vs risk - the difference?"</strong> Testing: precision. Framework: threat = actor/event, vulnerability = weakness, risk = likelihood x impact of the threat exploiting the weakness. One sentence linking all three.</li>
</ol>
<h2>Risk</h2>
<ol start="4">
<li><strong>"Walk me through how you would run a risk assessment."</strong> Testing: method. Framework: scope and criteria, asset identification, threats and vulnerabilities, likelihood x impact scoring, treatment selection, register entry, review cadence.</li>
<li><strong>"How do you decide whether to accept a risk?"</strong> Testing: judgment. Framework: compare against risk appetite, cost of control vs expected loss, and insist on risk-owner sign-off because acceptance is a business decision.</li>
<li><strong>"Inherent vs residual risk?"</strong> Testing: vocabulary with numbers. Framework: inherent = before controls, residual = after; give a sample score drop (20 to 8 after MFA and backups).</li>
</ol>
<h2>Controls &amp; ISO 27001</h2>
<ol start="7">
<li><strong>"What is a Statement of Applicability and how do you build one?"</strong> Testing: ISO depth. Framework: output of risk treatment, control selection from Annex A, documented justification for every exclusion, owner approval.</li>
<li><strong>"Name five Annex A controls relevant to remote work."</strong> Testing: control fluency (2022 numbering). Framework: 6.7 remote working, 8.1 user end point devices, 5.15 access control, 8.24 cryptography, 6.6 confidentiality agreements.</li>
<li><strong>"How would you prepare for a Stage 2 audit?"</strong> Testing: audit lifecycle. Framework: evidence map per clause, internal audit completed, management review minuted, all major nonconformities closed before the date.</li>
</ol>
<h2>Scenarios</h2>
<ol start="10">
<li><strong>"A critical vendor refuses to share their SOC 2. Now what?"</strong> Testing: vendor risk judgment. Framework: classify criticality, request alternative evidence (CAIQ, pen-test summary, ISO certificate), add contract clauses (breach notice, right to audit), apply compensating controls, escalate with options not emotions.</li>
<li><strong>"An employee clicked a phishing link. Walk me through response."</strong> Testing: IR process. Framework: contain (isolate host, rotate credentials), assess scope, eradicate, recover, then lessons learned and a control improvement.</li>
<li><strong>"How do you get engineers to care about compliance?"</strong> Testing: influence. Framework: speak their language, remove friction instead of adding gates, embed checks in CI/CD, show metrics they respect.</li>
</ol>
<h2>The meta-questions</h2>
<ol start="13">
<li><strong>"Tell me about a conflict with a control owner."</strong> Testing: stakeholder management. Deliver a 90-second STAR story - build five of these in the Story Bank before any interview.</li>
<li><strong>"Where is GRC going with AI?"</strong> Testing: curiosity. Framework: AI governance frameworks (NIST AI RMF, EU AI Act), model risk, and how GRC teams will assess autonomous agents - this one separates readers from practitioners.</li>
<li><strong>"What would you do in your first 30 days here?"</strong> Testing: pragmatism. Framework: learn scope and assets, review the register and SoA, meet control owners, deliver one quick win (close an overdue finding).</li>
</ol>
<h2>How to actually practice</h2>
<p>Out loud, timed, recorded. Read a framework, close the page, answer in 90 seconds, listen to yourself. The <a href="/app.html">AI Mock Interview Coach</a> grades your answers the way a hiring manager hears them - and the <a href="https://app.grcwithgaurav.com/questions/" rel="noopener">question library</a> has dozens more with model frameworks.</p>
"""
    }'''

idx = a.rfind("]")
a = a[:idx] + new_articles + "\n" + a[idx:]
open(ap, "w", encoding="utf-8").write(a)
print("[CMS] 2 Careers articles added + cross-linked")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Content: Careers cluster (GRC entry path + 15 interview questions with frameworks)"])
subprocess.run(["git", "push", "origin", "main"])
print("Pushed. Live in ~60s.")
