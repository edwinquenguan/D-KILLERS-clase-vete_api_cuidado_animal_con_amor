from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.features.dashboard.controllers.dashboard_controller import DashboardController
from app.middlewares.roles_middleware import require_roles

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

_admin = ["Admin"]


@router.get(
    "/pets-count",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_admin))]
)
def get_pets_count():
    return DashboardController.get_pets_count()


@router.get(
    "/owners-count",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_admin))]
)
def get_owners_count():
    return DashboardController.get_owners_count()


@router.get(
    "/appointments-by-status",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_admin))]
)
def get_appointments_by_status():
    return DashboardController.get_appointments_by_status()


@router.get(
    "/consultations-by-month",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_admin))]
)
def get_consultations_by_month():
    return DashboardController.get_consultations_by_month()


@router.get(
    "/pets-by-species",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_admin))]
)
def get_pets_by_species():
    return DashboardController.get_pets_by_species()


@router.get(
    "/vaccinations-by-month",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_admin))]
)
def get_vaccinations_by_month():
    return DashboardController.get_vaccinations_by_month()


@router.get(
    "/top-vets",
    dependencies=[Depends(RateLimiter(times=30, seconds=60)), Depends(require_roles(_admin))]
)
def get_top_vets():
    return DashboardController.get_top_vets()
