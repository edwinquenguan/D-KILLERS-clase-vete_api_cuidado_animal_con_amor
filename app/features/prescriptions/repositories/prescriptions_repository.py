from app.utils.logger import get_logger
from app.utils.date_formatter import date_formatter
from app.features.prescriptions.models.prescriptions_schema import CreatePrescriptionSchema, FilterPrescriptionsSchema
from app.features.prescriptions.models.prescriptions_response import PrescriptionResponse, PrescriptionDetailResponse

logger = get_logger("prescriptions.repository")


class PrescriptionsRepository:

    @staticmethod
    def find_all_prescriptions(filters: FilterPrescriptionsSchema, connection):
        data = filters.model_dump(exclude_none=True)
        cursor = connection.cursor()
        query = """
        SELECT DISTINCT pr.prescription_id, pr.prescription_date, pr.prescription_notes,
               c.consultation_id, c.consultation_date,
               p.pet_id, p.pet_name,
               CONCAT(o.owner_name,' ',o.owner_first_surname),
               CONCAT(u.user_name,' ',u.user_first_surname)
        FROM PRESCRIPTIONS AS pr
        INNER JOIN CONSULTATIONS AS c ON pr.consultation_id = c.consultation_id
        INNER JOIN PETS AS p ON c.pet_id = p.pet_id
        INNER JOIN OWNERS AS o ON p.owner_id = o.owner_id
        INNER JOIN USERS AS u ON c.user_id = u.user_id
        """
        filters_list, values = [], []
        if "consultation_id" in data:
            filters_list.append("pr.consultation_id = %s")
            values.append(data["consultation_id"])
        if "pet_id" in data:
            filters_list.append("c.pet_id = %s")
            values.append(data["pet_id"])
        if "start_date" in data:
            filters_list.append("DATE(pr.prescription_date) >= %s")
            values.append(data["start_date"])
        if "end_date" in data:
            filters_list.append("DATE(pr.prescription_date) <= %s")
            values.append(data["end_date"])
        if filters_list:
            query += " WHERE " + " AND ".join(filters_list)
        query += " ORDER BY pr.prescription_date DESC"
        try:
            cursor.execute(query, values)
            rows = cursor.fetchall()
            prescriptions = []
            for row in rows:
                details = PrescriptionsRepository._get_details(row[0], connection)
                prescriptions.append(PrescriptionResponse(
                    id=row[0], date=date_formatter(row[1]), notes=row[2],
                    consultation_id=row[3], consultation_date=date_formatter(row[4]),
                    pet_id=row[5], pet_name=row[6],
                    owner_full_name=row[7], vet_full_name=row[8],
                    details=details
                ))
            return None, prescriptions
        except Exception as e:
            logger.error("Error en find_all_prescriptions: %s", e, exc_info=True)
            return "Error al obtener las recetas", None
        finally:
            cursor.close()

    @staticmethod
    def find_prescription_by_id(prescription_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT pr.prescription_id, pr.prescription_date, pr.prescription_notes,
                   c.consultation_id, c.consultation_date,
                   p.pet_id, p.pet_name,
                   CONCAT(o.owner_name,' ',o.owner_first_surname),
                   CONCAT(u.user_name,' ',u.user_first_surname)
            FROM PRESCRIPTIONS AS pr
            INNER JOIN CONSULTATIONS AS c ON pr.consultation_id = c.consultation_id
            INNER JOIN PETS AS p ON c.pet_id = p.pet_id
            INNER JOIN OWNERS AS o ON p.owner_id = o.owner_id
            INNER JOIN USERS AS u ON c.user_id = u.user_id
            WHERE pr.prescription_id = %s
            """, (prescription_id,))
            row = cursor.fetchone()
            if not row:
                return None, None
            details = PrescriptionsRepository._get_details(row[0], connection)
            return None, PrescriptionResponse(
                id=row[0], date=date_formatter(row[1]), notes=row[2],
                consultation_id=row[3], consultation_date=date_formatter(row[4]),
                pet_id=row[5], pet_name=row[6],
                owner_full_name=row[7], vet_full_name=row[8],
                details=details
            )
        except Exception as e:
            logger.error("Error en find_prescription_by_id: %s", e, exc_info=True)
            return "Error al obtener la receta", None
        finally:
            cursor.close()

    @staticmethod
    def _get_details(prescription_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT pd.detail_id, m.medication_name, m.medication_presentation, m.medication_unit,
                   pd.detail_dose, pd.detail_frequency, pd.detail_duration, pd.detail_instructions
            FROM PRESCRIPTION_DETAILS AS pd
            INNER JOIN MEDICATIONS AS m ON pd.medication_id = m.medication_id
            WHERE pd.prescription_id = %s
            """, (prescription_id,))
            return [
                PrescriptionDetailResponse(
                    detail_id=r[0], medication_name=r[1], presentation=r[2], unit=r[3],
                    dose=r[4], frequency=r[5], duration=r[6], instructions=r[7]
                )
                for r in cursor.fetchall()
            ]
        finally:
            cursor.close()

    @staticmethod
    def create_prescription(data_in: CreatePrescriptionSchema, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO PRESCRIPTIONS (consultation_id, prescription_notes) VALUES (%s, %s)",
                (data_in.consultation_id, data_in.notes)
            )
            prescription_id = cursor.lastrowid

            for detail in data_in.details:
                cursor.execute(
                    """INSERT INTO PRESCRIPTION_DETAILS
                       (prescription_id, medication_id, detail_dose, detail_frequency, detail_duration, detail_instructions)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (prescription_id, detail.medication_id, detail.dose,
                     detail.frequency, detail.duration, detail.instructions)
                )
            return None, True, "Receta creada correctamente"
        except Exception as e:
            logger.error("Error en create_prescription: %s", e, exc_info=True)
            return "Error al crear la receta", False, None
        finally:
            cursor.close()
