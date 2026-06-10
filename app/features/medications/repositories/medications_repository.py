from app.utils.logger import get_logger
from app.features.medications.models.medications_schema import CreateMedicationSchema, FilterMedicationsSchema, UpdateMedicationSchema
from app.features.medications.models.medications_response import MedicationResponse

logger = get_logger("medications.repository")

MED_FIELDS = {
    "name": "medication_name",
    "presentation": "medication_presentation",
    "unit": "medication_unit",
}


class MedicationsRepository:

    @staticmethod
    def find_all_medications(filters: FilterMedicationsSchema, connection):
        data = filters.model_dump(exclude_none=True)
        cursor = connection.cursor()
        query = "SELECT medication_id, medication_name, medication_presentation, medication_unit, medication_status FROM MEDICATIONS"
        filters_list, values = [], []
        if "status" in data:
            filters_list.append("medication_status = %s")
            values.append(data["status"])
        if filters_list:
            query += " WHERE " + " AND ".join(filters_list)
        query += " ORDER BY medication_name ASC"
        try:
            cursor.execute(query, values)
            return None, [
                MedicationResponse(id=r[0], name=r[1], presentation=r[2], unit=r[3], status=r[4])
                for r in cursor.fetchall()
            ]
        except Exception as e:
            logger.error("Error en find_all_medications: %s", e, exc_info=True)
            return "Error al obtener los medicamentos", None
        finally:
            cursor.close()

    @staticmethod
    def find_medication_by_id(medication_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT medication_id, medication_name, medication_presentation, medication_unit, medication_status FROM MEDICATIONS WHERE medication_id = %s",
                (medication_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None, None
            return None, MedicationResponse(id=row[0], name=row[1], presentation=row[2], unit=row[3], status=row[4])
        except Exception as e:
            logger.error("Error en find_medication_by_id: %s", e, exc_info=True)
            return "Error al obtener el medicamento", None
        finally:
            cursor.close()

    @staticmethod
    def create_medication(data_in: CreateMedicationSchema, connection):
        data = data_in.model_dump()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO MEDICATIONS (medication_name, medication_presentation, medication_unit) VALUES (%s, %s, %s)",
                (data["name"], data["presentation"], data["unit"])
            )
            return None, True, "Medicamento creado correctamente"
        except Exception as e:
            logger.error("Error en create_medication: %s", e, exc_info=True)
            return "Error al crear el medicamento", False, None
        finally:
            cursor.close()

    @staticmethod
    def update_medication(medication_id: int, data_in: UpdateMedicationSchema, connection):
        data = data_in.model_dump(exclude_none=True)
        cursor = connection.cursor()
        try:
            mapped = {MED_FIELDS[k]: v for k, v in data.items() if k in MED_FIELDS}
            if not mapped:
                return "No hay campos para actualizar", False, None
            columns = ", ".join(f"{col} = %s" for col in mapped.keys())
            values = list(mapped.values()) + [medication_id]
            cursor.execute(f"UPDATE MEDICATIONS SET {columns} WHERE medication_id = %s", values)
            return None, True, "Medicamento actualizado correctamente"
        except Exception as e:
            logger.error("Error en update_medication: %s", e, exc_info=True)
            return "Error al actualizar el medicamento", False, None
        finally:
            cursor.close()

    @staticmethod
    def disable_medication(medication_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE MEDICATIONS SET medication_status = 1 WHERE medication_id = %s", (medication_id,))
            return None, True, "Medicamento deshabilitado correctamente"
        except Exception as e:
            logger.error("Error en disable_medication: %s", e, exc_info=True)
            return "Error al deshabilitar el medicamento", False, None
        finally:
            cursor.close()

    @staticmethod
    def enable_medication(medication_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE MEDICATIONS SET medication_status = 2 WHERE medication_id = %s", (medication_id,))
            return None, True, "Medicamento habilitado correctamente"
        except Exception as e:
            logger.error("Error en enable_medication: %s", e, exc_info=True)
            return "Error al habilitar el medicamento", False, None
        finally:
            cursor.close()
