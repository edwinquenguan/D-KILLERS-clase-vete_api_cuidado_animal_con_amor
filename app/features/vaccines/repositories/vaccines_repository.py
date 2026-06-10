from app.utils.logger import get_logger
from app.features.vaccines.models.vaccines_schema import CreateVaccineSchema, FilterVaccinesSchema, UpdateVaccineSchema
from app.features.vaccines.models.vaccines_response import VaccineResponse

logger = get_logger("vaccines.repository")

VACCINE_FIELDS = {
    "name": "vaccine_name",
    "disease": "vaccine_disease",
    "manufacturer": "vaccine_manufacturer",
}


class VaccinesRepository:

    @staticmethod
    def find_all_vaccines(filters: FilterVaccinesSchema, connection):
        data = filters.model_dump(exclude_none=True)
        cursor = connection.cursor()
        query = """
        SELECT v.vaccine_id, v.species_id, s.species_name, v.vaccine_name,
               v.vaccine_disease, v.vaccine_manufacturer, v.vaccine_status
        FROM VACCINES AS v INNER JOIN SPECIES AS s ON v.species_id = s.species_id
        """
        filters_list, values = [], []
        if "species_id" in data:
            filters_list.append("v.species_id = %s")
            values.append(data["species_id"])
        if "status" in data:
            filters_list.append("v.vaccine_status = %s")
            values.append(data["status"])
        if filters_list:
            query += " WHERE " + " AND ".join(filters_list)
        query += " ORDER BY s.species_name ASC, v.vaccine_name ASC"
        try:
            cursor.execute(query, values)
            result = cursor.fetchall()
            return None, [
                VaccineResponse(id=r[0], species_id=r[1], species_name=r[2], name=r[3],
                                disease=r[4], manufacturer=r[5], status=r[6])
                for r in result
            ]
        except Exception as e:
            logger.error("Error en find_all_vaccines: %s", e, exc_info=True)
            return "Error al obtener las vacunas", None
        finally:
            cursor.close()

    @staticmethod
    def find_vaccine_by_id(vaccine_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(
                """SELECT v.vaccine_id, v.species_id, s.species_name, v.vaccine_name,
                          v.vaccine_disease, v.vaccine_manufacturer, v.vaccine_status
                   FROM VACCINES AS v INNER JOIN SPECIES AS s ON v.species_id = s.species_id
                   WHERE v.vaccine_id = %s""",
                (vaccine_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None, None
            return None, VaccineResponse(id=row[0], species_id=row[1], species_name=row[2], name=row[3],
                                         disease=row[4], manufacturer=row[5], status=row[6])
        except Exception as e:
            logger.error("Error en find_vaccine_by_id: %s", e, exc_info=True)
            return "Error al obtener la vacuna", None
        finally:
            cursor.close()

    @staticmethod
    def create_vaccine(vaccine_data: CreateVaccineSchema, connection):
        data = vaccine_data.model_dump()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO VACCINES (species_id, vaccine_name, vaccine_disease, vaccine_manufacturer) VALUES (%s,%s,%s,%s)",
                (data["species_id"], data["name"], data["disease"], data["manufacturer"])
            )
            return None, True, "Vacuna creada correctamente"
        except Exception as e:
            logger.error("Error en create_vaccine: %s", e, exc_info=True)
            return "Error al crear la vacuna", False, None
        finally:
            cursor.close()

    @staticmethod
    def update_vaccine(vaccine_id: int, vaccine_data: UpdateVaccineSchema, connection):
        data = vaccine_data.model_dump(exclude_none=True)
        cursor = connection.cursor()
        try:
            mapped = {VACCINE_FIELDS[k]: v for k, v in data.items() if k in VACCINE_FIELDS}
            if not mapped:
                return "No hay campos para actualizar", False, None
            columns = ", ".join(f"{col} = %s" for col in mapped.keys())
            values = list(mapped.values()) + [vaccine_id]
            cursor.execute(f"UPDATE VACCINES SET {columns} WHERE vaccine_id = %s", values)
            return None, True, "Vacuna actualizada correctamente"
        except Exception as e:
            logger.error("Error en update_vaccine: %s", e, exc_info=True)
            return "Error al actualizar la vacuna", False, None
        finally:
            cursor.close()

    @staticmethod
    def disable_vaccine(vaccine_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE VACCINES SET vaccine_status = 1 WHERE vaccine_id = %s", (vaccine_id,))
            return None, True, "Vacuna deshabilitada correctamente"
        except Exception as e:
            logger.error("Error en disable_vaccine: %s", e, exc_info=True)
            return "Error al deshabilitar la vacuna", False, None
        finally:
            cursor.close()

    @staticmethod
    def enable_vaccine(vaccine_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE VACCINES SET vaccine_status = 2 WHERE vaccine_id = %s", (vaccine_id,))
            return None, True, "Vacuna habilitada correctamente"
        except Exception as e:
            logger.error("Error en enable_vaccine: %s", e, exc_info=True)
            return "Error al habilitar la vacuna", False, None
        finally:
            cursor.close()
