from fastapi import HTTPException
from app.features.pets.services.pets_service import PetsService
from app.features.pets.models.pets_schema import CreatePetSchema, FilterPetsSchema, UpdatePetSchema


class PetsController:

    @staticmethod
    def get_all_pets(filters: FilterPetsSchema):
        error, data = PetsService.get_all_pets(filters)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_pet_by_id(pet_id: int):
        error, data = PetsService.get_pet_by_id(pet_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def create_pet(pet_data: CreatePetSchema):
        error, success, message = PetsService.create_pet(pet_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def update_pet(pet_id: int, pet_data: UpdatePetSchema):
        error, success, message = PetsService.update_pet(pet_id, pet_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def disable_pet(pet_id: int):
        error, success, message = PetsService.disable_pet(pet_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def enable_pet(pet_id: int):
        error, success, message = PetsService.enable_pet(pet_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"success": success, "message": message}
