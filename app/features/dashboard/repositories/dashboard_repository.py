from app.utils.logger import get_logger
from app.features.dashboard.models.dashboard_responses import (
    DashboardCountResponse,
    AppointmentsByStatusResponse,
    ConsultationsByMonthResponse,
    PetsBySpeciesResponse,
    VaccinationsByMonthResponse,
    TopVetsResponse,
)

logger = get_logger("dashboard.repository")


class DashboardRepository:

    @staticmethod
    def find_pets_count(connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT
                (SELECT COUNT(*) FROM PETS) AS total,
                (SELECT COUNT(*) FROM PETS
                 WHERE MONTH(pet_date) = MONTH(CURDATE()) AND YEAR(pet_date) = YEAR(CURDATE())
                ) AS new_this_month
            """)
            row = cursor.fetchone()
            return None, [DashboardCountResponse(total=row[0], new_this_month=row[1])]
        except Exception as e:
            logger.error("Error en find_pets_count: %s", e, exc_info=True)
            return "Error al obtener el conteo de mascotas", None
        finally:
            cursor.close()

    @staticmethod
    def find_owners_count(connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT
                (SELECT COUNT(*) FROM OWNERS) AS total,
                (SELECT COUNT(*) FROM OWNERS
                 WHERE MONTH(owner_date) = MONTH(CURDATE()) AND YEAR(owner_date) = YEAR(CURDATE())
                ) AS new_this_month
            """)
            row = cursor.fetchone()
            return None, [DashboardCountResponse(total=row[0], new_this_month=row[1])]
        except Exception as e:
            logger.error("Error en find_owners_count: %s", e, exc_info=True)
            return "Error al obtener el conteo de propietarios", None
        finally:
            cursor.close()

    @staticmethod
    def find_appointments_by_status(connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT appointment_status, COUNT(*) AS total
            FROM APPOINTMENTS
            GROUP BY appointment_status
            ORDER BY appointment_status ASC
            """)
            result = cursor.fetchall()
            return None, [AppointmentsByStatusResponse(status=r[0], total=r[1]) for r in result]
        except Exception as e:
            logger.error("Error en find_appointments_by_status: %s", e, exc_info=True)
            return "Error al obtener citas por estado", None
        finally:
            cursor.close()

    @staticmethod
    def find_consultations_by_month(connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT YEAR(consultation_date) AS year, MONTH(consultation_date) AS month, COUNT(*) AS total
            FROM CONSULTATIONS
            WHERE consultation_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
            GROUP BY YEAR(consultation_date), MONTH(consultation_date)
            ORDER BY year ASC, month ASC
            """)
            result = cursor.fetchall()
            return None, [ConsultationsByMonthResponse(year=r[0], month=r[1], total=r[2]) for r in result]
        except Exception as e:
            logger.error("Error en find_consultations_by_month: %s", e, exc_info=True)
            return "Error al obtener consultas por mes", None
        finally:
            cursor.close()

    @staticmethod
    def find_pets_by_species(connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT s.species_name, COUNT(p.pet_id) AS total
            FROM SPECIES AS s
            LEFT JOIN PETS AS p ON s.species_id = p.species_id
            GROUP BY s.species_id, s.species_name
            ORDER BY total DESC
            """)
            result = cursor.fetchall()
            return None, [PetsBySpeciesResponse(species_name=r[0], total=r[1]) for r in result]
        except Exception as e:
            logger.error("Error en find_pets_by_species: %s", e, exc_info=True)
            return "Error al obtener mascotas por especie", None
        finally:
            cursor.close()

    @staticmethod
    def find_vaccinations_by_month(connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT YEAR(vaccination_date) AS year, MONTH(vaccination_date) AS month, COUNT(*) AS total
            FROM VACCINATIONS
            WHERE vaccination_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
            GROUP BY YEAR(vaccination_date), MONTH(vaccination_date)
            ORDER BY year ASC, month ASC
            """)
            result = cursor.fetchall()
            return None, [VaccinationsByMonthResponse(year=r[0], month=r[1], total=r[2]) for r in result]
        except Exception as e:
            logger.error("Error en find_vaccinations_by_month: %s", e, exc_info=True)
            return "Error al obtener vacunaciones por mes", None
        finally:
            cursor.close()

    @staticmethod
    def find_top_vets(connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT CONCAT(u.user_name,' ',u.user_first_surname) AS vet_name,
                   COUNT(c.consultation_id) AS consultations
            FROM USERS AS u
            LEFT JOIN CONSULTATIONS AS c ON u.user_id = c.user_id
            INNER JOIN ROLES AS r ON u.rol_id = r.rol_id
            WHERE r.rol_name = 'Veterinario'
            GROUP BY u.user_id
            ORDER BY consultations DESC
            LIMIT 5
            """)
            result = cursor.fetchall()
            return None, [TopVetsResponse(vet_name=r[0], consultations=r[1]) for r in result]
        except Exception as e:
            logger.error("Error en find_top_vets: %s", e, exc_info=True)
            return "Error al obtener el ranking de veterinarios", None
        finally:
            cursor.close()
