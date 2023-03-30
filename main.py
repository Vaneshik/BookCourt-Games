from fastapi import FastAPI, Response, Request
from fastapi.responses import PlainTextResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import uvicorn
import sqlite3
from os.path import isfile

from hashlib import sha256, md5

db_path = "data.db"


def init_db(db_name: str) -> None:
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS users
            ([id] INTEGER PRIMARY KEY,
            [email] TEXT NOT NULL UNIQUE,
            [password] TEXT NOT NULL)
            """)
    con.commit()
    con.close()


def connect_db(db_name: str) -> sqlite3.Connection | None:
    con = None
    try:
        con = sqlite3.connect(db_name)
    except Exception as e:
        print(e)
    return con


async def create_user(con: sqlite3.Connection, email: str, password: str) -> int | None:
    command = "INSERT INTO users (email, password) VALUES(?,?)"
    cur = con.cursor()
    cur.execute(command, (email, password))
    con.commit()
    return cur.lastrowid


async def auth_user(con: sqlite3.Connection, email: str, hashed_password: str) -> int | None:
    command = "SELECT id FROM users WHERE email = ? AND password = ?"
    cur = con.cursor()
    user_id = cur.execute(command, (email, hashed_password)).fetchone()
    if user_id != None:
        return user_id[0]
    return None

# Database connection
if not isfile(db_path):
    init_db(db_path)
con_db = connect_db(db_path)


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=PlainTextResponse)
async def index():
    return PlainTextResponse("Привет! Сыграй в наши игры!")


@app.get("/register", response_class=HTMLResponse)
async def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register", response_class=PlainTextResponse)
async def register_post(request: Request):
    form = await request.form()
    email = form["email"]
    plain_password = form["passwd"]
    try:
        hashed_password = sha256(plain_password.encode()).hexdigest()
        user_id = await create_user(con_db, email, hashed_password)
        return PlainTextResponse(f"User {user_id} succesful registered")
    except Exception as e:
        return PlainTextResponse(f"Error {e}")


@app.get("/login")
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=PlainTextResponse)
async def login_post(request: Request):
    form = await request.form()
    email = form["email"]
    plain_password = form["passwd"]
    try:
        hashed_password = sha256(plain_password.encode()).hexdigest()
        user_id = await auth_user(con_db, email, hashed_password)
        if user_id is None:
            return PlainTextResponse("Wrong email or password")
        else:
            cookie_data = (str(user_id)+email+hashed_password).encode()
            cookie = md5(cookie_data).hexdigest()
            response = PlainTextResponse(f"Login succesfull! Hello {email}!")
            response.set_cookie(key="sess_id", value=cookie)
            return response

    except Exception as e:
        return PlainTextResponse(f"Error {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
