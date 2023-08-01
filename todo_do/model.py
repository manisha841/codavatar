from sqlalchemy import Column, Integer, String

from .database import Base

class Todo(Base):
    __tablename__ = 'tododb'

    id = Column(Integer, primary_key = True, index = True)
    task = Column(String)
    minutes = Column(Integer)