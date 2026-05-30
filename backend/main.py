from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from contextlib import asynccontextmanager

from config import settings
from database import connect_to_mongo, close_mongo_connection, get_db
from schemas import (
    ContactCreate, ContactResponse, 
    ProjectResponse, SkillResponse, ExperienceResponse
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB
    await connect_to_mongo()
    yield
    # Shutdown: Close connection
    await close_mongo_connection()

app = FastAPI(
    title="Saba Portfolio API (MongoDB)",
    description="FastAPI backend for Saba's developer portfolio",
    version="2.0.0",
    lifespan=lifespan
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

# ── Helper ───────────────────────────────────────────────────────────────────
def serialize_doc(doc):
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

# ── Health ─────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {"message": "Saba Portfolio API on MongoDB is running 🚀"}


# ── Contact ────────────────────────────────────────────────────────────────────
@app.post("/api/contact", response_model=ContactResponse, tags=["Contact"])
async def send_message(payload: ContactCreate, db=Depends(get_db)):
    msg_dict = payload.model_dump()
    msg_dict["created_at"] = datetime.now()
    result = await db["contacts"].insert_one(msg_dict)
    msg_dict["_id"] = result.inserted_id
    return serialize_doc(msg_dict)

@app.get("/api/contact", response_model=List[ContactResponse], tags=["Contact"])
async def list_messages(skip: int = 0, limit: int = 50, db=Depends(get_db)):
    cursor = db["contacts"].find().skip(skip).limit(limit)
    messages = await cursor.to_list(length=limit)
    return [serialize_doc(m) for m in messages]


# ── Projects ───────────────────────────────────────────────────────────────────
@app.get("/api/projects", response_model=List[ProjectResponse], tags=["Projects"])
async def list_projects(db=Depends(get_db)):
    cursor = db["projects"].find()
    projects = await cursor.to_list(length=100)
    return [serialize_doc(p) for p in projects]

@app.post("/api/projects", response_model=ProjectResponse, tags=["Projects"])
async def create_project(payload: ProjectResponse, db=Depends(get_db)):
    data = payload.model_dump(exclude={"id"})
    result = await db["projects"].insert_one(data)
    data["_id"] = result.inserted_id
    return serialize_doc(data)

@app.delete("/api/projects/{item_id}", tags=["Projects"])
async def delete_project(item_id: str, db=Depends(get_db)):
    await db["projects"].delete_one({"_id": ObjectId(item_id)})
    return {"status": "deleted"}

@app.put("/api/projects/{item_id}", response_model=ProjectResponse, tags=["Projects"])
async def update_project(item_id: str, payload: ProjectResponse, db=Depends(get_db)):
    data = payload.model_dump(exclude={"id"})
    await db["projects"].update_one({"_id": ObjectId(item_id)}, {"$set": data})
    data["_id"] = ObjectId(item_id)
    return serialize_doc(data)


# ── Skills ──────────────────────────────────────────────────────────────────────
@app.get("/api/skills", response_model=List[SkillResponse], tags=["Skills"])
async def list_skills(db=Depends(get_db)):
    cursor = db["skills"].find()
    skills = await cursor.to_list(length=100)
    return [serialize_doc(s) for s in skills]

@app.post("/api/skills", response_model=SkillResponse, tags=["Skills"])
async def create_skill(payload: SkillResponse, db=Depends(get_db)):
    data = payload.model_dump(exclude={"id"})
    result = await db["skills"].insert_one(data)
    data["_id"] = result.inserted_id
    return serialize_doc(data)

@app.delete("/api/skills/{item_id}", tags=["Skills"])
async def delete_skill(item_id: str, db=Depends(get_db)):
    await db["skills"].delete_one({"_id": ObjectId(item_id)})
    return {"status": "deleted"}

@app.put("/api/skills/{item_id}", response_model=SkillResponse, tags=["Skills"])
async def update_skill(item_id: str, payload: SkillResponse, db=Depends(get_db)):
    data = payload.model_dump(exclude={"id"})
    await db["skills"].update_one({"_id": ObjectId(item_id)}, {"$set": data})
    data["_id"] = ObjectId(item_id)
    return serialize_doc(data)


# ── Experience ─────────────────────────────────────────────────────────────────
@app.get("/api/experience", response_model=List[ExperienceResponse], tags=["Experience"])
async def list_experience(db=Depends(get_db)):
    cursor = db["experience"].find()
    experience = await cursor.to_list(length=100)
    return [serialize_doc(e) for e in experience]

@app.post("/api/experience", response_model=ExperienceResponse, tags=["Experience"])
async def create_experience(payload: ExperienceResponse, db=Depends(get_db)):
    data = payload.model_dump(exclude={"id"})
    result = await db["experience"].insert_one(data)
    data["_id"] = result.inserted_id
    return serialize_doc(data)

@app.delete("/api/experience/{item_id}", tags=["Experience"])
async def delete_experience(item_id: str, db=Depends(get_db)):
    await db["experience"].delete_one({"_id": ObjectId(item_id)})
    return {"status": "deleted"}

@app.put("/api/experience/{item_id}", response_model=ExperienceResponse, tags=["Experience"])
async def update_experience(item_id: str, payload: ExperienceResponse, db=Depends(get_db)):
    data = payload.model_dump(exclude={"id"})
    await db["experience"].update_one({"_id": ObjectId(item_id)}, {"$set": data})
    data["_id"] = ObjectId(item_id)
    return serialize_doc(data)
