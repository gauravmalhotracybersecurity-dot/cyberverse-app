import subprocess, re

app = "frontend/app.html"
c = open(app, encoding="utf-8").read()
orig_len = len(c)

# === 1. REMOVE ORPHANED "<div " BEFORE PRICING SECTION ===
c2 = re.sub(r'<div[ \t]*\r?\n(?=<div id="pricing-section")', '', c, count=1)
if c2 != c:
    print("[FIXED] orphaned <div before pricing removed")
    c = c2

# === 2. RESTORE THE AUTH-SCREEN DIV TAG ===
if '<div id="auth-screen" class="auth-screen">' not in c:
    c2 = re.sub(r'(?<!<div )(?<!<div)\bid="auth-screen" class="auth-screen">', '<div id="auth-screen" class="auth-screen">', c, count=1)
    if c2 != c:
        print("[FIXED] auth-screen div tag restored")
        c = c2

# === 3. REMOVE BROKEN TRACKING INJECTION FROM JS LINES ===
bad = '.textContent; if(window.trackInterviewCompletion) window.trackInterviewCompletion(score);'
n = c.count(bad)
if n:
    c = c.replace(bad, '.textContent')
    print(f"[FIXED] removed {n} broken JS injection(s)")

# === 4. FIX LINKEDIN CAPTION (data.length was out of scope) ===
old_cap = '"Just completed " + data.length + "'
if old_cap in c:
    c = c.replace(old_cap, '"Just completed " + (JSON.parse(localStorage.getItem("cv_interviews_30d")||"[]").length || 1) + "')
    print("[FIXED] LinkedIn caption interview count")

# === 5. ADD "VIEW PRICING" TOGGLE ON AUTH SCREEN ===
if 'View pricing first' not in c:
    fp = c.find('Forgot your password?')
    if fp > 0:
        a_end = c.find('</a>', fp)
        if a_end > 0:
            link = '\n<p style="text-align:center;margin-top:14px"><a href="#" onclick="document.getElementById(\'auth-screen\').style.display=\'none\';document.getElementById(\'pricing-section\').style.display=\'block\';return false" style="color:var(--accent);font-size:.9rem">View pricing first &rarr;</a></p>'
            c = c[:a_end+4] + link + c[a_end+4:]
            print("[ADDED] 'View pricing first' toggle on login screen")

# === 6. SAFE SCORE-WATCH TRACKER (replaces broken hook) ===
watch = '''<script id="cv-score-watch">
(function(){ var seen=false; setInterval(function(){ var m=document.getElementById('scorecard-modal'); if(!m) return; var vis = m.style.display!=='none' && getComputedStyle(m).display!=='none'; if(vis && !seen){ seen=true; var sc=((document.getElementById('sc-score')||{}).textContent||''); var num=parseInt(sc,10)||0; if(window.trackInterviewCompletion) window.trackInterviewCompletion(num); } if(!vis) seen=false; },1500); })();
</script>'''
if 'cv-score-watch' not in c:
    body_end = c.rfind('</body>')
    c = c[:body_end] + watch + '\n' + c[body_end:]
    print("[ADDED] safe scorecard-watch tracking script")

# === SANITY CHECKS ===
print("\n=== SANITY ===")
print(f"  auth-screen div tag intact: {'YES' if '<div id=\"auth-screen\" class=\"auth-screen\">' in c else 'NO'}")
print(f"  raw broken tag remaining: {'YES (BAD)' if re.search(r'(?<!<div )id=\"auth-screen\" class=\"auth-screen\">', c) else 'NO (good)'}")
print(f"  broken JS injection remaining: {'YES (BAD)' if bad in c else 'NO (good)'}")
print(f"  size: {orig_len} -> {len(c)} chars")

open(app, "w", encoding="utf-8").write(c)

subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "FIX: restore auth-screen tag, repair JS injection, pricing toggle"], capture_output=True, text=True)
print(f"\n[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
