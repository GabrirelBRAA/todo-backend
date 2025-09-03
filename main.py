import secrets
from typing import Annotated, List

from fastapi import FastAPI, Response, Depends, Cookie, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status
from utils import make_token, hash_password, make_uuid4, verify_password, is_valid_uuid
from db import save_user_to_db, get_user_by_username, get_items_from_db, save_item_in_db
from models.models import User, UserRole, UserInput, Item
from fastapi.middleware.cors import CORSMiddleware


import redis
redis_connection = redis.Redis(host='localhost', port=6379, decode_responses=True)

app = FastAPI()
origins = ['http://localhost:5173']
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_session_id(response: Response,session_id: Annotated[str | None, Cookie()]) -> User | None:
    if not session_id:
        return None
    else:
        user = redis_connection.hgetall(session_id)
        if not user:
            response.delete_cookie(session_id)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return User(**user)

@app.post("/login", status_code=status.HTTP_200_OK)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),):
    user = get_user_by_username(form_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if verify_password(form_data.password, user.hash):
        session_id = make_token()
        redis_connection.hset(session_id, mapping=user.model_dump())
        response.set_cookie('session_id', session_id, samesite='none', secure=True, expires=3600, httponly=True)
        return {"message": "Login Successs"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

@app.get("/me/")
async def say_user(session: Annotated[User | None, Depends(get_current_session_id)]):
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return session


@app.put("/users/")
async def update_user(user: User):
    pass

@app.patch("/users/password/")
async def change_password(password: str):
    pass

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    pass

@app.post("/users/")
async def create_user(user: UserInput):
    hashed_password = hash_password(user.password)
    new_user = User(**user.model_dump())
    new_user.hash = hashed_password
    new_user.id = make_uuid4()
    save_user_to_db(new_user)
    return user


@app.get("/tags/")
async def list_tags(search_string: str):
    pass

@app.post("/tags/")
async def create_tag(user: UserInput):
    pass

@app.post("/items/")
async def create_item(item: Item, user: Annotated[User | None, Depends(get_current_session_id)]):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    item.user_id = user.id
    if not item.id or not is_valid_uuid(item.id):
        item.id = make_uuid4()
    save_item_in_db(item)
    return item

@app.get("/items/")
async def list_items(user: Annotated[User | None, Depends(get_current_session_id)], limit: int = 10, page: int = 0) -> List[Item]:
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_id = user.id
    items = get_items_from_db(user_id, limit, page)
    return items
