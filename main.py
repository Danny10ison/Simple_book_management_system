from fastapi import FastAPI,Request,Response,status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import models.models as models
from database.db_setup import SessionLocal
from database.db_setup import Base,engine
from models.models import Book

app = FastAPI()
templates = Jinja2Templates(directory="templates")
db = SessionLocal()
Base.metadata.create_all(engine)
  

@app.get("/index/",response_class=HTMLResponse)
def index(request:Request):
    book_db = db.query(models.Book).all()
    context = {'request':request,"book_db":book_db}
    return templates.TemplateResponse("index.html",context)
    

@app.get("/index/edit_details/{id}",response_class=HTMLResponse)
async def edit_details(id:int):
    response = f"""
    <h3 style="margin-bottom: 25px;"> Edit details for book with id {id} </h3>
    <body>
    <form class="mb-3">
        <input type="text" placeholder="Book Title" name="title" class="form-control mb-3" />
        <input type="text" placeholder="Book Author" name="author" class="form-control mb-3" />
        <input type="text" placeholder="Year published" name="year_published" class="form-control mb-3" />
    <button type="post" class="btn btn-primary" hx-put ="/update/{id}" hx-swap="body" hx-target = "body" hx-trigger = "click"> Update </button>
    </form>
    </body>   
     """
    return response
    

@app.delete("/delete/{id}")
async def edit_details(id:int,request:Request):
    book = db.query(models.Book).filter(models.Book.id==id).first()
    db.delete(book)
    db.commit()
    return Response(status_code=status.HTTP_200_OK)
        

@app.post("/submit/",response_class=HTMLResponse)
async def add_book(request:Request):
    form = await request.form()
    book_id = form.get("id")
    book_title = form.get("title")
    book_author = form.get("author")
    book_year_published = form.get("year_published")
    id_exist = db.query(models.Book).filter(models.Book.id==book_id).first()
    if id_exist is not None:
        print("ID already exist")
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)
    else:    
        new_book = models.Book(id=book_id, title=book_title,author=book_author,year_published = book_year_published)
        db.add(new_book)
        db.commit()
    response = f"""
    <tr> 
        <td>{book_id}</td>
        <td>{book_title}</td>
        <td>{book_author}</td>
        <td>{book_year_published}</td>
        <td>
            <button hx-get="edit_details/{book_id}" hx-trigger="click"
            hx-target="body"
            hx-swap="/index/" class="btn btn-primary">
            Edit Details
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{book_id}" 
                    hx-trigger="click"
                    hx-target="closest tr"
                    hx-swap="outerHTML"
                class="btn btn-primary">
                Delete
            </button>
        </td>
    </tr>
    """
    return response


@app.put("/update/{id}",response_class=HTMLResponse)
async def update_book(id:int,request:Request):
    form = await request.form()
    book_title = form.get("title")
    book_author = form.get("author")
    book_year_published = form.get("year_published")
    db.query(models.Book).filter(models.Book.id==id).update({"title": book_title,"author":book_author,"year_published": book_year_published})
    db.commit()
    book_db = db.query(models.Book).all()
    context = {'request':request,"book_db":book_db}
    return templates.TemplateResponse("index.html",context)

