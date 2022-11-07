# Simple_book_management_system
This is a project consisting mainly of fastapi,HTMX  and docker using postgres as the database. The purpose of this project is to demonstrate some of my backend capabilities in building web applications. This project illustrate a wide range of functionalities including authentication and authorization, CRUD functionalities, database creation and operations and also dockerization.

# HTMX Attributes

The following HTMX attributes are used in this project:

hx-get  --  Issues a GET request to the given URL.

hx-post --  Issues a POST request to the given URL.

hx-put --  Issues a PUT request to the given URL.

hx-delete -- Issues a DELETE request to the given URL.

hx-trigger -- It specifies the event that will trigger the request.

hx-target  -- It specifies the target element to load the the response into.

hx-swap  -- It specifies how to load the response.


#  Structure
My work folder is the backend which is structured as follows:

database - Database setup

models - Data models

templates - Contains my website templates

routers - Contains my api routes

static - Contains the favicon.ico file

main.py - Main operational file for running the FastAPI application

configure.py - Contain my application configurations

# How to run
Basically there are two ways of running this application. 

**RUNNING WITH DOCKER(Main)**
NB: One must have docker installed and make sure docker is running

- Configure your postgres database configuration. Also make sure you use the name of the postgres database image(db) as your postgres_host
- In the Simple_book_management_system directory run docker-compose up -d or docker-compose up --build inorder to build and run your application

**RUNNING WITHOUT DOCKER(Alternative)**
-Ensure that the postgres database configuration setting postgres_host must be localhost

-Create virtual environment

-Activate virtual environment

-Install requirements by running pip3 install -r requirements.txt

-Navigate into the backend directory and run uvicorn main:app --reload
