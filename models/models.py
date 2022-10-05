
from sqlalchemy import String,Integer,Column

from database.db_setup import Base



class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key = True)
    title =Column(String(255),nullable=False)
    author =Column(String(255),nullable=False)
    year_published = Column(Integer)

  