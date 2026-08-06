def _auth_headers(client, email="dana@example.com"):
    resp = client.post(
        "/api/auth/signup",
        json={"email": email, "password": "password123", "full_name": "Dana Test"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_default_profile(client):
    headers = _auth_headers(client)
    resp = client.get("/api/profile/me", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["skill_level"] == "beginner"
    assert data["certifications"] == []
    assert data["xp"] == 0


def test_update_profile_persists_mentor_memory(client):
    headers = _auth_headers(client)
    payload = {
        "skill_level": "intermediate",
        "certifications": ["Security+"],
        "weak_topics": ["SQL Injection"],
        "learning_goals": "Become a SOC Analyst",
    }
    resp = client.patch("/api/profile/me", headers=headers, json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["skill_level"] == "intermediate"
    assert data["certifications"] == ["Security+"]
    assert data["weak_topics"] == ["SQL Injection"]
    assert data["learning_goals"] == "Become a SOC Analyst"

    # confirm it actually persisted, not just echoed back
    resp2 = client.get("/api/profile/me", headers=headers)
    assert resp2.json()["skill_level"] == "intermediate"
