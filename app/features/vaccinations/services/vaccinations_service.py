from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.vaccinations.repositories.vaccinations_repository import VaccinationsRepository
from app.features.vaccinations.models.vaccinations_schema import CreateVaccinationSchema, FilterVaccinationsSchema

logger = get_logger("vaccinations.service")


class VaccinationsService:

    @staticmethod
    def get_all_vaccinations(filters: FilterVaccinationsSchema):
        connection = get_connection()
        try:
            error, data = VaccinationsRepository.find_all_vaccinations(filters, connection)
            if error:
                raise ServiceError(error)
            return None, data
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_all_vaccinations: %s", e, exc_info=True)
            return "Error al obtener las vacunaciones", None
        finally:
            connection.close()

    @staticmethod
    def get_vaccination_by_id(vaccination_id: int):
        connection = get_connection()
        try:
            error, vacc = VaccinationsRepository.find_vaccination_by_id(vaccination_id, connection)
            if error:
                raise ServiceError(error)
            if not vacc:
                raise ServiceError("Vacunación no encontrada")
            return None, vacc
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_vaccination_by_id: %s", e, exc_info=True)
            return "Error al obtener la vacunación", None
        finally:
            connection.close()

    @staticmethod
    def create_vaccination(data_in: CreateVaccinationSchema):
        connection = get_connection()
        try:
            error, success, message = VaccinationsRepository.create_vaccination(data_in, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Vacunación registrada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en create_vaccination: %s", e, exc_info=True)
            return "Error al registrar la vacunación", False, None
        finally:
            connection.close()
