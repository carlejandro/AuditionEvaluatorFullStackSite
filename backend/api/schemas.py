from datetime import datetime

from pydantic import BaseModel, ConfigDict

"""These are the pydantic models that definte the structure of the data that will be sent to and from the API endpoints.
   When the data is recieved from an API endpoint it will be structured this way in a JSON format so that the UI can easily read it. 
"""

# The attribute names HAVE TO MATCH whats in the Postgres DB 
# The pipeline will look like this --> SQLAlchemy objects returned from the database query --> converted to Pydantic models using the from_attributes config --> then sent to the UI in JSON format. This is critical for the UI to be able to read and display the data correctly. 
# The UI will read the json data retrieved via the API endpoints via javascript fetch calls and then use that data to populate the UI with the performers 
# This will be reversed for post data calls




# ----------- GET REQUEST MODELS ----------- #
class PerformerResponse(BaseModel):
    performer_id: int
    first_name: str
    last_name: str
    age: int
    email: str
    section_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SectionResponse(BaseModel):
    section_id: int
    instrument_name: str

    model_config = ConfigDict(from_attributes=True)


class PerformerScoreStatusResponse(BaseModel):
    performer_id: int
    has_score: bool


# ----------- POST REQUEST MODELS ----------- #
# these will be represented as dated retrieved from the UI that is sent TO the API when creating a new score for a performer. The API will then take this data and insert it into the database as a new score record linked to the respective performer via the performer_id foreign key. 
# This is critical for allowing the UI to submit new scores for performers and have that data persist in the database.
class ScoreCreate(BaseModel):
    performance_score: float
    timing_score: float
    rhythm_score: float
    total_score: float
    comments: str | None = None



class PerformerCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str
    section_id: int