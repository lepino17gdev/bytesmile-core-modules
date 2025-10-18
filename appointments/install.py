import os
import sys
from core.db import Base, engine
from models.appointment_model import Appointment

def install(app=None):
    """Register Appointment model and create its table."""
    Base.metadata.create_all(bind=engine, tables=[Appointment.__table__])
    print("✅ Appointments module installed successfully.")
