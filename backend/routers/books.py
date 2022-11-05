from database.db_setup import Book_SessionLocal, User_SessionLocal
from fastapi import APIRouter, Request, status, Response, responses
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.book import Book
from models.user import User
import jwt
from typing import List
from config import settings
from psycopg2 import connect

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)
bookDb = Book_SessionLocal()
userDb = User_SessionLocal()


@router.get("/home/", response_class=HTMLResponse)
def home(request: Request, msg: str = None, errors: List = []):
    try:
        token = request.cookies.get("access_token")
        if not token:
            errors.append("Kindly login first")
            context = {"request": request, "errors": errors}
            return templates.TemplateResponse("signin.html", context)
        scheme, _, param = token.partition(" ")
        payload = jwt.decode(param, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username = payload.get("username")
        user = userDb.query(User).filter(User.username == username).first()
        if user == None:
            errors.append(
                "You are not authenticated. Kindly create an account or login first"
            )
            context = {"request": request, "errors": errors}
            return templates.TemplateResponse("signin.html", context)
        else:
            book_db = bookDb.query(Book).all()
            context = {
                "request": request,
                "book_db": book_db,
                "msg": msg,
                "errors": errors,
            }
            return templates.TemplateResponse("home.html", context)
    except:
        errors.append("something went wrong! Please try again")
        context = {"request": request, "errors": errors}
        return templates.TemplateResponse("signin.html", context)


@router.get("/edit_details/{id}", response_class=HTMLResponse)
async def edit_details(id: int, request: Request):
    context = {"request": request, "id": id}
    return templates.TemplateResponse("edit_details.html", context)


@router.delete("/delete/{id}", response_class=HTMLResponse)
async def edit_details(id: int, request: Request):
    book = bookDb.query(Book).filter(Book.id == id).first()
    bookDb.delete(book)
    bookDb.commit()
    return Response(status_code=status.HTTP_200_OK)


@router.post("/submit", response_class=HTMLResponse)
async def add_book(request: Request, response: Response, msg: str = None):
    errors = []
    try:
        form = await request.form()
        book_id = int(form.get("id"))
        book_title = str(form.get("title"))
        book_author = str(form.get("author"))
        book_year_published = int(form.get("year_published"))
        id_exist = bookDb.query(Book).filter(Book.id == book_id).first()
        if id_exist is not None:
            errors.append("ID already exist")
        if not book_title or len(book_title) < 3:
            errors.append("title must be greater than 3 characters")
        if not book_author or len(book_author) < 3:
            errors.append("author must be greater than 3 characters")
        if not book_year_published or len(str(book_year_published)) < 4:
            errors.append("Enter a valid year")
        if len(errors) > 0:
            book_db = bookDb.query(Book).all()
            context = {"request": request, "errors": errors, "book_db": book_db}
            return templates.TemplateResponse("home.html", context)
        else:
            new_book = Book(
                id=book_id,
                title=book_title,
                author=book_author,
                year_published=book_year_published,
            )
            bookDb.add(new_book)
            bookDb.commit()
            return responses.RedirectResponse("/home", status_code=303)
    except ValueError:
        errors.append("something went wrong! Ensure that Year and id are integers")
        context = {"request": request, "errors": errors}
        return templates.TemplateResponse("home.html", context)


@router.put("/update/{id}", response_class=HTMLResponse)
async def update_book(request: Request, id: int):
    errors = []
    try:
        form = await request.form()
        book_title = str(form.get("title"))
        book_author = str(form.get("author"))
        book_year_published = int(form.get("year_published"))
        if len(book_author) < 3:
            errors.append("char must be greater than 3")
        if len(str(book_year_published)) < 4:
            errors.append("Enter valid year")
        if len(errors) > 0:
            context = {"request": request, "errors": errors, "id": id}
            return templates.TemplateResponse("edit_details.html", context)
        else:
            try:
                token = request.cookies.get("access_token")
                if not token:
                    errors.append("Kindly login first")
                    context = {"request": request, "errors": errors}
                    return templates.TemplateResponse("signin.html", context)
                scheme, _, param = token.partition(" ")
                payload = jwt.decode(
                    param, settings.SECRET_KEY, algorithms=settings.ALGORITHM
                )
                username = payload.get("username")
                user = userDb.query(User).filter(User.username == username).first()
                if user == None:
                    errors.append(
                        "You are not authenticated. Kindly create an account or login first"
                    )
                    context = {"request": request, "errors": errors}
                    return templates.TemplateResponse("signin.html", context)
                else:
                    bookDb.query(Book).filter(Book.id == id).update(
                        {
                            "title": book_title,
                            "author": book_author,
                            "year_published": book_year_published,
                        }
                    )
                    bookDb.commit()
                    return responses.RedirectResponse("/home", status_code=303)
            except:
                errors.append("something went wrong! Please login and try again")
                context = {"request": request, "errors": errors}
                return templates.TemplateResponse("signin.html", context)
    except ValueError:
        errors.append("Year must be integers")
        context = {"request": request, "errors": errors, "id": id}
        return templates.TemplateResponse("edit_details.html", context)
