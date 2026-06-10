from typing import Optional
from pydantic import BaseModel


class FilterBreedsSchema(BaseModel):
    species_id: Optional[int] = None
    status: Optional[int] = None


class CreateBreedSchema(BaseModel):
    species_id: int
    name: str


class UpdateBreedSchema(BaseModel):
    name: Optional[str] = None
