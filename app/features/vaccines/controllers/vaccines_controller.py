from fastapi import HTTPException
from app.features.vaccines.services.vaccines_service import VaccinesService
from app.features.vaccines.models.vaccines_schema import CreateVaccineSchema, FilterVaccinesSchema, UpdateVaccineSchema


class VaccinesController:

    @staticmethod
    def get_all_vaccines(filters: FilterVaccinesSchema):
        error, data = VaccinesService.get_all_vaccines(filters)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_vaccine_by_id(vaccine_id: int):
        error, data = VaccinesService.get_vaccine_by_id(vaccine_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def create_vaccine(vaccine_data: CreateVaccineSchema):
        error, success, message = VaccinesService.create_vaccine(vaccine_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def update_vaccine(vaccine_id: int, vaccine_data: UpdateVaccineSchema):
        error, success, message = VaccinesService.update_vaccine(vaccine_id, vaccine_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def disable_vaccine(vaccine_id: int):
        error, success, message = VaccinesService.disable_vaccine(vaccine_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def enable_vaccine(vaccine_id: int):
        error, success, message = VaccinesService.enable_vaccine(vaccine_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"success": success, "message": message}
