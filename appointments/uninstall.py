from core.db import Base, engine
from models.appointment_model import Appointment

def uninstall():
    """Drop appointment-related tables."""
    Appointment.__table__.drop(bind=engine)
    print("🗑️ Appointments module uninstalled successfully.")
