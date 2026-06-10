from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.middlewares.roles_middleware import require_roles
from app.features.vaccinations.controllers.vaccinations_controller import VaccinationsController
from app.features.vaccinations.models.vaccinations_schema import CreateVaccinationSchema, FilterVaccinationsSchema

router = APIRouter(prefix="/api/vaccinations", tags=["Vacunaciones"])

_all_roles = ["Admin", "Veterinario", "Recepcionista"]
_vet_roles = ["Admin", "Veterinario"]


@router.get(
    "/",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def get_all_vaccinations(filters: FilterVaccinationsSchema = Depends()):
    return VaccinationsController.get_all_vaccinations(filters)


@router.get(
    "/{vaccination_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def get_vaccination_by_id(vaccination_id: int):
    return VaccinationsController.get_vaccination_by_id(vaccination_id)


@router.post(
    "/create",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_vet_roles))]
)
def create_vaccination(data_in: CreateVaccinationSchema):
    return VaccinationsController.create_vaccination(data_in)
