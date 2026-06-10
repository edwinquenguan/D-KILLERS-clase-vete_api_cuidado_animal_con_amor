from typing import Optional
from pydantic import BaseModel


class FilterVaccinesSchema(BaseModel):
    species_id: Optional[int] = None
    status: Optional[int] = None


class CreateVaccineSchema(BaseModel):
    species_id: int
    name: str
    disease: str
    manufacturer: str


class UpdateVaccineSchema(BaseModel):
    name: Optional[str] = None
    disease: Optional[str] = None
    manufacturer: Optional[str] = None
