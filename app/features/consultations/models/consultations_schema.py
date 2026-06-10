from typing import Optional
from decimal import Decimal
from pydantic import BaseModel


class FilterConsultationsSchema(BaseModel):
    pet_id: Optional[int] = None
    user_id: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class CreateConsultationSchema(BaseModel):
    pet_id: int
    user_id: int
    appointment_id: Optional[int] = None
    weight: Decimal
    temperature: Decimal
    diagnosis: str
    treatment: str
    notes: Optional[str] = None


class UpdateConsultationSchema(BaseModel):
    weight: Optional[Decimal] = None
    temperature: Optional[Decimal] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None
