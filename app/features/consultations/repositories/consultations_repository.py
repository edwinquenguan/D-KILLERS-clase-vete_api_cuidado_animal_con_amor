from app.utils.logger import get_logger
from app.utils.date_formatter import date_formatter
from app.features.consultations.models.consultations_schema import CreateConsultationSchema, FilterConsultationsSchema, UpdateConsultationSchema
from app.features.consultations.models.consultations_response import ConsultationResponse

logger = get_logger("consultations.repository")

CONSULT_FIELDS = {
    "weight": "consultation_weight",
    "temperature": "consultation_temperature",
    "diagnosis": "consultation_diagnosis",
    "treatment": "consultation_treatment",
    "notes": "consultation_notes",
}

_BASE_QUERY = """
SELECT c.consultation_id, c.consultation_date, c.consultation_weight, c.consultation_temperature,
       c.consultation_diagnosis, c.consultation_treatment, c.consultation_notes,
       p.pet_id, p.pet_name, s.species_name, b.breed_name,
       o.owner_id, CONCAT(o.owner_name,' ',o.owner_first_surname), o.owner_phone,
       u.user_id, CONCAT(u.user_name,' ',u.user_first_surname),
       c.appointment_id
FROM CONSULTATIONS AS c
INNER JOIN PETS AS p ON c.pet_id = p.pet_id
INNER JOIN SPECIES AS s ON p.species_id = s.species_id
INNER JOIN BREEDS AS b ON p.breed_id = b.breed_id
INNER JOIN OWNERS AS o ON p.owner_id = o.owner_id
INNER JOIN USERS AS u ON c.user_id = u.user_id
"""


def _row_to_consult(row) -> ConsultationResponse:
    return ConsultationResponse(
        consultation_id=row[0], consultation_date=date_formatter(row[1]),
        consultation_weight=float(row[2]), consultation_temperature=float(row[3]),
        consultation_diagnosis=row[4], consultation_treatment=row[5], consultation_notes=row[6],
        pet_id=row[7], pet_name=row[8], species_name=row[9], breed_name=row[10],
        owner_id=row[11], owner_full_name=row[12], owner_phone=row[13],
        vet_id=row[14], vet_name=row[15],
        appointment_id=row[16]
    )


class ConsultationsRepository:

    @staticmethod
    def find_all_consultations(filters: FilterConsultationsSchema, connection):
        data = filters.model_dump(exclude_none=True)
        cursor = connection.cursor()
        query = _BASE_QUERY
        filters_list, values = [], []
        if "pet_id" in data:
            filters_list.append("c.pet_id = %s")
            values.append(data["pet_id"])
        if "user_id" in data:
            filters_list.append("c.user_id = %s")
            values.append(data["user_id"])
        if "start_date" in data:
            filters_list.append("DATE(c.consultation_date) >= %s")
            values.append(data["start_date"])
        if "end_date" in data:
            filters_list.append("DATE(c.consultation_date) <= %s")
            values.append(data["end_date"])
        if filters_list:
            query += " WHERE " + " AND ".join(filters_list)
        query += " ORDER BY c.consultation_date DESC"
        try:
            cursor.execute(query, values)
            return None, [_row_to_consult(r) for r in cursor.fetchall()]
        except Exception as e:
            logger.error("Error en find_all_consultations: %s", e, exc_info=True)
            return "Error al obtener las consultas", None
        finally:
            cursor.close()

    @staticmethod
    def find_consultation_by_id(consultation_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(_BASE_QUERY + " WHERE c.consultation_id = %s", (consultation_id,))
            row = cursor.fetchone()
            if not row:
                return None, None
            return None, _row_to_consult(row)
        except Exception as e:
            logger.error("Error en find_consultation_by_id: %s", e, exc_info=True)
            return "Error al obtener la consulta", None
        finally:
            cursor.close()

    @staticmethod
    def create_consultation(data_in: CreateConsultationSchema, connection):
        data = data_in.model_dump()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """INSERT INTO CONSULTATIONS
                   (pet_id, user_id, appointment_id, consultation_weight, consultation_temperature,
                    consultation_diagnosis, consultation_treatment, consultation_notes)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (data["pet_id"], data["user_id"], data.get("appointment_id"),
                 data["weight"], data["temperature"],
                 data["diagnosis"], data["treatment"], data.get("notes"))
            )
            return None, True, "Consulta registrada correctamente"
        except Exception as e:
            logger.error("Error en create_consultation: %s", e, exc_info=True)
            return "Error al registrar la consulta", False, None
        finally:
            cursor.close()

    @staticmethod
    def update_consultation(consultation_id: int, data_in: UpdateConsultationSchema, connection):
        data = data_in.model_dump(exclude_none=True)
        cursor = connection.cursor()
        try:
            mapped = {CONSULT_FIELDS[k]: v for k, v in data.items() if k in CONSULT_FIELDS}
            if not mapped:
                return "No hay campos para actualizar", False, None
            columns = ", ".join(f"{col} = %s" for col in mapped.keys())
            values = list(mapped.values()) + [consultation_id]
            cursor.execute(f"UPDATE CONSULTATIONS SET {columns} WHERE consultation_id = %s", values)
            return None, True, "Consulta actualizada correctamente"
        except Exception as e:
            logger.error("Error en update_consultation: %s", e, exc_info=True)
            return "Error al actualizar la consulta", False, None
        finally:
            cursor.close()
