from fastapi import HTTPException
from app.features.vaccinations.services.vaccinations_service import VaccinationsService
from app.features.vaccinations.models.vaccinations_schema import CreateVaccinationSchema, FilterVaccinationsSchema


class VaccinationsController:

    @staticmethod
    def get_all_vaccinations(filters: FilterVaccinationsSchema):
        error, data = VaccinationsService.get_all_vaccinations(filters)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_vaccination_by_id(vaccination_id: int):
        error, data = VaccinationsService.get_vaccination_by_id(vaccination_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def create_vaccination(data_in: CreateVaccinationSchema):
        error, success, message = VaccinationsService.create_vaccination(data_in)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}
