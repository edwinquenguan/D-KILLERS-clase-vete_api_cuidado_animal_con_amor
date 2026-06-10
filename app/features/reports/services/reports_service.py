from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.utils.periods import period_map, daily_periods

logger = get_logger("reports.service")


def _exec(connection, query, values=()):
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        return None, cursor.fetchall()
    except Exception as e:
        logger.error("Query error: %s", e, exc_info=True)
        return "Error al ejecutar la consulta", None
    finally:
        cursor.close()


class ReportsService:

    # ------------ MASCOTAS ------------
    @staticmethod
    def get_pets_by_species(period: str):
        connection = get_connection()
        interval = period_map.get(period, "30 DAY")
        try:
            error, rows = _exec(connection, f"""
            SELECT s.species_name, COUNT(p.pet_id) AS total
            FROM PETS AS p INNER JOIN SPECIES AS s ON p.species_id = s.species_id
            WHERE p.pet_date >= DATE_SUB(NOW(), INTERVAL {interval})
            GROUP BY s.species_name ORDER BY total DESC
            """)
            if error:
                raise ServiceError(error)
            return None, [{"species": r[0], "total": r[1]} for r in rows]
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_pets_by_species: %s", e, exc_info=True)
            return "Error al obtener mascotas por especie", None
        finally:
            connection.close()

    @staticmethod
    def get_pets_growth(period: str):
        connection = get_connection()
        interval = period_map.get(period, "30 DAY")
        use_daily = period in daily_periods
        group_expr = "DATE(pet_date)" if use_daily else "DATE_FORMAT(pet_date, '%Y-%m')"
        select_expr = "DATE(pet_date)" if use_daily else "DATE_FORMAT(pet_date, '%Y-%m')"
        try:
            error, rows = _exec(connection, f"""
            SELECT {select_expr} AS label, COUNT(*) AS total
            FROM PETS WHERE pet_date >= DATE_SUB(NOW(), INTERVAL {interval})
            GROUP BY {group_expr} ORDER BY {group_expr} ASC
            """)
            if error:
                raise ServiceError(error)
            return None, [{"date": str(r[0]), "total": r[1]} for r in rows]
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_pets_growth: %s", e, exc_info=True)
            return "Error al obtener el crecimiento de mascotas", None
        finally:
            connection.close()

    # ------------ CITAS ------------
    @staticmethod
    def get_appointments_growth(period: str):
        connection = get_connection()
        interval = period_map.get(period, "30 DAY")
        use_daily = period in daily_periods
        group_expr = "DATE(appointment_date_created)" if use_daily else "DATE_FORMAT(appointment_date_created, '%Y-%m')"
        select_expr = group_expr
        try:
            error, rows = _exec(connection, f"""
            SELECT {select_expr} AS label, COUNT(*) AS total
            FROM APPOINTMENTS WHERE appointment_date_created >= DATE_SUB(NOW(), INTERVAL {interval})
            GROUP BY {group_expr} ORDER BY {group_expr} ASC
            """)
            if error:
                raise ServiceError(error)
            return None, [{"date": str(r[0]), "total": r[1]} for r in rows]
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_appointments_growth: %s", e, exc_info=True)
            return "Error al obtener el crecimiento de citas", None
        finally:
            connection.close()

    @staticmethod
    def get_appointments_by_status():
        connection = get_connection()
        try:
            error, rows = _exec(connection, """
            SELECT appointment_status, COUNT(*) AS total
            FROM APPOINTMENTS GROUP BY appointment_status ORDER BY appointment_status
            """)
            if error:
                raise ServiceError(error)
            return None, [{"status": r[0], "total": r[1]} for r in rows]
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_appointments_by_status: %s", e, exc_info=True)
            return "Error al obtener citas por estado", None
        finally:
            connection.close()

    # ------------ CONSULTAS ------------
    @staticmethod
    def get_consultations_growth(period: str):
        connection = get_connection()
        interval = period_map.get(period, "30 DAY")
        use_daily = period in daily_periods
        group_expr = "DATE(consultation_date)" if use_daily else "DATE_FORMAT(consultation_date, '%Y-%m')"
        select_expr = group_expr
        try:
            error, rows = _exec(connection, f"""
            SELECT {select_expr} AS label, COUNT(*) AS total
            FROM CONSULTATIONS WHERE consultation_date >= DATE_SUB(NOW(), INTERVAL {interval})
            GROUP BY {group_expr} ORDER BY {group_expr} ASC
            """)
            if error:
                raise ServiceError(error)
            return None, [{"date": str(r[0]), "total": r[1]} for r in rows]
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_consultations_growth: %s", e, exc_info=True)
            return "Error al obtener el crecimiento de consultas", None
        finally:
            connection.close()

    @staticmethod
    def get_recent_consultations():
        connection = get_connection()
        try:
            error, rows = _exec(connection, """
            SELECT p.pet_name, CONCAT(o.owner_name,' ',o.owner_first_surname), s.species_name,
                   CONCAT(u.user_name,' ',u.user_first_surname), c.consultation_date,
                   c.consultation_diagnosis
            FROM CONSULTATIONS AS c
            INNER JOIN PETS AS p ON c.pet_id = p.pet_id
            INNER JOIN OWNERS AS o ON p.owner_id = o.owner_id
            INNER JOIN SPECIES AS s ON p.species_id = s.species_id
            INNER JOIN USERS AS u ON c.user_id = u.user_id
            ORDER BY c.consultation_id DESC LIMIT 8
            """)
            if error:
                raise ServiceError(error)
            return None, [
                {"pet_name": r[0], "owner": r[1], "species": r[2],
                 "vet": r[3], "date": str(r[4]), "diagnosis": r[5]}
                for r in rows
            ]
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_recent_consultations: %s", e, exc_info=True)
            return "Error al obtener las consultas recientes", None
        finally:
            connection.close()

    # ------------ VACUNACIONES ------------
    @staticmethod
    def get_vaccinations_growth(period: str):
        connection = get_connection()
        interval = period_map.get(period, "30 DAY")
        use_daily = period in daily_periods
        group_expr = "DATE(vaccination_date)" if use_daily else "DATE_FORMAT(vaccination_date, '%Y-%m')"
        select_expr = group_expr
        try:
            error, rows = _exec(connection, f"""
            SELECT {select_expr} AS label, COUNT(*) AS total
            FROM VACCINATIONS WHERE vaccination_date >= DATE_SUB(NOW(), INTERVAL {interval})
            GROUP BY {group_expr} ORDER BY {group_expr} ASC
            """)
            if error:
                raise ServiceError(error)
            return None, [{"date": str(r[0]), "total": r[1]} for r in rows]
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_vaccinations_growth: %s", e, exc_info=True)
            return "Error al obtener el crecimiento de vacunaciones", None
        finally:
            connection.close()

    @staticmethod
    def get_vaccinations_by_vaccine(period: str):
        connection = get_connection()
        interval = period_map.get(period, "30 DAY")
        try:
            error, rows = _exec(connection, f"""
            SELECT vac.vaccine_name, COUNT(va.vaccination_id) AS total
            FROM VACCINATIONS AS va INNER JOIN VACCINES AS vac ON va.vaccine_id = vac.vaccine_id
            WHERE va.vaccination_date >= DATE_SUB(NOW(), INTERVAL {interval})
            GROUP BY vac.vaccine_name ORDER BY total DESC
            """)
            if error:
                raise ServiceError(error)
            return None, [{"vaccine": r[0], "total": r[1]} for r in rows]
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_vaccinations_by_vaccine: %s", e, exc_info=True)
            return "Error al obtener vacunaciones por vacuna", None
        finally:
            connection.close()

    # ------------ PROPIETARIOS ------------
    @staticmethod
    def get_owners_growth(period: str):
        connection = get_connection()
        interval = period_map.get(period, "30 DAY")
        use_daily = period in daily_periods
        group_expr = "DATE(owner_date)" if use_daily else "DATE_FORMAT(owner_date, '%Y-%m')"
        select_expr = group_expr
        try:
            error, rows = _exec(connection, f"""
            SELECT {select_expr} AS label, COUNT(*) AS total
            FROM OWNERS WHERE owner_date >= DATE_SUB(NOW(), INTERVAL {interval})
            GROUP BY {group_expr} ORDER BY {group_expr} ASC
            """)
            if error:
                raise ServiceError(error)
            return None, [{"date": str(r[0]), "total": r[1]} for r in rows]
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_owners_growth: %s", e, exc_info=True)
            return "Error al obtener el crecimiento de propietarios", None
        finally:
            connection.close()
