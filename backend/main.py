from fastapi import FastAPI
from database.db_setup import Book_Base, book_engine, User_Base, user_engine
from routers import auth, users, books
from config import settings
from fastapi.staticfiles import StaticFiles
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def check_db_connection():
    con = None
    con = connect(
        user=settings.POSTGRES_USER, host="db", password=settings.POSTGRES_PASSWORD
    )
    books_db = "books"
    users_db = "users"
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute("CREATE DATABASE " + books_db)
        cur.execute("CREATE DATABASE " + users_db)
        cur.close()
        con.close()
    except:
        pass


def create_tables():
    Book_Base.metadata.create_all(book_engine)
    User_Base.metadata.create_all(user_engine)


def include_router(app):
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(books.router)


desc = """
This is a simple book management system
"""


def start_application():
    app = FastAPI(
        title=settings.PROJECT_TITLE,
        version=settings.PROJECT_VERSION,
        description=desc,
        contact={"name": "Ibrahim Aziz", "email": "ibrahimaziz200000@gmail.com"},
        redoc_url=None,
    )
    app.mount("/static", StaticFiles(directory="static"), name="static")
    create_tables()
    include_router(app)
    return app


check_db_connection()
app = start_application()
