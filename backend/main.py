from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime
from bson import ObjectId
from contextlib import asynccontextmanager
import json

from config import settings
from database import connect_to_mongo, close_mongo_connection, get_db
from schemas import ContactCreate, ProjectCreate, SkillCreate, ExperienceCreate

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
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

# ── Helper ────────────────────────────────────────────────────────────────────
def serialize(doc) -> dict:
    """Convert MongoDB document to JSON-serializable dict."""
    if doc is None:
        return {}
    doc["id"] = str(doc.pop("_id"))
    return doc

def serialize_list(docs) -> list:
    return [serialize(d) for d in docs]


# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {"message": "Saba Portfolio API on MongoDB is running 🚀"}


# ── Contact ───────────────────────────────────────────────────────────────────
@app.post("/api/contact", tags=["Contact"])
async def send_message(payload: ContactCreate, db=Depends(get_db)):
    data = payload.model_dump()
    data["created_at"] = datetime.now().isoformat()
    result = await db["contacts"].insert_one(data)
    data["id"] = str(result.inserted_id)
    data.pop("_id", None)
    return data

@app.get("/api/contact", tags=["Contact"])
async def list_messages(skip: int = 0, limit: int = 50, db=Depends(get_db)):
    docs = await db["contacts"].find().skip(skip).limit(limit).to_list(length=limit)
    return serialize_list(docs)


# ── Projects ──────────────────────────────────────────────────────────────────
@app.get("/api/projects", tags=["Projects"])
async def list_projects(db=Depends(get_db)):
    docs = await db["projects"].find().to_list(length=100)
    return serialize_list(docs)

@app.post("/api/projects", tags=["Projects"])
async def create_project(payload: ProjectCreate, db=Depends(get_db)):
    data = payload.model_dump()
    result = await db["projects"].insert_one(data)
    data["id"] = str(result.inserted_id)
    data.pop("_id", None)
    return data

@app.delete("/api/projects/{item_id}", tags=["Projects"])
async def delete_project(item_id: str, db=Depends(get_db)):
    await db["projects"].delete_one({"_id": ObjectId(item_id)})
    return {"status": "deleted"}

@app.put("/api/projects/{item_id}", tags=["Projects"])
async def update_project(item_id: str, payload: ProjectCreate, db=Depends(get_db)):
    data = payload.model_dump()
    await db["projects"].update_one({"_id": ObjectId(item_id)}, {"$set": data})
    data["id"] = item_id
    return data


# ── Skills ────────────────────────────────────────────────────────────────────
@app.get("/api/skills", tags=["Skills"])
async def list_skills(db=Depends(get_db)):
    docs = await db["skills"].find().to_list(length=100)
    return serialize_list(docs)

@app.post("/api/skills", tags=["Skills"])
async def create_skill(payload: SkillCreate, db=Depends(get_db)):
    data = payload.model_dump()
    result = await db["skills"].insert_one(data)
    data["id"] = str(result.inserted_id)
    data.pop("_id", None)
    return data

@app.delete("/api/skills/{item_id}", tags=["Skills"])
async def delete_skill(item_id: str, db=Depends(get_db)):
    await db["skills"].delete_one({"_id": ObjectId(item_id)})
    return {"status": "deleted"}

@app.put("/api/skills/{item_id}", tags=["Skills"])
async def update_skill(item_id: str, payload: SkillCreate, db=Depends(get_db)):
    data = payload.model_dump()
    await db["skills"].update_one({"_id": ObjectId(item_id)}, {"$set": data})
    data["id"] = item_id
    return data


# ── Experience ────────────────────────────────────────────────────────────────
@app.get("/api/experience", tags=["Experience"])
async def list_experience(db=Depends(get_db)):
    docs = await db["experience"].find().to_list(length=100)
    return serialize_list(docs)

@app.post("/api/experience", tags=["Experience"])
async def create_experience(payload: ExperienceCreate, db=Depends(get_db)):
    data = payload.model_dump()
    result = await db["experience"].insert_one(data)
    data["id"] = str(result.inserted_id)
    data.pop("_id", None)
    return data

@app.delete("/api/experience/{item_id}", tags=["Experience"])
async def delete_experience(item_id: str, db=Depends(get_db)):
    await db["experience"].delete_one({"_id": ObjectId(item_id)})
    return {"status": "deleted"}

@app.put("/api/experience/{item_id}", tags=["Experience"])
async def update_experience(item_id: str, payload: ExperienceCreate, db=Depends(get_db)):
    data = payload.model_dump()
    await db["experience"].update_one({"_id": ObjectId(item_id)}, {"$set": data})
    data["id"] = item_id
    return data
