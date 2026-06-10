from typing import Optional
from pydantic import BaseModel


class VaccinationResponse(BaseModel):
    id: int
    vaccination_date: str
    vaccination_next_date: str
    batch: str
    notes: Optional[str]
    pet_id: int
    pet_name: str
    species_name: str
    vaccine_id: int
    vaccine_name: str
    vaccine_disease: str
    vaccine_manufacturer: str
    vet_full_name: str
