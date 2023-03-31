from fastapi import FastAPI, Response, Request, Form, status
from fastapi.responses import PlainTextResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from typing import Annotated

from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from auth.schemas import UserCreate, UserRead
from auth.manager import get_user_manager
from auth.database import User


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


# templates = Jinja2Templates(directory="templates")


# @app.get("/", response_class=PlainTextResponse)
# async def index():
#     return PlainTextResponse("Привет! Сыграй в наши игры!")


# @app.get("/register", response_class=HTMLResponse)
# async def register_get(request: Request):
#     return templates.TemplateResponse("register.html", {"request": request})


# @app.post("/register", response_class=PlainTextResponse)
# async def register_post(email: Annotated[str, Form()], password: Annotated[str, Form()]):
#     try:
#         hashed_password = sha256(password.encode()).hexdigest()
#         user_id = await create_user(con_db, email, hashed_password)
#         return PlainTextResponse(f"User {user_id} succesful registered")
#     except Exception as e:
#         return PlainTextResponse(f"Error {e}")


# @app.get("/login")
# async def login_get(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})


# @app.post("/login", response_class=PlainTextResponse)
# async def login_post(email: Annotated[str, Form()], password: Annotated[str, Form()]):
#     try:
#         hashed_password = sha256(password.encode()).hexdigest()
#         user_id = await auth_user(con_db, email, hashed_password)
#         if user_id is None:
#             return PlainTextResponse("Wrong email or password")
#         else:
#             cookie_data = (str(user_id)+email+hashed_password).encode()
#             cookie = md5(cookie_data).hexdigest()

#             response = PlainTextResponse(f"Login succesfull! Hello {email}!")
#             response.set_cookie(key="sess_id", value=cookie)
#             return response

#     except Exception as e:
#         return PlainTextResponse(f"Error {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
