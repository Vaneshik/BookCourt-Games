from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from auth.base_config import auth_backend
from auth.models import User

from auth.schemas import UserCreate, UserRead
from auth.manager import get_user_manager

from pages.router import router as router_pages

app = FastAPI(title="BookCourt Games")


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

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

app.include_router(router_pages)
