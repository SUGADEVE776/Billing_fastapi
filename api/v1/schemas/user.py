from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserBase(BaseModel):
    username: str = Field(max_length=255)
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    email: EmailStr
    phone_number: str

class UserCreate(UserBase):
    password: str


class UserCreateResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    access_token: str
    expiry: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserLoginSchema(BaseModel):
    id: str
    username: str
    email: EmailStr
    phone_number: str
    created_at: datetime
    updated_at: datetime


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None



class LoginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    expiry: datetime
    user: UserLoginSchema