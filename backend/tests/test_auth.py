def signup(client, email="alice@example.com", password="password123"):
    return client.post(
        "/api/auth/signup",
        json={"email": email, "password": password, "full_name": "Alice Test"},
    )


def test_signup_returns_token(client):
    resp = signup(client)
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_signup_duplicate_email_rejected(client):
    signup(client)
    resp = signup(client)
    assert resp.status_code == 400


def test_login_success(client):
    signup(client)
    resp = client.post(
        "/api/auth/login", json={"email": "alice@example.com", "password": "password123"}
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(client):
    signup(client)
    resp = client.post(
        "/api/auth/login", json={"email": "alice@example.com", "password": "wrongpass"}
    )
    assert resp.status_code == 401


def test_profile_requires_auth(client):
    resp = client.get("/api/profile/me")
    assert resp.status_code == 401


def test_forgot_password_generic_message_for_unknown_email(client):
    resp = client.post("/api/auth/forgot-password", json={"email": "nobody@example.com"})
    assert resp.status_code == 200
    assert "reset link has been sent" in resp.json()["message"]


def test_full_password_reset_flow(client, monkeypatch):
    signup(client, email="bob@example.com", password="oldpassword1")

    captured = {}

    def fake_send(to, reset_token):
        captured["to"] = to
        captured["token"] = reset_token

    monkeypatch.setattr("routers.auth_routes.send_password_reset_email", fake_send)

    resp = client.post("/api/auth/forgot-password", json={"email": "bob@example.com"})
    assert resp.status_code == 200
    assert captured["to"] == "bob@example.com"
    assert captured["token"]

    resp = client.post(
        "/api/auth/reset-password",
        json={"token": captured["token"], "new_password": "newpassword2"},
    )
    assert resp.status_code == 200

    # old password no longer works
    resp = client.post(
        "/api/auth/login", json={"email": "bob@example.com", "password": "oldpassword1"}
    )
    assert resp.status_code == 401

    # new password works
    resp = client.post(
        "/api/auth/login", json={"email": "bob@example.com", "password": "newpassword2"}
    )
    assert resp.status_code == 200


def test_reset_with_garbage_token_rejected(client):
    resp = client.post(
        "/api/auth/reset-password",
        json={"token": "not-a-real-token", "new_password": "whatever123"},
    )
    assert resp.status_code == 400


def test_access_token_cannot_be_used_as_reset_token(client):
    """A normal session token has purpose=access and must not work for password reset."""
    resp = signup(client, email="carol@example.com")
    access_token = resp.json()["access_token"]
    resp = client.post(
        "/api/auth/reset-password",
        json={"token": access_token, "new_password": "whatever123"},
    )
    assert resp.status_code == 400
