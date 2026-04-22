from datetime import datetime

from pydantic import BaseModel, ConfigDict

"""These are the pydantic models that definte the structure of the data that will be sent to and from the API endpoints.
   When the data is recieved from an API endpoint it will be structured this way in a JSON format so that the UI can easily read it. 
"""

# The attribute names HAVE TO MATCH whats in the Postgres DB 

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


