from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.middlewares.roles_middleware import require_roles
from app.middlewares.jwt_middleware import verify_jwt
from app.features.pets.controllers.pets_controller import PetsController
from app.features.pets.models.pets_schema import CreatePetSchema, FilterPetsSchema, RegisterMyPetSchema, UpdatePetSchema

router = APIRouter(prefix="/api/pets", tags=["Mascotas"])

_all_roles = ["Admin", "Veterinario", "Recepcionista"]


@router.get(
    "/my",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(["Cliente"]))]
)
def get_my_pets(payload: dict = Depends(verify_jwt)):
    user_id = int(payload.get("user_id", 0))
    return PetsController.get_my_pets(user_id)


@router.post(
    "/my/register",
    dependencies=[Depends(RateLimiter(times=10, seconds=60)), Depends(require_roles(["Cliente"]))]
)
def register_my_pet(pet_data: RegisterMyPetSchema, payload: dict = Depends(verify_jwt)):
    user_id = int(payload.get("user_id", 0))
    return PetsController.register_my_pet(user_id, pet_data)


@router.get(
    "/",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def get_all_pets(filters: FilterPetsSchema = Depends()):
    return PetsController.get_all_pets(filters)


@router.get(
    "/{pet_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def get_pet_by_id(pet_id: int):
    return PetsController.get_pet_by_id(pet_id)


@router.post(
    "/create",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def create_pet(pet_data: CreatePetSchema):
    return PetsController.create_pet(pet_data)


@router.put(
    "/update/{pet_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_all_roles))]
)
def update_pet(pet_id: int, pet_data: UpdatePetSchema):
    return PetsController.update_pet(pet_id, pet_data)


@router.put(
    "/disable/{pet_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(["Admin"]))]
)
def disable_pet(pet_id: int):
    return PetsController.disable_pet(pet_id)


@router.put(
    "/enable/{pet_id}",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(["Admin"]))]
)
def enable_pet(pet_id: int):
    return PetsController.enable_pet(pet_id)
