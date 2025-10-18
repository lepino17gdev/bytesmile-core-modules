from core.db import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(100), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(String(255))
