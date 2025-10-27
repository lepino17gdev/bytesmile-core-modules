"""
modules/invites/models/model_invites.py
---------------------------------------
Database model for invitation tracking (invite-only registration).
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from core.db import Base


class Invites(Base):
    __tablename__ = "core_invites"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("core_roles.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(
        DateTime, default=lambda: datetime.utcnow() + timedelta(hours=24)
    )
    accepted = Column(Boolean, default=False)

    # ✅ Relationship cleanup: use back_populates instead of backref
    # Backref causes mapper conflicts when reinstalling dynamically.
    role = relationship("Role", back_populates="invite_links")

    def is_expired(self) -> bool:
        """Check if the invite token is expired."""
        return datetime.utcnow() > self.expires_at
