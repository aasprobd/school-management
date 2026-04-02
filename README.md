# Enterprise School Management System (ESMS)

## 🏫 Project Overview
The **Enterprise School Management System (ESMS)** is a comprehensive, data-driven platform designed to automate and streamline the operations of **Global International School & College**. From student admissions and academic tracking to financial accounting and HR management, ESMS provides a unified solution for modern educational institutions.

## 🚀 Key Features
- **Student Lifecycle Management**: Admissions, profiles, and academic history.
- **Academic Module**: Attendance, grading, exam management, and timetables.
- **Finance & Payroll**: Invoicing, payment gateway integration, and staff salary management.
- **Communication Bridge**: Internal notifications, parent-teacher communication, and notice boards.
- **Resource Management**: Digital library, inventory tracking, and transport management.
- **Advanced Analytics**: Data-driven insights into institutional performance.

## 🛠️ Tech Stack
### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database**: PostgreSQL with [SQLAlchemy](https://www.sqlalchemy.org/) ORM
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Authentication**: OAuth2 with JWT & Bcrypt

### Frontend
- **Landing Page**: Modern, responsive HTML5/CSS3 (Vanilla)
- **Application**: Planned migration to Next.js (React) for enhanced performance and SEO.

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx (Reverse Proxy)
- **CI/CD**: GitHub Actions

## 📂 Project Structure
```text
.
├── backend/            # FastAPI application source code
│   ├── routers/        # API endpoints grouped by module
│   ├── services/       # Business logic and external integrations
│   ├── models.py       # SQLAlchemy database models
│   └── main.py         # Application entry point
├── docs/               # Technical documentation and roadmaps
├── assets/             # Static assets (images, logos, etc.)
├── index.html          # Main landing page
├── docker-compose.yml  # Container orchestration
└── alembic.ini         # Database migration configuration
```

## 📖 Documentation
Detailed technical specifications and development tracking are available in the `docs/` directory:
- 📜 **[Software Blueprint](docs/software_blueprint.md)**: Architecture, data models, and system design.
- ✅ **[Development Roadmap](docs/tasks.md)**: 100-task checklist tracking project progress.

## 🛠️ Quick Start
### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- PostgreSQL

### Running Locally (Backend)
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

### Running with Docker
```bash
docker-compose up --build
```

## 📄 License
This project is proprietary and confidential. All rights reserved.
