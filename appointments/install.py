from core.db import Base, engine
from models.appointment_model import Appointment
from fastapi import APIRouter
from routes.appointments import router as appointment_router

def install(app):
    """Register module routes and create tables."""
    Base.metadata.create_all(bind=engine)
    app.include_router(appointment_router)
    print("✅ Appointments module installed successfully.")
