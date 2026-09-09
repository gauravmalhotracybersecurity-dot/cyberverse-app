import subprocess, os

articles_py = "backend/content/articles.py"
c = open(articles_py, encoding="utf-8").read()

# Article 1: SOC Analyst Interview Questions
art1 = r'''

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
})'''

# Article 2: Cybersecurity Portfolio
art2 = r'''

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
})'''

# Append both articles
if 'soc-analyst-interview-questions' not in c:
    c += art1
    print("[ADDED] SOC Analyst Interview Questions")
else:
    print("[SKIP] SOC article already present")

if 'cybersecurity-portfolio-guide' not in c:
    c += art2
    print("[ADDED] Cybersecurity Portfolio Guide")
else:
    print("[SKIP] Portfolio article already present")

# Verify syntax
try:
    compile(c, articles_py, "exec")
    print("[COMPILE] Verified clean")
except SyntaxError as e:
    print(f"[ABORT] Syntax error: {e}")
    raise SystemExit(1)

open(articles_py, "w", encoding="utf-8").write(c)

# Verify articles load
import sys
sys.path.insert(0, "backend")
for m in list(sys.modules):
    if 'content' in m or 'articles' in m:
        del sys.modules[m]
from content import articles
slugs = [a['slug'] for a in articles.ARTICLES]
print(f"\n[VERIFY] Total articles: {len(articles.ARTICLES)}")
print(f"[VERIFY] New slugs present:")
print(f"  - soc-analyst-interview-questions: {'✓' if 'soc-analyst-interview-questions' in slugs else '✗'}")
print(f"  - cybersecurity-portfolio-guide: {'✓' if 'cybersecurity-portfolio-guide' in slugs else '✗'}")

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "Content batch 6: SOC interview questions + portfolio guide"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout if r.returncode == 0 else r.stderr}")

r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
