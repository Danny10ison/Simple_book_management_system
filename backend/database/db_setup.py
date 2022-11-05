from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings


book_engine = create_engine(settings.BOOK_DATABASE_URL, echo=True)
user_engine = create_engine(settings.USER_DATABASE_URL, echo=True)
Book_SessionLocal = sessionmaker(bind=book_engine)
User_SessionLocal = sessionmaker(bind=user_engine)
Book_Base = declarative_base()
User_Base = declarative_base()
