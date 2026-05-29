from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ── Contact ────────────────────────────────────────────────────────────────────

class ContactCreate(BaseModel):
    name: str
    email: str
    subject: Optional[str] = None
    message: str


class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    subject: Optional[str]
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Project ────────────────────────────────────────────────────────────────────

class ProjectResponse(BaseModel):
    id: int
    number: str
    title: str
    description: str
    tags: Optional[str]
    features: Optional[str]
    color_class: str

    class Config:
        from_attributes = True


# ── Skill ──────────────────────────────────────────────────────────────────────

class SkillResponse(BaseModel):
    id: int
    category: str
    name: str
    pill_class: str

    class Config:
        from_attributes = True


# ── Experience ─────────────────────────────────────────────────────────────────

class ExperienceResponse(BaseModel):
    id: int
    position: str
    company: str
    period: str
    description: str
    details: Optional[str]

    class Config:
        from_attributes = True
