from sqlalchemy import MetaData, Table, Column, Integer, String, ARRAY

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False, unique=True),
    Column("password", String, nullable=False),
    Column("liked_books", ARRAY(Integer)),
)