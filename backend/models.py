from datetime import datetime
from sqlalchemy import Date, Boolean
import datetime as dt

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship

from database import Base


def now():
    return dt.datetime.utcnow()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, default="")
    created_at = Column(DateTime, default=now)

    # --- AI Mentor memory (Vision doc: "The AI should remember...") ---
    skill_level = Column(String, default="beginner")  # beginner | intermediate | advanced
    certifications = Column(JSON, default=list)       # ["Security+", ...]
    weak_topics = Column(JSON, default=list)           # ["SQL Injection", ...]
    learning_goals = Column(Text, default="")

    # --- Gamification (Feature Roadmap: XP, streak, rank) ---
    xp = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    is_pro = Column(Boolean, default=False)
    last_active_date = Column(String, default="")  # YYYY-MM-DD

    mentor_messages = relationship("MentorMessage", back_populates="user", cascade="all, delete-orphan")

    is_verified = Column(Boolean, default=False)
    reset_nonce = Column(String, nullable=True)
    verify_nonce = Column(String, nullable=True)
    streak_freeze_used_today = Column(Boolean, default=False)
    day3_email_sent_at = Column(DateTime, nullable=True)
    day7_email_sent_at = Column(DateTime, nullable=True)
    ctf_solves = Column(Integer, default=0)
    ctf_last_solved_date = Column(Date, nullable=True)
    referral_code = Column(String, unique=True, nullable=True)
    referred_by_id = Column(Integer, nullable=True)
    bonus_interviews = Column(Integer, default=0)
    bonus_resumes = Column(Integer, default=0)

class MentorMessage(Base):
    """Rolling conversation history the AI Mentor uses as short-term memory."""
    __tablename__ = "mentor_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False)  # "user" | "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=now)

    user = relationship("User", back_populates="mentor_messages")


class DailyBundle(Base):
    """One row per user per day: lesson, quiz, news, challenge, interview Q, task."""
    __tablename__ = "daily_bundles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(String, nullable=False)  # YYYY-MM-DD
    content = Column(JSON, nullable=False)  # {lesson, quiz, news, challenge, interview_question, task}
    created_at = Column(DateTime, default=now)
    emailed_at = Column(DateTime, nullable=True)


class ResumeReview(Base):
    __tablename__ = "resume_reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_text = Column(Text, nullable=False)
    review = Column(JSON, nullable=False)  # {score, strengths, gaps, ats_issues, rewritten_bullets}
    created_at = Column(DateTime, default=now)


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False)  # e.g. "SOC Analyst"
    status = Column(String, default="active")  # active | completed
    created_at = Column(DateTime, default=now)

    turns = relationship("InterviewTurn", back_populates="session", cascade="all, delete-orphan")

    overall_score = Column(Integer, nullable=True)
    nudge_sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    max_turns = Column(Integer, default=6)

class InterviewTurn(Base):
    __tablename__ = "interview_turns"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    speaker = Column(String, nullable=False)  # "interviewer" | "candidate"
    content = Column(Text, nullable=False)
    feedback = Column(JSON, nullable=True)  # set on candidate turns: {strengths, improvements, score}
    created_at = Column(DateTime, default=now)

    session = relationship("InterviewSession", back_populates="turns")

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)  # 'certification', 'interview', 'hired'
    title = Column(String, nullable=False) # 'Security+', 'SOC Analyst at Dell'
    date_achieved = Column(String, default=dt.date.today().isoformat())



class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    sid = Column(String, nullable=True)
    name = Column(String, index=True)
    path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class LabLog(Base):
    __tablename__ = "lab_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    lab_id = Column(String)
    notes = Column(Text, nullable=True)
    artifacts = Column(Text, nullable=True)
    completed_at = Column(DateTime, default=datetime.utcnow)


class Story(Base):
    __tablename__ = "stories"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    title = Column(String)
    source = Column(String, nullable=True)
    s = Column(Text)
    t = Column(Text, nullable=True)
    a = Column(Text)
    r = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class CtfSolve(Base):
    __tablename__ = "ctf_solves"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    solve_date = Column(String)
    xp = Column(Integer, default=0)
