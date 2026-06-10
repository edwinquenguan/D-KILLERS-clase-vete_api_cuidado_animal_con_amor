from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.medications.repositories.medications_repository import MedicationsRepository
from app.features.medications.models.medications_schema import CreateMedicationSchema, FilterMedicationsSchema, UpdateMedicationSchema

logger = get_logger("medications.service")


class MedicationsService:

    @staticmethod
    def get_all_medications(filters: FilterMedicationsSchema):
        connection = get_connection()
        try:
            error, data = MedicationsRepository.find_all_medications(filters, connection)
            if error:
                raise ServiceError(error)
            return None, data
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_all_medications: %s", e, exc_info=True)
            return "Error al obtener los medicamentos", None
        finally:
            connection.close()

    @staticmethod
    def get_medication_by_id(medication_id: int):
        connection = get_connection()
        try:
            error, med = MedicationsRepository.find_medication_by_id(medication_id, connection)
            if error:
                raise ServiceError(error)
            if not med:
                raise ServiceError("Medicamento no encontrado")
            return None, med
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_medication_by_id: %s", e, exc_info=True)
            return "Error al obtener el medicamento", None
        finally:
            connection.close()

    @staticmethod
    def create_medication(data_in: CreateMedicationSchema):
        connection = get_connection()
        try:
            error, success, message = MedicationsRepository.create_medication(data_in, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Medicamento creado correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en create_medication: %s", e, exc_info=True)
            return "Error al crear el medicamento", False, None
        finally:
            connection.close()

    @staticmethod
    def update_medication(medication_id: int, data_in: UpdateMedicationSchema):
        connection = get_connection()
        try:
            error, med = MedicationsRepository.find_medication_by_id(medication_id, connection)
            if error:
                raise ServiceError(error)
            if not med:
                raise ServiceError("Medicamento no encontrado")
            error, success, message = MedicationsRepository.update_medication(medication_id, data_in, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Medicamento actualizado correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en update_medication: %s", e, exc_info=True)
            return "Error al actualizar el medicamento", False, None
        finally:
            connection.close()

    @staticmethod
    def disable_medication(medication_id: int):
        connection = get_connection()
        try:
            error, med = MedicationsRepository.find_medication_by_id(medication_id, connection)
            if error:
                raise ServiceError(error)
            if not med:
                raise ServiceError("Medicamento no encontrado")
            error, success, message = MedicationsRepository.disable_medication(medication_id, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Medicamento deshabilitado correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en disable_medication: %s", e, exc_info=True)
            return "Error al deshabilitar el medicamento", False, None
        finally:
            connection.close()

    @staticmethod
    def enable_medication(medication_id: int):
        connection = get_connection()
        try:
            error, med = MedicationsRepository.find_medication_by_id(medication_id, connection)
            if error:
                raise ServiceError(error)
            if not med:
                raise ServiceError("Medicamento no encontrado")
            error, success, message = MedicationsRepository.enable_medication(medication_id, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Medicamento habilitado correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en enable_medication: %s", e, exc_info=True)
            return "Error al habilitar el medicamento", False, None
        finally:
            connection.close()
