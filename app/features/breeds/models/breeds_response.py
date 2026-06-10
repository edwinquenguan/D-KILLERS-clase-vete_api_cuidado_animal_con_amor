from pydantic import BaseModel


class BreedResponse(BaseModel):
    breed_id: int
    species_id: int
    species_name: str
    breed_name: str
    breed_status: int
