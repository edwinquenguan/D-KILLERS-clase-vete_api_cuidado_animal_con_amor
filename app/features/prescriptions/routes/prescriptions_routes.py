from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.middlewares.roles_middleware import require_roles
from app.features.prescriptions.controllers.prescriptions_controller import PrescriptionsController
from app.features.prescriptions.models.prescriptions_schema import CreatePrescriptionSchema, FilterPrescriptionsSchema

router = APIRouter(prefix="/api/prescriptions", tags=["Recetas"])

_all_roles = ["Admin", "Veterinario", "Recepcionista"]
_vet_roles = ["Admin", "Veterinario"]


@router.get(
    "/",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def get_all_prescriptions(filters: FilterPrescriptionsSchema = Depends()):
    return PrescriptionsController.get_all_prescriptions(filters)


@router.get(
    "/{prescription_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def get_prescription_by_id(prescription_id: int):
    return PrescriptionsController.get_prescription_by_id(prescription_id)


@router.post(
    "/create",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_vet_roles))]
)
def create_prescription(data_in: CreatePrescriptionSchema):
    return PrescriptionsController.create_prescription(data_in)
