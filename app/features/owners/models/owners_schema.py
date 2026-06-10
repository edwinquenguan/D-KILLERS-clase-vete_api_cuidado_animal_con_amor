from typing import Optional
from pydantic import BaseModel, EmailStr


class FilterOwnersSchema(BaseModel):
    name_order: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[int] = None
    city: Optional[int] = None


class CreateOwnerSchema(BaseModel):
    name: str
    first_surname: str
    second_surname: str
    phone: str
    email: EmailStr
    address: str
    city: int


class UpdateOwnerSchema(BaseModel):
    name: Optional[str] = None
    first_surname: Optional[str] = None
    second_surname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[int] = None
