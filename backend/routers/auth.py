from database.db_setup import User_SessionLocal
from fastapi import APIRouter, Request, status, HTTPException, Response, responses
from fastapi.templating import Jinja2Templates
from models.user import User
from passlib.context import CryptContext
from typing import List
import jwt
from config import settings


userDb = User_SessionLocal()
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


def authenticate_user(username: str, password: str):
    user_exist = userDb.query(User).filter(User.username == username).first()
    if user_exist is not None:
        if not verify_password(password, user_exist.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        else:
            return True
    else:
        return False


def hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


@router.post("/signin")
async def login(request: Request, response: Response):
    errors = []
    form = await request.form()
    username = str(form.get("username"))
    password = str(form.get("password"))
    if not username:
        errors.append("Please enter a valid username")
        context = {"request": request, "errors": errors}
        return templates.TemplateResponse("signin.html", context)
    if not password or len(password) < 5:
        errors.append("Password should be greater than 5 characters")
        context = {"request": request, "errors": errors}
        return templates.TemplateResponse("signin.html", context)
    try:
        user_exist = userDb.query(User).filter(User.username == username).first()
        if user_exist is None:
            errors.append("User does not exist")
            context = {"request": request, "errors": errors}
            return templates.TemplateResponse("signin.html", context)
        if authenticate_user(username, password):
            user = userDb.query(User).filter(User.username == username).first()
            user = {"id": user.id, "username": user.username, "password": user.password}
            msg = ["Login Successfull"]
            context = {"request": request, "msg": msg}
            response = responses.RedirectResponse("/home", status_code=303)
            token = jwt.encode(user, settings.SECRET_KEY, settings.ALGORITHM).decode(
                "utf-8"
            )
            response.set_cookie(
                key="access_token", value=f"Bearer {token}", httponly=True
            )
            return response
        else:
            errors.append("Password incorrect")
            context = {"request": request, "errors": errors}
            return templates.TemplateResponse("signin.html", context)
    except:
        errors.append("something went wrong!")
        context = {"request": request, "errors": errors}
        return templates.TemplateResponse("signin.html", context)


@router.get("/signin")
async def signin(request: Request, errors: List = []):
    context = {"request": request, "errors": errors}
    return templates.TemplateResponse("signin.html", context)
