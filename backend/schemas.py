from pydantic import BaseModel
from typing import Optional

# ── Contact ────────────────────────────────────────────────────────────────────
class ContactCreate(BaseModel):
    name: str
    email: str
    subject: Optional[str] = None
    message: str

# ── Project ────────────────────────────────────────────────────────────────────
class ProjectCreate(BaseModel):
    number: str
    title: str
    description: str
    tags: Optional[str] = None
    features: Optional[str] = None
    color_class: str = "p1"
    link: Optional[str] = None

# ── Skill ──────────────────────────────────────────────────────────────────────
class SkillCreate(BaseModel):
    category: str
    name: str
    pill_class: str = "fe"

# ── Experience ─────────────────────────────────────────────────────────────────
class ExperienceCreate(BaseModel):
    position: str
    company: str
    period: str
    description: str
    details: Optional[str] = None
