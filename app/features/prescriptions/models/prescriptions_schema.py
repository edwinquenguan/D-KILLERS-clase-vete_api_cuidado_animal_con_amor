from typing import Optional, List
from pydantic import BaseModel


class PrescriptionDetailSchema(BaseModel):
    medication_id: int
    dose: str
    frequency: str
    duration: str
    instructions: Optional[str] = None


class FilterPrescriptionsSchema(BaseModel):
    consultation_id: Optional[int] = None
    pet_id: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class CreatePrescriptionSchema(BaseModel):
    consultation_id: int
    notes: Optional[str] = None
    details: List[PrescriptionDetailSchema]
