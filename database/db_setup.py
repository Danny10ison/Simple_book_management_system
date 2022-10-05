from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql://zizo:1234@localhost/books", echo = True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
