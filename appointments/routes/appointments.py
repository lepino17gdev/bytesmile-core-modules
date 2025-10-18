from fastapi import APIRouter, HTTPException
from core.db import SessionLocal
from models.appointment_model import Appointment

router = APIRouter(prefix="/api/appointments", tags=["Appointments"])

@router.get("/")
def list_appointments():
    db = SessionLocal()
    data = db.query(Appointment).all()
    db.close()
    return {"appointments": [a.__dict__ for a in data]}

@router.post("/")
def create_appointment(patient_name: str, doctor_name: str):
    db = SessionLocal()
    appointment = Appointment(patient_name=patient_name, doctor_name=doctor_name)
    db.add(appointment)
    db.commit()
    db.close()
    return {"message": "Appointment created successfully"}
