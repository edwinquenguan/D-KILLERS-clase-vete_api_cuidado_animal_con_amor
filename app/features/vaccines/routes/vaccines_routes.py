from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.middlewares.roles_middleware import require_roles
from app.features.vaccines.controllers.vaccines_controller import VaccinesController
from app.features.vaccines.models.vaccines_schema import CreateVaccineSchema, FilterVaccinesSchema, UpdateVaccineSchema

router = APIRouter(prefix="/api/vaccines", tags=["Vacunas"])

_all_roles = ["Admin", "Veterinario", "Recepcionista"]


@router.get(
    "/",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def get_all_vaccines(filters: FilterVaccinesSchema = Depends()):
    return VaccinesController.get_all_vaccines(filters)


@router.get(
    "/{vaccine_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def get_vaccine_by_id(vaccine_id: int):
    return VaccinesController.get_vaccine_by_id(vaccine_id)


@router.post(
    "/create",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(["Admin"]))]
)
def create_vaccine(vaccine_data: CreateVaccineSchema):
    return VaccinesController.create_vaccine(vaccine_data)


@router.put(
    "/update/{vaccine_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(["Admin"]))]
)
def update_vaccine(vaccine_id: int, vaccine_data: UpdateVaccineSchema):
    return VaccinesController.update_vaccine(vaccine_id, vaccine_data)


@router.put(
    "/disable/{vaccine_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(["Admin"]))]
)
def disable_vaccine(vaccine_id: int):
    return VaccinesController.disable_vaccine(vaccine_id)


@router.put(
    "/enable/{vaccine_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(["Admin"]))]
)
def enable_vaccine(vaccine_id: int):
    return VaccinesController.enable_vaccine(vaccine_id)
