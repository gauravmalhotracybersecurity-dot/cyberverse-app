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
        body: JSON.stringify({ email, password, full_name }),
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
  $("#interview-start").disabled = true;
  try {
    const result = await api("/api/interview/start", { method: "POST", body: JSON.stringify({ role }) });
    currentInterviewSessionId = result.session_id;
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
  navigator.clipboard.writeText(text).then(() => {
    const b = $("#res-sc-copy"); 
    const orig = b.textContent;
    b.textContent = "✅ Copied! Paste it on LinkedIn";
    setTimeout(() => { b.textContent = orig; }, 2500);
  });
}


// ===== Mobile drawer =====
(function () {
  const btn = document.getElementById("mobile-menu-btn");
  const sb = document.querySelector(".app-shell .sidebar");
  const bd = document.getElementById("sidebar-backdrop");
  if (!btn || !sb) return;
  const close = () => { sb.classList.remove("open"); if (bd) bd.classList.add("hidden"); };
  btn.addEventListener("click", () => {
    sb.classList.toggle("open");
    if (bd) bd.classList.toggle("hidden", !sb.classList.contains("open"));
  });
  if (bd) bd.addEventListener("click", close);
  document.querySelectorAll(".nav-item").forEach(n => n.addEventListener("click", () => { if (window.innerWidth <= 860) close(); }));
})();


// ===== Email verification deep link =====
(function checkForVerifyToken() {
  const v = new URLSearchParams(window.location.search).get("verify");
  if (!v) return;
  window.history.replaceState({}, "", window.location.pathname);
  fetch(`${API_BASE}/api/auth/verify-email`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token: v }),
  }).then(r => r.json()).then(d => {
    const el = $("#auth-error");
    el.textContent = d.message || d.detail || "Email verified. You can log in now.";
    el.classList.remove("hidden");
  });
})();


// ===== Toast system =====
function toast(msg, type) {
  let host = document.getElementById("toast-host");
  if (!host) {
    host = document.createElement("div");
    host.id = "toast-host";
    host.style.cssText = "position:fixed;bottom:24px;right:24px;z-index:200;display:flex;flex-direction:column;gap:10px;";
    document.body.appendChild(host);
  }
  const t = document.createElement("div");
  t.textContent = msg;
  t.style.cssText = "background:#151515;color:#fff;border:1px solid " + (type === "error" ? "#ff5555" : "#00ffcc") + ";border-radius:10px;padding:12px 18px;font-size:.9rem;box-shadow:0 6px 24px rgba(0,0,0,.5);max-width:320px;";
  host.appendChild(t);
  setTimeout(() => { t.style.opacity = "0"; t.style.transition = "opacity .4s"; setTimeout(() => t.remove(), 400); }, 3500);
}

// ===== Onboarding checklist =====
function renderOnboarding() {
  const card = $("#onboarding-card");
  if (!card || !profile) return;
  if (localStorage.getItem("cv_onb_dismissed")) { card.classList.add("hidden"); return; }
  card.classList.remove("hidden");
  const steps = [
    { done: !!(profile.learning_goals || (profile.certifications || []).length), label: "Set your goal & skill level", view: "profile" },
    { done: localStorage.getItem("cv_onb_resume") === "1", label: "Get your resume reviewed", view: "resume" },
    { done: localStorage.getItem("cv_onb_interview") === "1", label: "Finish your first mock interview", view: "interview" },
  ];
  const doneCount = steps.filter(x => x.done).length;
  $("#onb-progress").textContent = doneCount + "/3";
  if (doneCount === 3) {
    $("#onb-steps").innerHTML = '<div style="color:var(--accent);font-weight:700">🎉 All set! You are officially ahead of 90% of candidates. Keep the streak alive!</div>';
  } else {
    $("#onb-steps").innerHTML = steps.map(x =>
      '<div style="display:flex;align-items:center;gap:10px">' +
      '<span style="color:' + (x.done ? "var(--accent)" : "#555") + ';font-weight:700">' + (x.done ? "✓" : "○") + '</span>' +
      '<span style="color:' + (x.done ? "#888" : "#fff") + ';' + (x.done ? "text-decoration:line-through;" : "") + '">' + x.label + '</span>' +
      (x.done ? "" : '<button class="btn-secondary" data-onb-goto="' + x.view + '" style="margin-left:auto;padding:6px 12px">Do it →</button>') +
      '</div>').join("");
    $("#onb-steps").querySelectorAll("[data-onb-goto]").forEach(b => b.addEventListener("click", () => goToView(b.dataset.onbGoto)));
  }
  const d = $("#onb-dismiss");
  if (d) d.onclick = () => { localStorage.setItem("cv_onb_dismissed", "1"); card.classList.add("hidden"); };
}


// ===== Count-up animation =====
function countUp(el, to) {
  if (!el) return;
  const t0 = performance.now(), dur = 900;
  function f(t) {
    const p = Math.min(1, (t - t0) / dur);
    el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3)));
    if (p < 1) requestAnimationFrame(f);
  }
  requestAnimationFrame(f);
}


// ===== Voice Interview Mode =====
(function () {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  const mic = document.getElementById("mic-btn");
  const input = document.getElementById("interview-input");
  const form = document.getElementById("interview-form");
  if (!mic || !input) return;
  if (!SR) { mic.addEventListener("click", () => toast("Voice mode needs Chrome or Edge", "error")); return; }
  let rec = null, base = "";
  const stopUI = () => { rec = null; mic.classList.remove("recording"); mic.textContent = "️"; };
  mic.addEventListener("click", () => {
    if (rec) { rec.stop(); return; }
    rec = new SR();
    rec.lang = "en-IN";
    rec.continuous = true;
    rec.interimResults = true;
    base = input.value ? input.value.replace(/\s+$/, "") + " " : "";
    rec.onresult = (e) => {
      let finalT = "", interim = "";
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const t = e.results[i][0].transcript;
        if (e.results[i].isFinal) finalT += t + " ";
        else interim += t;
      }
      if (finalT) base += finalT;
      input.value = (base + interim).trimStart();
    };
    rec.onend = stopUI;
    rec.onerror = (e) => { if (window.toast) toast("Mic error: " + e.error, "error"); stopUI(); };
    rec.start();
    mic.classList.add("recording");
    mic.textContent = "⏹️";
    if (window.toast) toast("Listening… speak your answer", "info");
  });
  if (form) form.addEventListener("submit", () => { if (rec) rec.stop(); });
})();
