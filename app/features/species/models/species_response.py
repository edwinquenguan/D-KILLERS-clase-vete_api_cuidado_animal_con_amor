from pydantic import BaseModel


class SpeciesResponse(BaseModel):
    species_id: int
    species_name: str
    species_status: int
