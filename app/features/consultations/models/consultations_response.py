from typing import Optional
from pydantic import BaseModel


class ConsultationResponse(BaseModel):
    consultation_id: int
    consultation_date: str
    consultation_weight: float
    consultation_temperature: float
    consultation_diagnosis: str
    consultation_treatment: str
    consultation_notes: Optional[str]
    pet_id: int
    pet_name: str
    species_name: str
    breed_name: str
    owner_id: int
    owner_full_name: str
    owner_phone: str
    vet_id: int
    vet_name: str
    appointment_id: Optional[int]
