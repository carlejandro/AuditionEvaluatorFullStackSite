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
from api.schemas import PerformerResponse, SectionResponse, ScoreCreate, PerformerCreate, PerformerScoreStatusResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins to access this API for local development. 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- GET ROUTES ---- #
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


# This endpoint checks if each performer has an associated score in the database and returns a list of performer IDs along with a boolean indicating whether they have a score or not. This is critical for the UI to determine which performers have been scored and which have not, allowing it to display that information accordingly.
@app.get("/performer-score-status", response_model=List[PerformerScoreStatusResponse])
def get_performer_score_status():
    db: Session = SessionLocal()

    try:
        performers = db.execute(select(Performer)).scalars().all()

        status_list = []

        for performer in performers:
            score = db.execute(
                select(Score)
                .where(Score.performer_id == performer.performer_id)
                .limit(1)
            ).scalar_one_or_none()

            status_list.append({
                "performer_id": performer.performer_id,
                "has_score": score is not None
            })

        return status_list

    except Exception as pgerror:
        print(f"Error fetching performer score status: {pgerror}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching score status.")

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

# pretty much same logic as the create_score endpoint but for creating a new performer instead of a score. This is critical for allowing the UI to submit new performers and have that data persist in the database.
@app.post("/performers", response_model=PerformerResponse) # include the performer response pydantic model 
def create_performer(performer_data: PerformerCreate):
    db: Session = SessionLocal()

    try:
        section = db.get(Section, performer_data.section_id)

        if not section:
            raise HTTPException(status_code=404, detail="Section not found")

        new_performer = Performer(
            first_name=performer_data.first_name,
            last_name=performer_data.last_name,
            age=performer_data.age,
            email=performer_data.email,
            section_id=performer_data.section_id
        )

        db.add(new_performer)
        db.commit()
        db.refresh(new_performer)

        return new_performer

    except HTTPException:
        raise

    except Exception as pgerror:
        db.rollback()
        print(f"Error creating performer: {pgerror}")
        raise HTTPException(status_code=500, detail="An error occurred while creating performer.")

    finally:
        db.close()