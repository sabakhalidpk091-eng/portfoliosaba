"""
Run once to seed the SQL Server database with initial portfolio data.
Usage:  python seed.py
"""

from database import SessionLocal, engine, Base
from models import Project, Skill, Experience, ContactMessage

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Clear existing seed data (safe to re-run)
db.query(Project).delete()
db.query(Skill).delete()
db.query(Experience).delete()

# NOTE: We do NOT clear ContactMessage — we want to keep real messages!
db.commit()

# ── Projects ────────────────────────────────────────────────────────────────────
projects = [
    Project(
        number="Project 01",
        title="Career Counselling Platform",
        description=(
            "An intelligent web platform helping students and professionals "
            "navigate their career journey with personalized guidance and resources."
        ),
        tags="React,FastAPI,sql,Tailwind",
        features=(
            "Career assessment quiz & personality matching\n"
            "Personalized career roadmap generator\n"
            "Resource library with courses & job links\n"
            "Mentor booking & consultation system\n"
            "Progress tracker dashboard"
        ),
        color_class="p1",
    ),

    Project(
        number="Project 02",
        title="HRM Management System",
        description=(
            "A comprehensive Human Resource Management system to streamline "
            "employee lifecycle, payroll, attendance, and performance management."
        ),
        tags="React,FastAPI,SQL Server,REST API",
        features=(
            "Employee onboarding & profile management\n"
            "Attendance & leave management module\n"
            "Payroll calculation & salary slips\n"
            "Performance review & appraisal system\n"
            "Role-based access control (Admin/HR/Employee)"
        ),
        color_class="p2",
    ),

    Project(
        number="Project 03",
        title="Hajj & Umra Guide",
        description=(
            "A comprehensive digital guide for pilgrims planning their Hajj and "
            "Umra journey with step-by-step instructions and important information."
        ),
        tags="React,FastAPI,sql Server,Maps API",
        features=(
            "Interactive pilgrimage route mapping\n"
            "Virtual tour of holy sites\n"
            "Checklist & planning tools\n"
            "Travel & accommodation booking\n"
            "Real-time updates & notifications"
        ),
        color_class="p1",
    ),
]

db.add_all(projects)

# ── Skills ──────────────────────────────────────────────────────────────────────
skills = [
    Skill(category="Frontend", name="React.js",         pill_class="fe"),
    Skill(category="Frontend", name="JavaScript 14",       pill_class="fe"),
   
    Skill(category="Frontend", name="HTML5 / CSS3",     pill_class="fe"),
    Skill(category="Frontend", name="JavaScript ES6+",  pill_class="fe"),

    Skill(category="Backend",  name="Python",           pill_class="be"),
    Skill(category="Backend",  name="FastAPI",          pill_class="be"),
    Skill(category="Backend",  name="Node.js",          pill_class="be"),
    
    Skill(category="Backend",  name="JWT Auth",         pill_class="be"),

    Skill(category="Databases", name="SQL Server",      pill_class="db"),
    Skill(category="Databases", name="PostgreSQL",      pill_class="db"),
    
    Skill(category="Databases", name="MySQL",           pill_class="db"),

    Skill(category="State & Data", name="Redux Toolkit", pill_class="st"),
    Skill(category="State & Data", name="React Query",   pill_class="st"),
    Skill(category="State & Data", name="Context API",   pill_class="st"),

    Skill(category="Styling", name="Tailwind CSS",      pill_class="sy"),
    Skill(category="Styling", name="Sass / SCSS",       pill_class="sy"),
    Skill(category="Styling", name="Framer Motion",     pill_class="sy"),

    Skill(category="Tools & DevOps", name="Git / GitHub", pill_class="tl"),
   
    Skill(category="Tools & DevOps", name="Vercel",       pill_class="tl"),
    Skill(category="Tools & DevOps", name="Postman",      pill_class="tl"),
    Skill(category="Tools & DevOps", name=" Canvas",        pill_class="tl"),
]

db.add_all(skills)

# ── Experience ─────────────────────────────────────────────────────────────────
experiences = [

    Experience(
        position="Full Stack Developer Intern",
        company="Bytewrite",
        period="Oct 2025 — Present",
        description=(
            "Developing scalable and user-friendly web applications using "
            "modern frontend and backend technologies."
        ),
        details=(
            "Built responsive and dynamic user interfaces using React.js\n"
            "Developed secure REST APIs with FastAPI\n"
            "Integrated SQL Server and PostgreSQL databases\n"
            "Implemented JWT authentication & role-based access control\n"
            "Collaborated with cross-functional teams on real-world HRM systems\n"
            "Optimized application performance and API response times"
        )
    ),

    Experience(
        position="Intern",
        company="FBR (Federal Board of Revenue)",
        period="Jun 2023 — Aug 2023",
        description=(
            "Completed a 3-month internship focused on office management, "
            "digital systems, and professional workflow practices."
        ),
        details=(
            "Assisted in managing digital records and documentation\n"
            "Worked with internal software systems and reporting tools\n"
            "Learned professional communication and workflow management\n"
            "Supported administrative and technical teams in daily operations\n"
            "Gained exposure to government organizational processes"
        )
    ),

    
    
]

db.add_all(experiences)

db.commit()
db.close()

print("✅ Database seeded successfully!")