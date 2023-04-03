from fastapi import FastAPI
from fastapi_users import FastAPIUsers
import uvicorn

from auth.base_config import auth_backend
from auth.models import User

from auth.schemas import UserCreate, UserRead
from auth.manager import get_user_manager


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()
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