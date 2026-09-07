import re, glob, subprocess
skip = ("venv", "node_modules", ".git")

v2 = r'''<script id="cv-razorpay">
(function(){
  console.log("[cv-razorpay] wired v2");
  function tok(){ try { return localStorage.getItem("cv_token"); } catch(e){ return null; } }
  function loadRz(cb){
    if (window.Razorpay) return cb();
    var s = document.createElement("script");
    s.src = "https://checkout.razorpay.com/v1/checkout.js";
    s.onload = cb;
    s.onerror = function(){ alert("Could not load Razorpay checkout script (CSP or network)."); };
    document.head.appendChild(s);
  }
  function verify(resp, plan){
    fetch("/api/analytics/billing/verify", { method:"POST", headers:{"Content-Type":"application/json","Authorization":"Bearer "+tok()}, body: JSON.stringify({order_id:resp.razorpay_order_id, payment_id:resp.razorpay_payment_id, signature:resp.razorpay_signature}) })
    .then(function(r){ return r.json(); })
    .then(function(v){ if (v && v.ok) { alert("Payment verified! " + v.plan.toUpperCase() + " access is active."); location.reload(); } else { alert("Verification failed: " + ((v && v.error) || "unknown")); } })
    .catch(function(e){ alert("Verify error: " + e.message); });
  }
  function start(plan){
    fetch("/api/analytics/billing/checkout", { method:"POST", headers:{"Content-Type":"application/json","Authorization":"Bearer "+tok()}, body: JSON.stringify({plan: plan}) })
    .then(function(r){ return r.json().catch(function(){ throw new Error("Server returned non-JSON (status " + r.status + ")"); }); })
    .then(function(d){
      if (!d) throw new Error("Empty response from checkout");
      if (d.status === "coming_soon") { alert(d.message || "Payments coming soon."); return; }
      if (d.status !== "ok") { alert(d.error || "Checkout unavailable right now."); return; }
      loadRz(function(){
        try {
          var rz = new Razorpay({
            key: d.key_id, order_id: d.order_id, name: "GRCWithGaurav",
            description: (plan === "premium" ? "Premium" : "Pro") + " - lifetime",
            handler: function(resp){ verify(resp, plan); },
            prefill: { email: d.email || "", name: d.name || "" },
            theme: { color: "#00ffcc" }
          });
          rz.open();
        } catch(e){ alert("Razorpay overlay error: " + e.message); }
      });
    })
    .catch(function(e){ alert("Checkout error: " + e.message); });
  }
  document.addEventListener("click", function(e){
    var el = e.target.closest ? e.target.closest("a,button") : null;
    if (!el) return;
    var t = (el.textContent || "").trim();
    if (t === "Get Pro" || t === "Get Premium") {
      e.preventDefault();
      e.stopPropagation();
      start(t === "Get Pro" ? "pro" : "premium");
    }
  }, true);
})();
</script>'''

ah = [x for x in glob.glob("**/app.html", recursive=True) if not any(t in x for t in skip)][0]
h = open(ah, encoding="utf-8").read()
if '<script id="cv-razorpay">' in h:
    h = re.sub(r'<script id="cv-razorpay">.*?</script>', lambda m: v2, h, count=1, flags=re.S)
    print("[REPLACED] cv-razorpay block with v2")
else:
    idx = h.rfind("</body>")
    h = h[:idx] + v2 + h[idx:]
    print("[INJECTED] cv-razorpay v2")
open(ah, "w", encoding="utf-8").write(h)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Fix: bulletproof Razorpay wiring (delegated clicks + visible errors)"])
subprocess.run(["git", "push", "origin", "main"])
print("PUSHED")
