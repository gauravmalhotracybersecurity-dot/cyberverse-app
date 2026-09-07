
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


const ROADMAPS = {
 soc: { label: "SOC Analyst", phases: [
  { name: "Phase 1 - Foundations", weeks: [
   { t: "Networking & Linux basics", tag: "Security+ SY0-701.1-1.3", items: ["TCP/IP, OSI model", "Linux permissions", "Quiz me on ports"] },
   { t: "Security fundamentals", tag: "Security+ SY0-701.1.4-2.2", items: ["CIA triad, AAA, zero trust", "Malware types, phishing", "Solve a CTF Bite"] },
   { t: "Threat landscape & MITRE ATT&CK", tag: "ATT&CK", items: ["Navigate the ATT&CK matrix", "Map 3 real breaches to TTPs", "Quiz on tactics vs techniques"] },
   { t: "Logging & SIEM basics", tag: "Splunk Fundamentals", items: ["Install Splunk free tier", "Ingest Sysmon logs", "Write your first SPL query"] } ] },
  { name: "Phase 2 - Detection & Response", weeks: [
   { t: "Alert triage drills", tag: "Practice", items: ["True vs false positive drills", "Phishing triage playbook", "Write an escalation note"] },
   { t: "Use-case building", tag: "Splunk Core", items: ["Correlation search basics", "Threshold tuning", "Document one use case end-to-end"] },
   { t: "Threat intel workflow", tag: "CTI", items: ["IOC vs TTP thinking", "Enrich an alert with intel", "Write an intel summary"] },
   { t: "Incident response basics", tag: "IR", items: ["PICERL lifecycle", "Contain a mock ransomware case", "Evidence handling quiz"] } ] },
  { name: "Phase 3 - Job-ready", weeks: [
   { t: "Triage case studies", tag: "Portfolio", items: ["Write 2 triage case studies", "Publish on LinkedIn", "Peer review exchange"] },
   { t: "Resume & ATS pass", tag: "Resume", items: ["Keyword-map to SOC JDs", "Rewrite bullets with metrics", "Run the ATS checker"] },
   { t: "Mock interview sprint", tag: "Interview", items: ["5 live mock interviews", "Explain detections out loud", "Apply feedback loop"] },
   { t: "Lab showcase", tag: "Lab Log", items: ["Polish home-lab writeups", "Link labs in resume", "Demo one lab in interview"] } ] } ] },
 grc: { label: "GRC Consultant", phases: [
  { name: "Phase 1 - Foundations", weeks: [
   { t: "GRC & frameworks map", tag: "ISO 27001", items: ["Governance, Risk, Compliance pillars", "ISO vs SOC 2 vs NIST CSF", "Quiz on clauses 4-10"] },
   { t: "Risk fundamentals", tag: "ISO 27001 6.1", items: ["5x5 likelihood-impact method", "Risk appetite vs tolerance", "Score 5 sample risks"] },
   { t: "Controls & Annex A", tag: "Annex A", items: ["4 themes overview (93 controls)", "Map 10 controls to risks", "Control Finder drill"] },
   { t: "Policies & documentation", tag: "Practice", items: ["Draft an InfoSec policy", "Version control basics", "Policy review cycle"] } ] },
  { name: "Phase 2 - Practice", weeks: [
   { t: "Gap assessment run", tag: "Practice", items: ["Run gap tool on a fictional company", "Prioritize findings", "Write remediation plan"] },
   { t: "Risk register mastery", tag: "Register", items: ["Build a 15-row register", "Assign owners & target dates", "Justify treatments"] },
   { t: "Vendor risk management", tag: "VRM", items: ["Design a vendor questionnaire", "Score 3 vendors", "Contract clauses quiz"] },
   { t: "Compliance monitoring", tag: "Audit", items: ["Evidence collection routines", "Define KPIs & metrics", "Prep a management review"] } ] },
  { name: "Phase 3 - Job-ready", weeks: [
   { t: "SoA & audit prep", tag: "SoA", items: ["Build a Statement of Applicability", "Justify excluded controls", "Internal audit checklist"] },
   { t: "GRC case studies", tag: "Portfolio", items: ["Write 2 GRC case studies", "Publish on LinkedIn", "Peer review exchange"] },
   { t: "Resume & ATS pass", tag: "Resume", items: ["GRC keyword mapping", "Metrics-driven bullets", "Run the ATS checker"] },
   { t: "Mock interview sprint", tag: "Interview", items: ["5 live mock interviews", "Explain your risk method out loud", "Apply feedback loop"] } ] } ] },
 seceng: { label: "Security Engineer", phases: [
  { name: "Phase 1 - Foundations", weeks: [
   { t: "Networking deep-dive", tag: "Security+", items: ["Subnetting, routing, TLS handshake", "Packet capture lab", "Ports & protocols quiz"] },
   { t: "Linux & scripting", tag: "Linux", items: ["Hardening basics", "Automate a task in Bash", "Cron + logging lab"] },
   { t: "Identity & access", tag: "IAM", items: ["MFA/SSO/OAuth flows", "Break-fix AD lab", "Design least privilege"] },
   { t: "Cloud fundamentals", tag: "Cloud", items: ["Core AWS/Azure services", "IAM policies lab", "Shared responsibility model"] } ] },
  { name: "Phase 2 - Engineering", weeks: [
   { t: "Secure architecture", tag: "Design", items: ["Segmentation design", "WAF/proxy placement", "Threat-model a web app"] },
   { t: "Hardening & baselines", tag: "CIS", items: ["CIS benchmarks overview", "Harden a VM lab", "Config drift check"] },
   { t: "Detection engineering", tag: "SIEM", items: ["Write 3 detection rules", "Tune false positives", "Document coverage"] },
   { t: "DevSecOps basics", tag: "CI/CD", items: ["SAST/DAST/SCA gates", "Secret scanning", "Fix a vulnerable pipeline"] } ] },
  { name: "Phase 3 - Job-ready", weeks: [
   { t: "Engineering writeups", tag: "Lab Log", items: ["3 build/harden writeups", "Architecture diagrams", "Publish them"] },
   { t: "Resume & ATS pass", tag: "Resume", items: ["Engineering keyword mapping", "Metrics-driven bullets", "Run the ATS checker"] },
   { t: "Mock interview sprint", tag: "Interview", items: ["5 live mock interviews", "Whiteboard TLS & OAuth", "Apply feedback loop"] },
   { t: "System design drill", tag: "Design", items: ["Design a secure SaaS edge", "Discuss tradeoffs out loud", "Peer review"] } ] } ] },
 auditor: { label: "ISO 27001 Auditor", phases: [
  { name: "Phase 1 - Standard mastery", weeks: [
   { t: "Clauses 4-7 deep-dive", tag: "ISO 27001", items: ["Context & leadership", "Planning & support", "Clause quiz"] },
   { t: "Clauses 8-10 + Annex A", tag: "ISO 27001", items: ["Operation & improvement", "Scan all 93 controls", "Mapping exercise"] },
   { t: "Audit principles", tag: "ISO 19011", items: ["Audit types & ethics", "Programme management", "Auditor competence"] },
   { t: "Documentation review", tag: "Practice", items: ["Review sample ISMS docs", "Find 10 gaps", "Write review notes"] } ] },
  { name: "Phase 2 - Auditing", weeks: [
   { t: "Audit planning", tag: "Practice", items: ["Scope & criteria", "Audit plan & checklist", "Sampling methods"] },
   { t: "Interviewing auditees", tag: "Practice", items: ["Open-question technique", "Evidence vs assertion", "Note-taking drill"] },
   { t: "Nonconformity writing", tag: "NC", items: ["Major vs minor NC", "Root-cause phrasing", "Write 5 NC statements"] },
   { t: "Stage 1 & Stage 2 mock", tag: "Audit", items: ["Run a mock Stage 1", "Run a mock Stage 2", "Write the audit report"] } ] },
  { name: "Phase 3 - Job-ready", weeks: [
   { t: "Lead Auditor prep", tag: "ISO LA", items: ["Exam syllabus map", "Practice questions", "Case studies"] },
   { t: "Auditor portfolio", tag: "Portfolio", items: ["Sample audit report", "Checklist pack", "Publish a summary"] },
   { t: "Resume & ATS pass", tag: "Resume", items: ["Auditor keyword mapping", "Metrics-driven bullets", "Run the ATS checker"] },
   { t: "Mock interview sprint", tag: "Interview", items: ["5 live mock interviews", "Defend NC decisions out loud", "Apply feedback loop"] } ] } ] },
 pentest: { label: "Penetration Tester", phases: [
  { name: "Phase 1 - Foundations", weeks: [
   { t: "Networking & web basics", tag: "Security+", items: ["HTTP, DNS, TLS in depth", "Burp Suite setup", "Recon basics"] },
   { t: "Linux & tooling", tag: "Linux", items: ["CLI fluency drills", "nmap/nuclei basics", "Build your lab"] },
   { t: "Web vulns I", tag: "OWASP", items: ["Injection & XSS labs", "Burp Repeater drills", "7 writeups"] },
   { t: "Web vulns II", tag: "OWASP", items: ["AuthN/Z & SSRF labs", "API testing basics", "7 writeups"] } ] },
  { name: "Phase 2 - Practice", weeks: [
   { t: "Network pentest basics", tag: "eJPT", items: ["Scanning & enumeration", "Priv-esc basics", "Report writing"] },
   { t: "Active Directory labs", tag: "AD", items: ["Kerberos attacks overview", "Lateral movement lab", "Detection awareness"] },
   { t: "Reporting & communication", tag: "Report", items: ["Executive vs technical", "Risk rating with CVSS", "Remediation advice"] },
   { t: "CTF grind", tag: "CTF", items: ["4 easy HTB boxes", "Time-boxed methodology", "Build your notes system"] } ] },
  { name: "Phase 3 - Job-ready", weeks: [
   { t: "Specialty depth", tag: "OSCP-prep", items: ["Pick web-API or AD", "20 focused labs", "Mentor review"] },
   { t: "Resume & ATS pass", tag: "Resume", items: ["Pentest keyword mapping", "Metrics-driven bullets", "Run the ATS checker"] },
   { t: "Mock interview sprint", tag: "Interview", items: ["5 live mock interviews", "Explain exploit chains out loud", "Apply feedback loop"] },
   { t: "Portfolio & ethics", tag: "Ethics", items: ["Public writeups", "Scope & rules of engagement", "Demo day"] } ] } ] }
};
function rmRole(){ return localStorage.getItem("cv_rm_role") || "soc"; }
function syncCoachRole(label){
  var sel = document.querySelector("#view-interview select");
  if (!sel) return;
  for (var i=0;i<sel.options.length;i++){ if (sel.options[i].text === label){ sel.value = sel.options[i].value; break; } }
}
function renderRoadmap() {
  if (localStorage.getItem("cv_roadmap") && !localStorage.getItem("cv_roadmap_soc")) {
    localStorage.setItem("cv_roadmap_soc", localStorage.getItem("cv_roadmap"));
  }
  var role = rmRole();
  var R = ROADMAPS[role] || ROADMAPS.soc;
  var titleEl = document.getElementById("rm-title");
  if (titleEl) titleEl.textContent = "\ud83d\uddfa\ufe0f 90-Day " + R.label + " Roadmap";
  var chips = document.getElementById("rm-roles");
  if (chips) {
    chips.innerHTML = "";
    Object.keys(ROADMAPS).forEach(function(k){
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = ROADMAPS[k].label;
      b.style.cssText = "padding:6px 12px;border-radius:16px;font-size:.8rem;cursor:pointer;border:1px solid #333;background:#151515;color:#fff;" + (k===role ? "background:var(--accent);color:#001512;border-color:var(--accent);font-weight:700;" : "");
      b.onclick = function(){ localStorage.setItem("cv_rm_role", k); syncCoachRole(ROADMAPS[k].label); renderRoadmap(); };
      chips.appendChild(b);
    });
  }
  var list = document.getElementById("rm-list");
  var storeKey = "cv_roadmap_" + role;
  var done = JSON.parse(localStorage.getItem(storeKey) || "{}");
  var total = R.phases.reduce(function(n,p){ return n + p.weeks.length; }, 0);
  var doneCount = 0;
  R.phases.forEach(function(p,pi){ p.weeks.forEach(function(w,wi){ if (done[pi+"-"+wi]) doneCount++; }); });
  document.getElementById("rm-bar").style.width = Math.round(100*doneCount/total) + "%";
  document.getElementById("rm-progress").textContent = doneCount + " / " + total + " weeks completed";
  list.innerHTML = "";
  R.phases.forEach(function(ph,pi){
    var hd = document.createElement("h2");
    hd.style.cssText = "color:var(--accent);margin:18px 0 10px;font-size:1.15rem";
    hd.textContent = ph.name;
    list.appendChild(hd);
    ph.weeks.forEach(function(w,wi){
      var key = pi+"-"+wi;
      var card = document.createElement("div");
      card.style.cssText = "background:#141414;border:1px solid #222;border-radius:12px;padding:16px;margin-bottom:12px";
      card.innerHTML = "<div style='display:flex;gap:12px;align-items:flex-start'><input type='checkbox' data-key='"+key+"' style='width:20px;height:20px;margin-top:4px;flex:none'"+(done[key]?" checked":"")+"><div><div style='font-weight:700;color:#fff;font-size:1.05rem'>"+w.t+" <span style='border:1px solid #f5af19;color:#f5af19;border-radius:14px;padding:2px 10px;font-size:.75rem;font-weight:600;margin-left:6px;white-space:nowrap'>"+w.tag+"</span></div><ul style='color:var(--text-muted);margin:8px 0 0;padding-left:18px;line-height:1.7'>"+w.items.map(function(i){return "<li>"+i+"</li>";}).join("")+"</ul><button class='btn-secondary rm-go' data-goto='interview' style='margin-top:10px;padding:6px 14px'>Practice \u2192</button></div></div>";
      list.appendChild(card);
    });
  });
  list.querySelectorAll("input[type=checkbox]").forEach(function(cb){
    cb.addEventListener("change", function(){
      var d = JSON.parse(localStorage.getItem(storeKey) || "{}");
      d[cb.dataset.key] = cb.checked;
      localStorage.setItem(storeKey, JSON.stringify(d));
      renderRoadmap();
    });
  });
  list.querySelectorAll(".rm-go").forEach(b => b.addEventListener("click", () => goToView(b.dataset.goto)));
}
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


// ===== LEAGUE/CTF OVERRIDES (clean loaders, appended) =====
function cvEsc(s) {
  if (!s) return "";
  return String(s).replace(/[&<>"']/g, function (m) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]; });
}
function cvFindList(secId, ids, loadingRe) {
  var l = null;
  for (var i = 0; i < ids.length; i++) { l = document.getElementById(ids[i]); if (l) return l; }
  var sv = document.getElementById(secId);
  if (sv) {
    var nodes = sv.querySelectorAll("div,p,section");
    for (var j = 0; j < nodes.length; j++) {
      if (nodes[j].children.length === 0 && loadingRe.test(nodes[j].textContent)) { l = nodes[j]; break; }
    }
    if (!l) { l = document.createElement("div"); sv.appendChild(l); }
  }
  return l;
}
window.loadLeaderboard = function () {
  var l = cvFindList("view-league", ["league-list", "leaderboard-list"], /loading leaderboard/i);
  if (!l) return;
  l.innerHTML = "Loading weekly league...";
  api("/api/leaderboard").then(function (data) {
    var users = (data && (data.users || data.leaders)) || (Array.isArray(data) ? data : []);
    if (!users.length) { l.innerHTML = "<p style='color:var(--text-muted)'>No league members yet. Finish an interview to join!</p>"; return; }
    var medals = ["🥇", "", ""];
    var html = '<table style="width:100%;border-collapse:collapse"><thead><tr><th style="padding:8px;text-align:left">#</th><th style="padding:8px;text-align:left">Player</th><th style="padding:8px;text-align:right">XP</th></tr></thead><tbody>';
    for (var i = 0; i < users.length; i++) {
      var u = users[i];
      html += '<tr style="border-bottom:1px solid #222"><td style="padding:10px 8px">' + (medals[i] || (i + 1)) + '</td><td style="padding:10px 8px">' + cvEsc(u.name || u.full_name || "Anonymous") + (u.is_pro ? ' <span style="color:var(--amber);font-size:.75rem">PRO</span>' : '') + '</td><td style="text-align:right;padding:10px 8px;color:var(--accent)">' + (u.xp || 0) + '</td></tr>';
    }
    l.innerHTML = html + '</tbody></table>';
  }).catch(function () { l.innerHTML = "Could not load league."; });
};
window.loadCTF = function () {
  var l = cvFindList("view-ctf", ["ctf-list", "ctf-container"], /loading/i);
  if (!l) return;
  var LOCAL = [
    {question: "Which Windows Event ID indicates a FAILED logon attempt?", options: ["4624", "4625", "4688", "4769"], answer: 1, explanation: "4625 = failed logon; 4624 = success."},
    {question: "An email urges urgent invoice payment; the header shows a look-alike domain. First action?", options: ["Pay it", "Report and quarantine", "Delete and ignore", "Reply"], answer: 1, explanation: "Treat as phishing."},
    {question: "DNS tunneling exfiltrates data by abusing which protocol?", options: ["HTTP", "DNS", "SMTP", "NTP"], answer: 1, explanation: "Data hidden in DNS queries."},
    {question: "In the cyber kill chain, which stage follows Delivery?", options: ["Reconnaissance", "Exploitation", "Installation", "Actions on Objectives"], answer: 1, explanation: "Delivery > Exploitation."},
    {question: "Which Splunk command counts events per host?", options: ["stats count by host", "table host", "fields - host", "rename host"], answer: 0, explanation: "stats count by host."},
    {question: "A CVSS score of 9.0-10.0 is rated as?", options: ["Low", "Medium", "High", "Critical"], answer: 3, explanation: "9.0-10.0 = Critical."},
    {question: "A Golden Ticket attack forges a TGT using which account hash?", options: ["Administrator", "KRBTGT", "Guest", "LocalSystem"], answer: 1, explanation: "KRBTGT signs TGTs."}
  ];
  function render(l, q, src) {
    var html = '<div class="card" style="padding:16px"><p style="font-weight:700;margin-bottom:10px">⚡ ' + cvEsc(q.question) + '</p><p style="font-size:.75rem;color:var(--text-muted)">source: ' + src + "</p>";
    for (var i = 0; i < q.options.length; i++) {
      html += '<label style="display:block;margin:6px 0;cursor:pointer"><input type="radio" name="ctf-opt9" value="' + i + '" style="margin-right:8px">' + cvEsc(q.options[i]) + "</label>";
    }
    html += '<button id="ctf-check9" class="btn-primary" style="margin-top:10px">Check answer</button><p id="ctf-fb9" style="margin-top:10px;display:none"></p></div>';
    l.innerHTML = html;
    l.querySelector("#ctf-check9").addEventListener("click", function () {
      var sel = l.querySelector('input[name="ctf-opt9"]:checked');
      var fb = l.querySelector("#ctf-fb9");
      fb.style.display = "block";
      if (!sel) { fb.style.color = "#f59e0b"; fb.textContent = "Pick an option first."; return; }
      var ok = parseInt(sel.value, 10) === q.answer;
      fb.style.color = ok ? "#00ffcc" : "#ef4444";
      fb.textContent = ok ? "✅ Correct! " + (q.explanation || "") : "❌ Not quite. " + (q.explanation || "");
      if (ok) { try { celebrate(); } catch (e) {} }
    });
  }
  l.innerHTML = "Loading today's CTF Bite...";
  api("/api/ctf/today").then(function (d) {
    var q = d && (d.question && d.options ? d : (d.bite || d.data || (d.questions && d.questions[0]) || null));
    if (q) render(l, q, "live");
    else render(l, LOCAL[new Date().getDate() % LOCAL.length], "offline");
  }).catch(function () { render(l, LOCAL[new Date().getDate() % LOCAL.length], "offline"); });
};
