from typing import Optional
from pydantic import BaseModel, EmailStr

class LoginModel(BaseModel):
    email: EmailStr
    password: str

class RegisterClientModel(BaseModel):
    name: str
    first_surname: str
    second_surname: Optional[str] = ""
    email: EmailStr
    phone: str
    password: str
    city: int
    address: Optional[str] = "Sin especificar"

class RecoverPassword(BaseModel):
    email: EmailStr

class VerifyRoleModel(BaseModel):
    roles: list[str]