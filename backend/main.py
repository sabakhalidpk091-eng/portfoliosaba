from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from config import settings
from database import engine, Base, get_db
from models import ContactMessage, Project, Skill, Experience
from schemas import ContactCreate, ContactResponse, ProjectResponse, SkillResponse, ExperienceResponse

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Saba Portfolio API",
    description="FastAPI backend for Saba's developer portfolio",
    version="1.0.0",
)

# ── CORS ───────────────────────────────────────────────────────────────────────
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ─────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"message": "Saba Portfolio API is running 🚀"}


# ── Contact ────────────────────────────────────────────────────────────────────
@app.post("/api/contact", response_model=ContactResponse, tags=["Contact"])
def send_message(payload: ContactCreate, db: Session = Depends(get_db)):
    """Save a contact form submission to SQL Server."""
    msg = ContactMessage(**payload.model_dump())
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


@app.get("/api/contact", response_model=List[ContactResponse], tags=["Contact"])
def list_messages(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List all contact messages (admin use)."""
    return db.query(ContactMessage).offset(skip).limit(limit).all()


# ── Projects ───────────────────────────────────────────────────────────────────
@app.get("/api/projects", response_model=List[ProjectResponse], tags=["Projects"])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

@app.post("/api/projects", response_model=ProjectResponse, tags=["Projects"])
def create_project(payload: ProjectResponse, db: Session = Depends(get_db)):
    # Simple creation for dashboard (omitting id from payload if needed, 
    # but here we'll assume a schema update or just manual mapping)
    data = payload.model_dump(exclude={"id"})
    proj = Project(**data)
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj

@app.delete("/api/projects/{item_id}", tags=["Projects"])
def delete_project(item_id: int, db: Session = Depends(get_db)):
    db.query(Project).filter(Project.id == item_id).delete()
    db.commit()
    return {"status": "deleted"}

@app.put("/api/projects/{item_id}", response_model=ProjectResponse, tags=["Projects"])
def update_project(item_id: int, payload: ProjectResponse, db: Session = Depends(get_db)):
    proj = db.query(Project).filter(Project.id == item_id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    
    data = payload.model_dump(exclude={"id"})
    for key, value in data.items():
        setattr(proj, key, value)
    
    db.commit()
    db.refresh(proj)
    return proj


# ── Skills ──────────────────────────────────────────────────────────────────────
@app.get("/api/skills", response_model=List[SkillResponse], tags=["Skills"])
def list_skills(db: Session = Depends(get_db)):
    return db.query(Skill).all()

@app.post("/api/skills", response_model=SkillResponse, tags=["Skills"])
def create_skill(payload: SkillResponse, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude={"id"})
    skill = Skill(**data)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill

@app.delete("/api/skills/{item_id}", tags=["Skills"])
def delete_skill(item_id: int, db: Session = Depends(get_db)):
    db.query(Skill).filter(Skill.id == item_id).delete()
    db.commit()
    return {"status": "deleted"}

@app.put("/api/skills/{item_id}", response_model=SkillResponse, tags=["Skills"])
def update_skill(item_id: int, payload: SkillResponse, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == item_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    data = payload.model_dump(exclude={"id"})
    for key, value in data.items():
        setattr(skill, key, value)
    
    db.commit()
    db.refresh(skill)
    return skill


# ── Experience ─────────────────────────────────────────────────────────────────
@app.get("/api/experience", response_model=List[ExperienceResponse], tags=["Experience"])
def list_experience(db: Session = Depends(get_db)):
    return db.query(Experience).all()

@app.post("/api/experience", response_model=ExperienceResponse, tags=["Experience"])
def create_experience(payload: ExperienceResponse, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude={"id"})
    exp = Experience(**data)
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

@app.delete("/api/experience/{item_id}", tags=["Experience"])
def delete_experience(item_id: int, db: Session = Depends(get_db)):
    db.query(Experience).filter(Experience.id == item_id).delete()
    db.commit()
    return {"status": "deleted"}

@app.put("/api/experience/{item_id}", response_model=ExperienceResponse, tags=["Experience"])
def update_experience(item_id: int, payload: ExperienceResponse, db: Session = Depends(get_db)):
    exp = db.query(Experience).filter(Experience.id == item_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    data = payload.model_dump(exclude={"id"})
    for key, value in data.items():
        setattr(exp, key, value)
    
    db.commit()
    db.refresh(exp)
    return exp
