from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi_users import FastAPIUsers

from auth.base_config import auth_backend
from auth.models import User
from auth.schemas import UserCreate, UserRead
from auth.manager import get_user_manager

from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException

from ml.reco2.reco2 import getAns as getAns_game2
from src.ml.reco2.game13 import getAns3 as getAns_game3
# from pages.router import router as router_pages

app = FastAPI(title="BookCourt Games")


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    if exc.status_code == 401:
        return RedirectResponse("/login", status_code=302)
    return await http_exception_handler(request, exc)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

# app.include_router(router_pages)


@app.get("/")
async def get_index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login")
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register")
async def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/hotcold")
async def get_register_page(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse("hotcold.html", {"request": request})


@app.post("/hotcold/getAns")
async def get_register_page(request: Request, user: User = Depends(current_user)):
    req_json = await request.json()
    print(req_json)
    return {"status": "ok"}


@app.get("/math")
async def get_register_page(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse("math.html", {"request": request})


@app.post("/math/getAns")
async def get_register_page(request: Request, user: User = Depends(current_user)):
    req_json = await request.json()
    ans = getAns_game2(req_json)
    return {"ans": ans}


@app.get("/history")
async def get_register_page(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse("history.html", {"request": request})


@app.post("/history/getAns")
async def get_register_page(request: Request, user: User = Depends(current_user)):
    req_json = await request.json()
    # print(req_json)
    ans = getAns_game3(req_json)
    return {"ans": ans}
