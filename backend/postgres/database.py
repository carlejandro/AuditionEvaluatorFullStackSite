from sqlalchemy import create_engine # this creates a connection to the database
from sqlalchemy.orm import sessionmaker, DeclarativeBase # this is used to create a session for interacting with the database


class Base(DeclarativeBase):
    pass

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/audition_evaluator_db"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

