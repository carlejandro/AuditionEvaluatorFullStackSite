from sqlalchemy.orm import Session

from postgres.database import SessionLocal
from postgres.models import Performer

# all we're doing in this file is seeding some sample data into the performer table. 
# Mimic the process of insertion of rows into the 3 tables we'll be using in the chen erd, kept simple for now.
def seed_performers():
    db: Session = SessionLocal()
    try:
        performers = [Performer(first_name="John", last_name="Doe", age=30, email="john.doe@example.com"),
                        Performer(first_name="Jane", last_name="Smith", age=25, email="jane.smith@example.com")]
        db.add_all(performers)
        db.commit()
        print("Sample performer data seeded successfully.")
    except Exception as pgerror:
        db.rollback()
        print(f"Error seeding performer data: {pgerror}")
        print("Rolling back transaction...")
    finally:
        db.close()

        

# run the seed function ONLY when module is called directly, not when imported so we dont have accidental db row insertions
if __name__ == "__main__":
    seed_performers()