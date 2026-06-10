from app.utils.logger import get_logger
from app.utils.date_formatter import date_formatter
from app.features.owners.models.owners_schema import CreateOwnerSchema, FilterOwnersSchema, UpdateOwnerSchema
from app.features.owners.models.owners_response import OwnerResponse

logger = get_logger("owners.repository")

OWNER_FIELDS = {
    "name": "owner_name",
    "first_surname": "owner_first_surname",
    "second_surname": "owner_second_surname",
    "phone": "owner_phone",
    "email": "owner_email",
    "address": "owner_address",
    "city": "owner_city",
}


class OwnersRepository:

    @staticmethod
    def find_all_owners(filters_data: FilterOwnersSchema, connection):
        data = filters_data.model_dump(exclude_none=True)
        cursor = connection.cursor()

        query = """
        SELECT
            o.owner_id, o.owner_name, o.owner_first_surname, o.owner_second_surname,
            o.owner_phone, o.owner_email, o.owner_address,
            o.owner_city, c.city_name, o.owner_status, o.owner_date
        FROM OWNERS AS o
        INNER JOIN CITIES AS c ON o.owner_city = c.city_id
        """

        filters = []
        values = []

        if "start_date" in data:
            filters.append("DATE(o.owner_date) >= %s")
            values.append(data["start_date"])
        if "end_date" in data:
            filters.append("DATE(o.owner_date) <= %s")
            values.append(data["end_date"])
        if "status" in data:
            filters.append("o.owner_status = %s")
            values.append(data["status"])
        if "city" in data:
            filters.append("o.owner_city = %s")
            values.append(data["city"])

        if filters:
            query += " WHERE " + " AND ".join(filters)

        if data.get("name_order") == "asc":
            query += " ORDER BY o.owner_name ASC"
        elif data.get("name_order") == "desc":
            query += " ORDER BY o.owner_name DESC"

        try:
            cursor.execute(query, values)
            result = cursor.fetchall()
            owners = [
                OwnerResponse(
                    owner_id=row[0], name=row[1], first_surname=row[2], second_surname=row[3],
                    phone=row[4], email=row[5], address=row[6],
                    city_id=row[7], city_name=row[8], owner_status=row[9], owner_date=date_formatter(row[10])
                )
                for row in result
            ]
            return None, owners
        except Exception as e:
            logger.error("Error en find_all_owners: %s", e, exc_info=True)
            return "Error al obtener los propietarios", None
        finally:
            cursor.close()

    @staticmethod
    def find_owner_by_id(owner_id: int, connection):
        cursor = connection.cursor()
        query = """
        SELECT
            o.owner_id, o.owner_name, o.owner_first_surname, o.owner_second_surname,
            o.owner_phone, o.owner_email, o.owner_address,
            o.owner_city, c.city_name, o.owner_status, o.owner_date
        FROM OWNERS AS o
        INNER JOIN CITIES AS c ON o.owner_city = c.city_id
        WHERE o.owner_id = %s
        """
        try:
            cursor.execute(query, (owner_id,))
            row = cursor.fetchone()
            if not row:
                return None, None
            owner = OwnerResponse(
                owner_id=row[0], name=row[1], first_surname=row[2], second_surname=row[3],
                phone=row[4], email=row[5], address=row[6],
                city_id=row[7], city_name=row[8], owner_status=row[9], owner_date=date_formatter(row[10])
            )
            return None, owner
        except Exception as e:
            logger.error("Error en find_owner_by_id: %s", e, exc_info=True)
            return "Error al obtener el propietario", None
        finally:
            cursor.close()

    @staticmethod
    def find_owner_by_email(email: str, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT owner_id FROM OWNERS WHERE LOWER(owner_email) = LOWER(%s)", (email,))
            return None, cursor.fetchone()
        except Exception as e:
            logger.error("Error en find_owner_by_email: %s", e, exc_info=True)
            return "Error al verificar el email del propietario", None
        finally:
            cursor.close()

    @staticmethod
    def create_owner(owner_data: CreateOwnerSchema, connection):
        data = owner_data.model_dump()
        cursor = connection.cursor()
        query = """
        INSERT INTO OWNERS (
            owner_name, owner_first_surname, owner_second_surname,
            owner_phone, owner_email, owner_address, owner_city
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (
                data["name"], data["first_surname"], data["second_surname"],
                data["phone"], data["email"], data["address"], data["city"]
            ))
            return None, True, "Propietario creado correctamente"
        except Exception as e:
            logger.error("Error en create_owner: %s", e, exc_info=True)
            return "Error al crear el propietario", False, None
        finally:
            cursor.close()

    @staticmethod
    def update_owner(owner_id: int, owner_data: UpdateOwnerSchema, connection):
        data = owner_data.model_dump(exclude_none=True)
        cursor = connection.cursor()
        try:
            mapped = {OWNER_FIELDS[k]: v for k, v in data.items() if k in OWNER_FIELDS}
            if not mapped:
                return "No hay campos para actualizar", False, None
            columns = ", ".join(f"{col} = %s" for col in mapped.keys())
            values = list(mapped.values()) + [owner_id]
            cursor.execute(f"UPDATE OWNERS SET {columns} WHERE owner_id = %s", values)
            return None, True, "Propietario actualizado correctamente"
        except Exception as e:
            logger.error("Error en update_owner: %s", e, exc_info=True)
            return "Error al actualizar el propietario", False, None
        finally:
            cursor.close()

    @staticmethod
    def disable_owner(owner_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE OWNERS SET owner_status = 1 WHERE owner_id = %s", (owner_id,))
            return None, True, "Propietario deshabilitado correctamente"
        except Exception as e:
            logger.error("Error en disable_owner: %s", e, exc_info=True)
            return "Error al deshabilitar el propietario", False, None
        finally:
            cursor.close()

    @staticmethod
    def enable_owner(owner_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE OWNERS SET owner_status = 2 WHERE owner_id = %s", (owner_id,))
            return None, True, "Propietario habilitado correctamente"
        except Exception as e:
            logger.error("Error en enable_owner: %s", e, exc_info=True)
            return "Error al habilitar el propietario", False, None
        finally:
            cursor.close()
