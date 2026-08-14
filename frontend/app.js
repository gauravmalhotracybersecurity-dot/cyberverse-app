
// ===== MOBILE RESCUE: Error Banner & Safe Storage =====
(function() {
  // 1. Show JS errors on screen (Red banner at bottom of phone)
  window.addEventListener("error", function(e) {
    var d = document.createElement("div");
    d.style.cssText = "position:fixed;bottom:0;left:0;right:0;background:#b00020;color:#fff;padding:12px;z-index:99999;font-size:12px;font-family:monospace;word-break:break-word;max-height:40vh;overflow:auto;";
    d.innerHTML = "<b>JS ERROR:</b> " + e.message + " (Line " + e.lineno + ")";
    document.body.appendChild(d);
    setTimeout(function(){ d.remove(); }, 10000);
  });
  window.addEventListener("unhandledrejection", function(e) {
    var d = document.createElement("div");
    d.style.cssText = "position:fixed;bottom:0;left:0;right:0;background:#b00020;color:#fff;padding:12px;z-index:99999;font-size:12px;font-family:monospace;word-break:break-word;";
    var msg = e.reason ? (e.reason.message || e.reason) : "Promise rejected";
    d.innerHTML = "<b>API/PROMISE ERROR:</b> " + msg;
    document.body.appendChild(d);
    setTimeout(function(){ d.remove(); }, 10000);
  });

  // 2. Safe LocalStorage Wrapper (Prevents Safari crashes on bad JSON)
  window.safeLS = function(key, fallback) {
    try {
      var v = localStorage.getItem(key);
      if (!v || v === "undefined" || v === "null") return fallback;
      return JSON.parse(v);
    } catch(e) { return fallback; }
  };
})();
// ===== Analytics tracking fallback =====
function cvTrack(event) {
  try {
    fetch("/api/analytics/event", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ event: event, t: Date.now() })
    }).catch(function(){});
  } catch(e) {}
}

// ===== Config =====
const API_BASE = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  ? "http://127.0.0.1:8000"
  : ""; // same-origin in production if you serve frontend + backend together

// ===== State =====
let token = localStorage.getItem("cv_token") || null;
let profile = null;
let authMode = "login";

// ===== Helpers =====
async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  let data = null;
  try { data = await res.json(); } catch (_) { /* no body */ }
  if (!res.ok) {
    const message = (data && data.detail) ? data.detail : `Request failed (${res.status})`;
    throw new Error(message);
  }
  return data;
}

function $(sel) { return document.querySelector(sel); }
function $all(sel) { return document.querySelectorAll(sel); }

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str ?? "";
  return div.innerHTML;
}

// ===== Auth screen =====
$all(".auth-tab").forEach(tab => {
  tab.addEventListener("click", () => {
    authMode = tab.dataset.mode;
    $all(".auth-tab").forEach(t => t.classList.toggle("active", t === tab));
    $("#signup-fields").classList.toggle("hidden", authMode !== "signup");
    $("#auth-submit").textContent = authMode === "signup" ? "Create account" : "Log in";
    $("#auth-error").classList.add("hidden");
  });
});

$("#auth-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = $("#email").value.trim();
  const password = $("#password").value;
  const errorEl = $("#auth-error");
  errorEl.classList.add("hidden");

  const submitBtn = $("#auth-submit");
  submitBtn.disabled = true;

  try {
    let result;
    if (authMode === "signup") {
      const full_name = $("#full-name").value.trim();
      result = await api("/api/auth/signup", {
        method: "POST",
        body: JSON.stringify({ email, password, full_name, referral_code: sessionStorage.getItem("cv_ref") || null }),
      });
    } else {
      result = await api("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
    }
    if (!result.access_token) {
      errorEl.textContent = result.message || "Check your inbox to verify your email, then log in.";
      errorEl.classList.remove("hidden");
      showAuthPanel("login");
      return;
    }
    cvTrack(authMode === "signup" ? "signup" : "login");
    token = result.access_token;
    localStorage.setItem("cv_token", token);
    await enterApp();
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.classList.remove("hidden");
  } finally {
    submitBtn.disabled = false;
  }
});

$("#logout-btn").addEventListener("click", () => {
  token = null;
  localStorage.removeItem("cv_token");
  $("#app-shell").classList.add("hidden");
  $("#auth-screen").classList.remove("hidden");
});

// ===== Forgot / reset password =====
function showAuthPanel(panel) {
  // panel: "login" | "forgot" | "reset"
  $("#auth-form").classList.toggle("hidden", panel !== "login");
  $("#forgot-form").classList.toggle("hidden", panel !== "forgot");
  $("#reset-form").classList.toggle("hidden", panel !== "reset");
  $(".auth-tabs").classList.toggle("hidden", panel !== "login");
}

$("#forgot-password-link").addEventListener("click", () => showAuthPanel("forgot"));
$("#back-to-login-link").addEventListener("click", () => showAuthPanel("login"));

$("#forgot-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = $("#forgot-email").value.trim();
  const btn = $("#forgot-submit");
  const msg = $("#forgot-message");
  btn.disabled = true;
  try {
    const result = await api("/api/auth/forgot-password", {
      method: "POST",
      body: JSON.stringify({ email }),
    });
    msg.textContent = result.message;
    msg.classList.remove("hidden");
  } catch (err) {
    msg.textContent = err.message;
    msg.classList.remove("hidden");
  } finally {
    btn.disabled = false;
  }
});

let pendingResetToken = null;

$("#reset-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const new_password = $("#reset-new-password").value;
  const btn = $("#reset-submit");
  const msg = $("#reset-message");
  const errorEl = $("#reset-error");
  msg.classList.add("hidden");
  errorEl.classList.add("hidden");
  btn.disabled = true;
  try {
    const result = await api("/api/auth/reset-password", {
      method: "POST",
      body: JSON.stringify({ token: pendingResetToken, new_password }),
    });
    msg.textContent = `${result.message} Redirecting to log in…`;
    msg.classList.remove("hidden");
    setTimeout(() => {
      window.history.replaceState({}, "", window.location.pathname);
      showAuthPanel("login");
    }, 1800);
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.classList.remove("hidden");
  } finally {
    btn.disabled = false;
  }
});

// If we arrived via a password-reset email link (?reset_token=...), jump
// straight to the reset panel.
(function checkForResetToken() {
  const params = new URLSearchParams(window.location.search);
  const t = params.get("reset_token");
  if (t) {
    pendingResetToken = t;
    showAuthPanel("reset");
  }
})();

// ===== Navigation =====
function goToView(view) {
  $all(".nav-item").forEach(n => n.classList.toggle("active", n.dataset.view === view));
  $all(".view").forEach(v => v.classList.toggle("active", v.id === `view-${view}`));
  if (view === "mentor") loadMentorHistory();
  if (view === "daily") loadDailyBundle();
  if (view === "achievements") loadAchievements();
  if (view === "leaderboard") loadLeaderboard();
  if (view === "ctf") loadCTF();
  if (view === "roadmap") renderRoadmap();
  if (view === "labs") renderLabs();
  if (view === "stories") renderStories();
  if (view === "profile") loadReferralData();
}
$all(".nav-item").forEach(n => n.addEventListener("click", () => goToView(n.dataset.view)));
$all("[data-goto]").forEach(el => el.addEventListener("click", () => goToView(el.dataset.goto)));

// ===== Enter app / load profile =====
async function enterApp() {
  try {
    profile = await api("/api/profile/me");
  } catch (err) {
    // token invalid/expired
    token = null;
    localStorage.removeItem("cv_token");
    $("#auth-error").textContent = "Session expired. Please log in again.";
    $("#auth-error").classList.remove("hidden");
    return;
  }
  $("#auth-screen").classList.add("hidden");
  $("#app-shell").classList.remove("hidden");
  renderStatusBar();
  checkProStatus();
  renderDashboardSnapshot();
  renderOnboarding();
  populateProfileForm();
}

function renderStatusBar() {
  $("#stat-name").textContent = profile.full_name || profile.email.split("@")[0];
  $("#stat-level").textContent = profile.skill_level.toUpperCase();
  $("#stat-xp").textContent = profile.xp;
  $("#stat-streak").textContent = `${profile.streak_days}d`;
  const proBadge = $("#pro-badge");
  if (proBadge) proBadge.classList.toggle("hidden", !profile.is_pro);
}

function renderDashboardSnapshot() {
  $("#snap-level").textContent = profile.skill_level;
  $("#snap-certs").textContent = profile.certifications.length ? profile.certifications.join(", ") : "None yet";
  $("#snap-weak").textContent = profile.weak_topics.length ? profile.weak_topics.join(", ") : "None identified yet";
  $("#snap-goal").textContent = profile.learning_goals || "Not set — add one in Profile";
}

// ===== Profile view =====
function populateProfileForm() {
  $("#p-name").value = profile.full_name || "";
  $("#p-level").value = profile.skill_level;
  $("#p-certs").value = profile.certifications.join(", ");
  $("#p-weak").value = profile.weak_topics.join(", ");
  $("#p-goals").value = profile.learning_goals || "";
}

$("#p-save").addEventListener("click", async () => {
  const payload = {
    full_name: $("#p-name").value.trim(),
    skill_level: $("#p-level").value,
    certifications: $("#p-certs").value.split(",").map(s => s.trim()).filter(Boolean),
    weak_topics: $("#p-weak").value.split(",").map(s => s.trim()).filter(Boolean),
    learning_goals: $("#p-goals").value.trim(),
  };
  profile = await api("/api/profile/me", { method: "PATCH", body: JSON.stringify(payload) });
  renderStatusBar();
  checkProStatus();
  renderDashboardSnapshot();
  renderOnboarding(); toast("Profile saved ✓");
  const saved = $("#p-saved");
  saved.classList.remove("hidden");
  setTimeout(() => saved.classList.add("hidden"), 2000);
});

// ===== AI Mentor chat =====
function renderChatLog(history) {
  const log = $("#chat-log");
  log.innerHTML = "";
  if (history.length === 0) {
    log.innerHTML = `<div class="msg assistant"><span class="msg-tag">MENTOR</span>Hey — I'm your AI Mentor. Ask me to explain a concept, build a study plan, quiz you, or review something you're stuck on.</div>`;
    return;
  }
  history.forEach(m => {
    const div = document.createElement("div");
    div.className = `msg ${m.role}`;
    div.innerHTML = `<span class="msg-tag">${m.role === "user" ? "YOU" : "MENTOR"}</span>${escapeHtml(m.content)}`;
    log.appendChild(div);
  });
  log.scrollTop = log.scrollHeight;
}

async function loadMentorHistory() {
  const history = await api("/api/mentor/history");
  renderChatLog(history);
}

$("#chat-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const input = $("#chat-input");
  const message = input.value.trim();
  if (!message) return;
  input.value = "";
  input.disabled = true;

  const log = $("#chat-log");
  const pending = document.createElement("div");
  pending.className = "msg user";
  pending.innerHTML = `<span class="msg-tag">YOU</span>${escapeHtml(message)}`;
  log.appendChild(pending);
  const thinking = document.createElement("div");
  thinking.className = "msg assistant";
  thinking.innerHTML = `<span class="msg-tag">MENTOR</span>Thinking…`;
  log.appendChild(thinking);
  log.scrollTop = log.scrollHeight;

  try {
    const result = await api("/api/mentor/chat", { method: "POST", body: JSON.stringify({ message }) });
    renderChatLog(result.history);
    profile.xp += 5;
    renderStatusBar();
  checkProStatus();
  } catch (err) {
    thinking.innerHTML = `<span class="msg-tag">MENTOR</span>Something went wrong: ${escapeHtml(err.message)}`;
  } finally {
    input.disabled = false;
    input.focus();
  }
});

// ===== Daily Ops =====
let dailyLoaded = false;
async function loadDailyBundle() {
  if (dailyLoaded) return;
  $("#daily-date").textContent = new Date().toDateString();
  $("#daily-loading").classList.remove("hidden");
  $("#daily-content").innerHTML = "";
  try {
    const bundle = await api("/api/daily");
    dailyLoaded = true;
    renderDailyBundle(bundle.content);
  } catch (err) {
    $("#daily-content").innerHTML = `<div class="daily-card">Couldn't load today's bundle: ${escapeHtml(err.message)}</div>`;
  } finally {
    $("#daily-loading").classList.add("hidden");
  }
}

function renderDailyBundle(c) {
  const container = $("#daily-content");
  container.innerHTML = "";

  const cards = [
    { eyebrow: "Lesson", title: c.lesson?.title, body: c.lesson?.body },
    { eyebrow: "News Brief", title: c.news_summary?.headline, body: `${c.news_summary?.summary}\n\nWhy it matters: ${c.news_summary?.why_it_matters}` },
    { eyebrow: "Challenge", title: c.challenge?.title, body: c.challenge?.description },
    { eyebrow: "Practical Task", title: c.practical_task?.title, body: c.practical_task?.description },
    { eyebrow: "Interview Question", title: c.interview_question?.question, body: `What a good answer covers: ${c.interview_question?.what_a_good_answer_covers}` },
  ];
  cards.forEach(card => {
    if (!card.title) return;
    const el = document.createElement("div");
    el.className = "daily-card";
    el.innerHTML = `<span class="eyebrow">${card.eyebrow}</span><h4>${escapeHtml(card.title)}</h4><p>${escapeHtml(card.body || "")}</p>`;
    container.appendChild(el);
  });

  if (c.quiz) {
    const quizEl = document.createElement("div");
    quizEl.className = "daily-card";
    quizEl.innerHTML = `<span class="eyebrow">Quiz</span><h4>${escapeHtml(c.quiz.question)}</h4>`;
    c.quiz.choices.forEach((choice, i) => {
      const btn = document.createElement("button");
      btn.className = "quiz-choice";
      btn.textContent = choice;
      btn.addEventListener("click", () => {
        quizEl.querySelectorAll(".quiz-choice").forEach((b, idx) => {
          b.disabled = true;
          if (idx === c.quiz.correct_index) b.classList.add("correct");
        });
        if (i !== c.quiz.correct_index) btn.classList.add("incorrect");
        const explain = document.createElement("div");
        explain.className = "quiz-explanation";
        explain.textContent = c.quiz.explanation;
        quizEl.appendChild(explain);
      });
      quizEl.appendChild(btn);
    });
    container.appendChild(quizEl);
  }
}

// ===== Resume Builder =====
$("#resume-submit").addEventListener("click", async () => {
  const resume_text = $("#resume-text").value.trim();
  const target_role = $("#resume-role").value;
  const fileInput = $("#resume-file");
  const file = fileInput.files[0];

  if (!file && resume_text.length < 50) {
    $("#resume-result").innerHTML = `<p style="color:var(--red)">Paste at least a few lines of resume text, or upload a file.</p>`;
    return;
  }

  $("#resume-loading").classList.remove("hidden");
  $("#resume-result").innerHTML = "";
  $("#resume-submit").disabled = true;

  try {
    let result;
    if (file) {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("target_role", target_role);
      const headers = {};
      if (token) headers["Authorization"] = `Bearer ${token}`;
      const res = await fetch(`${API_BASE}/api/resume/review-upload`, {
        method: "POST",
        headers,
        body: formData,
      });
      result = await res.json();
      if (!res.ok) throw new Error(result.detail || "Upload failed.");
    } else {
      result = await api("/api/resume/review", {
        method: "POST",
        body: JSON.stringify({ resume_text, target_role }),
      });
    }
    renderResumeResult(result.review);
    localStorage.setItem("cv_onb_resume", "1"); renderOnboarding();
    cvTrack("resume_reviewed");
    setTimeout(() => {
      const el = $("#resume-result");
      if (el && !$("#res-sc-download")) {
        el.innerHTML += `<div style="margin-top:24px; display:flex; gap:10px; justify-content:center; flex-wrap:wrap;">
          <button id="res-sc-download" class="btn-primary" style="flex:1; min-width:200px;">📥 Download Resume Scorecard</button>
          <button id="res-sc-copy" class="btn-secondary" style="flex:1; min-width:200px;">📋 Copy LinkedIn Post</button>
        </div>`;
        const score = result.review.overall_score;
        const role = $("#resume-role").value;
        $("#res-sc-download").onclick = () => downloadResumeScorecard(score, role);
        $("#res-sc-copy").onclick = () => copyResumeSharePost(score, role);
      }
    }, 100);
    profile.xp += 15;
    renderStatusBar();
  checkProStatus();
  } catch (err) {
    $("#resume-result").innerHTML = `<p style="color:var(--red)">${escapeHtml(err.message)}</p>`;
  } finally {
    $("#resume-loading").classList.add("hidden");
    $("#resume-submit").disabled = false;
  }
});

function renderResumeResult(r) {
  const el = $("#resume-result");
  const list = (items) => `<ul>${(items || []).map(i => `<li>${escapeHtml(i)}</li>`).join("")}</ul>`;
  el.innerHTML = `
    <div class="score-row">
      <div class="score-box"><div class="score-num">${escapeHtml(r.overall_score)}</div><div class="score-label">Overall</div></div>
      <div class="score-box"><div class="score-num">${escapeHtml(r.ats_score)}</div><div class="score-label">ATS</div></div>
    </div>
    <h4>Strengths</h4>${list(r.strengths)}
    <h4>Gaps</h4>${list(r.gaps)}
    <h4>Missing skills for target role</h4>${list(r.missing_skills_for_target_role)}
    <h4>ATS issues</h4>${list(r.ats_issues)}
    <h4>Rewritten bullets</h4>
    ${(r.rewritten_bullets || []).map(b => `<div class="bullet-pair"><div class="orig">${escapeHtml(b.original)}</div><div class="improved">${escapeHtml(b.improved)}</div></div>`).join("")}
  `;
}

// ===== Interview Coach =====
let currentInterviewSessionId = null;

$("#interview-start").addEventListener("click", async () => {
  const role = $("#interview-role").value;
  const quick = ($("#interview-mode") ? $("#interview-mode").value === "quick" : false);
  $("#interview-start").disabled = true;
  try {
    const result = await api("/api/interview/start", { method: "POST", body: JSON.stringify({ role, quick }) });
    currentInterviewSessionId = result.session_id;
    cvTrack("interview_started");
    $("#interview-setup").classList.add("hidden");
    $("#interview-session").classList.remove("hidden");
    renderInterviewLog(result.turns);
  } catch (err) {
    toast(err.message, "error");
  } finally {
    $("#interview-start").disabled = false;
  }
});

function renderInterviewLog(turns) {
  const log = $("#interview-log");
  log.innerHTML = "";
  turns.forEach(t => {
    if (t.feedback) {
      const fb = document.createElement("div");
      fb.className = "msg feedback";
      fb.innerHTML = `<span class="msg-tag">FEEDBACK · Score ${escapeHtml(t.feedback.score)}/10</span>
        <strong>Strengths:</strong> ${escapeHtml((t.feedback.strengths || []).join("; "))}<br/>
        <strong>Improve:</strong> ${escapeHtml((t.feedback.improvements || []).join("; "))}`;
      log.appendChild(fb);
    }
    const div = document.createElement("div");
    div.className = `msg ${t.speaker === "interviewer" ? "assistant" : "user"}`;
    div.innerHTML = `<span class="msg-tag">${t.speaker === "interviewer" ? "INTERVIEWER" : "YOU"}</span>${escapeHtml(t.content)}`;
    log.appendChild(div);
  });
  log.scrollTop = log.scrollHeight;
}

$("#interview-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const input = $("#interview-input");
  const answer = input.value.trim();
  if (!answer || !currentInterviewSessionId) return;
  input.value = "";
  input.disabled = true;

  try {
    const result = await api(`/api/interview/${currentInterviewSessionId}/respond`, {
      method: "POST",
      body: JSON.stringify({ answer }),
    });
    renderInterviewLog(result.turns);
    profile.xp += result.is_complete ? 25 : 5;
    renderStatusBar();
  checkProStatus();
    if (result.is_complete) {
      input.placeholder = "Interview complete.";
      $("#interview-form").querySelector("button").disabled = true;
      const _in = $("#interview-new"); if (_in) _in.classList.remove("hidden");
      localStorage.setItem("cv_onb_interview", "1"); renderOnboarding();
      cvTrack("interview_completed");
      celebrate();
    }
    if (result.is_complete && result.overall_score != null) showScorecard(result.overall_score, result.role, result.verdict);
  } catch (err) {
    toast(err.message, "error");
  } finally {
    input.disabled = false;
    input.focus();
  }
});

// ===== Boot =====
(async function boot() {
  const _urlRef = new URLSearchParams(window.location.search).get("ref");
  if (_urlRef) sessionStorage.setItem("cv_ref", _urlRef);
  if (token) {
    await enterApp();
  }
})();

// ===== Achievements =====
async function loadAchievements() {
  const listEl = $("#ach-list");
  if (!listEl) return;
  listEl.innerHTML = "Loading...";
  try {
    const achievements = await api("/api/achievements");
    if (!achievements || achievements.length === 0) {
      listEl.innerHTML = "<p>No achievements logged yet. Claim your first win!</p>";
      return;
    }
    listEl.innerHTML = "";
    achievements.forEach(a => {
      const badge = a.type === "hired" ? "🎉" : a.type === "certification" ? "📜" : "💼";
      const xp = a.type === "hired" ? 100 : a.type === "certification" ? 50 : 20;
      const div = document.createElement("div");
      div.className = "ach-item";
      div.innerHTML = `<span class="ach-badge">${badge}</span>
                       <div class="ach-details">
                         <strong>${escapeHtml(a.title)}</strong>
                         <span class="ach-meta">${a.type.toUpperCase()} · +${xp} XP</span>
                       </div>`;
      listEl.appendChild(div);
    });
  } catch (err) {
    listEl.innerHTML = `<p style="color:var(--red)">Failed to load: ${escapeHtml(err.message)}</p>`;
  }
}

$("#ach-submit").addEventListener("click", async () => {
  const type = $("#ach-type").value;
  const title = $("#ach-title").value.trim();
  if (!title) return toast("Please enter a title.", "error");

  const btn = $("#ach-submit");
  btn.disabled = true;
  try {
    const result = await api("/api/achievements", {
      method: "POST",
      body: JSON.stringify({ type, title })
    });
    $("#ach-title").value = "";
    $("#ach-saved").classList.remove("hidden");
    setTimeout(() => $("#ach-saved").classList.add("hidden"), 3000);

    if (profile) {
      profile.xp += result.xp_awarded;
      renderStatusBar();
  checkProStatus();
    }
    loadAchievements();
  } catch (err) {
    toast("Error: " + err.message, "error");
  } finally {
    btn.disabled = false;
  }
});
// ===== Paywall UI Logic =====
function showPaywall() {
  cvTrack("paywall_shown");
  const modal = document.getElementById('paywall-modal');
  if (modal) modal.classList.remove('hidden');
}
document.getElementById('go-pro-btn').addEventListener('click', showPaywall);

// Hide the Go Pro button if the user is already Pro
function checkProStatus() {
  const proBtn = document.getElementById('go-pro-btn');
  if (proBtn && profile) {
    proBtn.style.display = profile.is_pro ? 'none' : 'flex';
  }
}
const _newBtn = $("#interview-new");
if (_newBtn) _newBtn.addEventListener("click", () => {
  currentInterviewSessionId = null;
  $("#interview-session").classList.add("hidden");
  $("#interview-setup").classList.remove("hidden");
  _newBtn.classList.add("hidden");
  const btn = $("#interview-form").querySelector("button");
  btn.disabled = false;
  $("#interview-input").placeholder = "Type your answer...";
  $("#interview-input").disabled = false;
});


// ===== Shareable Scorecard =====
let _sc = null;
function showScorecard(score, role, verdict) {
  _sc = { score: score, role: role || "Cyber Security", verdict: verdict || "" };
  const certBtn = $("#sc-cert"); if (certBtn) { certBtn.classList.toggle("hidden", !profile.is_premium); certBtn.onclick = () => window.open(`${API_BASE}/api/interview/${currentInterviewSessionId}/certificate`, "_blank"); }
  countUp($("#sc-score"), score);
  $("#sc-role").textContent = _sc.role;
  $("#sc-verdict").textContent = _sc.verdict;
  $("#scorecard-modal").classList.remove("hidden");
}
const _scDl = $("#sc-download");
if (_scDl) _scDl.addEventListener("click", () => { if (_sc) downloadScorecard(_sc); });
const _scCp = $("#sc-copy");
if (_scCp) _scCp.addEventListener("click", () => { if (_sc) copySharePost(_sc); });

function wrapText(ctx, text, x, y, maxW, lh) {
  const words = String(text || "").split(" ");
  let line = "";
  for (const w of words) {
    const t = line + w + " ";
    if (ctx.measureText(t).width > maxW && line) { ctx.fillText(line.trim(), x, y); line = w + " "; y += lh; }
    else line = t;
  }
  if (line) ctx.fillText(line.trim(), x, y);
}

function downloadScorecard(sc) {
  const c = document.createElement("canvas");
  c.width = 1080; c.height = 1350;
  const x = c.getContext("2d");
  x.fillStyle = "#0a0a0a"; x.fillRect(0, 0, 1080, 1350);
  x.strokeStyle = "#00ffcc"; x.lineWidth = 6; x.strokeRect(40, 40, 1000, 1270);
  x.textAlign = "left";
  x.fillStyle = "#00ffcc"; x.font = "bold 46px Consolas, monospace";
  x.fillText(">_ CYBERVERSE.AI", 80, 150);
  x.fillStyle = "#888"; x.font = "30px Arial";
  x.fillText("AI MOCK INTERVIEW SCORECARD", 80, 200);
  x.textAlign = "center";
  x.fillStyle = "#ffffff"; x.font = "bold 280px Consolas, monospace";
  x.fillText(String(sc.score), 540, 640);
  x.fillStyle = "#888"; x.font = "44px Arial";
  x.fillText("/ 100", 540, 710);
  x.fillStyle = "#00ffcc"; x.font = "bold 58px Arial";
  x.fillText(String(sc.role).toUpperCase(), 540, 830);
  x.fillStyle = "#dddddd"; x.font = "36px Arial";
  wrapText(x, sc.verdict, 540, 920, 840, 50);
  x.fillStyle = "#ffffff"; x.font = "bold 44px Arial";
  x.fillText("Can you beat my score?", 540, 1150);
  x.fillStyle = "#00ffcc"; x.font = "bold 48px Consolas, monospace";
  x.fillText("app.grcwithgaurav.com", 540, 1225);
  const a = document.createElement("a");
  a.download = "cyberverse-scorecard.png";
  a.href = c.toDataURL("image/png");
  a.click();
}

function copySharePost(sc) {
  const tag = String(sc.role).replace(/[^a-zA-Z0-9]/g, "");
  const text = "I just scored " + sc.score + "/100 on the " + sc.role + " AI mock interview on CyberVerse AI 🎯\n\nThe AI grilled me like a real recruiter and told me exactly what to fix.\n\nCan you beat my score? 👇\nhttps://app.grcwithgaurav.com\n\n#cybersecurity #" + tag + " #AI #jobsearch";
  cvTrack("share_copied");
  navigator.clipboard.writeText(text).then(() => {
    const b = $("#sc-copy"); b.textContent = "✅ Copied! Paste it on LinkedIn";
    setTimeout(() => { b.textContent = "📋 Copy LinkedIn Post"; }, 2500);
  });
}


// ===== Resume Share Card (CV-102) =====
function downloadResumeScorecard(score, role) {
  const c = document.createElement("canvas");
  c.width = 1080; c.height = 1350;
  const x = c.getContext("2d");
  x.fillStyle = "#0a0a0a"; x.fillRect(0, 0, 1080, 1350);
  x.strokeStyle = "#00ffcc"; x.lineWidth = 6; x.strokeRect(40, 40, 1000, 1270);
  x.textAlign = "left";
  x.fillStyle = "#00ffcc"; x.font = "bold 46px Consolas, monospace";
  x.fillText(">_ CYBERVERSE.AI", 80, 150);
  x.fillStyle = "#888"; x.font = "30px Arial";
  x.fillText("AI RESUME REVIEW SCORECARD", 80, 200);
  x.textAlign = "center";
  x.fillStyle = "#ffffff"; x.font = "bold 280px Consolas, monospace";
  x.fillText(String(score), 540, 640);
  x.fillStyle = "#888"; x.font = "44px Arial";
  x.fillText("/ 100", 540, 710);
  x.fillStyle = "#00ffcc"; x.font = "bold 58px Arial";
  x.fillText("TARGET: " + String(role).toUpperCase(), 540, 830);
  x.fillStyle = "#dddddd"; x.font = "40px Arial";
  x.fillText("The AI found my exact missing skills", 540, 950);
  x.fillText("and rewrote my weak bullets.", 540, 1010);
  x.fillStyle = "#ffffff"; x.font = "bold 44px Arial";
  x.fillText("Can your resume beat mine?", 540, 1150);
  x.fillStyle = "#00ffcc"; x.font = "bold 48px Consolas, monospace";
  x.fillText("app.grcwithgaurav.com", 540, 1225);
  const a = document.createElement("a");
  a.download = "cyberverse-resume-scorecard.png";
  a.href = c.toDataURL("image/png");
  a.click();
}

function copyResumeSharePost(score, role) {
  const tag = String(role).replace(/[^a-zA-Z0-9]/g, "");
  const text = "My resume scored " + score + "/100 for a " + role + " role on CyberVerse AI 📄\n\nThe AI found the exact skills I was missing and rewrote my weak bullets like a real recruiter.\n\nCan your resume beat mine? 👇\nhttps://app.grcwithgaurav.com\n\n#cybersecurity #resume #" + tag + " #jobsearch";
  cvTrack("share_copied");
  navigator.clipboard.writeText(text).then(() => {
    const b = $("#res-sc-copy"); 
    const orig = b.textContent;
    b.textContent = "✅ Copied! Paste it on LinkedIn";
    setTimeout(() => { b.textContent = orig; }, 2500);
  });
}




// ===== Mobile drawer =====
(function () {
  const sb = document.querySelector(".sidebar");
  const ham = document.getElementById("cv-hamburger");
  const bd = document.getElementById("sidebar-backdrop");
  if (!sb || !ham) return;
  const isOpen = () => sb.classList.contains("open");
  const close = () => { sb.classList.remove("open"); if (bd) bd.style.display = "none"; };
  const open = () => { sb.classList.add("open"); if (bd) bd.style.display = "block"; };
  ham.onclick = (e) => { e.preventDefault(); e.stopPropagation(); isOpen() ? close() : open(); };
  if (bd) bd.onclick = close;
  document.querySelectorAll(".nav-item").forEach(b => b.addEventListener("click", () => {
    if (window.innerWidth <= 900) close();
  }));
})();


// ===== renderOnboarding fallback =====
if (typeof window.renderOnboarding !== "function") {
  window.renderOnboarding = function () {
    try {
      const card = document.getElementById("onboarding-card") || document.querySelector(".onboarding-card");
      if (!card) return;
      const flags = [
        !!localStorage.getItem("cv_onb_resume"),
        !!localStorage.getItem("cv_onb_interview"),
        !!localStorage.getItem("cv_onb_ops")
      ];
      const count = flags.filter(Boolean).length;
      card.querySelectorAll("input[type=checkbox]").forEach((cb, i) => {
        if (typeof flags[i] === "boolean") cb.checked = flags[i];
      });
      const prog = card.querySelector("#onb-progress") || card.querySelector("[data-onb-progress]");
      if (prog) prog.textContent = count + "/3";
      if (count === 3) card.style.display = "none";
    } catch (e) { /* never crash the app for a checklist */ }
  };
}


function celebrate() {
  if (!document.getElementById("cv-confetti-css")) {
    const st = document.createElement("style"); st.id = "cv-confetti-css";
    st.textContent = "@keyframes cvfall { to { transform: translateY(105vh) rotate(720deg); } }";
    document.head.appendChild(st);
  }
  const colors = ["#00ffcc", "#8b5cf6", "#f59e0b", "#ef4444", "#3b82f6"];
  for (let i = 0; i < 80; i++) {
    const el = document.createElement("div");
    el.style.cssText = "position:fixed;top:-12px;width:8px;height:12px;z-index:9999;pointer-events:none;background:" + colors[i % 5] + ";left:" + (Math.random() * 100) + "vw;transform:rotate(" + (Math.random() * 360) + "deg);animation:cvfall " + (2 + Math.random() * 1.5) + "s linear forwards;";
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 4200);
  }
}


const ROADMAP = [
  {phase: "Phase 1 - Foundations", weeks: [
    {id:"w1", t:"Networking & Linux basics", cert:"Security+ SY0-701 1.1-1.3", goto:"mentor", items:["TCP/IP, OSI model","Linux permissions","Quiz me on ports"]},
    {id:"w2", t:"Security fundamentals", cert:"Security+ SY0-701 1.4-2.2", goto:"ctf", items:["CIA triad, AAA, zero trust","Malware types, phishing","Solve a CTF Bite"]},
    {id:"w3", t:"Resume & presence", goto:"resume", items:["Run AI resume review","Rewrite LinkedIn headline","Add hands-on project"]},
    {id:"w4", t:"First mock interview", goto:"interview", items:["Quick Round (3 questions) voice mode","Review scorecard","Re-answer weakest question"]}]},
  {phase: "Phase 2 - Defense", weeks: [
    {id:"w5", t:"SIEM & log analysis", cert:"Security+ SY0-701 2.4", goto:"ctf", items:["Event IDs 4624, 4625, 4688","Splunk stats vs transaction","CTF log challenges"]},
    {id:"w6", t:"Alert triage drills", goto:"interview", items:["Phishing-click scenario","Validate, enrich, scope, contain","Target score 60+"]},
    {id:"w7", t:"Threat intel & vuln management", goto:"mentor", items:["CVE vs CVSS vs EPSS","Zero-day prioritization","Vuln scenario"]},
    {id:"w8", t:"GRC awareness", goto:"interview", items:["ISO 27001 risk assessment","Vendor risk tiering","GRC mock interview"]}]},
  {phase: "Phase 3 - Hunt & Get Hired", weeks: [
    {id:"w9", t:"Threat hunting basics", goto:"ctf", items:["Lateral movement indicators","Beaconing intervals","Golden vs silver ticket"]},
    {id:"w10", t:"Advanced interviews", goto:"interview", items:["Full 6-question voice interview","Defend against follow-ups","Share scorecard"]},
    {id:"w11", t:"Applications sprint", goto:"resume", items:["10 tailored applications","Attach scorecard","Ask for referrals"]},
    {id:"w12", t:"Offer readiness", goto:"interview", items:["Final mock interview","Prepare 'why cybersecurity' story","Download certificate"]}]}
];
function renderRoadmap() {
  const list = document.getElementById("rm-list");
  if (!list) return;
  const done = JSON.parse(localStorage.getItem("cv_roadmap") || "{}");
  const total = ROADMAP.reduce((n, p) => n + p.weeks.length, 0);
  const doneCount = Object.values(done).filter(Boolean).length;
  document.getElementById("rm-bar").style.width = Math.round(100 * doneCount / total) + "%";
  document.getElementById("rm-progress").textContent = doneCount + " / " + total + " weeks completed";
  let html = "";
  ROADMAP.forEach(ph => {
    html += '<h3 style="color:var(--accent);margin:24px 0 10px">' + ph.phase + "</h3>";
    ph.weeks.forEach(w => {
      const isDone = !!done[w.id];
      html += '<div class="card" style="padding:16px;margin-bottom:10px;' + (isDone ? "opacity:.65;" : "") + '">' +
        '<div style="display:flex;gap:12px;align-items:flex-start">' +
        '<input type="checkbox" data-week="' + w.id + '" ' + (isDone ? "checked" : "") + ' style="margin-top:4px;accent-color:var(--accent);width:18px;height:18px;cursor:pointer"/>' +
        '<div style="flex:1"><div style="font-weight:700">' + w.t +
        (w.cert ? ' <span style="color:var(--amber);font-size:.72rem;border:1px solid var(--amber);border-radius:10px;padding:1px 8px">' + w.cert + "</span>" : "") +
        "</div><ul style='margin:8px 0 0;padding-left:18px;color:var(--text-muted);font-size:.9rem'>" +
        w.items.map(it => "<li>" + it + "</li>").join("") +
        "</ul><button class='btn-secondary rm-go' data-goto='" + w.goto + "' style='margin-top:10px;padding:6px 14px'>Practice →</button></div></div></div>";
    });
  });
  list.innerHTML = html;
  list.querySelectorAll("input[data-week]").forEach(cb => cb.addEventListener("change", () => {
    const d = JSON.parse(localStorage.getItem("cv_roadmap") || "{}");
    d[cb.dataset.week] = cb.checked;
    localStorage.setItem("cv_roadmap", JSON.stringify(d));
    renderRoadmap();
  }));
  list.querySelectorAll(".rm-go").forEach(b => b.addEventListener("click", () => goToView(b.dataset.goto)));
}


const LABS = [
 {"id":"splunk-home","title":"Splunk Home Lab","tool":"Splunk","mins":90,"level":"Beginner","steps":["Install Splunk","Forwarder","SPL search","Create alert"],"evidence":["Search results"],"bullet":"Built a Splunk lab with Universal Forwarder and SPL alerts.","star":"S: Needed SIEM experience. A: Built Splunk lab. R: Walk interviewer through it.","linkedin":"Weekend build: Splunk lab."},
 {"id":"sysmon","title":"Sysmon: See Everything","tool":"Sysmon","mins":60,"level":"Beginner","steps":["Download Sysmon","Install","Event 1","Write 3 detection ideas"],"evidence":["Event 1"],"bullet":"Deployed Sysmon and analyzed Event 1.","star":"S: Host telemetry. A: Installed Sysmon. R: Explain telemetry.","linkedin":"Sysmon lab complete."},
 {"id":"wireshark","title":"Wireshark: Read the Wire","tool":"Wireshark","mins":60,"level":"Beginner","steps":["Capture 5 mins","Follow TCP","Document 3 anomalies"],"evidence":["TCP stream"],"bullet":"Analyzed live traffic with Wireshark.","star":"S: Network questions. A: Wireshark capture. R: Answer with specifics.","linkedin":"Followed my first TCP stream."},
 {"id":"elastic","title":"Elastic SIEM Quickstart","tool":"Elastic","mins":120,"level":"Intermediate","steps":["Start trial","Winlogbeat","Detection rule","Trigger"],"evidence":["Alert"],"bullet":"Stood up Elastic SIEM and created a detection rule.","star":"S: SIEM experience. A: Deployed Elastic. R: Discuss rule tuning.","linkedin":"My first Elastic detection rule fired."},
 {"id":"ad-audit","title":"AD Audit Policies","tool":"Windows","mins":90,"level":"Intermediate","steps":["Promote DC","Audit policies","Generate 4624/4625"],"evidence":["Events"],"bullet":"Promoted DC and enabled logon auditing.","star":"S: AD questions. A: Built DC. R: Kerberos answers.","linkedin":"Built my own domain controller."},
 {"id":"yara","title":"Write a YARA Rule","tool":"YARA","mins":45,"level":"Intermediate","steps":["Install","Sample file","Write rule","Run yara"],"evidence":["Hit"],"bullet":"Wrote and tested YARA rules.","star":"S: Detection basics. A: Authored YARA. R: Explain precision.","linkedin":"Wrote my first YARA rule."},
 {"id":"pfsense","title":"pfSense Firewall","tool":"pfSense","mins":120,"level":"Intermediate","steps":["Install","WAN/LAN","Block rule","Verify block"],"evidence":["Log"],"bullet":"Deployed pfSense and verified block rules.","star":"S: Firewall abstract. A: Deployed pfSense. R: Talk allow/deny.","linkedin":"My own firewall lab complete."},
 {"id":"phish-lab","title":"Phishing Analysis","tool":"Any","mins":60,"level":"Beginner","steps":["Sample email","Read headers","Trace hops","Write playbook"],"evidence":["Playbook"],"bullet":"Analyzed phishing email end to end.","star":"S: Phishing triage. A: Dissected email. R: Run pipeline.","linkedin":"Dissected a phishing email."}
];
async function renderLabs() {
  const list = document.getElementById("labs-list");
  if (!list) return;
  try {
    const d = await api("/api/labs");
    const doneCount = Object.keys(d.done).length;
    document.getElementById("labs-progress").textContent = doneCount + " / " + d.labs.length + " labs completed";
    list.innerHTML = d.labs.map(lab => {
      const done = d.done[lab.id];
      return '<div class="card" style="padding:16px;margin-bottom:12px;">' +
        '<div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap"><strong>' + lab.title + "</strong>" +
        '<span style="color:var(--text-muted);font-size:.8rem">' + lab.tool + " • " + lab.mins + " min • " + lab.level + (done ? " • ✅ done" : "") + "</span></div>" +
        "<details style='margin-top:8px'><summary style='cursor:pointer;color:var(--accent);font-size:.9rem'>Steps & evidence</summary>" +
        "<ol style='margin:8px 0 0;padding-left:18px;color:var(--text-muted);font-size:.9rem'>" + lab.steps.map(x => "<li>" + x + "</li>").join("") + "</ol></details>" +
        (done
          ? '<div style="margin-top:12px"><p style="font-size:.85rem;color:var(--text-muted)"><b>Resume:</b> ' + done.bullet + "</p>" +
            '<div style="display:flex;gap:8px;margin-top:8px"><button class="btn-secondary lab-copy" data-k="bullet" data-lab="' + lab.id + '">Copy bullet</button></div></div>'
          : '<div style="margin-top:12px"><button class="btn-primary lab-done" data-lab="' + lab.id + '">✅ Mark complete & generate pack</button></div>') +
        "</div>";
    }).join("");
    list.querySelectorAll(".lab-done").forEach(b => b.addEventListener("click", async () => {
      const r = await api("/api/labs/complete", { method: "POST", body: JSON.stringify({ lab_id: b.dataset.lab }) });
      if (!r.error) { try { cvTrack("lab_completed"); profile.xp += 15; renderStatusBar(); celebrate(); toast("Lab complete!"); renderLabs(); } catch(e){} }
    }));
    list.querySelectorAll(".lab-copy").forEach(b => b.addEventListener("click", () => {
      navigator.clipboard.writeText(d.done[b.dataset.lab][b.dataset.k]); toast("Copied");
    }));
  } catch (e) { list.innerHTML = "Could not load labs."; }
}


async function renderStories() {
  const list = document.getElementById("st-list");
  if (!list) return;
  try {
    const stories = await api("/api/stories");
    list.innerHTML = stories.length ? stories.map(st =>
      '<div class="card" style="padding:14px;margin-bottom:10px"><strong>' + escapeHtml(st.title) + "</strong>" +
      '<p style="color:var(--text-muted);font-size:.88rem;margin-top:6px"><b>S:</b> ' + escapeHtml(st.s) + ' <b>T:</b> ' + escapeHtml(st.t || "-") + ' <b>A:</b> ' + escapeHtml(st.a) + ' <b>R:</b> ' + escapeHtml(st.r || "-") + "</p>" +
      '<div style="display:flex;gap:8px"><button class="btn-secondary st-copy" data-id="' + st.id + '">Copy</button></div></div>').join("")
      : '<p style="color:var(--text-muted)">No stories yet. Build your first one above.</p>';
    list.querySelectorAll(".st-copy").forEach(b => b.addEventListener("click", () => {
      const st = stories.find(x => x.id == b.dataset.id);
      navigator.clipboard.writeText("Situation: " + st.s + "\nTask: " + (st.t || "-") + "\nAction: " + st.a + "\nResult: " + (st.r || "-"));
      toast("Copied");
    }));
  } catch (e) { list.innerHTML = "Could not load stories."; }
}


async function loadCTF() {
  const list = document.getElementById("ctf-list");
  if (!list) return;
  list.innerHTML = "Loading CTF Bites...";
  try {
    const data = await api("/api/ctf");
    if (!data.questions || data.questions.length === 0) { list.innerHTML = "No CTF Bites available."; return; }
    let html = "";
    data.questions.forEach((q, i) => {
      html += '<div class="card" style="margin-bottom:14px;padding:14px" data-idx="'+i+'">' +
        '<p style="font-weight:600;margin-bottom:8px">' + (i+1) + '. ' + escapeHtml(q.question) + '</p>' +
        '<div class="ctf-options"></div>' +
        '<p class="ctf-fb" style="display:none;margin-top:8px"></p>' +
        '<button class="btn-secondary ctf-check" style="margin-top:8px">Check Answer</button></div>';
    });
    list.innerHTML = html;
    list.querySelectorAll(".card").forEach(card => {
      const idx = parseInt(card.dataset.idx);
      const q = data.questions[idx];
      const optWrap = card.querySelector(".ctf-options");
      q.options.forEach((opt, oi) => {
        const lbl = document.createElement("label");
        lbl.style.cssText = "display:block;margin:4px 0;cursor:pointer";
        lbl.innerHTML = '<input type="radio" name="ctf-'+idx+'" value="'+oi+'" style="margin-right:6px"> ' + escapeHtml(opt);
        optWrap.appendChild(lbl);
      });
      card.querySelector(".ctf-check").addEventListener("click", () => {
        const sel = card.querySelector('input[name="ctf-'+idx+'"]:checked');
        const fb = card.querySelector(".ctf-fb");
        if (!sel) { fb.style.display="block"; fb.style.color="#f59e0b"; fb.textContent="Select an option first."; return; }
        const val = parseInt(sel.value);
        fb.style.display = "block";
        if (val === q.answer) {
          fb.style.color = "#00ffcc"; fb.textContent = "✅ Correct! " + (q.explanation || "");
          try { celebrate(); cvTrack("ctf_solved"); profile.xp += 5; renderStatusBar(); } catch(e){}
        } else {
          fb.style.color = "#ef4444"; fb.textContent = "❌ Incorrect. " + (q.explanation || "");
        }
      });
    });
  } catch (e) {
    list.innerHTML = "Could not load CTF Bites.";
  }
}


async function loadLeaderboard() {
  const list = document.getElementById("league-list") || document.getElementById("leaderboard-list");
  if (!list) return;
  list.innerHTML = "Loading leaderboard...";
  try {
    const data = await api("/api/leaderboard");
    if (!data.users || data.users.length === 0) { list.innerHTML = "No league members yet."; return; }
    let html = '<table style="width:100%;border-collapse:collapse"><thead><tr><th style="text-align:left;padding:8px">Rank</th><th style="text-align:left;padding:8px">User</th><th style="text-align:right;padding:8px">XP</th></tr></thead><tbody>';
    data.users.forEach((u, i) => {
      html += '<tr><td style="padding:8px">' + (i+1) + '</td><td style="padding:8px">' + escapeHtml(u.name) + '</td><td style="text-align:right;padding:8px;color:var(--accent)">' + (u.xp || 0) + '</td></tr>';
    });
    html += '</tbody></table>';
    list.innerHTML = html;
  } catch (e) {
    list.innerHTML = "Could not load leaderboard.";
  }
}


// ===== MOBILE MIC & LEAGUE RESCUE =====
(function() {
  // 1. Force Mic Permission Prompt (Intercepts click to force OS prompt)
  document.addEventListener('click', function(e) {
    const isMic = e.target.closest('#mic-btn, .mic-btn, #voice-btn, .voice-btn, [data-action="voice"], button[class*="mic"], button[id*="mic"], button[id*="voice"]');
    if (isMic && navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
          stream.getTracks().forEach(function(track) { track.stop(); }); // Stop immediately, just needed to trigger OS prompt
          console.log('Mic permission granted by OS');
        })
        .catch(function(err) {
          var d = document.createElement("div");
          d.style.cssText = "position:fixed;bottom:0;left:0;right:0;background:#b00020;color:#fff;padding:12px;z-index:99999;font-size:14px;font-family:monospace;";
          d.innerHTML = "<b>MIC BLOCKED:</b> " + err.message + ". Tap the 'Aa' or Lock icon in your URL bar to allow Microphone.";
          document.body.appendChild(d);
          setTimeout(function(){ d.remove(); }, 8000);
        });
    }
  }, true);

  // 2. Robust League/Leaderboard Loader with Red Debug Banner
  window.loadLeaderboard = async function() {
    var list = document.getElementById("league-list") || document.getElementById("leaderboard-list") || document.querySelector("[data-league]");
    if (!list) {
      var d = document.createElement("div");
      d.style.cssText = "position:fixed;bottom:0;left:0;right:0;background:#b00020;color:#fff;padding:12px;z-index:99999;font-size:12px;";
      d.innerHTML = "<b>LEAGUE HTML ERROR:</b> Cannot find #league-list element on this page.";
      document.body.appendChild(d); setTimeout(function(){ d.remove(); }, 8000);
      return;
    }
    list.innerHTML = "Loading weekly league...";
    try {
      var data = await api("/api/leaderboard");
      if (!data) throw new Error("Empty API response");
      var users = data.users || data.leaders || data;
      if (!Array.isArray(users) || users.length === 0) {
        list.innerHTML = "<p style='color:var(--text-muted)'>No league members yet. Complete an interview to join!</p>";
        return;
      }
      var html = '<table style="width:100%;border-collapse:collapse"><thead><tr><th style="padding:8px;text-align:left">Rank</th><th style="padding:8px;text-align:left">User</th><th style="padding:8px;text-align:right">XP</th></tr></thead><tbody>';
      users.forEach(function(u, i) {
        html += '<tr><td style="padding:8px">' + (i+1) + '</td><td style="padding:8px">' + escapeHtml(u.name || u.full_name || "Anonymous") + '</td><td style="text-align:right;padding:8px;color:var(--accent)">' + (u.xp || 0) + ' XP</td></tr>';
      });
      html += '</tbody></table>';
      list.innerHTML = html;
    } catch (e) {
      list.innerHTML = "Failed to load league.";
      var d = document.createElement("div");
      d.style.cssText = "position:fixed;bottom:0;left:0;right:0;background:#b00020;color:#fff;padding:12px;z-index:99999;font-size:12px;font-family:monospace;";
      d.innerHTML = "<b>LEAGUE API ERROR:</b> " + (e.message || e) + " (Check Render logs)";
      document.body.appendChild(d); setTimeout(function(){ d.remove(); }, 10000);
    }
  };

  // 3. Ensure View Router explicitly calls loadLeaderboard on tab switch
  document.querySelectorAll('.nav-item').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var view = btn.getAttribute('data-view');
      if (view === 'league' || view === 'leaderboard') {
        setTimeout(function() { window.loadLeaderboard(); }, 100);
      }
    });
  });
})();


// ===== MOBILE VOICE DEBUG CONSOLE =====
(function() {
  let debugBox = null;
  function logVoice(msg) {
    if (!debugBox) {
      debugBox = document.createElement("div");
      debugBox.id = "cv-voice-debug";
      debugBox.style.cssText = "position:fixed;bottom:10px;left:10px;right:10px;background:rgba(0,0,0,0.9);color:#0f0;padding:12px;z-index:99999;font-family:monospace;font-size:12px;border:1px solid #0f0;border-radius:8px;max-height:40vh;overflow:auto;white-space:pre-wrap;";
      document.body.appendChild(debugBox);
    }
    debugBox.innerHTML += new Date().toLocaleTimeString().split(" ")[0] + " | " + msg + "<br>";
    debugBox.scrollTop = debugBox.scrollHeight;
  }

  // Intercept clicks on ANY mic/voice button to start the debug session
  document.addEventListener("click", function(e) {
    const isMic = e.target.closest("#mic-btn, .mic-btn, #voice-btn, .voice-btn, [data-action='voice'], button[class*='mic'], button[id*='mic'], button[id*='voice']");
    if (isMic) {
      logVoice("🎙️ Mic button tapped. Checking API...");
      
      const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SR) {
        logVoice("❌ FATAL: SpeechRecognition API NOT SUPPORTED in this mobile browser.");
        return;
      }
      logVoice("✅ Speech API found. Creating instance...");

      try {
        const rec = new SR();
        rec.continuous = false;
        rec.interimResults = false;
        rec.lang = "en-US";

        rec.onstart = () => logVoice("🟢 State: LISTENING (Waiting for audio...)");
        rec.onaudiostart = () => logVoice("🎧 Audio stream opened.");
        rec.onsoundstart = () => logVoice("🔊 Sound detected!");
        rec.onspeechstart = () => logVoice("🗣️ Speech started!");
        rec.onspeechend = () => logVoice("⏹️ Speech ended.");
        rec.onend = () => logVoice("🏁 Session ended.");
        
        rec.onresult = (e) => {
          let transcript = "";
          for (let i = e.resultIndex; i < e.results.length; i++) {
            transcript += e.results[i][0].transcript;
          }
          logVoice("📝 TRANSCRIPT: " + transcript);
        };

        rec.onerror = (e) => {
          logVoice("❌ API ERROR: " + e.error + " (Message: " + (e.message || "None") + ")");
          if (e.error === "not-allowed") {
            logVoice("👉 FIX: Tap the 'Aa' or Lock icon in URL bar -> Site Settings -> Mic -> Allow.");
          }
        };

        logVoice("🚀 Calling rec.start()...");
        rec.start();
      } catch (err) {
        logVoice("❌ CRASH on start(): " + err.message);
      }
    }
  }, true);

  // Auto-hide debug box after 15 seconds of inactivity
  setInterval(() => {
    if (debugBox && document.getElementById("cv-voice-debug")) {
      // Keep it open while testing
    }
  }, 15000);
})();
