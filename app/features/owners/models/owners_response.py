from pydantic import BaseModel


class OwnerResponse(BaseModel):
    owner_id: int
    name: str
    first_surname: str
    second_surname: str
    phone: str
    email: str
    address: str
    city_id: int
    city_name: str
    owner_status: int
    owner_date: str
