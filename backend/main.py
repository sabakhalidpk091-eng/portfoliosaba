from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
from bson import ObjectId
from contextlib import asynccontextmanager

from config import settings
from database import connect_to_mongo, close_mongo_connection, get_db

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
def serialize_doc(doc):
    if not doc:
        return None
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

def serialize_list(docs) -> list:
    return [serialize_doc(d) for d in docs if d]


# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {"message": "Saba Portfolio API on MongoDB is running 🚀"}


# ── Contact ───────────────────────────────────────────────────────────────────
@app.post("/api/contact", tags=["Contact"])
async def send_message(payload: dict = Body(...), db=Depends(get_db)):
    payload["created_at"] = datetime.now().isoformat()
    payload.pop("_id", None)
    result = await db["contacts"].insert_one(payload)
    payload["id"] = str(result.inserted_id)
    payload.pop("_id", None)
    return payload

@app.get("/api/contact", response_model=List[dict], tags=["Contact"])
async def list_messages(skip: int = 0, limit: int = 50, db=Depends(get_db)):
    try:
        cursor = db["contacts"].find().skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        return serialize_list(docs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Projects ──────────────────────────────────────────────────────────────────
@app.get("/api/projects", response_model=List[dict], tags=["Projects"])
async def list_projects(db=Depends(get_db)):
    try:
        cursor = db["projects"].find()
        projects = await cursor.to_list(length=100)
        return [serialize_doc(p) for p in projects]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/projects", tags=["Projects"])
async def create_project(payload: dict = Body(...), db=Depends(get_db)):
    payload.pop("_id", None)
    result = await db["projects"].insert_one(payload)
    payload["id"] = str(result.inserted_id)
    payload.pop("_id", None)
    return payload

@app.delete("/api/projects/{item_id}", tags=["Projects"])
async def delete_project(item_id: str, db=Depends(get_db)):
    await db["projects"].delete_one({"_id": ObjectId(item_id)})
    return {"status": "deleted"}

@app.put("/api/projects/{item_id}", tags=["Projects"])
async def update_project(item_id: str, payload: dict = Body(...), db=Depends(get_db)):
    payload.pop("id", None)
    payload.pop("_id", None)
    await db["projects"].update_one({"_id": ObjectId(item_id)}, {"$set": payload})
    payload["id"] = item_id
    return payload


# ── Skills ────────────────────────────────────────────────────────────────────
@app.get("/api/skills", response_model=List[dict], tags=["Skills"])
async def list_skills(db=Depends(get_db)):
    try:
        cursor = db["skills"].find()
        skills = await cursor.to_list(length=100)
        return [serialize_doc(s) for s in skills]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/skills", tags=["Skills"])
async def create_skill(payload: dict = Body(...), db=Depends(get_db)):
    payload.pop("_id", None)
    result = await db["skills"].insert_one(payload)
    payload["id"] = str(result.inserted_id)
    payload.pop("_id", None)
    return payload

@app.delete("/api/skills/{item_id}", tags=["Skills"])
async def delete_skill(item_id: str, db=Depends(get_db)):
    await db["skills"].delete_one({"_id": ObjectId(item_id)})
    return {"status": "deleted"}

@app.put("/api/skills/{item_id}", tags=["Skills"])
async def update_skill(item_id: str, payload: dict = Body(...), db=Depends(get_db)):
    payload.pop("id", None)
    payload.pop("_id", None)
    await db["skills"].update_one({"_id": ObjectId(item_id)}, {"$set": payload})
    payload["id"] = item_id
    return payload


# ── Experience ────────────────────────────────────────────────────────────────
@app.get("/api/experience", response_model=List[dict], tags=["Experience"])
async def list_experience(db=Depends(get_db)):
    try:
        cursor = db["experience"].find()
        experience = await cursor.to_list(length=100)
        return [serialize_doc(e) for e in experience]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/experience", tags=["Experience"])
async def create_experience(payload: dict = Body(...), db=Depends(get_db)):
    payload.pop("_id", None)
    result = await db["experience"].insert_one(payload)
    payload["id"] = str(result.inserted_id)
    payload.pop("_id", None)
    return payload

@app.delete("/api/experience/{item_id}", tags=["Experience"])
async def delete_experience(item_id: str, db=Depends(get_db)):
    await db["experience"].delete_one({"_id": ObjectId(item_id)})
    return {"status": "deleted"}

@app.put("/api/experience/{item_id}", tags=["Experience"])
async def update_experience(item_id: str, payload: dict = Body(...), db=Depends(get_db)):
    payload.pop("id", None)
    payload.pop("_id", None)
    await db["experience"].update_one({"_id": ObjectId(item_id)}, {"$set": payload})
    payload["id"] = item_id
    return payload
