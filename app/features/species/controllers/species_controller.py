from fastapi import HTTPException
from app.features.species.services.species_service import SpeciesService
from app.features.species.models.species_schema import CreateSpeciesSchema, FilterSpeciesSchema, UpdateSpeciesSchema


class SpeciesController:

    @staticmethod
    def get_all_species(filters: FilterSpeciesSchema):
        error, data = SpeciesService.get_all_species(filters)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_species_by_id(species_id: int):
        error, data = SpeciesService.get_species_by_id(species_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def create_species(species_data: CreateSpeciesSchema):
        error, success, message = SpeciesService.create_species(species_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def update_species(species_id: int, species_data: UpdateSpeciesSchema):
        error, success, message = SpeciesService.update_species(species_id, species_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def disable_species(species_id: int):
        error, success, message = SpeciesService.disable_species(species_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def enable_species(species_id: int):
        error, success, message = SpeciesService.enable_species(species_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"success": success, "message": message}
