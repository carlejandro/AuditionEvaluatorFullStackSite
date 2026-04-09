from sqlalchemy.orm import Session

from postgres.database import SessionLocal
from postgres.models import Performer, Score, Section

# This file is to seed sample data for the secction performer and score tables. 
# Mimic the process of insertion of rows into the 3 tables we'll be using in the chen erd, kept simple for now.
def seed_data():
    db: Session = SessionLocal()

    try:
        # create sections first because performers depend on section_id
        # cool thing we can add more sections later like drumline/percussion 
        brass = Section(instrument_name="Brass")
        woodwind = Section(instrument_name="Woodwind")

        db.add_all([brass, woodwind])
        db.flush()

        # Create performers next because scores depend on performer_id
        performer_1 = Performer(
            first_name="John",
            last_name="Doe",
            age=30,
            email="john.doe@example.com",
            section_id=brass.section_id
        )

        performer_2 = Performer(
            first_name="Jane",
            last_name="Smith",
            age=25,
            email="jane.smith@example.com",
            section_id=woodwind.section_id
        )

        db.add_all([performer_1, performer_2])
        db.flush()

        # create scores last because each score depends on performer_id
        score_1 = Score(
            performance_score=8.5,
            timing_score=9.0,
            rhythm_score=8.0,
            total_score=25.5,
            comments="Strong overall audition.",
            performer_id=performer_1.performer_id #link the score to the first performer critical here
        )

        score_2 = Score(
            performance_score=9.0,
            timing_score=8.5,
            rhythm_score=9.5,
            total_score=27.0,
            comments="Excellent rhythm control.",
            performer_id=performer_2.performer_id # link the score to the second performer critical relationship 
        )

        db.add_all([score_1, score_2])
        db.commit()

        print("Sample section, performer, and score data seeded successfully.")

    except Exception as pgerror:
        db.rollback()
        print(f"Error seeding data: {pgerror}")
        print("Rolling back transaction...")

    finally:
        db.close()


# run the seed function only when this module is executed directly
if __name__ == "__main__":
    seed_data()