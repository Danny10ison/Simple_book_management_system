from sqlalchemy import String, Integer, Column

from database.db_setup import User_Base


class User(User_Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
