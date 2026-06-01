from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
import os
from supabase import create_client
from config import settings

def get_db():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    if not url or not key: return None
    try: return create_client(url, key)
    except: return None

app = FastAPI(
    title="Saba Portfolio API (Supabase)",
    description="FastAPI backend for Saba's developer portfolio (Supabase)",
    version="2.0.0",
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
def root():
    return {"message": "Saba Portfolio API on Supabase is running 🚀"}

@app.get("/api/test", tags=["Health"])
def test_api():
    return {"status": "Success", "message": "Backend is working perfectly without DB!"}


# ── Contact ───────────────────────────────────────────────────────────────────
@app.post("/api/contact", tags=["Contact"])
def send_message(payload: dict = Body(...)):
    db = get_db()
    try:
        payload["created_at"] = datetime.now().isoformat()
        payload.pop("_id", None)
        response = db.table("contacts").insert(payload).execute()
        if hasattr(response, "data") and response.data:
            return response.data[0]
        return {"error": "No data returned from Supabase", "details": str(response)}
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")


@app.get("/api/contact", response_model=List[dict], tags=["Contact"])
def list_messages(skip: int = 0, limit: int = 50):
    db = get_db()
    try:
        response = db.table("contacts").select("*").execute()
        items = response.data or []
        return items[skip: skip + limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Projects ──────────────────────────────────────────────────────────────────
@app.get("/api/projects", response_model=List[dict], tags=["Projects"])
def list_projects():
    db = get_db()
    # Mock data fallback as requested for testing
    mock_projects = [
        {"id": "1", "title": "Saba Portfolio", "description": "Full-stack conversion to FastAPI + Supabase", "tech_stack": ["React", "FastAPI", "Supabase"]},
        {"id": "2", "title": "Admin Dashboard", "description": "Real-time management system", "tech_stack": ["React", "CSS Modules"]}
    ]
    
    if db is None:
        return mock_projects
        
    try:
        response = db.table("projects").select("*").execute()
        return response.data if response.data else mock_projects
    except Exception:
        return mock_projects


@app.post("/api/projects", tags=["Projects"])
def create_project(payload: dict = Body(...)):
    db = get_db()
    try:
        payload.pop("_id", None)
        response = db.table("projects").insert(payload).execute()
        return response.data[0] if response and getattr(response, "data", None) else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/projects/{item_id}", tags=["Projects"])
def delete_project(item_id: str):
    db = get_db()
    try:
        db.table("projects").delete().eq("id", item_id).execute()
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/projects/{item_id}", tags=["Projects"])
def update_project(item_id: str, payload: dict = Body(...)):
    db = get_db()
    try:
        payload.pop("id", None)
        payload.pop("_id", None)
        response = db.table("projects").update(payload).eq("id", item_id).execute()
        return response.data[0] if response and getattr(response, "data", None) else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Skills ────────────────────────────────────────────────────────────────────
@app.get("/api/skills", response_model=List[dict], tags=["Skills"])
def list_skills():
    db = get_db()
    try:
        response = db.table("skills").select("*").execute()
        return response.data or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/skills", tags=["Skills"])
def create_skill(payload: dict = Body(...)):
    db = get_db()
    try:
        payload.pop("_id", None)
        response = db.table("skills").insert(payload).execute()
        return response.data[0] if response and getattr(response, "data", None) else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/skills/{item_id}", tags=["Skills"])
def delete_skill(item_id: str):
    db = get_db()
    try:
        db.table("skills").delete().eq("id", item_id).execute()
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/skills/{item_id}", tags=["Skills"])
def update_skill(item_id: str, payload: dict = Body(...)):
    db = get_db()
    try:
        payload.pop("id", None)
        payload.pop("_id", None)
        response = db.table("skills").update(payload).eq("id", item_id).execute()
        return response.data[0] if response and getattr(response, "data", None) else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Experience ────────────────────────────────────────────────────────────────
@app.get("/api/experience", response_model=List[dict], tags=["Experience"])
def list_experience():
    db = get_db()
    try:
        response = db.table("experience").select("*").execute()
        return response.data or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/experience", tags=["Experience"])
def create_experience(payload: dict = Body(...)):
    db = get_db()
    try:
        payload.pop("_id", None)
        response = db.table("experience").insert(payload).execute()
        return response.data[0] if response and getattr(response, "data", None) else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/experience/{item_id}", tags=["Experience"])
def delete_experience(item_id: str):
    db = get_db()
    try:
        db.table("experience").delete().eq("id", item_id).execute()
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/experience/{item_id}", tags=["Experience"])
def update_experience(item_id: str, payload: dict = Body(...)):
    db = get_db()
    try:
        payload.pop("id", None)
        payload.pop("_id", None)
        response = db.table("experience").update(payload).eq("id", item_id).execute()
        return response.data[0] if response and getattr(response, "data", None) else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
