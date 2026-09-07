import subprocess
ap = "backend/content/articles.py"
a = open(ap, encoding="utf-8").read()

new_articles = ''',
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
    }'''

idx = a.rfind("]")
a = a[:idx] + new_articles + "\n" + a[idx:]
open(ap, "w", encoding="utf-8").write(a)
print("[CMS] 2 SOC articles added (total now 8)")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Content: SOC cluster (SOC analyst role guide + SIEM comparison)"])
subprocess.run(["git", "push", "origin", "main"])
print("Pushed. Live in ~60s.")
