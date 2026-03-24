from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from postgres.database import Base

class Performer(Base):
    __tablename__ = "performer"

    # This is exactly how it looks, were mapping columns to the attributes of the class
    # which correspond to the columns in the audition_evaluator_db database
    performer_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # NOTE: In the CHEN Erd we have 3 more fields to add, but I will add those later once we have the basic structure down
    # TODO: Add section, score, timestamp fields from chen erd