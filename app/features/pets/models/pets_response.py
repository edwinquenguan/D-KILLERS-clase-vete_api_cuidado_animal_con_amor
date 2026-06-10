from pydantic import BaseModel


class PetResponse(BaseModel):
    pet_id: int
    name: str
    birthdate: str
    sex: str
    color: str
    weight: float
    pet_status: int
    pet_date: str
    owner_id: int
    owner_name: str
    owner_phone: str
    owner_email: str
    species_id: int
    species_name: str
    breed_id: int
    breed_name: str
