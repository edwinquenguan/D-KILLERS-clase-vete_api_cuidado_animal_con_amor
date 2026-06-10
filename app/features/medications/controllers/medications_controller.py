from fastapi import HTTPException
from app.features.medications.services.medications_service import MedicationsService
from app.features.medications.models.medications_schema import CreateMedicationSchema, FilterMedicationsSchema, UpdateMedicationSchema


class MedicationsController:

    @staticmethod
    def get_all_medications(filters: FilterMedicationsSchema):
        error, data = MedicationsService.get_all_medications(filters)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_medication_by_id(medication_id: int):
        error, data = MedicationsService.get_medication_by_id(medication_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def create_medication(data_in: CreateMedicationSchema):
        error, success, message = MedicationsService.create_medication(data_in)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def update_medication(medication_id: int, data_in: UpdateMedicationSchema):
        error, success, message = MedicationsService.update_medication(medication_id, data_in)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def disable_medication(medication_id: int):
        error, success, message = MedicationsService.disable_medication(medication_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def enable_medication(medication_id: int):
        error, success, message = MedicationsService.enable_medication(medication_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"success": success, "message": message}
