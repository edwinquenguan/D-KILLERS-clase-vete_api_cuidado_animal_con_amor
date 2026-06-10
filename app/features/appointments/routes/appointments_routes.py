from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.middlewares.roles_middleware import require_roles
from app.features.appointments.controllers.appointments_controller import AppointmentsController
from app.features.appointments.models.appointments_schema import CreateAppointmentSchema, FilterAppointmentsSchema, UpdateAppointmentSchema

router = APIRouter(prefix="/api/appointments", tags=["Citas"])

_all_roles = ["Admin", "Veterinario", "Recepcionista"]


@router.get(
    "/",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def get_all_appointments(filters: FilterAppointmentsSchema = Depends()):
    return AppointmentsController.get_all_appointments(filters)


@router.get(
    "/{appointment_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def get_appointment_by_id(appointment_id: int):
    return AppointmentsController.get_appointment_by_id(appointment_id)


@router.post(
    "/create",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def create_appointment(appt_data: CreateAppointmentSchema):
    return AppointmentsController.create_appointment(appt_data)


@router.put(
    "/update/{appointment_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def update_appointment(appointment_id: int, appt_data: UpdateAppointmentSchema):
    return AppointmentsController.update_appointment(appointment_id, appt_data)


@router.put(
    "/cancel/{appointment_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def cancel_appointment(appointment_id: int):
    return AppointmentsController.cancel_appointment(appointment_id)
