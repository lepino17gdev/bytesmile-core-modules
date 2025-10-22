from core.db import Base
from sqlalchemy import Column, Integer, String

class Sample(Base):
    __tablename__ = "sample"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
