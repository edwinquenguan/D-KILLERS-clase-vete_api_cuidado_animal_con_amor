from fastapi import HTTPException
from app.features.dashboard.services.dashboard_service import DashboardService


class DashboardController:

    @staticmethod
    def get_pets_count():
        error, data = DashboardService.get_pets_count()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_owners_count():
        error, data = DashboardService.get_owners_count()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_appointments_by_status():
        error, data = DashboardService.get_appointments_by_status()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_consultations_by_month():
        error, data = DashboardService.get_consultations_by_month()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_pets_by_species():
        error, data = DashboardService.get_pets_by_species()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_vaccinations_by_month():
        error, data = DashboardService.get_vaccinations_by_month()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_top_vets():
        error, data = DashboardService.get_top_vets()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}
