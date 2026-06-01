# Saba Portfolio
Updated: 2026-06-01
 - Full Stack Conversion

This project has been converted from a static Next.js setup to a modern Full Stack architecture.

## Architecture
- **Frontend**: React.js (Vite) with Vanilla CSS (Premium Aesthetics).
- **Backend**: FastAPI (Python) for high-performance REST APIs.
- **Database**: Microsoft SQL Server (SSMS) integration via SQLAlchemy.

---

## Getting Started

### 1. Backend Setup (FastAPI)
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Update `.env` with your SQL Server connection string.
4. Seed the database with initial data:
   ```bash
   python seed.py
   ```
5. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

### 2. Frontend Setup (React)
1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

---

## Key Features
- **Dynamic Projects**: Projects are fetched from SQL Server.
- **Skill Management**: Skills are grouped and rendered from the DB.
- **Functional Contact Form**: Messages are saved directly to the `contact_messages` table in SQL Server.
- **Premium UI**: Maintains the glassmorphism and micro-animations from the original design.
