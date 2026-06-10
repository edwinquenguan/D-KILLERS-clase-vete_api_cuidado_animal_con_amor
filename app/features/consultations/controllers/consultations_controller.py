from fastapi import HTTPException
from app.features.consultations.services.consultations_service import ConsultationsService
from app.features.consultations.models.consultations_schema import CreateConsultationSchema, FilterConsultationsSchema, UpdateConsultationSchema


class ConsultationsController:

    @staticmethod
    def get_all_consultations(filters: FilterConsultationsSchema):
        error, data = ConsultationsService.get_all_consultations(filters)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_consultation_by_id(consultation_id: int):
        error, data = ConsultationsService.get_consultation_by_id(consultation_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def create_consultation(data_in: CreateConsultationSchema):
        error, success, message = ConsultationsService.create_consultation(data_in)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def update_consultation(consultation_id: int, data_in: UpdateConsultationSchema):
        error, success, message = ConsultationsService.update_consultation(consultation_id, data_in)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}
