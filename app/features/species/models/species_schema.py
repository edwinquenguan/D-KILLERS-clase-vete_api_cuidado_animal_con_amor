from typing import Optional
from pydantic import BaseModel


class FilterSpeciesSchema(BaseModel):
    status: Optional[int] = None


class CreateSpeciesSchema(BaseModel):
    name: str


class UpdateSpeciesSchema(BaseModel):
    name: Optional[str] = None
