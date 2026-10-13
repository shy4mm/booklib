from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False)
    rating = Column(Integer, default=0)
