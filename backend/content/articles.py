ARTICLES = [
    {
        "slug": "what-is-iso-27001",
        "title": "What is ISO 27001? The Complete Beginner Guide (2026)",
        "category": "ISO 27001",
        "description": "What ISO 27001 certifies, what changed in the 2022 revision, how Annex A is structured, how certification works, and how to start implementing this week.",
        "author": "Gaurav Malhotra",
        "date": "2026-09-03",
        "read": "8 min read",
        "tools": [
            {"href": "/tools/iso-gap-assessment", "label": "ISO 27001 Gap Assessment"},
            {"href": "/tools/iso-risk-calculator", "label": "ISO 27001 Risk Calculator"},
            {"href": "/tools/risk-register-generator", "label": "Risk Register Generator"}
        ],
        "related": [
            {"slug": "iso-27001-risk-assessment", "title": "ISO 27001 Risk Assessment Explained (With a Worked Example)"}
        ],
        "faq": [
            ["Is ISO 27001 mandatory?", "No. It is a voluntary international standard. However, enterprise contracts, tenders and sector regulations often make certification a practical requirement to win business, especially in SaaS, fintech and healthcare."],
            ["How long does ISO 27001 certification take?", "Most small to mid-size organizations take 3 to 12 months from kickoff to certificate, depending on scope, existing maturity and how much documentation already exists."],
            ["What is the difference between ISO 27001 and ISO 27002?", "ISO 27001 defines the requirements for the management system and is the standard you certify against. ISO 27002 is the companion code of practice explaining how to implement the Annex A controls."],
            ["Do I need a consultant to get certified?", "No, but experienced help shortens the timeline. You can self-implement using the standard, a gap assessment and a solid risk register - the free tools on this site produce the core artifacts."]
        ],
        "body": """
<p>ISO/IEC 27001 is the international standard for an <strong>Information Security Management System (ISMS)</strong>. It does not tell you which firewall to buy - it requires you to build a management system that identifies your information security risks and treats them consistently, with evidence an auditor can verify.</p>
<h2>What ISO 27001 actually certifies</h2>
<p>Certification covers your <strong>management system</strong>, not a product. An auditor checks that you defined a scope, obtained leadership commitment, assessed risks, selected controls, and that you monitor, audit and improve the system over time. That is why a 20-person SaaS company and a bank can both be certified - the standard scales with your risk.</p>
<h2>What changed in the 2022 revision</h2>
<ul>
<li>The standard was restructured and renamed <strong>ISO/IEC 27001:2022</strong>.</li>
<li>Annex A now contains <strong>93 controls in four themes</strong> instead of 114 in 14 domains.</li>
<li>11 new controls were added, including threat intelligence, cloud security, ICT readiness for business continuity, secure coding, and data masking.</li>
<li>Certificates against the old 2013 version had to transition - any certificate you see today should be 2022-based.</li>
</ul>
<h2>The structure: Clauses 4-10</h2>
<ul>
<li><strong>Clause 4 - Context:</strong> internal/external issues, interested parties, ISMS scope.</li>
<li><strong>Clause 5 - Leadership:</strong> management commitment, policy, roles.</li>
<li><strong>Clause 6 - Planning:</strong> risk assessment, risk treatment, Statement of Applicability (SoA), objectives.</li>
<li><strong>Clause 7 - Support:</strong> competence, awareness, documented information.</li>
<li><strong>Clause 8 - Operation:</strong> doing what you planned, including periodic risk assessments.</li>
<li><strong>Clause 9 - Performance evaluation:</strong> metrics, internal audit, management review.</li>
<li><strong>Clause 10 - Improvement:</strong> nonconformities and corrective action.</li>
</ul>
<h2>Annex A: 93 controls in four themes</h2>
<ul>
<li><strong>Organizational (37):</strong> policies, vendor relationships, incident management, business continuity.</li>
<li><strong>People (8):</strong> screening, terms of employment, awareness training.</li>
<li><strong>Physical (14):</strong> perimeters, entry controls, equipment protection.</li>
<li><strong>Technological (34):</strong> access control, cryptography, logging, secure development.</li>
</ul>
<h2>How certification works</h2>
<ol>
<li><strong>Stage 1 audit:</strong> the certification body reviews documentation and readiness.</li>
<li><strong>Stage 2 audit:</strong> the auditor checks the ISMS is actually implemented and effective.</li>
<li><strong>Surveillance audits:</strong> annual check-ins in years 1 and 2.</li>
<li><strong>Recertification:</strong> full audit at year 3, then the cycle repeats.</li>
</ol>
<h2>How to start implementing (this week)</h2>
<ol>
<li>Define scope and get a signed information security policy (Clauses 4-5).</li>
<li>Run a <a href="/tools/iso-gap-assessment">gap assessment</a> to see where you stand.</li>
<li>Perform a <a href="/tools/iso-risk-calculator">risk assessment</a> using a documented 5x5 method.</li>
<li>Export a <a href="/tools/risk-register-generator">risk register</a> with owners, treatments and target dates.</li>
<li>Use the register to build your Statement of Applicability, then schedule an internal audit.</li>
</ol>
<h2>Common beginner mistakes</h2>
<ul>
<li>Writing 80 policies before doing a single risk assessment (the standard is risk-driven, not document-driven).</li>
<li>Scoping too broadly - certify the part of the business clients care about first.</li>
<li>Treating the SoA as a checklist instead of a justified decision record.</li>
</ul>
"""
    },
    {
        "slug": "iso-27001-risk-assessment",
        "title": "ISO 27001 Risk Assessment Explained (With a Worked Example)",
        "category": "ISO 27001",
        "description": "Clause 6.1.2 requirements, a simple 5x5 likelihood-impact method, a worked example risk table, and the four treatment options - with free tools to produce your register.",
        "author": "Gaurav Malhotra",
        "date": "2026-09-03",
        "read": "6 min read",
        "tools": [
            {"href": "/tools/iso-risk-calculator", "label": "ISO 27001 Risk Calculator"},
            {"href": "/tools/risk-register-generator", "label": "Risk Register Generator"}
        ],
        "related": [
            {"slug": "what-is-iso-27001", "title": "What is ISO 27001? The Complete Beginner Guide (2026)"}
        ],
        "faq": [
            ["How often should an ISO 27001 risk assessment be repeated?", "At planned intervals - commonly annually - and whenever a significant change occurs, such as a new system, a major incident, a new vendor or a change in scope."],
            ["What is risk acceptance and who signs it?", "Risks above your acceptance level must be treated. Any risk deliberately left above it must be signed off by the risk owner, because acceptance is a business decision, not a technical one."]
        ],
        "body": """
<p>Risk assessment is the engine of ISO 27001. Clause 6.1.2 requires you to <strong>define a method</strong> - including risk criteria and an acceptance level - then identify, analyse and evaluate risks, and retain documented results. The standard does not force a formula; it forces consistency. Here is a method that passes audits and is simple enough to run today.</p>
<h2>A simple, auditable 5x5 method</h2>
<p>Score each risk as <strong>Likelihood (1-5) x Impact (1-5)</strong>, giving a 1-25 score. Define bands up front, for example: 1-4 Low, 5-9 Medium, 10-16 High, 17-25 Critical. State your acceptance level (for example: accept nothing above Medium without sign-off). Documenting the method <em>before</em> scoring is what makes it auditable.</p>
<h2>Worked example</h2>
<table>
<tr><th>Asset</th><th>Threat / Vulnerability</th><th>L</th><th>I</th><th>Score</th><th>Level</th><th>Treatment</th></tr>
<tr><td>Customer database</td><td>Ransomware; unpatched OS, no admin MFA</td><td>4</td><td>5</td><td>20</td><td>Critical</td><td>Mitigate: EDR, MFA, offline backups</td></tr>
<tr><td>Employee laptops</td><td>Theft; no full-disk encryption</td><td>3</td><td>4</td><td>12</td><td>High</td><td>Mitigate: FDE + MDM remote wipe</td></tr>
<tr><td>SaaS admin console</td><td>Credential phishing; no phishing-resistant MFA</td><td>3</td><td>4</td><td>12</td><td>High</td><td>Mitigate: FIDO2 keys + awareness training</td></tr>
<tr><td>Marketing site</td><td>Defacement; outdated CMS plugins</td><td>2</td><td>2</td><td>4</td><td>Low</td><td>Accept with patch monitoring</td></tr>
</table>
<h2>The four treatment options</h2>
<ul>
<li><strong>Mitigate:</strong> apply controls (most common) - e.g., MFA, encryption, EDR.</li>
<li><strong>Transfer:</strong> shift impact, e.g., cyber insurance or a contractually responsible vendor.</li>
<li><strong>Avoid:</strong> stop the activity causing the risk.</li>
<li><strong>Accept:</strong> consciously live with it, with risk-owner sign-off.</li>
</ul>
<h2>From assessment to register to SoA</h2>
<p>Every assessed risk becomes a register row: asset, threat, vulnerability, score, existing controls, treatment, owner and target date - you can generate and export this with the <a href="/tools/risk-register-generator">Risk Register Generator</a>. The treatments you select then map to Annex A controls in your <strong>Statement of Applicability</strong>, closing the loop between Clauses 6 and 8. If you are new to the standard, start with the <a href="/learn/what-is-iso-27001">beginner guide</a> first.</p>
"""
    },
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
,
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
    }
,
    {
        "slug": "what-does-soc-analyst-do",
        "title": "What Does a SOC Analyst Do? Shifts, Tools, and Career Path (2026)",
        "category": "SOC",
        "description": "The honest picture of SOC work: the three tiers, a real shift walkthrough, the tool stack you will actually touch, and the path from first shift to threat hunting.",
        "author": "Gaurav Malhotra",
        "date": "2026-09-08",
        "read": "7 min read",
        "tools": [
            {"href": "/app.html", "label": "AI Mock Interview Coach"},
            {"href": "/tools/ats-resume-checker", "label": "Resume ATS Checker"}
        ],
        "related": [
            {"slug": "how-to-start-grc-career", "title": "How to Start a GRC Career in 2026 (Even Without an IT Background)"},
            {"slug": "grc-analyst-career-roadmap", "title": "GRC Analyst Career Roadmap (2026): Zero to Job-Ready"}
        ],
        "faq": [
            ["Is SOC analyst a good first job in cybersecurity?", "Yes - it is the most common entry point because it teaches detection, triage and incident process faster than any other role, and it hires from non-traditional backgrounds."],
            ["Do SOC analysts work nights?", "Many centers run 24x7 with rotating shifts, especially L1. Ask about rotation policy in interviews; plenty of enterprise SOCs also run follow-the-sun models with day shifts."],
            ["What tools will I touch in my first month?", "A SIEM (Splunk, Sentinel or Elastic), an EDR console, a ticketing system, and runbooks/playbooks. SOAR and threat-intel platforms usually come later."]
        ],
        "body": """
<p>A SOC analyst's job in one sentence: <strong>watch, triage, escalate, document</strong> - then make the next analyst's life easier. Everything else is detail. Here is the honest picture before you apply.</p>
<h2>The three tiers</h2>
<ul>
<li><strong>L1 (Triage):</strong> monitor queues, enrich alerts, separate signal from noise, open tickets, escalate with clean notes.</li>
<li><strong>L2 (Incident Response):</strong> own incidents end-to-end, contain threats, coordinate with IT, write post-incident summaries.</li>
<li><strong>L3 (Threat Hunting / Detection Engineering):</strong> hunt without alerts, build and tune detections, research adversary TTPs.</li>
</ul>
<h2>A realistic shift, hour by hour</h2>
<ol>
<li>Handover read: open incidents, watchlist changes, maintenance windows.</li>
<li>Queue sweep: rank alerts by asset criticality, not by timestamp.</li>
<li>Triage loop per alert: enrich (user, host, process, network), scope (one host or many?), decide (false positive, monitor, escalate).</li>
<li>Escalate with evidence: what fired, what you checked, what you ruled out, what you recommend.</li>
<li>Tune: propose one false-positive reduction per shift - this is how L1s get noticed.</li>
<li>Document: if it is not in the ticket, it did not happen.</li>
</ol>
<h2>The tool stack you will actually touch</h2>
<ul>
<li><strong>SIEM:</strong> Splunk, Microsoft Sentinel or Elastic - your primary lens.</li>
<li><strong>EDR:</strong> CrowdStrike, Defender for Endpoint or similar for host truth.</li>
<li><strong>Ticketing + playbooks:</strong> where decisions become process.</li>
<li><strong>Threat intel:</strong> MISP or commercial TIPs, used to enrich not to impress.</li>
</ul>
<h2>Shifts and lifestyle</h2>
<p>Expect rotation early (nights/weekends in 24x7 centers), strong handover culture, and quiet hours used for training. Follow-the-sun MSSPs and enterprise day-shift SOCs exist - ask in interviews.</p>
<h2>Career path and trajectory</h2>
<p>L1 to L2 typically 18-30 months with documented incidents and tuning wins; then L3/hunting, IR, detection engineering, or a lateral move into GRC or cloud security. The SOC is a launchpad, not a ceiling.</p>
<h2>Getting hired into your first shift</h2>
<ol>
<li>Fundamentals: networking, Windows/Linux internals, attack basics.</li>
<li>Home lab: ingest real logs into Splunk or Elastic and write three detections - the <a href="/app.html">Lab Log</a> ships ready-made lab plans.</li>
<li>Resume: metrics-driven bullets ("built 3 SPL detections cutting FP by 40%") checked with the <a href="/tools/ats-resume-checker">ATS checker</a>.</li>
<li>Interviews: practice triage scenarios out loud until your escalation notes sound professional.</li>
</ol>
"""
    },
    {
        "slug": "splunk-vs-elastic-vs-sentinel",
        "title": "Splunk vs Elastic vs Microsoft Sentinel: Which SIEM Should You Learn First? (2026)",
        "category": "SOC",
        "description": "A practitioner's comparison of the three SIEMs that dominate job descriptions: query languages, cost to learn, hiring demand, and a 30-day plan to get employable in one of them.",
        "author": "Gaurav Malhotra",
        "date": "2026-09-08",
        "read": "8 min read",
        "tools": [
            {"href": "/app.html", "label": "CyberVerse Lab Log (Splunk lab included)"}
        ],
        "related": [
            {"slug": "what-does-soc-analyst-do", "title": "What Does a SOC Analyst Do? Shifts, Tools, and Career Path (2026)"},
            {"slug": "how-to-start-grc-career", "title": "How to Start a GRC Career in 2026 (Even Without an IT Background)"}
        ],
        "faq": [
            ["Can I learn a SIEM for free?", "Yes. Splunk offers a free tier (500 MB/day), Elastic has a trial cluster, and Sentinel can be explored with Azure free credits. Your home lab costs nothing but time."],
            ["Which SIEM gets me hired fastest in India?", "Splunk still appears in the most Indian job descriptions (enterprise + MSSP install base), with Sentinel growing fast in Microsoft-heavy shops. Learn one deeply; mention the others knowingly."],
            ["Do I need to master all three?", "No. Concepts transfer: ingestion, correlation, alerting, dashboards. Depth in one plus vocabulary in the others beats shallow triple coverage."]
        ],
        "body": """
<p>The SIEM is the SOC's eye. Job descriptions name-drop three platforms more than any others - and choosing wrong costs months. Here is the practitioner's comparison, not the vendor's.</p>
<h2>Splunk</h2>
<ul>
<li><strong>Query language:</strong> SPL - pipe-based, expressive, its own dialect worth flaunting on a resume.</li>
<li><strong>Cost to learn:</strong> free tier 500 MB/day is genuinely enough for a home lab.</li>
<li><strong>Hiring demand:</strong> still the most-listed SIEM in enterprise and MSSP JDs globally and in India.</li>
<li><strong>Culture:</strong> mature playbooks, strong admin/tooling ecosystem, enterprise price tag at work.</li>
</ul>
<h2>Elastic (ELK / Elastic Security)</h2>
<ul>
<li><strong>Query language:</strong> KQL and Lucene; DevOps-friendly, JSON everywhere.</li>
<li><strong>Cost to learn:</strong> open-source core; cloud trial clusters are quick to spin.</li>
<li><strong>Hiring demand:</strong> strong in startups, product companies, detection-engineering teams.</li>
<li><strong>Culture:</strong> build-your-own mindset - great for learning detection engineering from scratch.</li>
</ul>
<h2>Microsoft Sentinel</h2>
<ul>
<li><strong>Query language:</strong> KQL - clean, readable, shared with Defender and Log Analytics.</li>
<li><strong>Cost to learn:</strong> Azure free credits; connectors for M365 make data appear instantly.</li>
<li><strong>Hiring demand:</strong> fastest-growing, especially in Microsoft-shop enterprises and MSSPs.</li>
<li><strong>Culture:</strong> cloud-native, ARM/Bicep automation, pay-per-ingest discipline.</li>
</ul>
<h2>Head-to-head</h2>
<ul>
<li><strong>Fastest first alert:</strong> Sentinel (connectors) &gt; Splunk (free tier + docs) &gt; Elastic (setup work).</li>
<li><strong>Most JD mentions:</strong> Splunk &gt; Sentinel &gt; Elastic (India, 2026).</li>
<li><strong>Best for detection-engineering depth:</strong> Elastic, then Splunk.</li>
<li><strong>Best for cloud-native careers:</strong> Sentinel.</li>
</ul>
<h2>Verdict: learn in this order</h2>
<ol>
<li><strong>Splunk fundamentals</strong> if your target market is enterprise/MSSP - the JD volume is unbeatable.</li>
<li><strong>Add KQL/Sentinel</strong> if your target companies run Microsoft 365 (most do).</li>
<li><strong>Touch Elastic</strong> only when a role or lab demands it - concepts transfer by then.</li>
</ol>
<h2>The 30-day SIEM study plan</h2>
<ol>
<li><strong>Week 1:</strong> install Splunk free, forward Sysmon + web logs, write 10 searches.</li>
<li><strong>Week 2:</strong> build 2 alerts + 1 dashboard; break them; fix them.</li>
<li><strong>Week 3:</strong> write one use case end-to-end (threat, data source, SPL, false-positive notes).</li>
<li><strong>Week 4:</strong> publish a writeup, convert it into resume bullets and a 90-second interview story.</li>
</ol>
<p>The <a href="/app.html">CyberVerse Lab Log</a> includes a guided Splunk home-lab plan with evidence checklist - finish it and you have lab proof, not just theory.</p>
"""
    }
]


# Batch 5 additions
ARTICLES.append({'slug': 'cybersecurity-salary-india-2026', 'title': 'Cybersecurity Salary in India 2026: Role-by-Role Breakdown', 'category': 'Career', 'description': 'Real cybersecurity salaries in India for 2026: SOC analyst, GRC consultant, pentester, security engineer. Entry-level to 10+ years experience.', 'author': 'Gaurav Malhotra', 'date': '2026-09-08', 'read': '12 min read', 'tools': [{'href': '/tools/cybersecurity-salary-calculator', 'label': 'Salary Calculator'}, {'href': '/tools/career-roadmap', 'label': 'Career Roadmap'}], 'related': [{'slug': 'grc-analyst-career-roadmap', 'title': 'GRC Analyst Career Roadmap'}, {'slug': 'grc-interview-questions', 'title': 'GRC Interview Questions'}], 'faq': [['What is the starting salary for a SOC analyst in India?', 'Entry-level SOC analysts (L1) earn 4-6 LPA at service companies, 8-12 LPA at Indian product companies, and 15-20 LPA at US/EU remote roles.'], ['Which certification increases salary the most?', 'OSCP adds 30-40% to pentesting salaries. CISSP and CISM add 20-30% to senior/management roles.'], ['Is GRC higher paying than pentesting?', 'At senior levels, yes. GRC managers earn 35-80 LPA while senior pentesters earn 25-40 LPA.'], ['How often should I switch jobs for salary growth?', 'Every 2-3 years. Staying 5+ years at the same company typically means 20-30% below market rate.']], 'body': '<p>Every week I get asked: <em>"What\'s the salary for X role in cybersecurity?"</em></p>\n<p>The honest answer: it depends on role, experience, location, company size, and industry. A SOC analyst at TCS makes 6-8 LPA. The same role at a US-based product company pays 18-25 LPA.</p>\n<p>This guide breaks down <strong>real 2026 salary data</strong> I\'ve gathered from hiring managers, candidates, and public compensation reports.</p>\n<h2>Entry-Level (0-2 years experience)</h2>\n<h3>SOC Analyst (L1)</h3>\n<ul>\n<li><strong>Service-based (TCS, Infosys, Wipro):</strong> 4-6 LPA</li>\n<li><strong>Product-based (Indian):</strong> 8-12 LPA</li>\n<li><strong>Product-based (US/EU remote):</strong> 15-20 LPA</li>\n</ul>\n<h3>Junior Penetration Tester</h3>\n<ul>\n<li><strong>Consulting firms:</strong> 6-10 LPA</li>\n<li><strong>Product companies:</strong> 12-18 LPA</li>\n</ul>\n<h3>GRC Associate / Compliance Analyst</h3>\n<ul>\n<li><strong>Big 4 (Deloitte, EY, PwC, KPMG):</strong> 7-10 LPA</li>\n<li><strong>Mid-size consulting:</strong> 5-8 LPA</li>\n<li><strong>In-house (product companies):</strong> 10-15 LPA</li>\n</ul>\n<h2>Mid-Level (3-5 years experience)</h2>\n<h3>SOC Analyst (L2/L3) / Incident Responder</h3>\n<ul>\n<li><strong>Service-based:</strong> 10-15 LPA</li>\n<li><strong>Product-based (Indian):</strong> 18-25 LPA</li>\n<li><strong>Product-based (US/EU remote):</strong> 30-45 LPA</li>\n</ul>\n<h3>Penetration Tester / Red Teamer</h3>\n<ul>\n<li><strong>Consulting:</strong> 15-22 LPA</li>\n<li><strong>In-house (product):</strong> 25-40 LPA</li>\n<li><strong>Bug bounty (full-time):</strong> 20-50 LPA (highly variable)</li>\n</ul>\n<h3>GRC Consultant / Security Analyst</h3>\n<ul>\n<li><strong>Big 4:</strong> 15-22 LPA</li>\n<li><strong>Product companies:</strong> 20-35 LPA</li>\n<li><strong>Freelance/consulting:</strong> 25-50 LPA (if you have client pipeline)</li>\n</ul>\n<h2>Senior-Level (6-10 years experience)</h2>\n<h3>Security Architect</h3>\n<ul>\n<li><strong>Product companies:</strong> 40-70 LPA</li>\n<li><strong>FAANG/MNC:</strong> 60-100 LPA (with stock)</li>\n</ul>\n<h3>GRC Manager / Head of Compliance</h3>\n<ul>\n<li><strong>Mid-size companies:</strong> 35-50 LPA</li>\n<li><strong>Large enterprises:</strong> 50-80 LPA</li>\n<li><strong>Startups (Series B+):</strong> 40-65 LPA + equity</li>\n</ul>\n<h3>CISO / VP of Security</h3>\n<ul>\n<li><strong>Mid-size:</strong> 60-100 LPA</li>\n<li><strong>Large enterprise:</strong> 100-200 LPA + significant equity</li>\n</ul>\n<h2>Location Matters</h2>\n<p><strong>Bangalore:</strong> Highest salaries but highest cost of living. 25 LPA in Bangalore = 18 LPA in Pune purchasing power.</p>\n<p><strong>Mumbai / Delhi NCR:</strong> Strong consulting presence. 10-15% lower than Bangalore but lower rent.</p>\n<p><strong>Pune / Hyderabad / Chennai:</strong> Best salary-to-cost-of-living ratio.</p>\n<p><strong>Remote (US/EU companies):</strong> 30-50 LPA for mid-level, 60-100 LPA for senior. Requires excellent English and timezone overlap.</p>\n<h2>The Bottom Line</h2>\n<p>Cybersecurity salaries in India are strong and growing. The highest earners specialize early, get certified, switch companies strategically, and target product companies over service companies.</p>\n<p>25-40 LPA by year 5 is realistic. 50-100 LPA by year 10 is achievable. But if you\'re staying at the same service company for 5+ years without specializing, you\'ll be stuck at 12-15 LPA.</p>'})

ARTICLES.append({'slug': 'best-cybersecurity-certifications-beginners-2026', 'title': 'Best Cybersecurity Certifications for Beginners (2026): Cost vs ROI', 'category': 'Career', 'description': 'Which cybersecurity certifications are worth the money in 2026? Honest cost vs ROI analysis: CompTIA Security+, CEH, OSCP, CISSP, and more.', 'author': 'Gaurav Malhotra', 'date': '2026-09-08', 'read': '14 min read', 'tools': [{'href': '/tools/certification-roadmap', 'label': 'Certification Roadmap'}, {'href': '/tools/grc-interview-prep', 'label': 'Interview Prep'}], 'related': [{'slug': 'cybersecurity-salary-india-2026', 'title': 'Cybersecurity Salary in India 2026'}, {'slug': 'how-to-start-grc-career', 'title': 'How to Start a GRC Career'}], 'faq': [['Is CompTIA Security+ worth it in 2026?', "Yes for entry-level. It's the 'driver's license' of cybersecurity - expected by 60-70% of entry-level job postings. Cost 40-50K, 2-3 months prep."], ['Should I get CEH or OSCP?', 'OSCP is 10x more respected in pentesting. CEH is mostly a multiple-choice test. Only get CEH if your employer pays for it.'], ['When should I get CISSP?', "Only after 5+ years experience targeting management/architect roles. Getting it early makes you 'Associate of (ISC)²' which looks weak."], ['Are certifications better than a GitHub portfolio?', 'Skills > certifications. A candidate with GitHub projects and blog posts beats someone with 5 certifications and no practical experience.']], 'body': '<p>Every year, thousands of aspiring cybersecurity professionals spend 50K-2L on certifications that <strong>don\'t help them get hired</strong>.</p>\n<p>I know because I\'ve been on both sides: I\'ve earned certifications, and I\'ve interviewed candidates who had them. The gap between "certification holder" and "qualified professional" is often enormous.</p>\n<h2>How to Evaluate a Certification</h2>\n<h3>1. Does it teach real skills?</h3>\n<p>A good certification should make you <em>actually better</em> at the job, not just better at passing a test.</p>\n<h3>2. Do employers care?</h3>\n<p>Check 20 job postings for your target role. If less than 30% list this cert as required/preferred, it\'s probably not worth it.</p>\n<h3>3. What\'s the ROI?</h3>\n<p>Calculate: (Salary increase) / (Cost + study time). If payback > 2 years, reconsider.</p>\n<h2>Entry-Level Certifications (0-2 years)</h2>\n<h3>CompTIA Security+ ✅ RECOMMENDED</h3>\n<ul>\n<li><strong>Cost:</strong> 40-50K total</li>\n<li><strong>Time:</strong> 2-3 months (10-15 hours/week)</li>\n<li><strong>Salary impact:</strong> +1-2 LPA</li>\n<li><strong>Employer recognition:</strong> 60-70%</li>\n</ul>\n<p><strong>Verdict:</strong> Worth it for entry-level. Pair with hands-on practice (TryHackMe, HackTheBox).</p>\n<h3>Certified Ethical Hacker (CEH) ⚠️ MIXED</h3>\n<ul>\n<li><strong>Cost:</strong> 70-90K total</li>\n<li><strong>Time:</strong> 3-4 months</li>\n<li><strong>Salary impact:</strong> +1-2 LPA</li>\n<li><strong>Employer recognition:</strong> 40-50%</li>\n</ul>\n<p><strong>Verdict:</strong> Only if employer pays or targeting government roles. Otherwise spend on OSCP prep.</p>\n<h2>Mid-Level Certifications (3-5 years)</h2>\n<h3>Offensive Security Certified Professional (OSCP) ✅ HIGHLY RECOMMENDED</h3>\n<ul>\n<li><strong>Cost:</strong> 1.2-1.5L (non-refundable)</li>\n<li><strong>Time:</strong> 3-6 months intensive</li>\n<li><strong>Salary impact:</strong> +5-8 LPA</li>\n<li><strong>Employer recognition:</strong> 80-90%</li>\n</ul>\n<p><strong>Verdict:</strong> Gold standard for pentesting. OSCP holders earn 30-40% more. Only attempt with 2+ years IT experience.</p>\n<h3>CISSP ⚠️ CONDITIONAL</h3>\n<ul>\n<li><strong>Cost:</strong> 70-90K total</li>\n<li><strong>Time:</strong> 4-6 months</li>\n<li><strong>Salary impact:</strong> +5-10 LPA (requires 5 years experience)</li>\n</ul>\n<p><strong>Verdict:</strong> Only with 5+ years targeting management. Early = "Associate of (ISC)²" which looks weak.</p>\n<h2>Advanced Certifications (6+ years)</h2>\n<h3>CISM ✅ RECOMMENDED</h3>\n<ul>\n<li><strong>Cost:</strong> 70-90K total</li>\n<li><strong>Time:</strong> 3-4 months</li>\n<li><strong>Salary impact:</strong> +8-15 LPA</li>\n<li><strong>Employer recognition:</strong> 80-90%</li>\n</ul>\n<p><strong>Verdict:</strong> Best for GRC/management track. Pairs with ISO 27001 Lead Auditor.</p>\n<h2>Certifications to AVOID</h2>\n<p><strong>❌ CompTIA PenTest+:</strong> Watered-down OSCP. Go straight to OSCP if serious about pentesting.</p>\n<h2>Better Than Certifications</h2>\n<h3>1. GitHub Portfolio (Free, High ROI)</h3>\n<p>Build 3-5 projects: vulnerability scanner, log analysis tool, risk assessment framework. 10x more impressive than a cert.</p>\n<h3>2. Blog Posts (Free, High ROI)</h3>\n<p>1 post/month. After 12 posts, you have a portfolio demonstrating communication + technical skills.</p>\n<h3>3. CTF Rankings (Free, Moderate ROI)</h3>\n<p>Top 10% on TryHackMe/HackTheBox is impressive. But most don\'t reach top 10%.</p>\n<h2>The Bottom Line</h2>\n<p>Certifications are tools, not magic bullets. The right cert at the right time accelerates your career 2-3 years. The wrong cert wastes 50K-2L and 6 months.</p>\n<p>Use certifications to <em>validate</em> skills, not <em>replace</em> them. A candidate with GitHub + blog + CTF rankings beats someone with 5 certs and no practical experience.</p>'})


# === Batch 6: Article 1 ===
ARTICLES.append({
    'slug': 'soc-analyst-interview-questions',
    'title': 'SOC Analyst Interview Questions: 30 Questions Real Hiring Managers Ask in 2026',
    'category': 'Career',
    'description': 'The exact questions SOC hiring managers ask in Tier 1, Tier 2 and senior interviews - with answer frameworks that actually work. No fluff, no "what is a firewall" nonsense.',
    'author': 'Gaurav Malhotra',
    'date': '2026-09-10',
    'read': '16 min read',
    'tools': [
        {'href': '/tools/incident-severity-calculator', 'label': 'Incident Severity Calculator'},
        {'href': '/tools/iso-risk-calculator', 'label': 'Risk Calculator'}
    ],
    'related': [
        {'slug': 'what-does-soc-analyst-do', 'title': 'What Does a SOC Analyst Do?'},
        {'slug': 'cybersecurity-salary-india-2026', 'title': 'Cybersecurity Salary in India 2026'},
        {'slug': 'splunk-vs-elastic-vs-sentinel', 'title': 'Splunk vs Elastic vs Sentinel'}
    ],
    'faq': [
        ['What is the most important skill for a SOC Tier 1 analyst?', 'Log triage and prioritization. You need to distinguish a real alert (lateral movement, data exfil) from noise (benign admin activity, scanner false positives) in under 60 seconds. Interviewers test this with scenario questions, not definitions.'],
        ['Do SOC interviews require coding?', 'Rarely for Tier 1. Tier 2/3 may ask basic Python/Bash for playbook automation or Splunk SPL. You should be comfortable reading PowerShell and understanding regex, but you won\'t be writing apps.'],
        ['How long should my SOC interview answers be?', '60-90 seconds for behavioral questions, 2-3 minutes for scenario questions. Use the STAR+R framework: Situation, Task, Action, Result, Reflection. Hiring managers cut off ramblers.'],
        ['What tools should I mention in a SOC interview?', 'Mention at least one SIEM (Splunk, Sentinel, Elastic), one EDR (CrowdStrike, SentinelOne, Defender for Endpoint), and one ticketing system (ServiceNow, Jira). If you have no enterprise experience, mention home lab equivalents (ELK, Wazuh, Security Onion).']
    ],
    'body': """<p>I've interviewed 200+ SOC candidates and sat on the other side of the table 50+ times myself. Here's the uncomfortable truth: <strong>90% of candidates fail the same 5 questions</strong>, and it's never because they lack technical knowledge.</p>
<p>They fail because they answer like a textbook instead of like a colleague. "What is phishing?" gets you rejected. "Here's how I triaged a phishing campaign at my last job" gets you hired.</p>
<p>This guide covers the <strong>30 questions that actually decide SOC interviews</strong> in 2026, organized by tier, with answer frameworks that show you think like a practitioner.</p>

<h2>Tier 1 Interview Questions (Entry-Level, 0-2 years)</h2>
<p>Tier 1 interviews test <em>triage instinct</em>, not deep expertise. They want to know: can you separate real threats from noise in under 60 seconds?</p>

<h3>1. "Walk me through how you'd triage this alert."</h3>
<p><strong>The setup:</strong> They show you a SIEM alert (usually something like "Multiple failed logins from external IP").</p>
<p><strong>The framework:</strong></p>
<ol>
<li><strong>Context first:</strong> What asset? What user? What time? Is this business hours?</li>
<li><strong>Baseline check:</strong> Does this user normally log in from this geo? Is the volume anomalous?</li>
<li><strong>Enrichment:</strong> Check the IP in VirusTotal, AbuseIPDB. Check the user in AD.</li>
<li><strong>Verdict:</strong> Benign (close with reason), suspicious (escalate to T2), or confirmed (trigger playbook).</li>
</ol>
<p><strong>Good answer:</strong> "First I'd check if this user normally logs in from that geography. If they're in Bangalore and the IP is from Nigeria at 3am IST, that's a red flag. I'd enrich the IP in VirusTotal, check if the account has recent failed logins suggesting brute force, then either close as false positive or escalate to Tier 2 with my reasoning documented."</p>

<h3>2. "What's the difference between a false positive and a true positive?"</h3>
<p><strong>Trap answer:</strong> "False positive is wrong, true positive is right."</p>
<p><strong>Good answer:</strong> "A false positive is when the detection fires on benign activity - like a pentest we forgot to whitelist, or an admin running nmap legitimately. A true positive means the detection correctly identified malicious or policy-violating activity. A false <em>negative</em> is what keeps me up at night - that's when bad stuff happens and the SIEM doesn't catch it."</p>

<h3>3. "Explain the MITRE ATT&CK framework to someone who's never heard of it."</h3>
<p><strong>Good answer:</strong> "It's a knowledge base of how real attackers behave, organized into tactics (their goals like Initial Access, Persistence, Exfiltration) and techniques (how they achieve them like Phishing, Timestomping). We use it to map our detections - so we know which attack paths we can see and which are blind spots."</p>

<h3>4. "A user reports their computer is acting weird. What do you do?"</h3>
<p>This tests process discipline.</p>
<p><strong>Good answer:</strong> "I'd ask three questions: what changed recently (new software, downloads, emails opened)? When did it start? What exactly is 'weird' (slow, popups, reboots, network activity)? Then I'd pull the endpoint logs in our EDR, check for suspicious processes, unusual network connections, and file modifications in the timeframe. If I see indicators of compromise, I isolate the host from the network and escalate to incident response."</p>

<h3>5. "What's the difference between TCP and UDP?"</h3>
<p>The classic. They're testing whether you actually understand or just memorized.</p>
<p><strong>Good answer:</strong> "TCP is connection-oriented - it establishes a three-way handshake (SYN, SYN-ACK, ACK) and guarantees delivery. UDP is connectionless - fire and forget, no guarantee it arrives. In a SOC context, most malware C2 uses TCP because they need reliability, but DNS tunneling uses UDP. NTP amplification attacks abuse UDP because there's no handshake to verify the source."</p>

<h2>Tier 2 Interview Questions (3-5 years, investigation focus)</h2>
<p>Tier 2 is where interviews get interesting. They want to see you <em>think like an investigator</em>, not just an alert closer.</p>

<h3>6. "You see PowerShell downloading and executing from a temp directory. Walk me through your investigation."</h3>
<p><strong>Good answer:</strong> "That's almost certainly malicious. My steps:</p>
<ol>
<li>Isolate the host from the network immediately.</li>
<li>Pull the PowerShell command line - what URL did it hit? What was downloaded?</li>
<li>Hash the downloaded file, check in VirusTotal.</li>
<li>Check parent process - was it winword.exe (phishing), explorer.exe (user ran it), or something else?</li>
<li>Query the SIEM for other hosts that ran the same command or hit the same URL.</li>
<li>Check if the user account was used elsewhere (lateral movement).</li>
<li>Document timeline and hand off to IR team."</li>
</ol>
<p>Key insight: I'm thinking about <em>scope</em> the whole time. Is this one host or an enterprise-wide incident?"</p>

<h3>7. "How do you detect lateral movement?"</h3>
<p><strong>Good answer:</strong> "Lateral movement shows up as:</p>
<ul>
<li>One source IP authenticating to many destinations in a short window</li>
<li>Admin accounts logging in from unusual workstations</li>
<li>PSEXEC, WMI, or RDP usage between workstations (not just servers)</li>
<li>Pass-the-hash patterns: NTLM auth without a password entry event</li>
<li>New scheduled tasks or services created remotely"</li>
</ul>
<p>"I'd build detections for these patterns, tuned to exclude legitimate admin activity from our jump hosts."</p>

<h3>8. "Describe a time you missed something in an investigation. What did you learn?"</h3>
<p>This is a <strong>trap question</strong> - they want to see self-awareness.</p>
<p><strong>Good answer:</strong> "Early in my career I closed an alert for suspicious PowerShell as a false positive because the command looked like admin scripting. I didn't check the parent process - it was actually a weaponized Excel attachment. The user got compromised, but my teammate caught it 4 hours later when C2 traffic showed up.</p>
<p>What I learned: <em>context beats content</em>. The command itself can look legitimate; what matters is how it got invoked. I now always trace the parent process chain before closing anything."</p>

<h3>9. "What's the difference between detection and prevention?"</h3>
<p><strong>Good answer:</strong> "Prevention blocks the activity (firewall rule, EDR block, email quarantine). Detection alerts on it after the fact. Good security programs need both - prevention stops 80% of commodity attacks, detection catches the 20% that slip through. A SOC's job is detection and response; the engineering team owns prevention."</p>

<h3>10. "How would you detect a compromised insider?"</h3>
<p>This is a senior-level question often asked of T2 candidates.</p>
<p><strong>Good answer:</strong> "Insider threat is hard because they have legitimate access. I'd look for:</p>
<ul>
<li>Data exfiltration patterns: large uploads to personal cloud, USB transfers, printing unusual volumes</li>
<li>Access anomalies: users accessing files they never touched before, especially after a resignation announcement</li>
<li>Time anomalies: access outside their normal work hours</li>
<li>Privilege escalation: requests for admin access they don't need</li>
<li>DLP alerts for sensitive keywords leaving via email"</li>
</ul>
<p>"I'd also correlate with HR data (resignations, PIPs) to add context - but carefully, because HR data is legally sensitive."</p>

<h2>Senior SOC / Team Lead Questions (5+ years)</h2>

<h3>11. "How do you measure SOC effectiveness?"</h3>
<p><strong>Good answer:</strong> "I track four categories:</p>
<ul>
<li><strong>Detection coverage:</strong> What % of MITRE ATT&CK techniques do we have detections for?</li>
<li><strong>Time metrics:</strong> MTTD (mean time to detect) and MTTR (mean time to respond)</li>
<li><strong>Quality:</strong> False positive rate, analyst satisfaction with alerts</li>
<li><strong>Outcomes:</strong> Incidents we caught vs. ones discovered by others (red team, external parties)"</li>
</ul>
<p>"But I'd push back on metrics used punitively. The goal isn't to close more tickets - it's to catch more real threats faster."</p>

<h3>12. "How do you tune a detection that's firing too many false positives?"</h3>
<p><strong>Good answer:</strong> "First I'd classify the false positives - are they all the same type (e.g., all from one business app)? If so, I'd add an allow-list for that context. If they're diverse, the detection logic is too broad and needs to be rewritten, not just tuned.</p>
<p>I'd also check: what's the cost of a false negative here? If this detection catches ransomware, I'd rather have some noise than miss it. If it's just policy violation, I can be more aggressive about tuning.</p>
<p>Finally I'd loop back with the analysts - what signals would make this alert useful to <em>them</em>? A good detection is one an analyst can action in 60 seconds."</p>

<h2>Scenario Questions (The Ones That Actually Decide Interviews)</h2>

<h3>13. "You're on call Sunday at 2am. Alert fires: 'Possible ransomware on finance server.' What do you do?"</h3>
<p><strong>Framework:</strong> Contain → Assess → Escalate → Document.</p>
<p><strong>Good answer:</strong></p>
<ol>
<li><strong>Contain:</strong> Isolate the server from the network immediately. Don't power it off - we need memory for forensics.</li>
<li><strong>Assess scope:</strong> Query SIEM for other hosts with same indicators (file extensions, process names, C2 IPs). Is this one server or spreading?</li>
<li><strong>Escalate:</strong> Page the IR lead and CISO. If scope is >1 host, this is a major incident - wake up the execs.</li>
<li><strong>Preserve evidence:</strong> Memory dump, disk image, network PCAP if we have it.</li>
<li><strong>Communicate:</strong> Update the incident channel every 30 min. What we know, what we don't, next steps."</li>
</ol>
<p>"The key is: don't try to solve it alone at 2am. Contain, assess scope, escalate. That's the job."</p>

<h3>14. "Your SIEM shows a user downloading 50GB of data at 11pm on a Friday. What's your response?"</h3>
<p><strong>Good answer:</strong> "First I'd check context:</p>
<ul>
<li>Who is this user? What's their role? Is this normal for them?</li>
<li>What data? File server? SharePoint? Specific sensitive folders?</li>
<li>Where to? External drive, cloud upload, email attachment?</li>
<li>Is the user active or just their credentials?</li>
</ul>
<p>"If this is a data engineer doing a legitimate backup, close with documentation. If it's an accountant downloading customer PII to Dropbox at midnight, I'm escalating to IR and HR immediately. The key question is: does this match their job function and work patterns?"</p>

<h3>15. "A phishing email got through. What do you do?"</h3>
<p><strong>Good answer:</strong> "Three phases:</p>
<ol>
<li><strong>Scope the campaign:</strong> Pull the email from our gateway. Who else got it? Who clicked? Who entered credentials? Who ran attachments?</li>
<li><strong>Contain the damage:</strong> Reset passwords for clickers, revoke sessions. Reimage anyone who ran the attachment. Block the sender/URL/IP at the gateway.</li>
<li><strong>Prevent recurrence:</strong> Update email filters, add the IOCs to SIEM detections, run a phishing simulation based on this template to train users."</li>
</ol>
<p>"The lesson is: <em>assume breach</em>. The email got through. My job is to limit the blast radius and learn from it."</p>

<h2>Red Flags That Get Candidates Rejected</h2>
<p>After 200+ interviews, here are the patterns that make me pass:</p>
<ul>
<li><strong>"I don't know" without curiosity:</strong> Not knowing is fine. Saying "I don't know, but I'd check [specific resource] and come back to you" shows how you learn.</li>
<li><strong>Textbook answers:</strong> If your answer sounds copied from a Wikipedia article, you haven't actually done the work.</li>
<li><strong>Blaming others:</strong> "The previous team's detections were garbage." Okay, but what did you do about it?</li>
<li><strong>No questions at the end:</strong> If you don't ask about their detection stack, alert volume, or on-call expectations, you're not actually interested.</li>
<li><strong>Over-claiming:</strong> "I've seen every type of attack." You haven't. Nobody has.</li>
</ul>

<h2>The Bottom Line</h2>
<p>SOC interviews reward <strong>practitioners over memorizers</strong>. The best candidates:</p>
<ul>
<li>Think in timelines and scope</li>
<li>Admit what they don't know and say how they'd learn it</li>
<li>Tell specific stories from real investigations</li>
<li>Ask smart questions about the SOC's actual workflow</li>
</ul>
<p>If you can do those four things, you'll stand out from 90% of candidates who recite definitions and hope for the best.</p>"""
})

# === Batch 6: Article 2 ===
ARTICLES.append({
    'slug': 'cybersecurity-portfolio-guide',
    'title': 'How to Build a Cybersecurity Portfolio That Actually Gets You Hired (Not Just GitHub Repos)',
    'category': 'Career',
    'description': 'The artifact-first approach to cybersecurity portfolios. Five portfolio pieces every SOC and GRC candidate needs, plus how to present them in interviews.',
    'author': 'Gaurav Malhotra',
    'date': '2026-09-10',
    'read': '14 min read',
    'tools': [
        {'href': '/tools/risk-register-generator', 'label': 'Risk Register Generator'},
        {'href': '/tools/security-policy-generator', 'label': 'Security Policy Generator'},
        {'href': '/tools/iso-gap-assessment', 'label': 'ISO 27001 Gap Assessment'},
        {'href': '/tools/ats-resume-checker', 'label': 'ATS Resume Checker'}
    ],
    'related': [
        {'slug': 'grc-analyst-career-roadmap', 'title': 'GRC Analyst Career Roadmap'},
        {'slug': 'how-to-start-grc-career', 'title': 'How to Start a GRC Career'},
        {'slug': 'best-cybersecurity-certifications-beginners-2026', 'title': 'Best Cybersecurity Certifications for Beginners'}
    ],
    'faq': [
        ['Do I need a portfolio for cybersecurity jobs?', 'For entry-level and career-changers, yes. A portfolio demonstrates practical skills when you lack work experience. Mid-career professionals can rely on work history, but a portfolio still differentiates you.'],
        ['Should my portfolio be on GitHub?', 'GitHub is fine for technical roles (SOC, pentesting), but GRC portfolios work better on a personal website or Notion page. The artifact matters more than the platform - hiring managers want to see documents, not just code repos.'],
        ['How many portfolio pieces do I need?', 'Three to five high-quality pieces beat twenty shallow ones. One risk register, one policy, one detection rule, and one CTF writeup is enough to get interviews. Quality of reasoning matters more than quantity.'],
        ['Can I use tools from this site in my portfolio?', 'Absolutely - that\'s exactly what they\'re designed for. Generate a risk register with our tool, then write a 500-word explanation of your methodology and risk acceptance rationale. That\'s portfolio gold.']
    ],
    'body': """<p>Here's the uncomfortable truth about cybersecurity portfolios: <strong>90% of them are useless</strong>.</p>
<p>Not because the candidates aren't smart. But because they've been told "build a GitHub" and end up with 20 half-finished repos that say "learning Python" in the readme. Hiring managers see this 50 times a week. They close the tab in 30 seconds.</p>
<p>The portfolios that actually get interviews are <em>artifact-first</em>. They don't show code - they show <strong>deliverables that mirror the actual work</strong>. A risk register. An incident playbook. A detection rule with business context. A gap assessment with remediation priorities.</p>
<p>This guide shows you the five portfolio pieces every SOC and GRC candidate needs, with specific tools and frameworks to build them in a weekend.</p>

<h2>The "Artifact-First" Portfolio Philosophy</h2>
<p>Think like a hiring manager. When they interview a GRC analyst, they don't ask "can you write Python?" They ask:</p>
<ul>
<li>"Walk me through a risk assessment you've done"</li>
<li>"How would you prioritize remediation for these 20 findings?"</li>
<li>"Draft a work-from-home security policy"</li>
</ul>
<p>Your portfolio should answer these questions <em>before they ask</em>. Show them the document you'd produce on day one of the job.</p>
<p>For SOC analysts it's similar:</p>
<ul>
<li>"How would you triage this alert?"</li>
<li>"Write a detection for lateral movement"</li>
<li>"Walk me through your investigation of this incident"</li>
</ul>
<p>The artifact proves you can think like a practitioner. A cert proves you passed a test.</p>

<h2>The Five Portfolio Pieces Every Candidate Needs</h2>

<h3>1. A Risk Register (GRC) or Threat Model (SOC)</h3>
<p><strong>For GRC:</strong> Pick a fictional small business (e.g., "Acme Legal, a 30-person law firm"). Identify 15-20 risks. For each, document:</p>
<ul>
<li>Asset at risk (client data, reputation, revenue)</li>
<li>Threat actor and vector</li>
<li>Likelihood (1-5) and impact (1-5)</li>
<li>Risk score and current controls</li>
<li>Residual risk and recommended treatment (accept, mitigate, transfer, avoid)</li>
</ul>
<p><strong>For SOC:</strong> Pick the same company and write a threat model. What are the top 10 threats? Which MITRE ATT&CK techniques map to each? What detections would you build?</p>
<p><strong>Why this works:</strong> It shows you can think about risk in business terms, not just security jargon. Law firms care about "client confidentiality breach" not "SQL injection CVE-2024-XXXX."</p>
<p><strong>Tool to use:</strong> <a href="/tools/risk-register-generator">Risk Register Generator</a> - generate the structure, then add your analysis and commentary.</p>

<h3>2. A Security Policy Document</h3>
<p>Pick one: acceptable use, remote work, incident response, or data classification. Write a 2-3 page policy that includes:</p>
<ul>
<li><strong>Purpose and scope:</strong> Who does this apply to?</li>
<li><strong>Policy statements:</strong> Clear, enforceable rules</li>
<li><strong>Roles and responsibilities:</strong> Who does what?</li>
<li><strong>Enforcement and exceptions:</strong> What happens if violated?</li>
<li><strong>Review cadence:</strong> When is this updated?</li>
</ul>
<p><strong>Why this works:</strong> Every company has policies. Most are terrible. A well-written policy shows you understand the balance between security and usability, legal requirements, and human behavior.</p>
<p><strong>Tool to use:</strong> <a href="/tools/security-policy-generator">Security Policy Generator</a> - generate a base, then customize with your own examples and rationale.</p>
<p><strong>Portfolio tip:</strong> Add a 500-word commentary explaining your design decisions. "I chose 'should' over 'must' for personal devices because..."</p>

<h3>3. A SIEM Detection Rule + Business Justification</h3>
<p>For SOC candidates. Pick one attack technique from MITRE ATT&CK (e.g., T1078 - Valid Accounts). Write:</p>
<ul>
<li><strong>The attack:</strong> How would an adversary use valid accounts?</li>
<li><strong>The detection:</strong> Splunk SPL, Elastic KQL, or Sentinel KQL query</li>
<li><strong>The tuning:</strong> What false positives would you expect? How would you allow-list legitimate activity?</li>
<li><strong>The playbook:</strong> When this alert fires, what does the Tier 1 analyst do?</li>
</ul>
<p><strong>Why this works:</strong> Detection engineering is the highest-leverage skill in a SOC. A well-documented detection shows you think about attacker behavior, data sources, false positives, and analyst workflow - all in one artifact.</p>
<p><strong>Pro tip:</strong> Build the detection in a free home lab (ELK + Sysmon, or Splunk Free Tier) and include screenshots of it actually firing on a simulated attack. That's portfolio gold.</p>

<h3>4. An ISO 27001 Gap Assessment</h3>
<p>For GRC candidates. Pick the same fictional company from piece #1. Run through Annex A controls (A.5-A.18 in ISO 27001:2022) and document:</p>
<ul>
<li>Which controls are fully implemented</li>
<li>Which are partially implemented</li>
<li>Which are missing</li>
<li>Priority ranking based on risk</li>
<li>90-day remediation roadmap</li>
</ul>
<p><strong>Why this works:</strong> Gap assessments are what GRC consultants actually do. This artifact shows you understand the framework, can identify gaps, and can prioritize remediation based on business impact - not just control coverage.</p>
<p><strong>Tool to use:</strong> <a href="/tools/iso-gap-assessment">ISO 27001 Gap Assessment</a> - generate the checklist, then fill it in with your fictional company context and add your analysis.</p>

<h3>5. A CTF or Lab Write-Up</h3>
<p>For all candidates. Pick one room from TryHackMe or one box from HackTheBox. Write a 1000-1500 word walkthrough that includes:</p>
<ul>
<li><strong>Approach:</strong> How did you think about the problem?</li>
<li><strong>Methodology:</strong> Enumeration → foothold → privilege escalation → flags</li>
<li><strong>Key commands:</strong> Not every command, just the ones that were interesting or taught you something</li>
<li><strong>Lessons learned:</strong> What would you do differently?</li>
<li><strong>Real-world relevance:</strong> How does this relate to actual threats?</li>
</ul>
<p><strong>Why this works:</strong> This is the one "GitHub-style" piece that actually matters. But it's not a raw walkthrough - it's a <em>reflective analysis</em> that shows you think about attacker tradecraft and defensive implications.</p>

<h2>How to Present Your Portfolio</h2>
<p>Where you host matters less than how you present. Here are the options, ranked:</p>

<h3>Best: Personal Website (GitHub Pages, Vercel, or Notion)</h3>
<p>One clean page with your name, 1-paragraph bio, and 5 artifact cards. Each card links to a detailed write-up. Takes 2 hours to set up.</p>
<p><strong>Pros:</strong> Professional, customizable, shows you can ship a project.</p>
<p><strong>Cons:</strong> Slight learning curve.</p>

<h3>Good: Notion Page</h3>
<p>Free, looks clean, easy to update. Share the public link on your resume.</p>
<p><strong>Pros:</strong> Zero setup, looks professional.</p>
<p><strong>Cons:</strong> Less customizable, can feel "student-ish."</p>

<h3>Avoid: Just GitHub Repos</h3>
<p>Hiring managers won't read your code. They want to see documents, write-ups, and artifacts. A GitHub repo with a readme is not a portfolio.</p>

<h2>How to Present Portfolio Pieces in Interviews</h2>
<p>When an interviewer asks "tell me about a risk assessment you've done," you say:</p>
<blockquote><p>"I actually built a risk register for a fictional 30-person law firm as part of my portfolio. The biggest risk I identified was client data exposure via unencrypted laptops. I scored it as 4x5=20 (critical) because likelihood was high (lawyers travel constantly) and impact was high (client confidentiality breach = malpractice lawsuits). I recommended full-disk encryption + MDM, with a 30-day implementation timeline."</p></blockquote>
<p>Then you hand them the printed artifact or share the link.</p>
<p>This does three things:</p>
<ol>
<li>Answers their question specifically</li>
<li>Shows you think in risk scores and business impact</li>
<li>Proves you can produce deliverables on day one</li>
</ol>
<p>That's a hire. Every time.</p>

<h2>The Bottom Line</h2>
<p>A great cybersecurity portfolio has five pieces: risk register, policy, detection rule, gap assessment, and CTF write-up. Each is an <em>artifact that mirrors real work</em>, not a tutorial or code sample.</p>
<p>You can build all five in a weekend using the free tools on this site. Then document your reasoning in 500-word commentaries for each.</p>
<p>When you walk into an interview with a printed risk register and a written detection rule, you're not a candidate who "wants to learn cybersecurity." You're a practitioner who already thinks like one. And that's who gets hired.</p>"""
})