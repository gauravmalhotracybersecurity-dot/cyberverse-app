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
    }
]
