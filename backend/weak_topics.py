"""Helpers for the Weak Topics Loop: resume gaps and interview feedback
flow into user.weak_topics, which the Daily Ops bundle and AI Mentor
already read when personalizing content."""


def merge_weak_topics(user, new_topics, limit=12):
    """Merge short topic strings into user.weak_topics (dedupe, cap length)."""
    existing = [t for t in (user.weak_topics or []) if isinstance(t, str) and t.strip()]
    seen = {t.strip().lower() for t in existing}
    for topic in new_topics or []:
        if not isinstance(topic, str):
            continue
        t = topic.strip()
        if not t or len(t) > 60 or t.lower() in seen:
            continue
        existing.append(t)
        seen.add(t.lower())
    user.weak_topics = existing[:limit]