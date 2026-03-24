from postgres.database import Base, engine
from postgres.models import Performer

print("Creating tables...")
Base.metadata.create_all(bind=engine) # bind the postgres db connection when creating tables, create all the tables defined in the models.py[metadata]
print("Tables created successfully.")

# Same as 

"""CREATE TABLE performer (
    performer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age INTEGER NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);"""