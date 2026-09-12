import subprocess, re

app = "frontend/app.html"
c = open(app, encoding="utf-8").read()

print("=== STAGE 2: APP MONETIZATION ===")

# === 1. ADD PRICING TABLE (before auth screen) ===
pricing_html = '''
<div id="pricing-section" style="max-width:900px;margin:0 auto;padding:2rem;display:none">
  <div style="text-align:center;margin-bottom:2rem">
    <h2 style="color:#fff;margin:0">Start free. Upgrade when you're ready to go all in.</h2>
    <p style="color:var(--muted);margin:.5rem 0 0">CyberVerse AI gives you real mock interviews with AI feedback - no credit card needed to start.</p>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;max-width:750px;margin:0 auto">
    <div style="padding:2rem;background:#151515;border:1px solid #333;border-radius:14px">
      <h4 style="color:#fff;margin:0 0 .5rem">Free</h4>
      <p style="color:var(--muted);font-size:.85rem;margin:0 0 1.5rem">Get started, no card needed</p>
      <ul style="color:#c9c9c9;font-size:.9rem;line-height:2;padding-left:1.2rem;margin:0">
        <li>3 mock interviews / month</li>
        <li>Basic feedback (pass/fail + summary)</li>
        <li>GRC & SOC fundamentals</li>
        <li>Community support</li>
      </ul>
      <button class="btn-secondary" onclick="document.getElementById('pricing-section').style.display='none';document.getElementById('auth-screen').style.display='block'" style="width:100%;margin-top:1.5rem">Start Free</button>
    </div>
    <div style="padding:2rem;background:#151515;border:2px solid var(--accent);border-radius:14px;position:relative">
      <span style="position:absolute;top:-12px;right:16px;background:var(--accent);color:#000;font-size:.75rem;font-weight:700;padding:.2rem .7rem;border-radius:10px">MOST POPULAR</span>
      <h4 style="color:var(--accent);margin:0 0 .5rem">Pro</h4>
      <p style="color:var(--muted);font-size:.85rem;margin:0 0 1.5rem">For serious career builders</p>
      <ul style="color:#c9c9c9;font-size:.9rem;line-height:2;padding-left:1.2rem;margin:0">
        <li>Unlimited interviews</li>
        <li>Detailed scoring + improvement plan</li>
        <li>All topic tracks (Auditor, Analyst, Compliance)</li>
        <li>Streak tracking + weak-area analytics</li>
        <li>Shareable verified certificate</li>
        <li>Priority AI response speed</li>
      </ul>
      <button class="btn-primary" onclick="alert('Redirecting to payment...');window.location.href='/billing/checkout/pro'" style="width:100%;margin-top:1.5rem">Upgrade to Pro →</button>
      <p style="text-align:center;color:var(--muted);font-size:.75rem;margin-top:.6rem">7-day money-back guarantee. Cancel anytime.</p>
    </div>
  </div>
</div>
'''

# Insert pricing before auth-screen
if 'id="pricing-section"' not in c:
    auth_idx = c.find('id="auth-screen"')
    if auth_idx > 0:
        c = c[:auth_idx] + pricing_html + '\n' + c[auth_idx:]
        print("[ADDED] Pricing table section")

# === 2. ADD FREEMIUM MODAL + SOFT NUDGE BANNER ===
freemium_html = '''
<div id="freemium-modal" class="modal-overlay" style="display:none;position:fixed;inset:0;z-index:9999;justify-content:center;align-items:center">
  <div class="modal-card" style="background:#151515;border:1px solid var(--accent);border-radius:16px;padding:2rem;max-width:500px;width:90%">
    <h3 style="color:#fff;margin:0 0 1rem">You've used all 3 free interviews this month 🎯</h3>
    <p style="color:var(--muted);line-height:1.6;margin:0 0 1.5rem">You're improving - your last score was <span id="freemium-score" style="color:var(--accent);font-weight:600">72</span>%. Unlock unlimited interviews, detailed feedback on every answer, and a shareable certificate when you're ready.</p>
    <div style="display:flex;gap:.75rem">
      <button class="btn-primary" onclick="window.location.href='/billing/checkout/pro'" style="flex:1">Upgrade to Pro</button>
      <button class="btn-secondary" onclick="document.getElementById('freemium-modal').style.display='none'" style="flex:1">Remind me next month</button>
    </div>
  </div>
</div>

<div id="freemium-nudge" style="display:none;position:fixed;bottom:20px;right:20px;z-index:9998;background:#151515;border:1px solid var(--accent);border-radius:12px;padding:1rem 1.5rem;max-width:320px;box-shadow:0 8px 24px rgba(0,0,0,.5)">
  <button onclick="this.parentElement.style.display='none';localStorage.setItem('cv_nudge_dismissed','1')" style="position:absolute;top:8px;right:8px;background:none;border:none;color:#666;cursor:pointer;font-size:1.2rem">×</button>
  <p style="color:#fff;margin:0 0 .5rem;font-size:.95rem">1 free interview left this month</p>
  <p style="color:var(--muted);font-size:.85rem;margin:0 0 .75rem;line-height:1.5">Pro members get unlimited practice + detailed scoring.</p>
  <button class="btn-primary" onclick="window.location.href='/billing/checkout/pro'" style="width:100%;padding:.5rem 1rem;font-size:.85rem">Upgrade →</button>
</div>
'''

# Insert before </body>
if 'id="freemium-modal"' not in c:
    body_end = c.rfind('</body>')
    if body_end > 0:
        c = c[:body_end] + freemium_html + '\n' + c[body_end:]
        print("[ADDED] Freemium modal + soft nudge banner")

# === 3. ADD INTERVIEW TRACKING SCRIPT ===
tracking_script = '''
<script id="cv-freemium-tracking">
(function(){
  // Track interview completions in localStorage
  function trackInterview(score){
    var key = 'cv_interviews_30d';
    var data = JSON.parse(localStorage.getItem(key) || '[]');
    var now = Date.now();
    var thirtyDaysAgo = now - (30 * 24 * 60 * 60 * 1000);
    
    // Filter to last 30 days
    data = data.filter(function(d){ return d.ts > thirtyDaysAgo; });
    
    // Add this interview
    data.push({ts: now, score: score});
    localStorage.setItem(key, JSON.stringify(data));
    
    // Check triggers
    if(data.length === 2 && !localStorage.getItem('cv_nudge_dismissed')){
      setTimeout(function(){
        document.getElementById('freemium-nudge').style.display = 'block';
      }, 2000);
    }
    if(data.length >= 3){
      document.getElementById('freemium-score').textContent = score || '72';
      document.getElementById('freemium-modal').style.display = 'flex';
    }
  }
  
  // Hook into interview completion
  window.trackInterviewCompletion = trackInterview;
  
  // Check on page load if nudge should show
  setTimeout(function(){
    var key = 'cv_interviews_30d';
    var data = JSON.parse(localStorage.getItem(key) || '[]');
    var thirtyDaysAgo = Date.now() - (30 * 24 * 60 * 60 * 1000);
    data = data.filter(function(d){ return d.ts > thirtyDaysAgo; });
    if(data.length === 2 && !localStorage.getItem('cv_nudge_dismissed')){
      document.getElementById('freemium-nudge').style.display = 'block';
    }
  }, 3000);
})();
</script>
'''

if 'id="cv-freemium-tracking"' not in c:
    body_end = c.rfind('</body>')
    if body_end > 0:
        c = c[:body_end] + tracking_script + '\n' + c[body_end:]
        print("[ADDED] Interview tracking script")

# === 4. ENHANCE CERTIFICATE WITH LINKEDIN SHARE ===
# Find the cv-credential script and enhance it
old_credential = '''btn.textContent = "\\u2705 Copied: " + d.url;
          setTimeout(function(){ btn.textContent = "\\ud83d\\udd17 Copy verification link"; }, 5000);'''

new_credential = '''btn.textContent = "\\u2705 Copied: " + d.url;
          
          // Add LinkedIn share button
          var linkedinBtn = document.getElementById("sc-linkedin");
          if(!linkedinBtn){
            linkedinBtn = document.createElement("button");
            linkedinBtn.id = "sc-linkedin";
            linkedinBtn.className = btn.className;
            linkedinBtn.style.marginTop = "8px";
            linkedinBtn.style.background = "#0077b5";
            linkedinBtn.style.color = "#fff";
            linkedinBtn.textContent = "Share on LinkedIn";
            btn.parentNode.insertBefore(linkedinBtn, btn.nextSibling);
            
            linkedinBtn.addEventListener("click", function(){
              var caption = "Just completed " + data.length + " mock interviews on CyberVerse AI and scored " + score + "% average. Practicing out loud > just reading. #GRC #Cybersecurity #CareerGrowth";
              var shareUrl = "https://www.linkedin.com/sharing/share-offsite/?url=" + encodeURIComponent(d.url);
              window.open(shareUrl, "_blank");
            });
          }
          
          setTimeout(function(){ btn.textContent = "\\ud83d\\udd17 Copy verification link"; }, 5000);'''

if old_credential in c:
    c = c.replace(old_credential, new_credential, 1)
    print("[UPDATED] Certificate script with LinkedIn share")

# === 5. HOOK TRACKING INTO INTERVIEW COMPLETION ===
# Find where interview score is displayed and add tracking call
old_score = 'document.getElementById("sc-score").textContent'
if old_score in c and 'trackInterviewCompletion' not in c:
    c = c.replace(old_score, old_score + '; if(window.trackInterviewCompletion) window.trackInterviewCompletion(score);')
    print("[UPDATED] Interview completion hook")

# Write back
open(app, "w", encoding="utf-8").write(c)
print(f"[SAVED] app.html ({len(c)} chars)")

# Commit and push
subprocess.run(["git", "add", "-A"])
r = subprocess.run(["git", "commit", "-m", "App monetization: pricing table, freemium modal, tracking, LinkedIn share"], capture_output=True, text=True)
print(f"[COMMIT] {r.stdout.strip() if r.returncode == 0 else r.stderr.strip()}")
r = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print("[PUSHED]" if r.returncode == 0 else f"[PUSH FAILED] {r.stderr}")
