from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.middlewares.roles_middleware import require_roles
from app.features.species.controllers.species_controller import SpeciesController
from app.features.species.models.species_schema import CreateSpeciesSchema, FilterSpeciesSchema, UpdateSpeciesSchema

router = APIRouter(prefix="/api/species", tags=["Especies"])


@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Veterinario", "Recepcionista"]))
    ]
)
def get_all_species(filters: FilterSpeciesSchema = Depends()):
    return SpeciesController.get_all_species(filters)


@router.get(
    "/{species_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Veterinario", "Recepcionista"]))
    ]
)
def get_species_by_id(species_id: int):
    return SpeciesController.get_species_by_id(species_id)


@router.post(
    "/create",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def create_species(species_data: CreateSpeciesSchema):
    return SpeciesController.create_species(species_data)


@router.put(
    "/update/{species_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def update_species(species_id: int, species_data: UpdateSpeciesSchema):
    return SpeciesController.update_species(species_id, species_data)


@router.put(
    "/disable/{species_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def disable_species(species_id: int):
    return SpeciesController.disable_species(species_id)


@router.put(
    "/enable/{species_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def enable_species(species_id: int):
    return SpeciesController.enable_species(species_id)
