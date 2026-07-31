from fastapi import FastAPI

app = FastAPI(
    title="Task Manager API",
    version="0.1.0",
    description="A REST API for managing personal tasks."
)

@app.get("/status")
def root():
    return {
        "status": "...",
        "service": "Task Manager API"
    }