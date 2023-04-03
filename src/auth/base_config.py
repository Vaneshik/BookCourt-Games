from fastapi_users.authentication import AuthenticationBackend, JWTStrategy, CookieTransport

cookie_transport = CookieTransport(cookie_name="session")

SECRET = "SECRET"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600*24)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
