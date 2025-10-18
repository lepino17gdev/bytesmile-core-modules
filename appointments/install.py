from core.db import Base, engine
from sqlalchemy import inspect
from models.appointment_model import Appointment

def install(app=None):
    """Safely install the Appointments module without duplicate models."""
    inspector = inspect(engine)

    # If the table doesn't exist, create it
    if "appointments" not in inspector.get_table_names():
        Base.metadata.create_all(bind=engine, tables=[Appointment.__table__])
        print("✅ Appointments table created.")
    else:
        print("ℹ️ Appointments table already exists — skipping creation.")
