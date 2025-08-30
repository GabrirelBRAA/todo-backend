import secrets
from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error
from psycopg2.errors import InvalidPassword
from uuid import uuid4, UUID


def make_token():
    """
    Used to make a new session token
    """
    return secrets.token_urlsafe(16)

def make_uuid4():
    return str(uuid4())

def is_valid_uuid(val):
    try:
        UUID(str(val))
        return True
    except ValueError:
        return False

def hash_password(password):
    ph = PasswordHasher()
    hashed_password = ph.hash(password)
    return hashed_password

def verify_password(password: str, hashed_password: str) -> bool:
    ph = PasswordHasher()
    try:
        ph.verify(hashed_password, password)
    except Argon2Error as e:
        return False
    return True