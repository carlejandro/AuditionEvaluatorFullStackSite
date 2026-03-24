# This is the main entry point for the FastAPI application. It defines the API endpoints and their corresponding handlers. Uvicorn calls App 
# when the server starts, and the API is ready to handle incoming HTTP requests on your local machine. I put a root endpoint for basic tesing which returns a simple message

from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from postgres.database import SessionLocal
from postgres.models import Performer

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Audition evaluation API is running!"}

@app.get("/performers")
def get_performers():
    db: Session = SessionLocal()
    try:
        performers = db.execute(select(Performer)).scalars().all() # This selects all the rows from the performer table and returns them as a list of Performer objects. 
        # we use scalars() to get the actual Performer objects from the result of the query, and then call all() to get them as a list.
        return performers
    except Exception as pgerror:
        print(f"Error fetching performers: {pgerror}")
        return {"error": "An error occurred while fetching performers."}
    finally:
        db.close()
