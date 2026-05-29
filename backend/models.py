from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False)
    subject = Column(String(200), nullable=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(10), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    tags = Column(String(500), nullable=True)   # comma-separated
    features = Column(Text, nullable=True)       # newline-separated
    color_class = Column(String(10), default="p1")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False)  # Frontend / Backend / Databases & Tools
    name = Column(String(100), nullable=False)
    pill_class = Column(String(20), default="")     # fe / be / db


class Experience(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True, index=True)
    position = Column(String(200), nullable=False)
    company = Column(String(200), nullable=False)
    period = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    details = Column(Text, nullable=True) # newline-separated
