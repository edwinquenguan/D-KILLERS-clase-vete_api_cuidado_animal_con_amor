from typing import Optional, List
from pydantic import BaseModel


class PrescriptionDetailResponse(BaseModel):
    detail_id: int
    medication_name: str
    presentation: str
    unit: str
    dose: str
    frequency: str
    duration: str
    instructions: Optional[str]


class PrescriptionResponse(BaseModel):
    id: int
    date: str
    notes: Optional[str]
    consultation_id: int
    consultation_date: str
    pet_id: int
    pet_name: str
    owner_full_name: str
    vet_full_name: str
    details: List[PrescriptionDetailResponse]
