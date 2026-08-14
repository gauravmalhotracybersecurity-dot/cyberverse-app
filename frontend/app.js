window.__cvAppRan = true;
// ===== CV DIAG (on-screen Safari diagnostics) =====
(function () {
  function show(msg) {
    var d = document.getElementById("cv-diag");
    if (!d) {
      d = document.createElement("div");
      d.id = "cv-diag";
      d.style.cssText = "position:fixed;bottom:0;left:0;right:0;background:#400;color:#fff;font:11px monospace;padding:8px;z-index:99999;white-space:pre-wrap;max-height:35vh;overflow:auto;";
      document.documentElement.appendChild(d);
    }
    d.textContent += msg + "\n";
  }
  window.__cvShow = show;
  try {
    localStorage.setItem("__cv_t", "1");
    var v = localStorage.getItem("__cv_t");
    show("storage: " + (v === "1" ? "OK" : "BROKEN"));
  } catch (e) { show("storage: BLOCKED (" + (e.name || e.message) + ")"); }
  window.addEventListener("error", function (e) { show("ERR: " + e.message + " (line " + e.lineno + ")"); });
  window.addEventListener("unhandledrejection", function (e) {
    var r = e.reason;
    show("REJECT: " + (r && r.message ? r.message : r));
  });
})();

// ===== STORAGE RESILIENCE (Safari-proof login) =====
(function () {
  var mem = {};
  var origSet = Storage.prototype.setItem;
  var origGet = Storage.prototype.getItem;
  Storage.prototype.setItem = function (k, v) {
    mem[k] = String(v);
    try { return origSet.call(this, k, v); } catch (e) {
      try { document.cookie = k + "=" + encodeURIComponent(v) + "; path=/; max-age=604800; Secure; SameSite=Lax"; } catch (e2) {}
    }
  };
  Storage.prototype.getItem = function (k) {
    var v = null;
    try { v = origGet.call(this, k); } catch (e) {}
    if (v === null || v === undefined) {
      if (k in mem) v = mem[k];
      else {
        var m = document.cookie.match(new RegExp("(?:^|; )" + k + "=([^;]+)"));
        if (m) v = decodeURIComponent(m[1]);
      }
    }
    return v;
  };
})();



function escapeHtml(str) {
  if (!str) return "";
  return String(str).replace(/[&<>"']/g, function (m) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m];
  });
}
function celebrate() {
  if (!document.getElementById("cv-confetti-css")) {
    const st = document.createElement("style");
    st.id = "cv-confetti-css";
    st.textContent = "@keyframes cvfall { to { transform: translateY(105vh) rotate(720deg); } }";
    document.head.appendChild(st);
  }
  const colors = ["#00ffcc", "#8b5cf6", "#f59e0b", "#ef4444", "#3b82f6"];
  for (let i = 0; i < 80; i++) {
    const el = document.createElement("div");
    el.style.cssText = "position:fixed;top:-12px;width:8px;height:12px;z-index:9999;pointer-events:none;background:" + colors[i % 5] + ";left:" + (Math.random() * 100) + "vw;transform:rotate(" + (Math.random() * 360) + "deg);animation:cvfall " + (2 + Math.random() * 1.5) + "s linear forwards;";
    document.body.appendChild(el);
    setTimeout(function (e) { return function () { e.remove(); }; }(el), 4200);
  }
}
if (typeof window.renderOnboarding !== "function") {
  window.renderOnboarding = function () {
    try {
      const card = document.getElementById("onboarding-card") || document.querySelector(".onboarding-card");
      if (!card) return;
      const flags = [!!localStorage.getItem("cv_onb_resume"), !!localStorage.getItem("cv_onb_interview"), !!localStorage.getItem("cv_onb_ops")];
      const count = flags.filter(Boolean).length;
      card.querySelectorAll("input[type=checkbox]").forEach(function (cb, i) { if (typeof flags[i] === "boolean") cb.checked = flags[i]; });
      if (count === 3) card.style.display = "none";
    } catch (e) {}
  };
}
const ROADMAP = [
  {phase: "Phase 1 - Foundations", weeks: [
    {id: "w1", t: "Networking & Linux basics", cert: "Security+ 1.1-1.3", goto: "mentor", items: ["TCP/IP, OSI model", "Linux permissions", "Quiz me on ports"]},
    {id: "w2", t: "Security fundamentals", cert: "Security+ 1.4-2.2", goto: "ctf", items: ["CIA triad, zero trust", "Malware & phishing", "Solve a CTF Bite"]},
    {id: "w3", t: "Resume & presence", goto: "resume", items: ["AI resume review", "LinkedIn headline", "Add hands-on project"]},
    {id: "w4", t: "First mock interview", goto: "interview", items: ["Quick Round voice mode", "Review scorecard", "Re-answer weakest"]}]},
  {phase: "Phase 2 - Defense", weeks: [
    {id: "w5", t: "SIEM & log analysis", cert: "Security+ 2.4", goto: "ctf", items: ["Event IDs 4624/4625/4688", "Splunk stats vs transaction", "CTF log challenges"]},
    {id: "w6", t: "Alert triage drills", goto: "interview", items: ["Phishing-click scenario", "Validate, enrich, scope, contain", "Target score 60+"]},
    {id: "w7", t: "Threat intel & vulns", goto: "mentor", items: ["CVE vs CVSS vs EPSS", "Zero-day prioritization", "Vuln scenario"]},
    {id: "w8", t: "GRC awareness", goto: "interview", items: ["ISO 27001 risk assessment", "Vendor risk tiering", "GRC mock interview"]}]},
  {phase: "Phase 3 - Hunt & Get Hired", weeks: [
    {id: "w9", t: "Threat hunting basics", goto: "ctf", items: ["Lateral movement indicators", "Beaconing intervals", "Golden vs silver ticket"]},
    {id: "w10", t: "Advanced interviews", goto: "interview", items: ["Full 6-question voice", "Defend follow-ups", "Share scorecard"]},
    {id: "w11", t: "Applications sprint", goto: "resume", items: ["10 tailored applications", "Attach scorecard", "Ask referrals"]},
    {id: "w12", t: "Offer readiness", goto: "interview", items: ["Final mock interview", "Why cybersecurity story", "Download certificate"]}]}
];
function renderRoadmap() {
  const list = document.getElementById("rm-list");
  if (!list) return;
  const done = JSON.parse(localStorage.getItem("cv_roadmap") || "{}");
  const total = ROADMAP.reduce(function (n, p) { return n + p.weeks.length; }, 0);
  const doneCount = Object.values(done).filter(Boolean).length;
  const bar = document.getElementById("rm-bar");
  if (bar) bar.style.width = Math.round(100 * doneCount / total) + "%";
  const pr = document.getElementById("rm-progress");
  if (pr) pr.textContent = doneCount + " / " + total + " weeks completed";
  let html = "";
  ROADMAP.forEach(function (ph) {
    html += '<h3 style="color:var(--accent);margin:24px 0 10px">' + ph.phase + "</h3>";
    ph.weeks.forEach(function (w) {
      const isDone = !!done[w.id];
      html += '<div class="card" style="padding:16px;margin-bottom:10px;' + (isDone ? "opacity:.65;" : "") + '"><div style="display:flex;gap:12px;align-items:flex-start"><input type="checkbox" data-week="' + w.id + '" ' + (isDone ? "checked" : "") + ' style="margin-top:4px;accent-color:var(--accent);width:18px;height:18px;cursor:pointer"/><div style="flex:1"><div style="font-weight:700">' + w.t + (w.cert ? ' <span style="color:var(--amber);font-size:.72rem;border:1px solid var(--amber);border-radius:10px;padding:1px 8px">' + w.cert + "</span>" : "") + "</div><ul style='margin:8px 0 0;padding-left:18px;color:var(--text-muted);font-size:.9rem'>" + w.items.map(function (it) { return "<li>" + it + "</li>"; }).join("") + "</ul><button class='btn-secondary rm-go' data-goto='" + w.goto + "' style='margin-top:10px;padding:6px 14px'>Practice →</button></div></div></div>";
    });
  });
  list.innerHTML = html;
  list.querySelectorAll("input[data-week]").forEach(function (cb) {
    cb.addEventListener("change", function () {
      const d = JSON.parse(localStorage.getItem("cv_roadmap") || "{}");
      d[cb.dataset.week] = cb.checked;
      localStorage.setItem("cv_roadmap", JSON.stringify(d));
      renderRoadmap();
    });
  });
  list.querySelectorAll(".rm-go").forEach(function (b) { b.addEventListener("click", function () { goToView(b.dataset.goto); }); });
}
async function renderLabs() {
  const list = document.getElementById("labs-list");
  if (!list) return;
  try {
    const d = await api("/api/labs");
    const doneCount = Object.keys(d.done).length;
    const pr = document.getElementById("labs-progress");
    if (pr) pr.textContent = doneCount + " / " + d.labs.length + " labs completed";
    list.innerHTML = d.labs.map(function (lab) {
      const done = d.done[lab.id];
      return '<div class="card" style="padding:16px;margin-bottom:12px;"><div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap"><strong>' + lab.title + "</strong><span style='color:var(--text-muted);font-size:.8rem'>" + lab.tool + " • " + lab.mins + " min • " + lab.level + (done ? " • ✅ done" : "") + "</span></div><details style='margin-top:8px'><summary style='cursor:pointer;color:var(--accent);font-size:.9rem'>Steps & evidence</summary><ol style='margin:8px 0 0;padding-left:18px;color:var(--text-muted);font-size:.9rem'>" + lab.steps.map(function (x) { return "<li>" + x + "</li>"; }).join("") + "</ol></details>" + (done ? '<div style="margin-top:12px"><p style="font-size:.85rem;color:var(--text-muted)"><b>Resume:</b> ' + done.bullet + "</p><div style='display:flex;gap:8px;margin-top:8px'><button class='btn-secondary lab-copy' data-k='bullet' data-lab='" + lab.id + "'>Copy bullet</button></div></div>" : '<div style="margin-top:12px"><button class="btn-primary lab-done" data-lab="' + lab.id + '">✅ Mark complete & generate pack</button></div>') + "</div>";
    }).join("");
    list.querySelectorAll(".lab-done").forEach(function (b) {
      b.addEventListener("click", async function () {
        const r = await api("/api/labs/complete", { method: "POST", body: JSON.stringify({ lab_id: b.dataset.lab }) });
        if (!r.error) { try { cvTrack("lab_completed"); profile.xp += 15; renderStatusBar(); celebrate(); toast("Lab complete! +15 XP"); renderLabs(); } catch (e) {} }
      });
    });
    list.querySelectorAll(".lab-copy").forEach(function (b) {
      b.addEventListener("click", function () { navigator.clipboard.writeText(d.done[b.dataset.lab][b.dataset.k]); toast("Copied"); });
    });
  } catch (e) { list.innerHTML = "Could not load labs."; }
}
async function renderStories() {
  const list = document.getElementById("st-list");
  if (!list) return;
  try {
    const stories = await api("/api/stories");
    list.innerHTML = stories.length ? stories.map(function (st) {
      return '<div class="card" style="padding:14px;margin-bottom:10px"><strong>' + escapeHtml(st.title) + "</strong><p style='color:var(--text-muted);font-size:.88rem;margin-top:6px'><b>S:</b> " + escapeHtml(st.s) + ' <b>T:</b> ' + escapeHtml(st.t || "-") + ' <b>A:</b> ' + escapeHtml(st.a) + ' <b>R:</b> ' + escapeHtml(st.r || "-") + "</p><div style='display:flex;gap:8px'><button class='btn-secondary st-copy' data-id='" + st.id + "'>Copy</button></div></div>";
    }).join("") : '<p style="color:var(--text-muted)">No stories yet. Build your first one above.</p>';
    list.querySelectorAll(".st-copy").forEach(function (b) {
      b.addEventListener("click", function () {
        const st = stories.find(function (x) { return x.id == b.dataset.id; });
        navigator.clipboard.writeText("Situation: " + st.s + "\nTask: " + (st.t || "-") + "\nAction: " + st.a + "\nResult: " + (st.r || "-"));
        toast("Copied");
      });
    });
  } catch (e) { list.innerHTML = "Could not load stories."; }
}
(function () {
  const V = "2026-08-14";
  if (localStorage.getItem("cv_token") && localStorage.getItem("cv_seen_news") !== V) {
    localStorage.setItem("cv_seen_news", V);
    setTimeout(function () { toast("🆕 New this week: Lab Log, Story Bank & the 90-day Roadmap!", "success"); }, 1800);
  }
})();
document.querySelectorAll(".mentor-chip").forEach(function (b) {
  b.addEventListener("click", function () {
    const inp = document.getElementById("mentor-input");
    if (!inp) return;
    inp.value = b.textContent;
    const sb = document.getElementById("mentor-send");
    if (sb) sb.click();
  });
});
(function () {
  const sb = document.querySelector(".sidebar") || document.querySelector("aside");
  const ham = document.getElementById("cv-hamburger");
  const bd = document.getElementById("sidebar-backdrop");
  if (!sb || !ham) return;
  const close = function () { sb.classList.remove("open"); if (bd) bd.style.display = "none"; };
  const open = function () { sb.classList.add("open"); if (bd) bd.style.display = "block"; };
  ham.onclick = function (e) { e.preventDefault(); e.stopPropagation(); sb.classList.contains("open") ? close() : open(); };
  if (bd) bd.onclick = close;
  document.querySelectorAll(".nav-item").forEach(function (b) {
    b.addEventListener("click", function () { if (window.innerWidth <= 900) close(); });
  });
})();
document.addEventListener("click", function (e) {
  const t = e.target.closest ? e.target.closest("#mic-btn, .mic-btn, #voice-btn, .voice-btn, [data-action='voice'], button[id*='mic'], button[id*='voice'], button[class*='mic']") : null;
  if (t && navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
      stream.getTracks().forEach(function (tr) { tr.stop(); });
    }).catch(function () {});
  }
}, true);
(function () {
  let box = null;
  function logV(msg) { console.log("[voice]", msg); }
  function findAnswerBox() {
    const ids = ["iv-answer", "answer-input", "interview-answer", "answer", "iv-input", "interview-input", "iv-text"];
    for (const id of ids) { const el = document.getElementById(id); if (el) return el; }
    const els = document.querySelectorAll("textarea, input[type=text]");
    for (const el of els) {
      const ph = (el.placeholder || "").toLowerCase();
      if (ph.includes("answer") || ph.includes("type your")) return el;
    }
    return null;
  }
  const Orig = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!Orig) return;
  let active = null;
  document.addEventListener("click", function (e) {
    const t = e.target.closest ? e.target.closest("#mic-btn, .mic-btn, #voice-btn, .voice-btn, [data-action='voice'], button[id*='mic'], button[id*='voice'], button[class*='mic']") : null;
    if (!t) return;
    if (active) { try { active.stop(); } catch (e2) {} active = null; return; }
    try {
      const rec = new Orig();
      rec.lang = "en-US";
      rec.interimResults = false;
      rec.continuous = false;
      rec.addEventListener("start", function () { logV("listening"); });
      rec.addEventListener("result", function (e3) {
        let txt = "";
        for (let i = e3.resultIndex; i < e3.results.length; i++) txt += e3.results[i][0].transcript;
        const ab = findAnswerBox();
        if (ab) { ab.value = (ab.value ? ab.value + " " : "") + txt; ab.dispatchEvent(new Event("input", { bubbles: true })); }
      });
      rec.addEventListener("error", function (e4) { logV("err " + e4.error); active = null; });
      rec.addEventListener("end", function () { active = null; });
      active = rec;
      rec.start();
    } catch (e5) { active = null; }
  }, true);
})();
(function () {
  let loaded = false;
  function sec() { return document.getElementById("view-league") || document.getElementById("view-leaderboard") || document.querySelector("section[id*='league']"); }
  function listEl() {
    let l = document.getElementById("league-list") || document.getElementById("leaderboard-list");
    const sv = sec();
    if (!l && sv) { l = document.createElement("div"); l.id = "league-list"; l.style.cssText = "max-width:720px;margin-top:12px"; sv.appendChild(l); }
    return l;
  }
  async function tryLoad() {
    const sv = sec();
    if (!sv || loaded) return;
    loaded = true;
    const l = listEl();
    l.innerHTML = "Loading weekly league…";
    try {
      const data = await api("/api/leaderboard");
      const users = (data && (data.users || data.leaders)) || (Array.isArray(data) ? data : []);
      if (!users.length) { l.innerHTML = "<p style='color:var(--text-muted)'>No league members yet. Finish an interview to join the board!</p>"; return; }
      const medals = ["🥇", "", ""];
      let html = '<table style="width:100%;border-collapse:collapse"><thead><tr><th style="padding:8px;text-align:left">#</th><th style="padding:8px;text-align:left">Player</th><th style="padding:8px;text-align:right">XP</th></tr></thead><tbody>';
      users.forEach(function (u, i) {
        html += '<tr style="border-bottom:1px solid #222"><td style="padding:10px 8px">' + (medals[i] || (i + 1)) + '</td><td style="padding:10px 8px">' + escapeHtml(u.name || u.full_name || "Anonymous") + (u.is_pro ? ' <span style="color:var(--amber);font-size:.75rem">PRO</span>' : '') + '</td><td style="text-align:right;padding:10px 8px;color:var(--accent)">' + (u.xp || 0) + '</td></tr>';
      });
      l.innerHTML = html + '</tbody></table>';
    } catch (e) { l.innerHTML = "Could not load league."; }
  }
  window.addEventListener("click", function () { setTimeout(tryLoad, 150); });
  setInterval(tryLoad, 1500);
  tryLoad();
})();
(function () {
  let done = false, tries = 0;
  const LOCAL = [
    {question: "Which Windows Event ID indicates a FAILED logon attempt?", options: ["4624", "4625", "4688", "4769"], answer: 1, explanation: "4625 = failed logon; 4624 = success."},
    {question: "An email urges urgent invoice payment; the header shows a look-alike domain. First action?", options: ["Pay it", "Report and quarantine", "Delete and ignore", "Reply"], answer: 1, explanation: "Treat as phishing: report and contain."},
    {question: "DNS tunneling exfiltrates data by abusing which protocol?", options: ["HTTP", "DNS", "SMTP", "NTP"], answer: 1, explanation: "Data hidden in DNS queries."},
    {question: "In the cyber kill chain, which stage follows Delivery?", options: ["Reconnaissance", "Exploitation", "Installation", "Actions on Objectives"], answer: 1, explanation: "Delivery > Exploitation."},
    {question: "Which Splunk command counts events per host?", options: ["stats count by host", "table host", "fields - host", "rename host"], answer: 0, explanation: "stats count by host."},
    {question: "A CVSS score of 9.0-10.0 is rated as?", options: ["Low", "Medium", "High", "Critical"], answer: 3, explanation: "9.0-10.0 = Critical."},
    {question: "A Golden Ticket attack forges a TGT using which account hash?", options: ["Administrator", "KRBTGT", "Guest", "LocalSystem"], answer: 1, explanation: "KRBTGT signs TGTs."}
  ];
  function getBox() {
    let l = document.getElementById("ctf-list");
    if (l) return l;
    const sv = document.getElementById("view-ctf") || document.querySelector("[id*='ctf']");
    if (!sv) return null;
    l = document.createElement("div"); l.id = "ctf-list"; l.style.cssText = "max-width:720px;margin-top:12px";
    sv.appendChild(l);
    return l;
  }
  function pick(d) {
    if (!d) return null;
    if (d.question && d.options) return d;
    if (d.bite) return pick(d.bite);
    if (d.data) return pick(d.data);
    if (d.questions && d.questions.length) return pick(d.questions[0]);
    if (d.length) return pick(d[0]);
    return null;
  }
  function render(l, q, src) {
    let html = '<div class="card" style="padding:16px"><p style="font-weight:700;margin-bottom:10px">⚡ ' + escapeHtml(q.question) + '</p><p style="font-size:.75rem;color:var(--text-muted)">source: ' + src + "</p>";
    for (let i = 0; i < q.options.length; i++) {
      html += '<label style="display:block;margin:6px 0;cursor:pointer"><input type="radio" name="ctf-opt7" value="' + i + '" style="margin-right:8px">' + escapeHtml(q.options[i]) + "</label>";
    }
    html += '<button id="ctf-check7" class="btn-primary" style="margin-top:10px">Check answer</button><p id="ctf-fb7" style="margin-top:10px;display:none"></p></div>';
    l.innerHTML = html;
    l.querySelector("#ctf-check7").addEventListener("click", function () {
      const sel = l.querySelector('input[name="ctf-opt7"]:checked');
      const fb = l.querySelector("#ctf-fb7");
      fb.style.display = "block";
      if (!sel) { fb.style.color = "#f59e0b"; fb.textContent = "Pick an option first."; return; }
      const ok = parseInt(sel.value, 10) === q.answer;
      fb.style.color = ok ? "#00ffcc" : "#ef4444";
      fb.textContent = ok ? "✅ Correct! " + (q.explanation || "") : "❌ Not quite. " + (q.explanation || "");
      if (ok) { try { celebrate(); } catch (e) {} }
    });
  }
  function tick() {
    if (done) return;
    const l = getBox();
    if (!l) return;
    tries++;
    api("/api/ctf/today").then(function (d) {
      const q = pick(d);
      if (q) { done = true; render(l, q, "live"); }
      else if (tries >= 3) { done = true; render(l, LOCAL[new Date().getDate() % LOCAL.length], "offline"); }
    }).catch(function () {
      if (tries >= 3) { done = true; render(l, LOCAL[new Date().getDate() % LOCAL.length], "offline"); }
    });
  }
  setInterval(tick, 2000);
  document.addEventListener("click", function () { setTimeout(tick, 200); });
  tick();
})();
