from typing import Optional
from pydantic import BaseModel


class FilterVaccinationsSchema(BaseModel):
    pet_id: Optional[int] = None
    vaccine_id: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class CreateVaccinationSchema(BaseModel):
    pet_id: int
    vaccine_id: int
    user_id: int
    vaccination_date: str
    vaccination_next_date: str
    batch: str
    notes: Optional[str] = None
