from pydantic import BaseModel


class DashboardCountResponse(BaseModel):
    total: int
    new_this_month: int


class AppointmentsByStatusResponse(BaseModel):
    status: int
    total: int


class ConsultationsByMonthResponse(BaseModel):
    year: int
    month: int
    total: int


class PetsBySpeciesResponse(BaseModel):
    species_name: str
    total: int


class VaccinationsByMonthResponse(BaseModel):
    year: int
    month: int
    total: int


class TopVetsResponse(BaseModel):
    vet_name: str
    consultations: int
