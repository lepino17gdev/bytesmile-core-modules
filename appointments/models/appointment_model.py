from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from core.db import Base
from datetime import datetime

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(100))
    doctor_name = Column(String(100))
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="Scheduled")