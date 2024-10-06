from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserAuth(BaseModel):
    email: str
    password: str

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    username: str
    names: str
    lastnames: str
    phone_number: str
    age: int
    birthday: date
    password: str

class User(UserBase):
    id: int
    names: str
    lastnames: str
    phone_number: str
    age: int
    birthday: date

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    success: bool = True
    user: User
    data: Optional[dict] = None
