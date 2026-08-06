import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database import Base, get_db  # noqa: E402
import models  # noqa: E402,F401  (register tables on Base.metadata)


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    from rate_limit import limiter

    limiter.reset()
    yield


@pytest.fixture()
def test_db():
    """Fresh in-memory SQLite DB per test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    yield TestingSessionLocal
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(test_db, monkeypatch):
    # Import main AFTER test_db exists so we can override get_db before any
    # request is handled.
    import main

    def override_get_db():
        db = test_db()
        try:
            yield db
        finally:
            db.close()

    main.app.dependency_overrides[get_db] = override_get_db

    with TestClient(main.app) as c:
        yield c

    main.app.dependency_overrides.clear()


@pytest.fixture()
def mock_claude(monkeypatch):
    """Stub out real Anthropic API calls with canned responses."""

    async def fake_call_claude(system, messages, max_tokens=1024, temperature=0.7):
        return "This is a mocked mentor reply."

    async def fake_call_claude_json(system, messages, max_tokens=1500, temperature=0.7):
        # Return shapes that satisfy every prompts.py schema used in the app.
        return {
            "lesson": {"title": "Mock Lesson", "body": "Mock body text."},
            "quiz": {
                "question": "What is 2+2?",
                "choices": ["3", "4", "5", "6"],
                "correct_index": 1,
                "explanation": "Basic arithmetic.",
            },
            "news_summary": {
                "headline": "Mock breach reported",
                "summary": "A mock summary.",
                "why_it_matters": "Mock relevance.",
            },
            "challenge": {"title": "Mock challenge", "description": "Do a mock thing."},
            "interview_question": {
                "question": "Tell me about yourself.",
                "what_a_good_answer_covers": "Background and motivation.",
            },
            "practical_task": {"title": "Mock task", "description": "Mock 20 min task."},
            # resume review shape
            "overall_score": 80,
            "ats_score": 75,
            "strengths": ["Clear structure"],
            "gaps": ["Missing metrics"],
            "missing_skills_for_target_role": ["SIEM"],
            "ats_issues": ["No standard section headers"],
            "rewritten_bullets": [{"original": "Did stuff", "improved": "Did stuff, quantified"}],
            # interview shape
            "feedback": None,
            "next_question": "Tell me about a time you handled an incident.",
            "is_complete": False,
            "closing_remarks": None,
        }

    monkeypatch.setattr("routers.mentor_routes.call_claude", fake_call_claude)
    monkeypatch.setattr("routers.daily_routes.call_claude_json", fake_call_claude_json)
    monkeypatch.setattr("routers.resume_routes.call_claude_json", fake_call_claude_json)
    monkeypatch.setattr("routers.interview_routes.call_claude_json", fake_call_claude_json)
