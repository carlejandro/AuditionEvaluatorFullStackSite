from postgres.database import Base, engine
from postgres.models import Performer, Score, Section

print("Creating tables...")
Base.metadata.create_all(bind=engine) # bind the postgres db connection when creating tables, create all the tables defined in the models.py[metadata]
print("All 3 tables--> Performer, Score, and Section created successfully.")

# Same as exmple:

"""CREATE TABLE performer (
    performer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age INTEGER NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);"""


"""CREATE TABLE section (
        section_id SERIAL NOT NULL,
        instrument_name VARCHAR(100) NOT NULL,
        PRIMARY KEY (section_id),
        UNIQUE (instrument_name)
)


2026-04-08 20:15:36,738 INFO sqlalchemy.engine.Engine [no key 0.00014s] {}
2026-04-08 20:15:36,817 INFO sqlalchemy.engine.Engine CREATE INDEX ix_section_section_id ON section (section_id)
2026-04-08 20:15:36,818 INFO sqlalchemy.engine.Engine [no key 0.00018s] {}
2026-04-08 20:15:36,819 INFO sqlalchemy.engine.Engine
CREATE TABLE performer (
        performer_id SERIAL NOT NULL,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        age INTEGER NOT NULL,
        email VARCHAR(100) NOT NULL,
        section_id INTEGER NOT NULL,
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        PRIMARY KEY (performer_id),
        UNIQUE (email),
        FOREIGN KEY(section_id) REFERENCES section (section_id)
)


2026-04-08 20:15:36,819 INFO sqlalchemy.engine.Engine [no key 0.00024s] {}
2026-04-08 20:15:36,824 INFO sqlalchemy.engine.Engine CREATE INDEX ix_performer_performer_id ON performer (performer_id)
2026-04-08 20:15:36,824 INFO sqlalchemy.engine.Engine [no key 0.00013s] {}
2026-04-08 20:15:36,825 INFO sqlalchemy.engine.Engine
CREATE TABLE score (
        score_id SERIAL NOT NULL,
        performance_score FLOAT NOT NULL,
        timing_score FLOAT NOT NULL,
        rhythm_score FLOAT NOT NULL,
        total_score FLOAT NOT NULL,
        comments VARCHAR(255),
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        performer_id INTEGER NOT NULL,
        PRIMARY KEY (score_id),
        FOREIGN KEY(performer_id) REFERENCES performer (performer_id)
)


2026-04-08 20:15:36,827 INFO sqlalchemy.engine.Engine [no key 0.00018s] {}
2026-04-08 20:15:36,829 INFO sqlalchemy.engine.Engine CREATE INDEX ix_score_score_id ON score (score_id)
2026-04-08 20:15:36,829 INFO sqlalchemy.engine.Engine [no key 0.00014s] {}
2026-04-08 20:15:36,830 INFO sqlalchemy.engine.Engine COMMIT
All 3 tables--> Performer, Score, and Section created successfully."""