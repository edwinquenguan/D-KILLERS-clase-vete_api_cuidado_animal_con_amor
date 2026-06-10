from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.appointments.repositories.appointments_repository import AppointmentsRepository
from app.features.appointments.models.appointments_schema import CreateAppointmentSchema, FilterAppointmentsSchema, UpdateAppointmentSchema

logger = get_logger("appointments.service")


class AppointmentsService:

    @staticmethod
    def get_all_appointments(filters: FilterAppointmentsSchema):
        connection = get_connection()
        try:
            error, data = AppointmentsRepository.find_all_appointments(filters, connection)
            if error:
                raise ServiceError(error)
            return None, data
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_all_appointments: %s", e, exc_info=True)
            return "Error al obtener las citas", None
        finally:
            connection.close()

    @staticmethod
    def get_appointment_by_id(appointment_id: int):
        connection = get_connection()
        try:
            error, appt = AppointmentsRepository.find_appointment_by_id(appointment_id, connection)
            if error:
                raise ServiceError(error)
            if not appt:
                raise ServiceError("Cita no encontrada")
            return None, appt
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_appointment_by_id: %s", e, exc_info=True)
            return "Error al obtener la cita", None
        finally:
            connection.close()

    @staticmethod
    def create_appointment(appt_data: CreateAppointmentSchema):
        connection = get_connection()
        try:
            error, success, message = AppointmentsRepository.create_appointment(appt_data, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Cita creada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en create_appointment: %s", e, exc_info=True)
            return "Error al crear la cita", False, None
        finally:
            connection.close()

    @staticmethod
    def update_appointment(appointment_id: int, appt_data: UpdateAppointmentSchema):
        connection = get_connection()
        try:
            error, appt = AppointmentsRepository.find_appointment_by_id(appointment_id, connection)
            if error:
                raise ServiceError(error)
            if not appt:
                raise ServiceError("Cita no encontrada")
            error, success, message = AppointmentsRepository.update_appointment(appointment_id, appt_data, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Cita actualizada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en update_appointment: %s", e, exc_info=True)
            return "Error al actualizar la cita", False, None
        finally:
            connection.close()

    @staticmethod
    def cancel_appointment(appointment_id: int):
        connection = get_connection()
        try:
            error, appt = AppointmentsRepository.find_appointment_by_id(appointment_id, connection)
            if error:
                raise ServiceError(error)
            if not appt:
                raise ServiceError("Cita no encontrada")
            error, success, message = AppointmentsRepository.cancel_appointment(appointment_id, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Cita cancelada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en cancel_appointment: %s", e, exc_info=True)
            return "Error al cancelar la cita", False, None
        finally:
            connection.close()
