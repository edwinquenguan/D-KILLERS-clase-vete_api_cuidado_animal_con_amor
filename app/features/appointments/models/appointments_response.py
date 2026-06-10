from pydantic import BaseModel


class AppointmentResponse(BaseModel):
    appointment_id: int
    appointment_date: str
    appointment_time: str
    appointment_reason: str
    appointment_status: int
    appointment_date_created: str
    pet_id: int
    pet_name: str
    species_name: str
    owner_id: int
    owner_full_name: str
    owner_phone: str
    vet_id: int
    vet_name: str
