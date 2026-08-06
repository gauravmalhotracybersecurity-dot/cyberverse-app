def _auth_headers(client, email="erin@example.com"):
    resp = client.post(
        "/api/auth/signup",
        json={"email": email, "password": "password123", "full_name": "Erin Test"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_mentor_chat_persists_history(client, mock_claude):
    headers = _auth_headers(client)
    resp = client.post(
        "/api/mentor/chat", headers=headers, json={"message": "Explain phishing simply."}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["reply"] == "This is a mocked mentor reply."
    assert len(data["history"]) == 2  # user turn + assistant turn

    history_resp = client.get("/api/mentor/history", headers=headers)
    assert len(history_resp.json()) == 2


def test_mentor_chat_awards_xp(client, mock_claude):
    headers = _auth_headers(client)
    before = client.get("/api/profile/me", headers=headers).json()["xp"]
    client.post("/api/mentor/chat", headers=headers, json={"message": "Hi"})
    after = client.get("/api/profile/me", headers=headers).json()["xp"]
    assert after == before + 5


def test_daily_bundle_generated_and_cached(client, mock_claude):
    headers = _auth_headers(client)
    resp1 = client.get("/api/daily", headers=headers)
    assert resp1.status_code == 200
    assert resp1.json()["content"]["lesson"]["title"] == "Mock Lesson"

    # second call same day should hit the cache, not regenerate
    resp2 = client.get("/api/daily", headers=headers)
    assert resp2.json() == resp1.json()


def test_daily_bundle_updates_streak_and_xp(client, mock_claude):
    headers = _auth_headers(client)
    before = client.get("/api/profile/me", headers=headers).json()
    client.get("/api/daily", headers=headers)
    after = client.get("/api/profile/me", headers=headers).json()
    assert after["xp"] == before["xp"] + 10
    assert after["streak_days"] == 1


def test_resume_review_text(client, mock_claude):
    headers = _auth_headers(client)
    resume_text = "Experienced security analyst " * 10
    resp = client.post(
        "/api/resume/review",
        headers=headers,
        json={"resume_text": resume_text, "target_role": "SOC Analyst"},
    )
    assert resp.status_code == 200
    review = resp.json()["review"]
    assert review["overall_score"] == 80
    assert review["rewritten_bullets"][0]["improved"] == "Did stuff, quantified"


def test_resume_review_too_short_rejected(client, mock_claude):
    headers = _auth_headers(client)
    resp = client.post(
        "/api/resume/review", headers=headers, json={"resume_text": "too short", "target_role": "SOC Analyst"}
    )
    assert resp.status_code == 422  # pydantic min_length validation


def test_interview_start_and_respond(client, mock_claude):
    headers = _auth_headers(client)
    start_resp = client.post("/api/interview/start", headers=headers, json={"role": "SOC Analyst"})
    assert start_resp.status_code == 200
    session_id = start_resp.json()["session_id"]
    assert len(start_resp.json()["turns"]) == 1  # first interviewer question

    respond_resp = client.post(
        f"/api/interview/{session_id}/respond",
        headers=headers,
        json={"answer": "I would check the SIEM alerts first."},
    )
    assert respond_resp.status_code == 200
    turns = respond_resp.json()["turns"]
    assert len(turns) == 3  # question, candidate answer, next question
    assert respond_resp.json()["is_complete"] is False


def test_interview_respond_requires_valid_session(client, mock_claude):
    headers = _auth_headers(client)
    resp = client.post(
        "/api/interview/99999/respond", headers=headers, json={"answer": "test"}
    )
    assert resp.status_code == 404
