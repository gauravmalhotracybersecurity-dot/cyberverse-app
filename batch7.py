import subprocess, sys

articles_py = "backend/content/articles.py"
c = open(articles_py, encoding="utf-8").read()

art1 = r'''

# === Batch 7: Article 1 ===
ARTICLES.append({
    'slug': 'nist-csf-vs-iso-27001-vs-soc2',
    'title': 'NIST CSF vs ISO 27001 vs SOC 2: Which Framework Should Your Company Use?',
    'category': 'GRC',
    'description': 'A practitioner comparison of NIST CSF 2.0, ISO 27001:2022 and SOC 2 - cost, timeline, certification, and which one your company actually needs. No vendor fluff.',
    'author': 'Gaurav Malhotra',
    'date': '2026-09-10',
    'read': '15 min read',
    'tools': [
        {'href': '/tools/iso-gap-assessment', 'label': 'ISO 27001 Gap Assessment'},
        {'href': '/tools/iso-risk-calculator', 'label': 'Risk Calculator'},
        {'href': '/tools/security-policy-generator', 'label': 'Policy Generator'}
    ],
    'related': [
        {'slug': 'what-is-iso-27001', 'title': 'What is ISO 27001?'},
        {'slug': 'iso-27001-risk-assessment', 'title': 'ISO 27001 Risk Assessment'},
        {'slug': 'what-is-grc', 'title': 'What is GRC?'}
    ],
    'faq': [
        ['Can a company use more than one framework?', 'Yes, and most mature companies do. A common stack is NIST CSF as the internal operating framework, ISO 27001 for international certification, and SOC 2 for US enterprise customers. They map to each other well, so the incremental cost of adding a second is lower than starting fresh.'],
        ['Which is cheaper: ISO 27001 or SOC 2?', 'SOC 2 Type I is usually cheaper and faster (8-12 weeks, $15-30K). ISO 27001 certification costs $20-50K and takes 4-8 months. But SOC 2 Type II (12-month observation) ends up comparable to ISO in total cost. For most startups, SOC 2 Type I first, then Type II or ISO based on customer demand.'],
        ['Is NIST CSF certifiable?', 'No. NIST CSF is a voluntary improvement framework - there is no certification or audit. You can self-assess or hire a consultant to assess against it, but there is no certificate to show customers. That is exactly why companies pair it with ISO 27001 or SOC 2 for external proof.'],
        ['Do frameworks replace each other?', 'No. They complement. NIST CSF gives you the operating language and improvement roadmap. ISO 27001 gives you a certifiable ISMS. SOC 2 gives you an attestation report for US customers. Most enterprises run all three mapped together.']
    ],
    'body': """<p>Every quarter I get the same question from founders and new GRC hires: <em>"Should we do ISO 27001, SOC 2, or NIST?"</em></p>
<p>The honest answer is: it depends on who is asking you for proof, how much time you have, and whether you need a certificate or just better security. Most blog posts on this topic are written by compliance vendors selling one specific product, so they all conclude with "buy our ISO module."</p>
<p>This guide is different. I have implemented all three. Here is the practitioner comparison - cost, timeline, certification status, and a decision framework you can use in a board meeting.</p>

<h2>The 60-Second Answer</h2>
<table>
<tr><th>Factor</th><th>NIST CSF 2.0</th><th>ISO 27001:2022</th><th>SOC 2</th></tr>
<tr><td>Type</td><td>Voluntary framework</td><td>Certifiable standard</td><td>Attestation report</td></tr>
<tr><td>Certificate?</td><td>No</td><td>Yes (3-year cycle)</td><td>No (report only)</td></tr>
<tr><td>Primary market</td><td>US + global internal</td><td>International / EU / enterprise</td><td>US enterprise + SaaS</td></tr>
<tr><td>Typical timeline</td><td>Ongoing</td><td>4-8 months</td><td>Type I: 8-12 wks; Type II: 12 mo</td></tr>
<tr><td>Typical cost</td><td>Internal effort</td><td>$20-50K + auditor</td><td>$15-60K + auditor</td></tr>
<tr><td>Best for</td><td>Improving security posture</td><td>Winning EU/enterprise deals</td><td>Winning US SaaS deals</td></tr>
</table>

<h2>NIST CSF 2.0: The Operating Framework</h2>
<p>The NIST Cybersecurity Framework is not a certification. It is a <strong>risk-management language</strong> organized into six functions: Govern, Identify, Protect, Detect, Respond, Recover. Version 2.0 (2024) added the Govern function, which finally made it usable for board-level reporting.</p>
<p><strong>What it gives you:</strong> A way to profile your current posture ("where are we?"), define a target posture ("where do we need to be?"), and prioritize the gaps. It maps cleanly to almost every other control set.</p>
<p><strong>What it does NOT give you:</strong> A certificate. You cannot put a NIST CSF badge on your website that a customer's procurement team will accept as proof. Some US federal and regulated buyers reference it, but for commercial sales it is internal-only.</p>
<p><strong>When to choose it:</strong> You want to improve security without the overhead of certification, or you need a common language across engineering, security, and the board. Many companies start here and layer ISO or SOC 2 on top later.</p>

<h2>ISO 27001:2022: The Certifiable ISMS</h2>
<p>ISO 27001 is an international standard for an Information Security Management System (ISMS). Certification means an accredited auditor verified that you have a working ISMS: risk assessment, Statement of Applicability, controls from Annex A (93 controls in the 2022 version), internal audit, and management review.</p>
<p><strong>What it gives you:</strong> A certificate recognized worldwide. For EU, UK, Middle East, and APAC enterprise sales, ISO 27001 is often a hard requirement in RFPs. It is also the strongest signal of a mature security program.</p>
<p><strong>What it costs:</strong> Real money and real time. Gap assessment (2-4 weeks), risk assessment + SoA (4-6 weeks), policy and control implementation (2-4 months), internal audit + management review (2-4 weeks), Stage 1 + Stage 2 certification audit (4-6 weeks). Total: 4-8 months, $20-50K including auditor fees.</p>
<p><strong>When to choose it:</strong> Your pipeline includes EU/enterprise/government deals that require it, or you want the strongest possible external proof. See our <a href="/learn/what-is-iso-27001">ISO 27001 explainer</a> and <a href="/tools/iso-gap-assessment">gap assessment tool</a> to start.</p>

<h2>SOC 2: The US SaaS Attestation</h2>
<p>SOC 2 is not a certification - it is an <strong>attestation report</strong> produced by a CPA firm against the AICPA Trust Services Criteria (Security is mandatory; Availability, Confidentiality, Processing Integrity, Privacy are optional).</p>
<p><strong>Type I</strong> = point-in-time: "these controls are designed appropriately as of date X." Fast (8-12 weeks), cheaper, and enough to unblock many early enterprise deals.</p>
<p><strong>Type II</strong> = period-of-time: "these controls operated effectively over 3-12 months." This is what mature US buyers actually want. It requires a 3-12 month observation window, so plan accordingly.</p>
<p><strong>What it gives you:</strong> A report you share under NDA with prospects. US SaaS buyers expect it. It is faster to first value than ISO but has no international recognition.</p>
<p><strong>When to choose it:</strong> You are a US-facing SaaS startup and enterprise prospects are blocking deals on security review. Start with Type I, then commit to Type II.</p>

<h2>The Decision Framework (Use This in Your Board Meeting)</h2>
<ol>
<li><strong>Who is asking for proof?</strong> If US SaaS prospects → SOC 2. If EU/enterprise/government → ISO 27001. If nobody yet but you want better security → NIST CSF.</li>
<li><strong>What is your timeline?</strong> Need something in a quarter → SOC 2 Type I. Have 6-9 months → ISO 27001. No deadline → NIST CSF first.</li>
<li><strong>What is your budget?</strong> Under $20K → NIST CSF + SOC 2 Type I prep. $30-60K → pick one certifiable path. $80K+ → run ISO and SOC 2 mapped together.</li>
<li><strong>Do you need a badge or a report?</strong> Badge for website/RFPs → ISO. NDA-shareable report → SOC 2. Internal improvement → NIST.</li>
</ol>

<h2>How They Map to Each Other</h2>
<p>The good news: these are not competing control sets, they are overlapping lenses. A single control (say, MFA on remote access) satisfies NIST CSF Protect, ISO 27001 Annex A 8.5/5.17, and SOC 2 CC6.1 simultaneously. Build your control library once, then map it to each framework's identifiers.</p>
<p>Practical mapping tip: use NIST CSF as your internal operating taxonomy (it is the most readable), ISO 27001 Annex A as your control catalog (it is the most complete), and SOC 2 TSC as your US reporting layer. One control, three labels.</p>

<h2>Common Mistakes</h2>
<ul>
<li><strong>Buying a framework to win one deal:</strong> If a single prospect demands SOC 2, negotiate a security questionnaire + pen test instead of a 6-month program.</li>
<li><strong>Certification without operation:</strong> An ISO certificate for a paper ISMS fails surveillance audits and, worse, fails real incidents. Operate the ISMS first.</li>
<li><strong>Ignoring Govern:</strong> NIST CSF 2.0's Govern function (risk strategy, roles, oversight) is where most programs are actually weak. Do not skip it.</li>
<li><strong>Tool-first thinking:</strong> A GRC platform does not make you compliant. Risk assessment and control operation do. Tools just evidence it.</li>
</ul>

<h2>The Bottom Line</h2>
<p>NIST CSF makes you better. ISO 27001 proves it internationally. SOC 2 proves it to US buyers. Most mature companies run NIST internally and hold one or both external attestations.</p>
<p>Start with the question "who is asking for proof?" and the answer chooses itself. Then use our <a href="/tools/iso-gap-assessment">free gap assessment</a> to see exactly how far you are from whichever path you pick.</p>"""
})'''

art2 = r'''

# === Batch 7: Article 2 ===
ARTICLES.append({
    'slug': 'vendor-risk-assessment-guide',
    'title': 'Vendor Risk Assessment: A Practical Guide for Security Teams (With Scoring Model)',
    'category': 'GRC',
    'description': 'How to run vendor risk assessments that actually catch breaches: tiering, questionnaires, scoring, and continuous monitoring. Includes a ready-to-use scoring model.',
    'author': 'Gaurav Malhotra',
    'date': '2026-09-10',
    'read': '13 min read',
    'tools': [
        {'href': '/tools/vendor-risk-assessment', 'label': 'Vendor Risk Assessment Tool'},
        {'href': '/tools/iso-risk-calculator', 'label': 'Risk Calculator'},
        {'href': '/tools/risk-register-generator', 'label': 'Risk Register Generator'}
    ],
    'related': [
        {'slug': 'iso-27001-risk-assessment', 'title': 'ISO 27001 Risk Assessment'},
        {'slug': 'what-is-grc', 'title': 'What is GRC?'},
        {'slug': 'nist-csf-vs-iso-27001-vs-soc2', 'title': 'NIST CSF vs ISO 27001 vs SOC 2'}
    ],
    'faq': [
        ['How often should vendors be reassessed?', 'By tier: Critical vendors annually (or on material change), High every 12-18 months, Medium every 2 years, Low at renewal. Always reassess on trigger events: breach news, acquisition, major incident, or scope change.'],
        ['What is the difference between vendor risk and third-party risk?', 'They are used interchangeably. Some organizations distinguish third-party (direct vendors) from fourth-party (your vendor\'s vendors). Fourth-party risk is harder to assess and is usually managed through contract clauses requiring your vendor to assess their own suppliers.'],
        ['Do small vendors need full assessments?', 'No. Tier them low and use a lightweight questionnaire or rely on certifications (SOC 2 / ISO 27001) plus contract clauses. Reserve deep assessments for vendors with access to sensitive data or critical operations.'],
        ['What documents should I request from a vendor?', 'SOC 2 Type II or ISO 27001 certificate, pen test summary, incident response policy, data processing agreement, subprocessor list, and evidence of encryption and access controls. A vendor that cannot produce these is telling you something.']
    ],
    'body': """<p>Most of the worst breaches of the last decade did not start at the victim company. They started at a vendor. Target (HVAC contractor), SolarWinds (software supply chain), Kaseya (MSP downstream), and hundreds of others.</p>
<p>Yet most vendor risk programs are a spreadsheet, an annual questionnaire nobody reads, and a checkbox. This guide shows you how to build one that actually catches risk - with a scoring model you can copy today.</p>

<h2>What Vendor Risk Assessment Actually Is</h2>
<p>Vendor risk assessment (VRA) is the process of identifying, scoring, and managing the risk introduced by third parties that touch your data, systems, or operations. It is a core requirement in ISO 27001 (Annex A 5.19-5.23), NIST CSF (Identify/Supply Chain), and most regulatory regimes.</p>
<p>The goal is not to eliminate vendor risk - that is impossible. The goal is to <strong>know which vendors can hurt you, how badly, and what you are doing about it</strong>.</p>

<h2>Step 1: Build the Vendor Inventory</h2>
<p>You cannot assess what you cannot see. Start by enumerating every vendor that:</p>
<ul>
<li>Stores, processes, or transmits your data (customer PII, employee data, financials)</li>
<li>Has network or system access (SSO, VPN, admin consoles)</li>
<li>Provides critical operations (payroll, hosting, payments, communications)</li>
<li>Is embedded in your product (SDKs, APIs, subprocessors)</li>
</ul>
<p>Sources: accounts payable records, SSO logs, contract repository, cloud billing, and asking team leads. Expect to find 30-50% more vendors than anyone guessed.</p>

<h2>Step 2: Tier Your Vendors</h2>
<p>Not all vendors deserve equal scrutiny. Tier by two axes: <strong>data access</strong> and <strong>business criticality</strong>.</p>
<table>
<tr><th>Tier</th><th>Definition</th><th>Assessment Depth</th><th>Frequency</th></tr>
<tr><td>Critical</td><td>Bulk sensitive data OR single point of failure for operations</td><td>Full questionnaire + evidence + pen test review</td><td>Annual</td></tr>
<tr><td>High</td><td>Limited sensitive data OR important but replaceable service</td><td>Full questionnaire + certifications</td><td>12-18 months</td></tr>
<tr><td>Medium</td><td>Internal data only, non-critical</td><td>Short questionnaire or cert review</td><td>2 years</td></tr>
<tr><td>Low</td><td>No data access, easily replaceable</td><td>Self-attestation + contract clauses</td><td>At renewal</td></tr>
</table>

<h2>Step 3: The Questionnaire (Ask What Matters)</h2>
<p>Skip the 300-question SIG Lite dump for everyone. Ask targeted questions per tier. Core questions that catch real risk:</p>
<ul>
<li><strong>Access:</strong> Do you store our data? Where (regions)? Do you have production access to our environment?</li>
<li><strong>Subprocessors:</strong> List all subprocessors touching our data. How do you notify us of changes?</li>
<li><strong>Security proof:</strong> Current SOC 2 Type II or ISO 27001? Most recent pen test summary?</li>
<li><strong>Incidents:</strong> Breach notification SLA? Have you had a reportable incident in 24 months?</li>
<li><strong>Controls:</strong> MFA everywhere? Encryption at rest and in transit? Logging and monitoring? Offboarding process?</li>
<li><strong>Resilience:</strong> Backups tested? DR plan? RTO/RPO commitments?</li>
</ul>
<p>For Critical tier, demand evidence, not assertions: certificates, pen test executive summaries, and screenshots or policy excerpts where appropriate.</p>

<h2>Step 4: The Scoring Model (Copy This)</h2>
<p>Score each vendor 1-5 on four dimensions, then compute inherent and residual risk.</p>
<ul>
<li><strong>Data Sensitivity (D):</strong> 1 = no data, 5 = bulk regulated/PII</li>
<li><strong>Access Depth (A):</strong> 1 = none, 5 = production admin</li>
<li><strong>Business Criticality (B):</strong> 1 = nice-to-have, 5 = operations stop without them</li>
<li><strong>Control Maturity (C):</strong> 1 = strong evidence, 5 = no evidence / weak answers</li>
</ul>
<p><strong>Inherent Risk = max(D, A, B)</strong> (how bad could it get). <strong>Residual Risk = Inherent x (C / 5)</strong> rounded up. Then map:</p>
<ul>
<li>Residual 1-2: Accept, monitor at renewal</li>
<li>Residual 3: Mitigate - contract clauses + remediation plan</li>
<li>Residual 4-5: Escalate - remediation with deadline, or replace vendor</li>
</ul>
<p>Example: payroll provider with employee PII (D=4), SSO access (A=3), operations-critical (B=4) → Inherent 4. They produce SOC 2 Type II and clean pen test (C=2) → Residual = ceil(4 x 0.4) = 2 → Accept with annual review. Same vendor with no evidence (C=5) → Residual 4 → Escalate.</p>
<p>Run this in our <a href="/tools/vendor-risk-assessment">Vendor Risk Assessment tool</a> to generate the scored register automatically.</p>

<h2>Step 5: Remediate and Contract</h2>
<p>For every vendor above your risk appetite, do one or more of:</p>
<ul>
<li><strong>Remediation plan:</strong> Written commitments with dates (e.g., "MFA on admin console by Q3").</li>
<li><strong>Contract clauses:</strong> Breach notification within 72h, right to audit, subprocessor approval, data return/deletion on exit, security requirements exhibit.</li>
<li><strong>Compensating controls:</strong> Restrict their access, segment network, DLP on exports, require SSO.</li>
<li><strong>Replace:</strong> If residual risk stays 4-5 after remediation attempts, start exit planning.</li>
</ul>

<h2>Step 6: Continuous Monitoring (The Part Everyone Skips)</h2>
<p>Annual questionnaires go stale the day they are signed. Add trigger-based monitoring:</p>
<ul>
<li>Security rating services or news alerts for breach mentions</li>
<li>Certificate expiry and subprocessor change notifications</li>
<li>SSO/VPN access reviews quarterly for Critical tier</li>
<li>Re-assessment on trigger events: acquisition, breach, major outage, scope expansion</li>
</ul>

<h2>Common Mistakes</h2>
<ul>
<li><strong>Assessing everything equally:</strong> You will drown. Tier first, always.</li>
<li><strong>Trusting self-attestation for Critical vendors:</strong> Ask for evidence.</li>
<li><strong>No owner per vendor:</strong> Every Critical/High vendor needs a business owner accountable for the relationship, not just security.</li>
<li><strong>Ignoring fourth parties:</strong> Require Critical vendors to disclose and manage their own subprocessors.</li>
<li><strong>Assessment without action:</strong> A scored register with no remediation column is decoration.</li>
</ul>

<h2>The Bottom Line</h2>
<p>Vendor risk is where modern breaches live. A working program is: inventory → tier → targeted questionnaire → score → remediate → monitor. Six steps, one register, and the discipline to reassess on triggers.</p>
<p>Start this week: pull your accounts payable list, tier the top 20 vendors, and score them with the model above. You will find at least one Critical vendor with no evidence - and that is the one that would have been next quarter's headline.</p>"""
})'''

if 'nist-csf-vs-iso-27001-vs-soc2' not in c:
    c += art1
    print("[ADDED] NIST CSF vs ISO 27001 vs SOC 2")
else:
    print("[SKIP] Framework article already present")

if 'vendor-risk-assessment-guide' not in c:
    c += art2
    print("[ADDED] Vendor Risk Assessment Guide")
else:
    print("[SKIP] Vendor article already present")

try:
    compile(c, articles_py, "exec")
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print(f"[ABORT] Syntax error: {e}")
    raise SystemExit(1)

open(articles_py, "w", encoding="utf-8").write(c)

sys.path.insert(0, "backend")
for m in list(sys.modules):
    if 'content' in m or 'articles' in m:
        del sys.modules[m]
from content import articles
slugs = [a['slug'] for a in articles.ARTICLES]
print(f"\n[VERIFY] Total articles: {len(articles.ARTICLES)}")
print(f"  - nist-csf-vs-iso-27001-vs-soc2: {'YES' if 'nist-csf-vs-iso-27001-vs-soc2' in slugs else 'NO'}")
print(f"  - vendor-risk-assessment-guide: {'YES' if 'vendor-risk-assessment-guide' in slugs else 'NO'}")

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Content batch 7: framework comparison + vendor risk guide"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout if r.returncode == 0 else r.stderr}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
