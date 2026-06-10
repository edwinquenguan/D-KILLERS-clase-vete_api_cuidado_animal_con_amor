from pydantic import BaseModel


class VaccineResponse(BaseModel):
    id: int
    species_id: int
    species_name: str
    name: str
    disease: str
    manufacturer: str
    status: int
