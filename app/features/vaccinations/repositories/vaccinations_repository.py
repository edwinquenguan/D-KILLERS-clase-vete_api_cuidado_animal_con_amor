from app.utils.logger import get_logger
from app.features.vaccinations.models.vaccinations_schema import CreateVaccinationSchema, FilterVaccinationsSchema
from app.features.vaccinations.models.vaccinations_response import VaccinationResponse

logger = get_logger("vaccinations.repository")

_BASE_QUERY = """
SELECT va.vaccination_id, va.vaccination_date, va.vaccination_next_date, va.vaccination_batch, va.vaccination_notes,
       p.pet_id, p.pet_name, s.species_name,
       vac.vaccine_id, vac.vaccine_name, vac.vaccine_disease, vac.vaccine_manufacturer,
       CONCAT(u.user_name,' ',u.user_first_surname)
FROM VACCINATIONS AS va
INNER JOIN PETS AS p ON va.pet_id = p.pet_id
INNER JOIN SPECIES AS s ON p.species_id = s.species_id
INNER JOIN VACCINES AS vac ON va.vaccine_id = vac.vaccine_id
INNER JOIN USERS AS u ON va.user_id = u.user_id
"""


def _row_to_vaccination(row) -> VaccinationResponse:
    return VaccinationResponse(
        id=row[0], vaccination_date=str(row[1]), vaccination_next_date=str(row[2]),
        batch=row[3], notes=row[4],
        pet_id=row[5], pet_name=row[6], species_name=row[7],
        vaccine_id=row[8], vaccine_name=row[9], vaccine_disease=row[10], vaccine_manufacturer=row[11],
        vet_full_name=row[12]
    )


class VaccinationsRepository:

    @staticmethod
    def find_all_vaccinations(filters: FilterVaccinationsSchema, connection):
        data = filters.model_dump(exclude_none=True)
        cursor = connection.cursor()
        query = _BASE_QUERY
        filters_list, values = [], []
        if "pet_id" in data:
            filters_list.append("va.pet_id = %s")
            values.append(data["pet_id"])
        if "vaccine_id" in data:
            filters_list.append("va.vaccine_id = %s")
            values.append(data["vaccine_id"])
        if "start_date" in data:
            filters_list.append("va.vaccination_date >= %s")
            values.append(data["start_date"])
        if "end_date" in data:
            filters_list.append("va.vaccination_date <= %s")
            values.append(data["end_date"])
        if filters_list:
            query += " WHERE " + " AND ".join(filters_list)
        query += " ORDER BY va.vaccination_date DESC"
        try:
            cursor.execute(query, values)
            return None, [_row_to_vaccination(r) for r in cursor.fetchall()]
        except Exception as e:
            logger.error("Error en find_all_vaccinations: %s", e, exc_info=True)
            return "Error al obtener las vacunaciones", None
        finally:
            cursor.close()

    @staticmethod
    def find_vaccination_by_id(vaccination_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(_BASE_QUERY + " WHERE va.vaccination_id = %s", (vaccination_id,))
            row = cursor.fetchone()
            if not row:
                return None, None
            return None, _row_to_vaccination(row)
        except Exception as e:
            logger.error("Error en find_vaccination_by_id: %s", e, exc_info=True)
            return "Error al obtener la vacunación", None
        finally:
            cursor.close()

    @staticmethod
    def create_vaccination(data_in: CreateVaccinationSchema, connection):
        data = data_in.model_dump()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """INSERT INTO VACCINATIONS
                   (pet_id, vaccine_id, user_id, vaccination_date, vaccination_next_date, vaccination_batch, vaccination_notes)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (data["pet_id"], data["vaccine_id"], data["user_id"],
                 data["vaccination_date"], data["vaccination_next_date"],
                 data["batch"], data.get("notes"))
            )
            return None, True, "Vacunación registrada correctamente"
        except Exception as e:
            logger.error("Error en create_vaccination: %s", e, exc_info=True)
            return "Error al registrar la vacunación", False, None
        finally:
            cursor.close()
