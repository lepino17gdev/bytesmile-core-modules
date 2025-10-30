from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from core.db import Base

class AccessMatrix(Base):
    __tablename__ = "core_access_matrix"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("core_roles.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("core_users.id"), nullable=True)
    module = Column(String, nullable=False)
    permission = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('role_id', 'user_id', 'module', 'permission', name='_unique_access'),)
