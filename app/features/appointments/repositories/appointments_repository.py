from app.utils.logger import get_logger
from app.utils.date_formatter import date_formatter
from app.features.appointments.models.appointments_schema import CreateAppointmentSchema, FilterAppointmentsSchema, UpdateAppointmentSchema
from app.features.appointments.models.appointments_response import AppointmentResponse

logger = get_logger("appointments.repository")

APPT_FIELDS = {
    "user_id": "user_id",
    "appointment_date": "appointment_date",
    "appointment_time": "appointment_time",
    "reason": "appointment_reason",
    "status": "appointment_status",
}

_BASE_QUERY = """
SELECT a.appointment_id, a.appointment_date, a.appointment_time, a.appointment_reason,
       a.appointment_status, a.appointment_date_created,
       p.pet_id, p.pet_name, s.species_name,
       o.owner_id, CONCAT(o.owner_name,' ',o.owner_first_surname), o.owner_phone,
       u.user_id, CONCAT(u.user_name,' ',u.user_first_surname)
FROM APPOINTMENTS AS a
INNER JOIN PETS AS p ON a.pet_id = p.pet_id
INNER JOIN SPECIES AS s ON p.species_id = s.species_id
INNER JOIN OWNERS AS o ON p.owner_id = o.owner_id
INNER JOIN USERS AS u ON a.user_id = u.user_id
"""


def _row_to_appt(row) -> AppointmentResponse:
    return AppointmentResponse(
        appointment_id=row[0], appointment_date=str(row[1]), appointment_time=str(row[2]),
        appointment_reason=row[3], appointment_status=row[4], appointment_date_created=date_formatter(row[5]),
        pet_id=row[6], pet_name=row[7], species_name=row[8],
        owner_id=row[9], owner_full_name=row[10], owner_phone=row[11],
        vet_id=row[12], vet_name=row[13]
    )


class AppointmentsRepository:

    @staticmethod
    def find_all_appointments(filters: FilterAppointmentsSchema, connection):
        data = filters.model_dump(exclude_none=True)
        cursor = connection.cursor()
        query = _BASE_QUERY
        filters_list, values = [], []
        if "pet_id" in data:
            filters_list.append("a.pet_id = %s")
            values.append(data["pet_id"])
        if "user_id" in data:
            filters_list.append("a.user_id = %s")
            values.append(data["user_id"])
        if "status" in data:
            filters_list.append("a.appointment_status = %s")
            values.append(data["status"])
        if "start_date" in data:
            filters_list.append("a.appointment_date >= %s")
            values.append(data["start_date"])
        if "end_date" in data:
            filters_list.append("a.appointment_date <= %s")
            values.append(data["end_date"])
        if filters_list:
            query += " WHERE " + " AND ".join(filters_list)
        query += " ORDER BY a.appointment_date ASC, a.appointment_time ASC"
        try:
            cursor.execute(query, values)
            return None, [_row_to_appt(r) for r in cursor.fetchall()]
        except Exception as e:
            logger.error("Error en find_all_appointments: %s", e, exc_info=True)
            return "Error al obtener las citas", None
        finally:
            cursor.close()

    @staticmethod
    def find_appointment_by_id(appointment_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(_BASE_QUERY + " WHERE a.appointment_id = %s", (appointment_id,))
            row = cursor.fetchone()
            if not row:
                return None, None
            return None, _row_to_appt(row)
        except Exception as e:
            logger.error("Error en find_appointment_by_id: %s", e, exc_info=True)
            return "Error al obtener la cita", None
        finally:
            cursor.close()

    @staticmethod
    def create_appointment(appt_data: CreateAppointmentSchema, connection):
        data = appt_data.model_dump()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """INSERT INTO APPOINTMENTS (pet_id, user_id, appointment_date, appointment_time, appointment_reason)
                   VALUES (%s, %s, %s, %s, %s)""",
                (data["pet_id"], data["user_id"], data["appointment_date"], data["appointment_time"], data["reason"])
            )
            return None, True, "Cita creada correctamente"
        except Exception as e:
            logger.error("Error en create_appointment: %s", e, exc_info=True)
            return "Error al crear la cita", False, None
        finally:
            cursor.close()

    @staticmethod
    def update_appointment(appointment_id: int, appt_data: UpdateAppointmentSchema, connection):
        data = appt_data.model_dump(exclude_none=True)
        cursor = connection.cursor()
        try:
            mapped = {APPT_FIELDS[k]: v for k, v in data.items() if k in APPT_FIELDS}
            if not mapped:
                return "No hay campos para actualizar", False, None
            columns = ", ".join(f"{col} = %s" for col in mapped.keys())
            values = list(mapped.values()) + [appointment_id]
            cursor.execute(f"UPDATE APPOINTMENTS SET {columns} WHERE appointment_id = %s", values)
            return None, True, "Cita actualizada correctamente"
        except Exception as e:
            logger.error("Error en update_appointment: %s", e, exc_info=True)
            return "Error al actualizar la cita", False, None
        finally:
            cursor.close()

    @staticmethod
    def cancel_appointment(appointment_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE APPOINTMENTS SET appointment_status = 1 WHERE appointment_id = %s",
                (appointment_id,)
            )
            return None, True, "Cita cancelada correctamente"
        except Exception as e:
            logger.error("Error en cancel_appointment: %s", e, exc_info=True)
            return "Error al cancelar la cita", False, None
        finally:
            cursor.close()
