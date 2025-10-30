from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base


class AccessMatrix(Base):
    __tablename__ = "core_access_matrix"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("core_roles.id"), nullable=False)
    module = Column(String, nullable=False)
    permission = Column(String, nullable=False)

    role = relationship("Role", backref="access_permissions")
