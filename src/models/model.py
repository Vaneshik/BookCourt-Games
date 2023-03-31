from sqlalchemy import MetaData, Table, Column, Integer, String, ARRAY, Boolean

metadata = MetaData()

users = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False, unique=True),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
    Column("liked_books", ARRAY(Integer)),
)
