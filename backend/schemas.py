from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

# Helper to handle MongoDB ObjectId as a string
class MongoBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

# ── Contact ────────────────────────────────────────────────────────────────────

class ContactCreate(BaseModel):
    name: str
    email: str
    subject: Optional[str] = None
    message: str

class ContactResponse(MongoBaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    email: str
    subject: Optional[str] = None
    message: str
    created_at: datetime = Field(default_factory=datetime.now)

# ── Project ────────────────────────────────────────────────────────────────────

class ProjectResponse(MongoBaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    number: str
    title: str
    description: str
    tags: Optional[str] = None
    features: Optional[str] = None
    color_class: str

# ── Skill ──────────────────────────────────────────────────────────────────────

class SkillResponse(MongoBaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    category: str
    name: str
    pill_class: str

# ── Experience ─────────────────────────────────────────────────────────────────

class ExperienceResponse(MongoBaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    position: str
    company: str
    period: str
    description: str
    details: Optional[str] = None
