"""
modules/staff_invites/models/model_staff_invites.py
---------------------------------------
Database model for invitation tracking (invite-only registration).
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from datetime import datetime, timedelta
from core.db import Base


class Invites(Base):
    __tablename__ = "core_staff_invites"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("core_roles.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(
        DateTime, default=lambda: datetime.utcnow() + timedelta(hours=24)
    )
    accepted = Column(Boolean, default=False)

    def is_expired(self) -> bool:
        """Check if the staff_invites token is expired."""
        return datetime.utcnow() > self.expires_at
