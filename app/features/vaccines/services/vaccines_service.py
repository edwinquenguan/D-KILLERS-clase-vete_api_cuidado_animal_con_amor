from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.vaccines.repositories.vaccines_repository import VaccinesRepository
from app.features.vaccines.models.vaccines_schema import CreateVaccineSchema, FilterVaccinesSchema, UpdateVaccineSchema

logger = get_logger("vaccines.service")


class VaccinesService:

    @staticmethod
    def get_all_vaccines(filters: FilterVaccinesSchema):
        connection = get_connection()
        try:
            error, data = VaccinesRepository.find_all_vaccines(filters, connection)
            if error:
                raise ServiceError(error)
            return None, data
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_all_vaccines: %s", e, exc_info=True)
            return "Error al obtener las vacunas", None
        finally:
            connection.close()

    @staticmethod
    def get_vaccine_by_id(vaccine_id: int):
        connection = get_connection()
        try:
            error, vaccine = VaccinesRepository.find_vaccine_by_id(vaccine_id, connection)
            if error:
                raise ServiceError(error)
            if not vaccine:
                raise ServiceError("Vacuna no encontrada")
            return None, vaccine
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_vaccine_by_id: %s", e, exc_info=True)
            return "Error al obtener la vacuna", None
        finally:
            connection.close()

    @staticmethod
    def create_vaccine(vaccine_data: CreateVaccineSchema):
        connection = get_connection()
        try:
            error, success, message = VaccinesRepository.create_vaccine(vaccine_data, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Vacuna creada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en create_vaccine: %s", e, exc_info=True)
            return "Error al crear la vacuna", False, None
        finally:
            connection.close()

    @staticmethod
    def update_vaccine(vaccine_id: int, vaccine_data: UpdateVaccineSchema):
        connection = get_connection()
        try:
            error, vaccine = VaccinesRepository.find_vaccine_by_id(vaccine_id, connection)
            if error:
                raise ServiceError(error)
            if not vaccine:
                raise ServiceError("Vacuna no encontrada")
            error, success, message = VaccinesRepository.update_vaccine(vaccine_id, vaccine_data, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Vacuna actualizada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en update_vaccine: %s", e, exc_info=True)
            return "Error al actualizar la vacuna", False, None
        finally:
            connection.close()

    @staticmethod
    def disable_vaccine(vaccine_id: int):
        connection = get_connection()
        try:
            error, vaccine = VaccinesRepository.find_vaccine_by_id(vaccine_id, connection)
            if error:
                raise ServiceError(error)
            if not vaccine:
                raise ServiceError("Vacuna no encontrada")
            error, success, message = VaccinesRepository.disable_vaccine(vaccine_id, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Vacuna deshabilitada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en disable_vaccine: %s", e, exc_info=True)
            return "Error al deshabilitar la vacuna", False, None
        finally:
            connection.close()

    @staticmethod
    def enable_vaccine(vaccine_id: int):
        connection = get_connection()
        try:
            error, vaccine = VaccinesRepository.find_vaccine_by_id(vaccine_id, connection)
            if error:
                raise ServiceError(error)
            if not vaccine:
                raise ServiceError("Vacuna no encontrada")
            error, success, message = VaccinesRepository.enable_vaccine(vaccine_id, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Vacuna habilitada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en enable_vaccine: %s", e, exc_info=True)
            return "Error al habilitar la vacuna", False, None
        finally:
            connection.close()
