from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from postgres.database import Base

# treat this file as the definition of the database schema and respective attributes in ORM format.

class Section(Base):
    __tablename__ = "section"

    section_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    instrument_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # One section contains many performers
    performers: Mapped[list["Performer"]] = relationship(back_populates="section")




class Performer(Base):
    __tablename__ = "performer"

    # This is exactly how it looks, were mapping columns to the attributes of the class
    # which correspond to the columns in the audition_evaluator_db database
    performer_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    section_id: Mapped[int] = mapped_column(ForeignKey("section.section_id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    # Relationship back to Section
    section: Mapped["Section"] = relationship(back_populates="performers")
    # One performer can receive many scores
    scores: Mapped[list["Score"]] = relationship(back_populates="performer")


class Score(Base):
    __tablename__ = "score"

    score_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    performance_score: Mapped[float] = mapped_column(Float, nullable=False)
    timing_score: Mapped[float] = mapped_column(Float, nullable=False)
    rhythm_score: Mapped[float] = mapped_column(Float, nullable=False)
    total_score: Mapped[float] = mapped_column(Float, nullable=False)

    comments: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # fkey: each score belongs to one performer
    performer_id: Mapped[int] = mapped_column(ForeignKey("performer.performer_id"), nullable=False)

    # Relationship back to Performer
    performer: Mapped["Performer"] = relationship(back_populates="scores")
    