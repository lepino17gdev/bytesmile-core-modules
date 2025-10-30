from core.db import Base
from sqlalchemy import Column, Integer, String

class AccessMatrix(Base):
    __tablename__ = "core_access_matrix"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
