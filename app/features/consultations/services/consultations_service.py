from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.consultations.repositories.consultations_repository import ConsultationsRepository
from app.features.consultations.models.consultations_schema import CreateConsultationSchema, FilterConsultationsSchema, UpdateConsultationSchema

logger = get_logger("consultations.service")


class ConsultationsService:

    @staticmethod
    def get_all_consultations(filters: FilterConsultationsSchema):
        connection = get_connection()
        try:
            error, data = ConsultationsRepository.find_all_consultations(filters, connection)
            if error:
                raise ServiceError(error)
            return None, data
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_all_consultations: %s", e, exc_info=True)
            return "Error al obtener las consultas", None
        finally:
            connection.close()

    @staticmethod
    def get_consultation_by_id(consultation_id: int):
        connection = get_connection()
        try:
            error, consult = ConsultationsRepository.find_consultation_by_id(consultation_id, connection)
            if error:
                raise ServiceError(error)
            if not consult:
                raise ServiceError("Consulta no encontrada")
            return None, consult
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_consultation_by_id: %s", e, exc_info=True)
            return "Error al obtener la consulta", None
        finally:
            connection.close()

    @staticmethod
    def create_consultation(data_in: CreateConsultationSchema):
        connection = get_connection()
        try:
            error, success, message = ConsultationsRepository.create_consultation(data_in, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Consulta registrada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en create_consultation: %s", e, exc_info=True)
            return "Error al registrar la consulta", False, None
        finally:
            connection.close()

    @staticmethod
    def update_consultation(consultation_id: int, data_in: UpdateConsultationSchema):
        connection = get_connection()
        try:
            error, consult = ConsultationsRepository.find_consultation_by_id(consultation_id, connection)
            if error:
                raise ServiceError(error)
            if not consult:
                raise ServiceError("Consulta no encontrada")
            error, success, message = ConsultationsRepository.update_consultation(consultation_id, data_in, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Consulta actualizada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en update_consultation: %s", e, exc_info=True)
            return "Error al actualizar la consulta", False, None
        finally:
            connection.close()
