from typing import Optional
from pydantic import BaseModel


class FilterMedicationsSchema(BaseModel):
    status: Optional[int] = None


class CreateMedicationSchema(BaseModel):
    name: str
    presentation: str
    unit: str


class UpdateMedicationSchema(BaseModel):
    name: Optional[str] = None
    presentation: Optional[str] = None
    unit: Optional[str] = None
