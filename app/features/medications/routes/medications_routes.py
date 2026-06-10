from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.middlewares.roles_middleware import require_roles
from app.features.medications.controllers.medications_controller import MedicationsController
from app.features.medications.models.medications_schema import CreateMedicationSchema, FilterMedicationsSchema, UpdateMedicationSchema

router = APIRouter(prefix="/api/medications", tags=["Medicamentos"])

_all_roles = ["Admin", "Veterinario", "Recepcionista"]


@router.get(
    "/",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def get_all_medications(filters: FilterMedicationsSchema = Depends()):
    return MedicationsController.get_all_medications(filters)


@router.get(
    "/{medication_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def get_medication_by_id(medication_id: int):
    return MedicationsController.get_medication_by_id(medication_id)


@router.post(
    "/create",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(["Admin"]))]
)
def create_medication(data_in: CreateMedicationSchema):
    return MedicationsController.create_medication(data_in)


@router.put(
    "/update/{medication_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(["Admin"]))]
)
def update_medication(medication_id: int, data_in: UpdateMedicationSchema):
    return MedicationsController.update_medication(medication_id, data_in)


@router.put(
    "/disable/{medication_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(["Admin"]))]
)
def disable_medication(medication_id: int):
    return MedicationsController.disable_medication(medication_id)


@router.put(
    "/enable/{medication_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(["Admin"]))]
)
def enable_medication(medication_id: int):
    return MedicationsController.enable_medication(medication_id)
