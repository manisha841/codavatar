from database import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base,relationship

class Todo(Base):
    __tablename__ = 'tododb'

    id = Column(Integer, primary_key = True, index = True)
    task = Column(String)
    minutes = Column(Integer)
    # user_id = Column()
    owner = relationship("users", back_populates="todos")

    def __repr__(self):
        return f"<Todo {self.name}>"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True,autoincrement=True)
    name = Column(String)
    email = Column(String, nullable= False, unique= True)
    password = Column(String, nullable=False)
    disabled = Column(Boolean,default=False)
    todos = relationship("tododb", back_populates="owner",cascade="all, delete" )

    def __repr__(self):
        return f"<User {self.name}>"