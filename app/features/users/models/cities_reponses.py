from pydantic import BaseModel

class CityResponse(BaseModel):
    city_id: int
    city_name: str
