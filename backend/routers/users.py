from database.db_setup import User_SessionLocal
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from models.user import User
from routers.auth import hashed_password
from typing import List

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)
userDb = User_SessionLocal()


@router.get("/")
def redirect(request: Request):
    return RedirectResponse(url="/signin")


@router.post("/signup", response_class=HTMLResponse)
async def createNewUser(request: Request):
    form = await request.form()
    username = str(form.get("username"))
    password1 = str(form.get("password1"))
    password2 = str(form.get("password2"))
    errors = []
    user_exist = userDb.query(User).filter(User.username == username).first()
    if len(username) < 4:
        errors.append("Username must be greater than 4 characters")
    if len(password1 and password2) < 5:
        errors.append("Password must be greater than 5 characters")
    if user_exist is not None:
        errors.append("User already exist")
    if password1 != password2:
        errors.append("Passwords do not match")
    if len(errors) > 0:
        context = {"request": request, "errors": errors}
        return templates.TemplateResponse("signup.html", context)
    else:
        password = password2
        new_user = User(username=username, password=hashed_password(password))
        userDb.add(new_user)
        userDb.commit()
        msg = ["Registration successful"]
        context = {"request": request, "msg": msg}
        return templates.TemplateResponse("signin.html", context)


@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request, errors: List = []):
    context = {"request": request, "errors": errors}
    return templates.TemplateResponse("signup.html", context)


@router.get("/signout")
async def signout(request: Request, response: Response):
    response = RedirectResponse(url="/signin")
    response.delete_cookie("access_token")
    return response
