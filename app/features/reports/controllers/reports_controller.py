from fastapi import HTTPException
from app.features.reports.services.reports_service import ReportsService


class ReportsController:

    @staticmethod
    def get_pets_by_species(period: str):
        error, data = ReportsService.get_pets_by_species(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_pets_growth(period: str):
        error, data = ReportsService.get_pets_growth(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_appointments_growth(period: str):
        error, data = ReportsService.get_appointments_growth(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_appointments_by_status():
        error, data = ReportsService.get_appointments_by_status()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_consultations_growth(period: str):
        error, data = ReportsService.get_consultations_growth(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_recent_consultations():
        error, data = ReportsService.get_recent_consultations()
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_vaccinations_growth(period: str):
        error, data = ReportsService.get_vaccinations_growth(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_vaccinations_by_vaccine(period: str):
        error, data = ReportsService.get_vaccinations_by_vaccine(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_owners_growth(period: str):
        error, data = ReportsService.get_owners_growth(period)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}
