from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Todo(Base):
    __tablename__ = 'tododb'

    id = Column(Integer, primary_key = True, index = True)
    task = Column(String)
    minutes = Column(Integer)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete= "CASCADE"
    ),nullable= False)

    owner = relationship("User", back_populates="todos",cascade="all, delete")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True,autoincrement=True)
    name = Column(String)
    email = Column(String, nullable= False, unique= True)
    password = Column(String, nullable=False)
    disabled = Column(Boolean,default=False)
    todos = relationship("Todo", back_populates="owner",cascade="all, delete" )
