from typing import Optional
from pydantic import BaseModel


class FilterAppointmentsSchema(BaseModel):
    pet_id: Optional[int] = None
    user_id: Optional[int] = None
    status: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class CreateAppointmentSchema(BaseModel):
    pet_id: int
    user_id: int
    appointment_date: str
    appointment_time: str
    reason: str


class UpdateAppointmentSchema(BaseModel):
    user_id: Optional[int] = None
    appointment_date: Optional[str] = None
    appointment_time: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[int] = None
