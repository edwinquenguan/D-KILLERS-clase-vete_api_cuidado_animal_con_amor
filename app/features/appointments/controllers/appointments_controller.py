from fastapi import HTTPException
from app.features.appointments.services.appointments_service import AppointmentsService
from app.features.appointments.models.appointments_schema import CreateAppointmentSchema, FilterAppointmentsSchema, RequestAppointmentSchema, UpdateAppointmentSchema


class AppointmentsController:

    @staticmethod
    def get_all_appointments(filters: FilterAppointmentsSchema):
        error, data = AppointmentsService.get_all_appointments(filters)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_my_appointments(user_id: int):
        error, data = AppointmentsService.get_my_appointments(user_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_appointment_by_id(appointment_id: int):
        error, data = AppointmentsService.get_appointment_by_id(appointment_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def request_appointment(appt_data: RequestAppointmentSchema):
        error, success, message = AppointmentsService.request_appointment(appt_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def create_appointment(appt_data: CreateAppointmentSchema):
        error, success, message = AppointmentsService.create_appointment(appt_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def update_appointment(appointment_id: int, appt_data: UpdateAppointmentSchema):
        error, success, message = AppointmentsService.update_appointment(appointment_id, appt_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def cancel_appointment(appointment_id: int):
        error, success, message = AppointmentsService.cancel_appointment(appointment_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"success": success, "message": message}
