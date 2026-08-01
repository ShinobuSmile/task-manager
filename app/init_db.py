from app.database import engine, Base
from app.users.model import User   
from app.tasks.model import Task

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Tables successfully created.")