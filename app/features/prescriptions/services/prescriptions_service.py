from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.prescriptions.repositories.prescriptions_repository import PrescriptionsRepository
from app.features.prescriptions.models.prescriptions_schema import CreatePrescriptionSchema, FilterPrescriptionsSchema

logger = get_logger("prescriptions.service")


class PrescriptionsService:

    @staticmethod
    def get_all_prescriptions(filters: FilterPrescriptionsSchema):
        connection = get_connection()
        try:
            error, data = PrescriptionsRepository.find_all_prescriptions(filters, connection)
            if error:
                raise ServiceError(error)
            return None, data
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_all_prescriptions: %s", e, exc_info=True)
            return "Error al obtener las recetas", None
        finally:
            connection.close()

    @staticmethod
    def get_prescription_by_id(prescription_id: int):
        connection = get_connection()
        try:
            error, prescription = PrescriptionsRepository.find_prescription_by_id(prescription_id, connection)
            if error:
                raise ServiceError(error)
            if not prescription:
                raise ServiceError("Receta no encontrada")
            return None, prescription
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_prescription_by_id: %s", e, exc_info=True)
            return "Error al obtener la receta", None
        finally:
            connection.close()

    @staticmethod
    def create_prescription(data_in: CreatePrescriptionSchema):
        connection = get_connection()
        try:
            if not data_in.details:
                raise ServiceError("La receta debe tener al menos un medicamento")
            error, success, message = PrescriptionsRepository.create_prescription(data_in, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Receta creada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en create_prescription: %s", e, exc_info=True)
            return "Error al crear la receta", False, None
        finally:
            connection.close()
