from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="", tags=["Pages"])

templates = Jinja2Templates(directory="templates")

@router.get("/")
def get_index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login")
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register")
def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
