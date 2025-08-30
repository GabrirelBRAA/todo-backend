from sqlalchemy import create_engine, text, insert, Table, Column, MetaData, String, Integer, select, ForeignKey
from starlette import status

from models.models import User, Item
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException

engine = create_engine("postgresql://postgres:mysecretpassword@localhost:3000/postgres", echo=True)
metadata = MetaData()

users = Table("user",
              metadata,
              Column("id", String, primary_key=True),
              Column("firstname", String),
              Column("lastname", String),
              Column("role", Integer),
              Column("hash", String),
              Column("username", String),
              )

items = Table("item",
              metadata,
              Column("id", String, primary_key=True),
              Column("user_id", String, ForeignKey(users.columns.id)),
              Column("title", String),
              Column("description", String),
              )



def save_user_to_db(user: User):
    try:
        with engine.connect() as connection:
            connection.execute(users.insert(), {'id': user.id,
                                                'firstname': user.firstname,
                                                'lastname': user.lastname,
                                                'role': user.role,
                                                'hash': user.hash,
                                                'username': user.username})
            connection.commit()
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str("Username already exists."))

def get_user_by_username(username: str) -> User | None:
    with engine.connect() as connection:
        stmt = select(users).where(users.columns.username == username).limit(1)
        result = connection.execute(stmt).first()
        if not result:
            return None
        else: return User(**dict(result._mapping))

def save_item_in_db(item: Item):
    with engine.connect() as connection:
        connection.execute(items.insert(), item.model_dump())
        connection.commit()

def get_items_from_db(user_id: str, limit: int = 10, offset: int = 0) -> list[Item]:
    with engine.connect() as connection:
        stmt = select(items).where(items.columns.user_id == user_id).limit(limit).offset(offset)
        result = connection.execute(stmt).all()
        if not result:
            return []
        else:
            return [Item(**dict(item._mapping)) for item in result]
