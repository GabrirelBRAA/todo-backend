from pydantic import BaseModel, field_serializer, field_validator, Field
from typing import Literal, Optional
from custom_types.types import UserRole

class User(BaseModel):
    id: Optional[str] = None
    username: str
    firstname: str
    lastname: str
    hash: Optional[str] = Field(None, exclude=True)
    role: UserRole | str | int

    @field_serializer("role")
    def serialize_role(self, role: UserRole) -> str:
        return role.name

    @field_validator("role")
    def validate_role(cls, value: int | str | UserRole):
        if isinstance(value, UserRole):
            return value
        elif isinstance(value, str):
            return UserRole[value]
        else:
            return UserRole(value)

class UserInput(BaseModel):
    firstname: str
    lastname: str
    username: str
    password: str
    role: Literal["ADMIN", "NORMAL", "SUPERADMIN"] = "NORMAL"

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        else: return value


#TAGS

#ITEM
class Item(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    user_id: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Item Title",
                    "description": "Item Description",
                }
            ]
        }
    }