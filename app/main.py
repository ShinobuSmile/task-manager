from dotenv import load_dotenv
load_dotenv()
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


#Verifies the status of the service and returns the name of the application
@app.get("/status", summary = "Service status", description = "Verifies the status of the service and returns the name of the application")
def root():
    return {
        "status": "ok",
        "service": "Task Manager API"
    }