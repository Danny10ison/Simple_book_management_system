# Simple_book_management_system
This is a project of fastapi and HTMX using postgres as the database. The purpose of this project is to illustrate how I create a simple website plus CRUD functionalities with no JavaScript, using only HTML, CSS, and Python. HTMX is a plugin that allows this to be possible.

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

database - Database setup

models - Data models

templates - Contains the main webpage which is the index.html 

main.py - Main operational file for running FastAPI.

# How to run
Create virtual environment

Activate virtual environment

Install requirements pip3 install -r requirements.txt

Run project python3 -m uvicorn main:app --reload
