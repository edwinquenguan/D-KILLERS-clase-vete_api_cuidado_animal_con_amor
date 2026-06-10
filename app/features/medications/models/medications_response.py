from pydantic import BaseModel


class MedicationResponse(BaseModel):
    id: int
    name: str
    presentation: str
    unit: str
    status: int
