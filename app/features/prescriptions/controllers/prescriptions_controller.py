from fastapi import HTTPException
from app.features.prescriptions.services.prescriptions_service import PrescriptionsService
from app.features.prescriptions.models.prescriptions_schema import CreatePrescriptionSchema, FilterPrescriptionsSchema


class PrescriptionsController:

    @staticmethod
    def get_all_prescriptions(filters: FilterPrescriptionsSchema):
        error, data = PrescriptionsService.get_all_prescriptions(filters)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_prescription_by_id(prescription_id: int):
        error, data = PrescriptionsService.get_prescription_by_id(prescription_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def create_prescription(data_in: CreatePrescriptionSchema):
        error, success, message = PrescriptionsService.create_prescription(data_in)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}
