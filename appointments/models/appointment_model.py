from core.db import Base
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

# Guard against duplicate model registration
if 'Appointment' in Base._decl_class_registry:
    Appointment = Base._decl_class_registry['Appointment']
else:
    class Appointment(Base):
        __tablename__ = 'appointments'
        id = Column(Integer, primary_key=True, index=True)
        patient_name = Column(String(100), nullable=False)
        date = Column(DateTime(timezone=True), server_default=func.now())
        notes = Column(String(255))
