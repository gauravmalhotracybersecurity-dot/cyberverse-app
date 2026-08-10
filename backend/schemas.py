from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# ---------- Auth ----------

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = ""


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8)


class MessageResponse(BaseModel):
    message: str


# ---------- Profile ----------

class ProfileUpdate(BaseModel):
    skill_level: Optional[str] = None
    certifications: Optional[list[str]] = None
    weak_topics: Optional[list[str]] = None
    learning_goals: Optional[str] = None
    full_name: Optional[str] = None


class ProfileResponse(BaseModel):
    id: int
    email: str
    full_name: str
    skill_level: str
    certifications: list[str]
    weak_topics: list[str]
    learning_goals: str
    xp: int
    streak_days: int
    is_pro: bool

    class Config:
        from_attributes = True


# ---------- Mentor chat ----------

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ChatMessageOut(BaseModel):
    role: str
    content: str

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    reply: str
    history: list[ChatMessageOut]


# ---------- Daily learning ----------

class DailyBundleResponse(BaseModel):
    date: str
    content: dict


# ---------- Resume ----------

class ResumeReviewRequest(BaseModel):
    resume_text: str = Field(min_length=50)
    target_role: str = "SOC Analyst"


class ResumeReviewResponse(BaseModel):
    id: int
    review: dict
    created_at: str


# ---------- Interview coach ----------

class InterviewStartRequest(BaseModel):
    role: str = "SOC Analyst"


class InterviewTurnOut(BaseModel):
    speaker: str
    content: str
    feedback: Optional[dict] = None

    class Config:
        from_attributes = True


class InterviewStartResponse(BaseModel):
    session_id: int
    role: str
    turns: list[InterviewTurnOut]


class InterviewRespondRequest(BaseModel):
    answer: str = Field(min_length=1)


class InterviewRespondResponse(BaseModel):
    session_id: int
    turns: list[InterviewTurnOut]
    is_complete: bool
    overall_score: int | None = None
    verdict: str | None = None
    role: str | None = None
