from database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, nullable= False)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    author_id = Column(Integer, ForeignKey(
        "author.id", ondelete= "CASCADE"
    ),nullable= False)

    author = relationship("Author")


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    name = Column(String)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))