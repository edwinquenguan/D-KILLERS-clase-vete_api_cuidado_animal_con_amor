from fastapi import APIRouter, Depends
from app.middlewares.roles_middleware import require_roles
from app.features.reports.controllers.reports_controller import ReportsController

router = APIRouter(prefix="/api/reports", tags=["Reportes"])

_admin = ["Admin"]


# ------------ MASCOTAS ------------
@router.get("/pets-by-species/{period}", dependencies=[Depends(require_roles(_admin))])
def get_pets_by_species(period: str = "30d"):
    return ReportsController.get_pets_by_species(period)


@router.get("/pets-growth/{period}", dependencies=[Depends(require_roles(_admin))])
def get_pets_growth(period: str = "30d"):
    return ReportsController.get_pets_growth(period)


# ------------ CITAS ------------
@router.get("/appointments-growth/{period}", dependencies=[Depends(require_roles(_admin))])
def get_appointments_growth(period: str = "30d"):
    return ReportsController.get_appointments_growth(period)


@router.get("/appointments-by-status", dependencies=[Depends(require_roles(_admin))])
def get_appointments_by_status():
    return ReportsController.get_appointments_by_status()


# ------------ CONSULTAS ------------
@router.get("/consultations-growth/{period}", dependencies=[Depends(require_roles(_admin))])
def get_consultations_growth(period: str = "30d"):
    return ReportsController.get_consultations_growth(period)


@router.get("/recent-consultations", dependencies=[Depends(require_roles(_admin))])
def get_recent_consultations():
    return ReportsController.get_recent_consultations()


# ------------ VACUNACIONES ------------
@router.get("/vaccinations-growth/{period}", dependencies=[Depends(require_roles(_admin))])
def get_vaccinations_growth(period: str = "30d"):
    return ReportsController.get_vaccinations_growth(period)


@router.get("/vaccinations-by-vaccine/{period}", dependencies=[Depends(require_roles(_admin))])
def get_vaccinations_by_vaccine(period: str = "30d"):
    return ReportsController.get_vaccinations_by_vaccine(period)


# ------------ PROPIETARIOS ------------
@router.get("/owners-growth/{period}", dependencies=[Depends(require_roles(_admin))])
def get_owners_growth(period: str = "30d"):
    return ReportsController.get_owners_growth(period)
