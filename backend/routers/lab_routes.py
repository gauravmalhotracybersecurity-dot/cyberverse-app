from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
import json

import models
from auth import get_current_user
from database import get_db

router = APIRouter(prefix="/api/labs", tags=["labs"])

LABS = [
 {"id":"splunk-home","title":"Splunk Home Lab: Ingest & Alert","tool":"Splunk","mins":90,"level":"Beginner",
  "steps":["Install Splunk Enterprise trial on a VM","Install a Universal Forwarder on a Windows VM","Enable Windows Security event monitoring","Search with SPL: index=wineventlog EventCode=4625","Create an alert that fires on 5+ failed logins in 10 minutes"],
  "evidence":["Screenshot of your SPL search results","Screenshot of the alert configuration","One custom SPL query you wrote"],
  "bullet":"Built a two-VM Splunk home lab: deployed a Universal Forwarder, ingested Windows Security events, and authored an SPL alert firing on 5+ failed logins (Event 4625).",
  "star":"S: I needed real SIEM experience, not theory, for SOC interviews. T: I had to prove I could run ingestion to detection on my own. A: I built a Splunk lab, forwarded Windows Security logs, and wrote an SPL alert for repeated failed logons. R: I can now walk an interviewer through ingest, search and alerting end to end - my strongest interview story.",
  "linkedin":"Weekend build: I set up a two-VM Splunk lab, ingested Windows Security events, and wrote my first SPL alert (5+ failed logons). Nothing teaches detection like building it yourself. #SOC #Splunk #HomeLab"},
 {"id":"sysmon","title":"Sysmon: See Everything","tool":"Sysmon","mins":60,"level":"Beginner",
  "steps":["Download Sysmon and a community config (SwiftOnSecurity)","Install on a Windows lab VM: sysmon -accepteula -i config.xml","Open Event Viewer > Applications and Services Logs > Microsoft > Windows > Sysmon","Run test commands (whoami, net user) and inspect Event 1","Write 3 detection ideas from what you observed"],
  "evidence":["Screenshot of Sysmon Event 1 entries","Your 3 detection ideas in notes"],
  "bullet":"Deployed Sysmon with a community configuration on a Windows lab VM and mapped observed process-creation events (Event 1) to three written detection ideas.",
  "star":"S: I wanted to understand host telemetry instead of memorizing definitions. T: I needed to see what real process creation looks like. A: I installed Sysmon with a community config, ran controlled commands, and analyzed Event 1 fields. R: I can now explain which telemetry catches which technique - interviewers noticed the difference.",
  "linkedin":"Installed Sysmon on my lab VM today. Watching process creation in real time changes how you think about detection. #Sysmon #BlueTeam"},
 {"id":"wireshark","title":"Wireshark: Read the Wire","tool":"Wireshark","mins":60,"level":"Beginner",
  "steps":["Capture live traffic on your machine for 5 minutes","Apply filters: tcp.port==443, http, dns","Follow one full TCP stream and describe the handshake","Load any sample pcap and find the noisiest talker","Document 3 anomalies with screenshots"],
  "evidence":["Screenshot of a followed TCP stream","Your 3 documented anomalies"],
  "bullet":"Captured and analyzed live traffic with Wireshark: filtered TLS handshakes, followed TCP streams, and documented three anomalies from a sample capture.",
  "star":"S: Network questions always made me vague in interviews. T: I needed packet-level confidence. A: I captured my own traffic, followed TCP streams, and hunted anomalies in a sample pcap. R: I now answer network questions with specific fields and flags, not guesses.",
  "linkedin":"Followed my first full TCP stream in Wireshark today. The wire does not lie. #Wireshark #NetworkDefense"},
 {"id":"elastic","title":"Elastic SIEM Quickstart","tool":"Elastic","mins":120,"level":"Intermediate",
  "steps":["Start an Elastic Cloud trial (or docker)","Ship Windows events with Winlogbeat","Explore events in Discover; build one visualization","Create a Kibana detection rule on failed logons","Trigger it and confirm the alert appears"],
  "evidence":["Screenshot of your detection rule","Screenshot of the triggered alert"],
  "bullet":"Stood up an Elastic SIEM trial, shipped Windows events via Winlogbeat, and created a Kibana detection rule validated with a simulated trigger.",
  "star":"S: Every SOC job listed SIEM experience I did not have. T: I needed a real detection workflow. A: I deployed Elastic, shipped logs with Winlogbeat, and wrote a rule that alerted on failed logons. R: I can discuss rule tuning and alert triage from first-hand experience.",
  "linkedin":"My first Elastic detection rule fired today - on my own simulated attack. That is the moment theory becomes skill. #Elastic #SIEM"},
 {"id":"ad-audit","title":"AD Audit Policies","tool":"Windows Server","mins":90,"level":"Intermediate",
  "steps":["Install a Windows Server eval VM and promote to DC","Enable audit policies: logon events, account logon, object access","Generate 4624 and 4625 events with a test account","Locate both events and explain their fields","Write one line explaining what KRBTGT protects"],
  "evidence":["Screenshots of 4624 and 4625 from your DC","Your KRBTGT one-liner"],
  "bullet":"Promoted a Windows Server eval VM to domain controller, enabled logon auditing, and located 4624/4625 events for test accounts.",
  "star":"S: Active Directory questions were my weakest area. T: I needed to see AD auth logs myself. A: I built a DC, enabled auditing, and generated success and failure logons to analyze. R: Kerberos and NTLM questions now get calm, specific answers.",
  "linkedin":"Built my own domain controller this weekend and watched 4624/4625 events appear as I logged on. AD finally makes sense from the inside. #ActiveDirectory"},
 {"id":"yara","title":"Write a YARA Rule","tool":"YARA","mins":45,"level":"Intermediate",
  "steps":["Install YARA (or use a Linux VM)","Create a harmless sample file containing marker strings","Write a rule with a string and a condition that detects it","Run yara and confirm the hit","Extend the rule with 2 extra conditions and re-test"],
  "evidence":["Your final .yar rule file","Screenshot of the yara hit output"],
  "bullet":"Wrote and tested YARA rules detecting custom marker strings, extending the rule with two additional conditions and validating hits.",
  "star":"S: Malware-adjacent roles expect detection engineering basics. T: I had never written a rule. A: I authored YARA rules against sample markers and iterated on conditions. R: I can explain rule precision vs recall with a real example.",
  "linkedin":"Wrote my first YARA rule today and watched it catch my sample. Small win, big confidence. #YARA #DetectionEngineering"},
 {"id":"pfsense","title":"pfSense: Your Own Firewall","tool":"pfSense","mins":120,"level":"Intermediate",
  "steps":["Install pfSense in a VM with two adapters","Complete WAN/LAN setup and reach the web UI","Create a LAN block rule for one destination","Verify the block with a test request","Read the firewall logs and describe 3 entries"],
  "evidence":["Screenshot of your block rule","Screenshot of the matching log entry"],
  "bullet":"Deployed a pfSense firewall VM, configured LAN/WAN interfaces, and verified custom block rules via firewall log analysis.",
  "star":"S: Firewall questions felt abstract. T: I needed to own a rulebase. A: I deployed pfSense, wrote block rules, and validated them in logs. R: I now talk about allow vs deny logic and logging like a practitioner.",
  "linkedin":"My own firewall, my own rules, my own logs. pfSense lab complete. #pfSense #Networking"},
 {"id":"phish-lab","title":"Phishing Analysis Pipeline","tool":"Any","mins":60,"level":"Beginner",
  "steps":["Take any sample phishing email (public corpus)","Extract and read the full header chain","Trace the Received hops and spot the lie","Evaluate every URL: domain age, lookalikes, redirects","Write a 5-step user-response playbook"],
  "evidence":["Your annotated header analysis","Your 5-step playbook"],
  "bullet":"Analyzed a sample phishing email end to end: traced Received headers, evaluated the URL chain, and wrote a five-step user-response playbook.",
  "star":"S: Phishing triage is the most common SOC screen. T: I wanted a repeatable analysis method. A: I dissected a real sample - headers, hops, URLs - and wrote a response playbook. R: I now run the same pipeline under interview pressure.",
  "linkedin":"Dissected a phishing email header by header today. The Received chain always tells on the sender. #Phishing #SOC"},
]

class LabComplete(BaseModel):
    lab_id: str
    notes: str = ""

@router.get("")
def list_labs(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    done = {}
    for log in db.query(models.LabLog).filter(models.LabLog.user_id == user.id).all():
        done[log.lab_id] = json.loads(log.artifacts or "{}")
    return {"labs": LABS, "done": done}

@router.post("/complete")
def complete_lab(payload: LabComplete, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    lab = next((l for l in LABS if l["id"] == payload.lab_id), None)
    if not lab:
        return {"error": "unknown lab"}
    existing = db.query(models.LabLog).filter(models.LabLog.user_id == user.id, models.LabLog.lab_id == lab["id"]).first()
    if existing:
        return {"artifacts": json.loads(existing.artifacts or "{}"), "already": True}
    artifacts = {"bullet": lab["bullet"], "star": lab["star"], "linkedin": lab["linkedin"], "notes": payload.notes}
    db.add(models.LabLog(user_id=user.id, lab_id=lab["id"], notes=payload.notes, artifacts=json.dumps(artifacts)))
    user.xp = (user.xp or 0) + 15
    db.commit()
    return {"artifacts": artifacts, "already": False}
