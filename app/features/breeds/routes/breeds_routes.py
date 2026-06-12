from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.middlewares.roles_middleware import require_roles
from app.features.breeds.controllers.breeds_controller import BreedsController
from app.features.breeds.models.breeds_schema import CreateBreedSchema, FilterBreedsSchema, UpdateBreedSchema

router = APIRouter(prefix="/api/breeds", tags=["Razas"])


@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Veterinario", "Recepcionista", "Cliente"]))
    ]
)
def get_all_breeds(filters: FilterBreedsSchema = Depends()):
    return BreedsController.get_all_breeds(filters)


@router.get(
    "/{breed_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Veterinario", "Recepcionista"]))
    ]
)
def get_breed_by_id(breed_id: int):
    return BreedsController.get_breed_by_id(breed_id)


@router.post(
    "/create",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def create_breed(breed_data: CreateBreedSchema):
    return BreedsController.create_breed(breed_data)


@router.put(
    "/update/{breed_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def update_breed(breed_id: int, breed_data: UpdateBreedSchema):
    return BreedsController.update_breed(breed_id, breed_data)


@router.put(
    "/disable/{breed_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def disable_breed(breed_id: int):
    return BreedsController.disable_breed(breed_id)


@router.put(
    "/enable/{breed_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def enable_breed(breed_id: int):
    return BreedsController.enable_breed(breed_id)
