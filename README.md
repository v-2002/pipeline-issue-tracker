# PRJ - Pipeline Issue Tracker API

A production-grade REST API built with FastAPI for tracking and managing data pipeline failures and incidents.

## Problem Statement

Data engineering teams lack a structured system to report, assign, track, and resolve ETL pipeline failures. Issues get lost in Slack messages and Excel sheets with no audit trail. This API provides a centralized backend to manage pipeline incidents from creation to resolution.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10 | Core language |
| FastAPI | REST API framework |
| SQLAlchemy | ORM for database operations |
| Alembic | Database migrations |
| SQLite (local) / Azure SQL (production) | Database |
| JWT (python-jose) | Authentication |
| Passlib + bcrypt | Password hashing |
| Pytest | Unit and integration testing |
| Docker | Containerization |
| Azure Container Registry | Docker image storage |
| Azure App Service | Application hosting |
| GitHub Actions | CI/CD pipeline |

## Architecture
```
Client (Swagger UI / Frontend / Project 2)
        ↓
FastAPI Routes (app/api/routes/)
        ↓
Service Layer (app/services/)
        ↓
SQLAlchemy ORM (app/models/)
        ↓
SQLite (local) / Azure SQL (production)
```

## Project Structure
```
pipeline-issue-tracker/
├── app/
│   ├── api/routes/        # API endpoints
│   ├── core/              # Config, security, JWT
│   ├── db/                # Database session
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   └── services/          # Business logic
├── tests/                 # Pytest test suite
├── .github/workflows/     # CI/CD pipeline
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Getting Started

### Prerequisites
- Python 3.10+
- Docker (optional)

### Run Locally
```bash
# Clone the repo
git clone https://github.com/viki/pipeline-issue-tracker.git
cd pipeline-issue-tracker

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation.

### Run with Docker
```bash
docker compose up --build
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get JWT token |

### Issues
| Method | Endpoint | Description |
|---|---|---|
| POST | `/issues/` | Create new pipeline issue |
| GET | `/issues/` | Get all issues (with filters) |
| GET | `/issues/{id}` | Get issue by ID |
| PATCH | `/issues/{id}` | Update issue |
| DELETE | `/issues/{id}` | Soft delete issue |

### Filters available on GET /issues/
- `status` — OPEN, IN_PROGRESS, RESOLVED, CLOSED
- `severity` — LOW, MEDIUM, HIGH, CRITICAL
- `pipeline_name` — filter by pipeline
- `assigned_to` — filter by assignee

## Authentication

All issue endpoints are protected with JWT. To use:

1. Register at `POST /auth/register`
2. Login at `POST /auth/login` to get token
3. Click **Authorize** in Swagger UI and enter credentials
4. All subsequent requests automatically include the token

## Running Tests
```bash
pytest tests/ -v
```

Currently 14 tests passing across auth and issue endpoints.

## CI/CD

GitHub Actions pipeline automatically runs on every push to `main`:
1. Installs dependencies
2. Runs full test suite
3. Fails the pipeline if any test fails

Pipeline config: `.github/workflows/deploy.yml`

## Future Improvements

- Connect to Project 2 (ETL Orchestration API) for auto-logging pipeline failures
- Add Azure Key Vault for secrets management
- Re-enable Azure deployment with Container Apps (cost-optimized)
- Add metrics endpoint for pipeline failure analytics
- Implement role-based access control (admin vs developer)

## Connection to Project 2

This API is designed to integrate with the ETL Pipeline Orchestration API. When a pipeline run fails in Project 2, it automatically calls `POST /issues/` to log the incident — no manual intervention needed.
```

---

Also create `.env.example` — a template showing what variables are needed without actual secrets:
```
APP_NAME=Pipeline Issue Tracker
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./pipeline_tracker.db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30