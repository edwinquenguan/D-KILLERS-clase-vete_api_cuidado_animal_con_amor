from typing import Optional
from decimal import Decimal
from pydantic import BaseModel


class FilterPetsSchema(BaseModel):
    owner_id: Optional[int] = None
    species_id: Optional[int] = None
    status: Optional[int] = None


class CreatePetSchema(BaseModel):
    owner_id: int
    species_id: int
    breed_id: int
    name: str
    birthdate: str
    sex: str
    color: str
    weight: Decimal


class RegisterMyPetSchema(BaseModel):
    species_id: int
    breed_id: int
    name: str
    birthdate: str
    sex: str
    color: str
    weight: Decimal


class UpdatePetSchema(BaseModel):
    name: Optional[str] = None
    birthdate: Optional[str] = None
    sex: Optional[str] = None
    color: Optional[str] = None
    weight: Optional[Decimal] = None
    breed_id: Optional[int] = None
