import subprocess, textwrap, re

content_file = "backend/content/articles.py"
c = open(content_file, encoding="utf-8").read()

new_articles = r'''
    {
        "slug": "what-is-grc",
        "title": "What is GRC? Governance, Risk and Compliance Explained",
        "category": "GRC",
        "description": "A practical beginner guide to GRC: what governance, risk and compliance mean, how GRC teams work, common frameworks, and how to start a GRC career.",
        "author": "Gaurav Malhotra",
        "date": "2026-09-03",
        "read": "7 min read",
        "tools": [
            {"href": "/tools/iso-gap-assessment", "label": "ISO 27001 Gap Assessment"},
            {"href": "/tools/risk-register-generator", "label": "Risk Register Generator"},
            {"href": "/tools/vendor-risk-assessment", "label": "Vendor Risk Assessment"}
        ],
        "related": [
            {"slug": "grc-analyst-career-roadmap", "title": "GRC Analyst Career Roadmap"},
            {"slug": "grc-interview-questions", "title": "GRC Interview Questions and Answers"}
        ],
        "faq": [
            ["Is GRC part of cybersecurity?", "Yes. GRC is the governance, risk and compliance layer of cybersecurity. It ensures security decisions align with business goals, regulatory obligations and risk appetite."],
            ["Does GRC require coding?", "Most GRC roles do not require coding. However, understanding systems, cloud, identity, logging and basic security architecture helps you perform better."],
            ["What frameworks should a beginner learn first?", "Start with ISO 27001, NIST Cybersecurity Framework, SOC 2, risk management basics, vendor risk and internal audit fundamentals."]
        ],
        "body": """
<p>GRC stands for <strong>Governance, Risk and Compliance</strong>. In cybersecurity, GRC is the discipline that connects security work to business objectives, legal obligations, audit requirements and risk decisions.</p>

<h2>What governance means</h2>
<p>Governance defines how decisions are made. In security, this includes policies, roles, committees, risk ownership, approvals, reporting and accountability. Good governance answers: who owns security risk, who approves exceptions, and how leadership knows the program is working?</p>

<h2>What risk means</h2>
<p>Risk is the possibility that a threat exploits a vulnerability and causes business impact. A GRC analyst helps identify risks, score them, assign owners, document treatment plans and track remediation. Use the <a href="/tools/risk-register-generator">Risk Register Generator</a> to see what this looks like in practice.</p>

<h2>What compliance means</h2>
<p>Compliance means meeting requirements from standards, regulations, contracts and internal policies. Examples include ISO 27001, SOC 2, GDPR, DPDP, PCI DSS and customer security questionnaires. Compliance is not the same as security, but it creates evidence that controls exist and are operating.</p>

<h2>Common GRC activities</h2>
<ul>
<li>Running ISO 27001 or SOC 2 readiness assessments</li>
<li>Maintaining risk registers and Statements of Applicability</li>
<li>Coordinating internal audits</li>
<li>Reviewing vendor security questionnaires</li>
<li>Writing and reviewing security policies</li>
<li>Tracking control gaps and remediation plans</li>
<li>Preparing evidence for auditors and customers</li>
</ul>

<h2>GRC vs technical cybersecurity</h2>
<p>Technical teams configure systems, monitor alerts and respond to incidents. GRC teams make sure risks are known, owners are assigned, controls are documented, and leadership has evidence to make decisions. Strong security programs need both.</p>

<h2>How to start learning GRC</h2>
<ol>
<li>Understand risk: asset, threat, vulnerability, likelihood, impact and treatment.</li>
<li>Learn ISO 27001 basics and Annex A controls.</li>
<li>Practice with a <a href="/tools/iso-gap-assessment">gap assessment</a>.</li>
<li>Create sample policies using the <a href="/tools/security-policy-generator">Security Policy Generator</a>.</li>
<li>Practice explaining concepts out loud using CyberVerse AI mock interviews.</li>
</ol>
"""
    },
    {
        "slug": "grc-analyst-career-roadmap",
        "title": "GRC Analyst Career Roadmap: Skills, Certifications and Projects",
        "category": "GRC",
        "description": "A practical roadmap for becoming a GRC analyst: skills to learn, certifications to consider, beginner projects, resume tips and interview preparation.",
        "author": "Gaurav Malhotra",
        "date": "2026-09-03",
        "read": "8 min read",
        "tools": [
            {"href": "/tools/ats-resume-checker", "label": "Resume ATS Checker"},
            {"href": "/tools/iso-gap-assessment", "label": "ISO 27001 Gap Assessment"},
            {"href": "/tools/vendor-risk-assessment", "label": "Vendor Risk Assessment"}
        ],
        "related": [
            {"slug": "what-is-grc", "title": "What is GRC?"},
            {"slug": "grc-interview-questions", "title": "GRC Interview Questions and Answers"}
        ],
        "faq": [
            ["Can freshers get GRC roles?", "Yes, but you need proof of practical understanding. Build sample risk registers, policy drafts, audit checklists and vendor assessments."],
            ["Which certification is best for GRC beginners?", "ISO 27001 Foundation or Lead Auditor, Security+, and later CISA or CRISC depending on your career path."],
            ["Is GRC easier than SOC?", "It is different. GRC is less tool-heavy but requires strong writing, communication, risk thinking and evidence management."]
        ],
        "body": """
<p>A GRC analyst helps organizations manage cybersecurity risk, comply with frameworks and produce evidence for audits, customers and leadership. It is one of the best cybersecurity paths for people who enjoy structure, documentation, business communication and risk analysis.</p>

<h2>Core skills to learn</h2>
<ul>
<li><strong>Risk management:</strong> likelihood, impact, inherent risk, residual risk and treatment.</li>
<li><strong>Frameworks:</strong> ISO 27001, SOC 2, NIST CSF, CIS Controls and privacy basics.</li>
<li><strong>Audit thinking:</strong> evidence, sampling, control testing and nonconformities.</li>
<li><strong>Policy writing:</strong> clear, enforceable policies mapped to real controls.</li>
<li><strong>Vendor risk:</strong> questionnaires, DPAs, certifications and contract clauses.</li>
<li><strong>Communication:</strong> explaining risk to technical and non-technical stakeholders.</li>
</ul>

<h2>Certifications to consider</h2>
<p>Beginners can start with Security+ or ISO 27001 Foundation. If you want audit roles, consider ISO 27001 Lead Auditor or CISA. If you want risk management roles, CRISC becomes valuable after you gain experience.</p>

<h2>Portfolio projects for beginners</h2>
<ol>
<li>Create an ISO 27001 risk register for a sample SaaS company.</li>
<li>Perform a gap assessment using the <a href="/tools/iso-gap-assessment">ISO 27001 Gap Assessment</a>.</li>
<li>Write three policies: access control, incident response and vendor risk.</li>
<li>Assess a vendor using the <a href="/tools/vendor-risk-assessment">Vendor Risk Assessment</a>.</li>
<li>Prepare a mock audit evidence checklist.</li>
</ol>

<h2>Resume tips for GRC roles</h2>
<p>Your resume should mention specific frameworks, artifacts and outcomes. Instead of writing "knowledge of ISO 27001," write "built a sample ISO 27001 risk register with 15 risks, treatment owners and Annex A control mapping." Test your resume with the <a href="/tools/ats-resume-checker">ATS Resume Checker</a>.</p>

<h2>Interview preparation</h2>
<p>Practice explaining risk treatment, SoA, internal audit, vendor risk and policy exceptions. Hiring managers want to know whether you can think clearly, document evidence and communicate with stakeholders. CyberVerse AI can drill you with GRC mock interviews and score your answers.</p>
"""
    },
    {
        "slug": "grc-interview-questions",
        "title": "GRC Interview Questions and Answers for Beginners",
        "category": "GRC",
        "description": "Common GRC interview questions with answer frameworks covering ISO 27001, risk registers, audits, vendor risk, policies and compliance.",
        "author": "Gaurav Malhotra",
        "date": "2026-09-03",
        "read": "9 min read",
        "tools": [
            {"href": "/tools/iso-risk-calculator", "label": "ISO Risk Calculator"},
            {"href": "/tools/security-policy-generator", "label": "Security Policy Generator"},
            {"href": "/tools/vendor-risk-assessment", "label": "Vendor Risk Assessment"}
        ],
        "related": [
            {"slug": "what-is-grc", "title": "What is GRC?"},
            {"slug": "grc-analyst-career-roadmap", "title": "GRC Analyst Career Roadmap"}
        ],
        "faq": [
            ["How should I answer GRC interview questions?", "Use a structured answer: define the concept, explain why it matters, give a practical example, and mention the evidence or artifact produced."],
            ["What should I revise before a GRC interview?", "Revise risk assessment, ISO 27001 clauses, Annex A controls, internal audits, vendor risk, policies and basic privacy concepts."],
            ["Do GRC interviewers ask technical questions?", "Yes, but usually at a conceptual level: MFA, encryption, logging, backups, vulnerability management, access reviews and incident response."]
        ],
        "body": """
<p>GRC interviews test whether you can think in terms of risk, controls, evidence and business impact. The best answers are not memorized definitions. They show how you would apply a framework in a real organization.</p>

<h2>1. What is GRC?</h2>
<p><strong>Answer framework:</strong> GRC stands for governance, risk and compliance. Governance defines accountability and decision-making. Risk identifies what can go wrong and how it affects the business. Compliance ensures requirements from standards, regulations and contracts are met with evidence.</p>

<h2>2. How do you perform a risk assessment?</h2>
<p>Start by identifying assets, threats and vulnerabilities. Score likelihood and impact using a defined methodology. Calculate inherent risk, document existing controls, select a treatment option, assign an owner and track remediation. You can practice this with the <a href="/tools/iso-risk-calculator">ISO Risk Calculator</a>.</p>

<h2>3. What is the difference between risk assessment and risk treatment?</h2>
<p>Risk assessment identifies and evaluates risk. Risk treatment decides what to do with it: mitigate, avoid, transfer or accept. Treatment should have an owner, target date and evidence of completion.</p>

<h2>4. What is a Statement of Applicability?</h2>
<p>The SoA is an ISO 27001 document that lists Annex A controls and explains whether each control is applicable. For applicable controls, it records implementation status. For excluded controls, it records justification.</p>

<h2>5. What is an internal audit?</h2>
<p>An internal audit checks whether the ISMS conforms to ISO 27001 requirements and the organization’s own policies. It should be independent, planned, evidence-based and followed by corrective actions where gaps are found.</p>

<h2>6. How do you assess vendor risk?</h2>
<p>Review data handled, system access, criticality, certifications, encryption, incident response, business continuity, privacy obligations and subprocessors. High-risk vendors need stronger contracts, audit rights and ongoing monitoring. Try the <a href="/tools/vendor-risk-assessment">Vendor Risk Assessment</a>.</p>

<h2>7. What makes a good security policy?</h2>
<p>A good policy is approved, clear, enforceable, owned, reviewed periodically and linked to controls. It should avoid vague statements and define responsibilities. Use the <a href="/tools/security-policy-generator">Security Policy Generator</a> to create a draft, then customize it for the organization.</p>

<h2>8. How do you handle a policy exception?</h2>
<p>Document the exception request, business justification, risk impact, compensating controls, expiry date and approval by the risk owner. Exceptions should not be permanent bypasses.</p>

<h2>9. What evidence would you collect for access control?</h2>
<p>User access review records, MFA configuration screenshots, joiner-mover-leaver tickets, privileged access approvals, IAM logs and policy documents.</p>

<h2>10. What is the difference between compliance and security?</h2>
<p>Compliance means meeting defined requirements. Security means reducing actual risk. A company can be compliant but still insecure if controls are poorly implemented or threats change. Good GRC connects compliance evidence to real risk reduction.</p>

<h2>Practice tip</h2>
<p>Do not only read these answers. Speak them out loud. CyberVerse AI can ask follow-up questions and score whether your answers sound specific enough for a real interview.</p>
"""
    }
'''

if '"slug": "what-is-grc"' not in c:
    # Insert before final closing bracket of ARTICLES list
    idx = c.rfind("]")
    c = c[:idx].rstrip()
    if not c.endswith("["):
        c += ",\n"
    c += new_articles.strip() + "\n]\n"
    open(content_file, "w", encoding="utf-8").write(c)
    print("[ADDED] 3 GRC articles")
else:
    print("[INFO] GRC articles already present")

# Update sitemap tool paths to include all public tool pages
sr = "backend/routers/site_routes.py"
r = open(sr, encoding="utf-8").read()

new_tool_paths = '''TOOL_PATHS = [
    "/tools/iso-risk-calculator",
    "/tools/cvss-calculator",
    "/tools/iso-gap-assessment",
    "/tools/ats-resume-checker",
    "/tools/risk-register-generator",
    "/tools/security-policy-generator",
    "/tools/iso27001-control-finder",
    "/tools/incident-severity-calculator",
    "/tools/vendor-risk-assessment",
]'''

r = re.sub(r'TOOL_PATHS\s*=\s*\[[\s\S]*?\]', new_tool_paths, r, count=1)
open(sr, "w", encoding="utf-8").write(r)
print("[UPDATED] sitemap tool paths")

# Add Latest Articles section to homepage
hp = "backend/templates/index.html"
h = open(hp, encoding="utf-8").read()
if "Latest Articles" not in h:
    section = '''
<section class="section">
    <h2>Latest Articles</h2>
    <div class="grid-3">
        <div class="card"><h3>What is GRC?</h3><p>Governance, risk and compliance explained for cybersecurity beginners.</p><a href="/learn/what-is-grc">Read guide &rarr;</a></div>
        <div class="card"><h3>GRC Analyst Career Roadmap</h3><p>Skills, certifications, portfolio projects and interview prep.</p><a href="/learn/grc-analyst-career-roadmap">Read guide &rarr;</a></div>
        <div class="card"><h3>GRC Interview Questions</h3><p>Practical answer frameworks for common beginner GRC interviews.</p><a href="/learn/grc-interview-questions">Read guide &rarr;</a></div>
    </div>
</section>
'''
    idx = h.rfind("{% endblock %}")
    h = h[:idx] + section + h[idx:]
    open(hp, "w", encoding="utf-8").write(h)
    print("[ADDED] Latest Articles section to homepage")
else:
    print("[INFO] Latest Articles section already present")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Content: add GRC cluster and update sitemap for all tools"])
subprocess.run(["git", "push", "origin", "main"])
print("Pushed. Live in ~60s.")
