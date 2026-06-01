from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
import os

def get_db():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    if not url or not key:
        return None
    try:
        from supabase import create_client
        return create_client(url, key)
    except Exception:
        return None

app = FastAPI(
    title="Saba Portfolio API",
    description="FastAPI backend for Saba's developer portfolio",
    version="2.0.0",
)

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Mock Data ─────────────────────────────────────────────────────────────────
MOCK_PROJECTS = [
    {
        "id": "1",
        "title": "Saba Portfolio",
        "description": "Full-stack portfolio built with React and FastAPI, deployed on Vercel.",
        "tags": "React, FastAPI, Supabase, Tailwind CSS",
        "link": "https://portfoliosabakhalid-9sls.vercel.app"
    },
    {
        "id": "2",
        "title": "Admin Dashboard",
        "description": "Real-time content management system for portfolio data.",
        "tags": "React, FastAPI, Python",
        "link": "#"
    },
    {
        "id": "3",
        "title": "Full Stack Web App",
        "description": "Modern web application with authentication and database integration.",
        "tags": "React, Node.js, PostgreSQL",
        "link": "#"
    }
]

MOCK_SKILLS = [
    {"id": "1", "name": "React", "category": "Frontend"},
    {"id": "2", "name": "Tailwind CSS", "category": "Frontend"},
    {"id": "3", "name": "JavaScript", "category": "Frontend"},
    {"id": "4", "name": "HTML & CSS", "category": "Frontend"},
    {"id": "5", "name": "Python", "category": "Backend"},
    {"id": "6", "name": "FastAPI", "category": "Backend"},
    {"id": "7", "name": "REST APIs", "category": "Backend"},
    {"id": "8", "name": "Supabase", "category": "Database"},
    {"id": "9", "name": "PostgreSQL", "category": "Database"},
    {"id": "10", "name": "Git & GitHub", "category": "Tools"},
    {"id": "11", "name": "Vercel", "category": "Tools"},
]

MOCK_EXPERIENCE = [
    {
        "id": "1",
        "position": "Full Stack Developer",
        "company": "Freelance",
        "period": "2024 - Present",
        "description": "Building modern web applications using React and FastAPI. Delivering complete end-to-end solutions for clients."
    },
    {
        "id": "2",
        "position": "Frontend Developer Intern",
        "company": "Tech Startup",
        "period": "2023 - 2024",
        "description": "Developed responsive UI components using React and Tailwind CSS. Collaborated with backend team on API integration."
    }
]

# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"message": "Saba Portfolio API is running!"}

@app.get("/api/test", tags=["Health"])
def test_api():
    db = get_db()
    return {"status": "OK", "db_connected": db is not None}


# ── Projects ──────────────────────────────────────────────────────────────────
@app.get("/api/projects", response_model=List[dict], tags=["Projects"])
def list_projects():
    db = get_db()
    if db is None:
        return MOCK_PROJECTS
    try:
        response = db.table("projects").select("*").execute()
        return response.data if response.data else MOCK_PROJECTS
    except Exception:
        return MOCK_PROJECTS


@app.post("/api/projects", tags=["Projects"])
def create_project(payload: dict = Body(...)):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    try:
        payload.pop("id", None)
        payload.pop("_id", None)
        response = db.table("projects").insert(payload).execute()
        return response.data[0] if response and getattr(response, "data", None) else payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/projects/{item_id}", tags=["Projects"])
def update_project(item_id: str, payload: dict = Body(...)):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    try:
        payload.pop("id", None)
        payload.pop("_id", None)
        response = db.table("projects").update(payload).eq("id", item_id).execute()
        return response.data[0] if response and getattr(response, "data", None) else payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/projects/{item_id}", tags=["Projects"])
def delete_project(item_id: str):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    try:
        db.table("projects").delete().eq("id", item_id).execute()
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Skills ────────────────────────────────────────────────────────────────────
@app.get("/api/skills", response_model=List[dict], tags=["Skills"])
def list_skills():
    db = get_db()
    if db is None:
        return MOCK_SKILLS
    try:
        response = db.table("skills").select("*").execute()
        return response.data if response.data else MOCK_SKILLS
    except Exception:
        return MOCK_SKILLS


@app.post("/api/skills", tags=["Skills"])
def create_skill(payload: dict = Body(...)):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    try:
        payload.pop("id", None)
        payload.pop("_id", None)
        response = db.table("skills").insert(payload).execute()
        return response.data[0] if response and getattr(response, "data", None) else payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/skills/{item_id}", tags=["Skills"])
def update_skill(item_id: str, payload: dict = Body(...)):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    try:
        payload.pop("id", None)
        payload.pop("_id", None)
        response = db.table("skills").update(payload).eq("id", item_id).execute()
        return response.data[0] if response and getattr(response, "data", None) else payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/skills/{item_id}", tags=["Skills"])
def delete_skill(item_id: str):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    try:
        db.table("skills").delete().eq("id", item_id).execute()
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Experience ────────────────────────────────────────────────────────────────
@app.get("/api/experience", response_model=List[dict], tags=["Experience"])
def list_experience():
    db = get_db()
    if db is None:
        return MOCK_EXPERIENCE
    try:
        response = db.table("experience").select("*").execute()
        return response.data if response.data else MOCK_EXPERIENCE
    except Exception:
        return MOCK_EXPERIENCE


@app.post("/api/experience", tags=["Experience"])
def create_experience(payload: dict = Body(...)):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    try:
        payload.pop("id", None)
        payload.pop("_id", None)
        response = db.table("experience").insert(payload).execute()
        return response.data[0] if response and getattr(response, "data", None) else payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/experience/{item_id}", tags=["Experience"])
def update_experience(item_id: str, payload: dict = Body(...)):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    try:
        payload.pop("id", None)
        payload.pop("_id", None)
        response = db.table("experience").update(payload).eq("id", item_id).execute()
        return response.data[0] if response and getattr(response, "data", None) else payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/experience/{item_id}", tags=["Experience"])
def delete_experience(item_id: str):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    try:
        db.table("experience").delete().eq("id", item_id).execute()
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Contact ───────────────────────────────────────────────────────────────────
@app.get("/api/contact", response_model=List[dict], tags=["Contact"])
def list_messages():
    db = get_db()
    if db is None:
        return []
    try:
        response = db.table("contacts").select("*").execute()
        return response.data or []
    except Exception:
        return []


@app.post("/api/contact", tags=["Contact"])
def send_message(payload: dict = Body(...)):
    db = get_db()
    if db is None:
        return {"status": "Message received (DB not connected)"}
    try:
        payload["created_at"] = datetime.now().isoformat()
        payload.pop("_id", None)
        response = db.table("contacts").insert(payload).execute()
        return response.data[0] if response.data else {"status": "saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
