# Task Manager API

A RESTful API for managing personal tasks, built with FastAPI and PostgreSQL.
Users can register, authenticate via JWT, and perform CRUD operations on their own tasks,
with filtering support by title, priority, completion status, and due date.

## Technologies

- **FastAPI** – modern async Python web framework
- **PostgreSQL** – relational database
- **SQLAlchemy** – ORM and database toolkit
- **JWT** – JSON Web Tokens for stateless authentication (python-jose)
- **bcrypt** – secure password hashing
- **Pydantic** – data validation and serialization
- **Pytest** – automated testing with in‑memory SQLite
- **Swagger / OpenAPI** – interactive API documentation
- **Docker & Docker Compose** – containerization and orchestration
- **python-dotenv** – environment variable management

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 16 (or later) running locally

### Setup

1. Clone the repository:
    git clone https://github.com/ShinobuSmile/task-manager.git
    cd task-manager

2. Create and activate a virtual environment:
    python -m venv .venv
    source .venv/bin/activate   # Linux / macOS
    .venv\Scripts\activate      # Windows

3. Install dependencies:
    pip install -r requirements.txt

4. Create a .env file in the project root:
    SECRET_KEY=your-secret-key-here
    DATABASE_URL=postgresql://postgres:password@localhost:5432/taskmanager

5. Start the server:
    uvicorn app.main:app --reload

    The API will be available at http://localhost:8000.
    Interactive documentation at http://localhost:8000/docs.

    Database tables are created automatically when the server starts.
    If you prefer to create them manually without starting the server, you can run:
        python -m app.init_db

## Usage

### Authentication - All task endpoints require a valid JWT token. Obtain one by:

1. **Register** a new user:
    POST /users/
    {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "Str0ng!Pass"
    }

2. **Login** to get a token:
    POST /users/login
    {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "Str0ng!Pass"
    }

    The response contains:
    {
        "access_token": "eyJhbGciOiJIUzI1NiIs...",
        "token_type": "bearer"
    }

3. Include the token in the Authorization header for protected endpoints:
    Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

## API Endpoints

| Method | Endpoint               | Description                                          | Auth |
|--------|------------------------|------------------------------------------------------|------|
| GET    | `/status`              | Health check                                         | No   |
| POST   | `/users/`              | Register a new user                                  | No   |
| POST   | `/users/login`         | Login and receive JWT token                          | No   |
| GET    | `/users/me`            | Get current user profile                             | Yes  |
| POST   | `/tasks/`              | Create a new task                                    | Yes  |
| GET    | `/tasks/tasks`         | List user's tasks (with optional filters)            | Yes  |
| GET    | `/tasks/{task_id}`     | Get a single task (owner only)                       | Yes  |
| PATCH  | `/tasks/{task_id}`     | Update a task (owner only)                           | Yes  |
| DELETE | `/tasks/{task_id}`     | Delete a task (owner only)                           | Yes  |


## Testing
Run the test suite with pytest.
Tests use an in‑memory SQLite database and override the get_db dependency,
so they do not touch your real database.

## Docker
**Prerequisites**
- Docker Desktop installed and running

**Start the application**
- docker-compose up --build

This will start two containers:
- app – the FastAPI server on http://localhost:8000
- db – PostgreSQL 16 with persistent storage

The database tables are created automatically on startup.

**Stop the application**
- docker-compose down          # stops containers, keeps database data
- docker-compose down -v       # stops containers and removes all data

**Run tests inside Docker**
- docker-compose run app pytest

## Project Structure
```
task-manager/
├── app/
│ ├── main.py # FastAPI application entry point
│ ├── database.py # Database engine and session
│ ├── auth.py # JWT creation and current user dependency
│ ├── security.py # Password hashing (bcrypt)
│ ├── init_db.py # Manual table creation script (optional)
│ ├── users/
│ │ ├── model.py # SQLAlchemy User model
│ │ ├── schemas.py # Pydantic schemas (UserCreate, UserLogin, Token)
│ │ └── router.py # User endpoints
│ └── tasks/
│ ├── model.py # SQLAlchemy Task model + PriorityEnum
│ ├── schemas.py # Pydantic schemas (TaskCreate, TaskUpdate, TaskOut)
│ └── router.py # Task endpoints
├── tests/
│ ├── conftest.py # Shared test configuration (env vars)
│ ├── test_main.py # Status endpoint test
│ ├── test_users.py # User registration and login tests
│ └── test_tasks.py # Task CRUD and filter tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example # Example environment variables
└── README.md
```