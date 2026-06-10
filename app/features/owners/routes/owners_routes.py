from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.middlewares.roles_middleware import require_roles
from app.features.owners.controllers.owners_controller import OwnersController
from app.features.owners.models.owners_schema import CreateOwnerSchema, FilterOwnersSchema, UpdateOwnerSchema

router = APIRouter(prefix="/api/owners", tags=["Propietarios"])


@router.get(
    "/",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Veterinario", "Recepcionista"]))
    ]
)
def get_all_owners(filters: FilterOwnersSchema = Depends()):
    return OwnersController.get_all_owners(filters)


@router.get(
    "/{owner_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Veterinario", "Recepcionista"]))
    ]
)
def get_owner_by_id(owner_id: int):
    return OwnersController.get_owner_by_id(owner_id)


@router.post(
    "/create",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Recepcionista"]))
    ]
)
def create_owner(owner_data: CreateOwnerSchema):
    return OwnersController.create_owner(owner_data)


@router.put(
    "/update/{owner_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin", "Recepcionista"]))
    ]
)
def update_owner(owner_id: int, owner_data: UpdateOwnerSchema):
    return OwnersController.update_owner(owner_id, owner_data)


@router.put(
    "/disable/{owner_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def disable_owner(owner_id: int):
    return OwnersController.disable_owner(owner_id)


@router.put(
    "/enable/{owner_id}",
    dependencies=[
        Depends(RateLimiter(times=30, seconds=60)),
        Depends(require_roles(["Admin"]))
    ]
)
def enable_owner(owner_id: int):
    return OwnersController.enable_owner(owner_id)
