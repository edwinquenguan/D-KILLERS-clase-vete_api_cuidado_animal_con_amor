from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.dashboard.repositories.dashboard_repository import DashboardRepository
from app.utils.logger import get_logger

logger = get_logger("dashboard.service")


def _run(method_name, repo_fn, connection):
    try:
        error, data = repo_fn(connection)
        if error:
            raise ServiceError(error)
        return None, data
    except ServiceError as e:
        return e.message, None
    except Exception as e:
        logger.error("Error en %s: %s", method_name, e, exc_info=True)
        return f"Error en {method_name}", None


class DashboardService:

    @staticmethod
    def get_pets_count():
        connection = get_connection()
        try:
            return _run("get_pets_count", DashboardRepository.find_pets_count, connection)
        finally:
            connection.close()

    @staticmethod
    def get_owners_count():
        connection = get_connection()
        try:
            return _run("get_owners_count", DashboardRepository.find_owners_count, connection)
        finally:
            connection.close()

    @staticmethod
    def get_appointments_by_status():
        connection = get_connection()
        try:
            return _run("get_appointments_by_status", DashboardRepository.find_appointments_by_status, connection)
        finally:
            connection.close()

    @staticmethod
    def get_consultations_by_month():
        connection = get_connection()
        try:
            return _run("get_consultations_by_month", DashboardRepository.find_consultations_by_month, connection)
        finally:
            connection.close()

    @staticmethod
    def get_pets_by_species():
        connection = get_connection()
        try:
            return _run("get_pets_by_species", DashboardRepository.find_pets_by_species, connection)
        finally:
            connection.close()

    @staticmethod
    def get_vaccinations_by_month():
        connection = get_connection()
        try:
            return _run("get_vaccinations_by_month", DashboardRepository.find_vaccinations_by_month, connection)
        finally:
            connection.close()

    @staticmethod
    def get_top_vets():
        connection = get_connection()
        try:
            return _run("get_top_vets", DashboardRepository.find_top_vets, connection)
        finally:
            connection.close()
