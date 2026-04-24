# This is the main entry point for the FastAPI application. It defines the API endpoints and their corresponding handlers. Uvicorn calls App 
# when the server starts, and the API is ready to handle incoming HTTP requests on your local machine. I put a root endpoint for basic tesing which returns a simple message

# ---- API Pipeline Logic ----#
"""Get the sql alchemy objects returned into a list using .scalars().all()--> Sql againt the Postgres DB
after we recieve the objects , use the pydantic model class to convert the SQL Alchemy objects into a JSON format with validated atttributes that
match the shape of the data we want to send to the UI and what we defined in the UML + ERD."""


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

from postgres.database import SessionLocal
from postgres.models import Performer, Section, Score
from api.schemas import PerformerResponse, SectionResponse, ScoreCreate

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins to access this API for local development. 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Audition evaluation API is running!"}

@app.get("/performers", response_model=List[PerformerResponse]) # convert the response to a json list that the UI can easily read and construct
def get_performers():
    db: Session = SessionLocal()
    try:
        performers = db.execute(select(Performer)).scalars().all()
        return performers
    except Exception as pgerror:
        print(f"Error fetching performers: {pgerror}")
        return {"error": "An error occurred while fetching performers."}
    finally:
        db.close()

# filter on the specific performer_id and return the details of that performer, if not found return a 404 error with a message. This is critical for the UI to display the details of a specific performer when selected.
@app.get("/performers/{performer_id}", response_model=PerformerResponse)
def get_performer(performer_id: int):
    db: Session = SessionLocal()
    try:
        performer = db.get(Performer, performer_id)

        if not performer:
            raise HTTPException(status_code=404, detail="Performer not found")

        return performer

    finally:
        db.close()

@app.get("/sections", response_model=List[SectionResponse])
def get_sections():
    db: Session = SessionLocal()
    try:
        sections = db.execute(select(Section)).scalars().all() # execute the select statement to get all sections from the database, then convert the result to a list of Section objects using scalars().all()
        return sections
    except Exception as pgerror:
        print(f"Error fetching sections: {pgerror}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching sections.")
    finally:
        db.close()



### --- POST ROUTES --- ###
@app.post("/performers/{performer_id}/scores")
def create_score(performer_id: int, score_data: ScoreCreate):
    db: Session = SessionLocal() # The current postgres instance

    try:
        performer = db.get(Performer, performer_id)

        if not performer:
            raise HTTPException(status_code=404, detail="Performer not found")

        #This is a sql_alchemy object that is being created using pydantic validated data from the request body
        new_score = Score(
            performance_score=score_data.performance_score,
            timing_score=score_data.timing_score,
            rhythm_score=score_data.rhythm_score,
            total_score=score_data.total_score,
            comments=score_data.comments,
            performer_id=performer_id
        )

        db.add(new_score)
        db.commit()
        db.refresh(new_score)


        # To check query the scored id in the http 200 response in the PG instance 
        return {
            "message": "Score saved successfully",
            "score_id": new_score.score_id
        }

    except HTTPException:
        raise

    except Exception as pgerror:
        db.rollback()
        print(f"Error saving score: {pgerror}")
        raise HTTPException(status_code=500, detail="An error occurred while saving the score.")

    finally:
        db.close()