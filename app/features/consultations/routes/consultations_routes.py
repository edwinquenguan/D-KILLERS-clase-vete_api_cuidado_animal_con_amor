from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.middlewares.roles_middleware import require_roles
from app.features.consultations.controllers.consultations_controller import ConsultationsController
from app.features.consultations.models.consultations_schema import CreateConsultationSchema, FilterConsultationsSchema, UpdateConsultationSchema

router = APIRouter(prefix="/api/consultations", tags=["Consultas"])

_vet_roles = ["Admin", "Veterinario"]
_all_roles = ["Admin", "Veterinario", "Recepcionista"]


@router.get(
    "/",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def get_all_consultations(filters: FilterConsultationsSchema = Depends()):
    return ConsultationsController.get_all_consultations(filters)


@router.get(
    "/{consultation_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def get_consultation_by_id(consultation_id: int):
    return ConsultationsController.get_consultation_by_id(consultation_id)


@router.post(
    "/create",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_vet_roles))]
)
def create_consultation(data_in: CreateConsultationSchema):
    return ConsultationsController.create_consultation(data_in)


@router.put(
    "/update/{consultation_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_vet_roles))]
)
def update_consultation(consultation_id: int, data_in: UpdateConsultationSchema):
    return ConsultationsController.update_consultation(consultation_id, data_in)
