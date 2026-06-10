from fastapi import HTTPException
from app.features.breeds.services.breeds_service import BreedsService
from app.features.breeds.models.breeds_schema import CreateBreedSchema, FilterBreedsSchema, UpdateBreedSchema


class BreedsController:

    @staticmethod
    def get_all_breeds(filters: FilterBreedsSchema):
        error, data = BreedsService.get_all_breeds(filters)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_breed_by_id(breed_id: int):
        error, data = BreedsService.get_breed_by_id(breed_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def create_breed(breed_data: CreateBreedSchema):
        error, success, message = BreedsService.create_breed(breed_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def update_breed(breed_id: int, breed_data: UpdateBreedSchema):
        error, success, message = BreedsService.update_breed(breed_id, breed_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def disable_breed(breed_id: int):
        error, success, message = BreedsService.disable_breed(breed_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def enable_breed(breed_id: int):
        error, success, message = BreedsService.enable_breed(breed_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"success": success, "message": message}
