from fastapi import FastAPI
from app.users.router import router as users_router
from app.tasks.router import router as tasks_router


app = FastAPI(
    title="Task Manager API",
    version="0.1.0",
    description="A REST API for managing personal tasks."
)

app.include_router(users_router)
app.include_router(tasks_router)

@app.get("/status")
def root():
    return {
        "status": "...",
        "service": "Task Manager API"
    }