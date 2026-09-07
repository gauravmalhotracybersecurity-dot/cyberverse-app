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
]
