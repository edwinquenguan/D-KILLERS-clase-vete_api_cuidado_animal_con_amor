from app.utils.logger import get_logger
from app.utils.date_formatter import date_formatter
from app.features.pets.models.pets_schema import CreatePetSchema, FilterPetsSchema, UpdatePetSchema
from app.features.pets.models.pets_response import PetResponse

logger = get_logger("pets.repository")

PET_FIELDS = {
    "name": "pet_name",
    "birthdate": "pet_birthdate",
    "sex": "pet_sex",
    "color": "pet_color",
    "weight": "pet_weight",
    "breed_id": "breed_id",
}


def _row_to_pet(row) -> PetResponse:
    return PetResponse(
        pet_id=row[0], name=row[1], birthdate=str(row[2]), sex=row[3],
        color=row[4], weight=float(row[5]), pet_status=row[6], pet_date=date_formatter(row[7]),
        owner_id=row[8], owner_name=row[9], owner_phone=row[10], owner_email=row[11],
        species_id=row[12], species_name=row[13], breed_id=row[14], breed_name=row[15]
    )


class PetsRepository:

    @staticmethod
    def find_all_pets(filters: FilterPetsSchema, connection):
        data = filters.model_dump(exclude_none=True)
        cursor = connection.cursor()
        query = """
        SELECT p.pet_id, p.pet_name, p.pet_birthdate, p.pet_sex, p.pet_color, p.pet_weight,
               p.pet_status, p.pet_date,
               o.owner_id, CONCAT(o.owner_name,' ',o.owner_first_surname), o.owner_phone, o.owner_email,
               s.species_id, s.species_name, b.breed_id, b.breed_name
        FROM PETS AS p
        INNER JOIN OWNERS AS o ON p.owner_id = o.owner_id
        INNER JOIN SPECIES AS s ON p.species_id = s.species_id
        INNER JOIN BREEDS AS b ON p.breed_id = b.breed_id
        """
        filters_list, values = [], []
        if "owner_id" in data:
            filters_list.append("p.owner_id = %s")
            values.append(data["owner_id"])
        if "species_id" in data:
            filters_list.append("p.species_id = %s")
            values.append(data["species_id"])
        if "status" in data:
            filters_list.append("p.pet_status = %s")
            values.append(data["status"])
        if filters_list:
            query += " WHERE " + " AND ".join(filters_list)
        query += " ORDER BY p.pet_name ASC"
        try:
            cursor.execute(query, values)
            return None, [_row_to_pet(r) for r in cursor.fetchall()]
        except Exception as e:
            logger.error("Error en find_all_pets: %s", e, exc_info=True)
            return "Error al obtener las mascotas", None
        finally:
            cursor.close()

    @staticmethod
    def find_pet_by_id(pet_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(
                """SELECT p.pet_id, p.pet_name, p.pet_birthdate, p.pet_sex, p.pet_color, p.pet_weight,
                          p.pet_status, p.pet_date,
                          o.owner_id, CONCAT(o.owner_name,' ',o.owner_first_surname), o.owner_phone, o.owner_email,
                          s.species_id, s.species_name, b.breed_id, b.breed_name
                   FROM PETS AS p
                   INNER JOIN OWNERS AS o ON p.owner_id = o.owner_id
                   INNER JOIN SPECIES AS s ON p.species_id = s.species_id
                   INNER JOIN BREEDS AS b ON p.breed_id = b.breed_id
                   WHERE p.pet_id = %s""",
                (pet_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None, None
            return None, _row_to_pet(row)
        except Exception as e:
            logger.error("Error en find_pet_by_id: %s", e, exc_info=True)
            return "Error al obtener la mascota", None
        finally:
            cursor.close()

    @staticmethod
    def create_pet(pet_data: CreatePetSchema, connection):
        data = pet_data.model_dump()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """INSERT INTO PETS (owner_id, species_id, breed_id, pet_name, pet_birthdate, pet_sex, pet_color, pet_weight)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (data["owner_id"], data["species_id"], data["breed_id"], data["name"],
                 data["birthdate"], data["sex"], data["color"], data["weight"])
            )
            return None, True, "Mascota registrada correctamente"
        except Exception as e:
            logger.error("Error en create_pet: %s", e, exc_info=True)
            return "Error al registrar la mascota", False, None
        finally:
            cursor.close()

    @staticmethod
    def update_pet(pet_id: int, pet_data: UpdatePetSchema, connection):
        data = pet_data.model_dump(exclude_none=True)
        cursor = connection.cursor()
        try:
            mapped = {PET_FIELDS[k]: v for k, v in data.items() if k in PET_FIELDS}
            if not mapped:
                return "No hay campos para actualizar", False, None
            columns = ", ".join(f"{col} = %s" for col in mapped.keys())
            values = list(mapped.values()) + [pet_id]
            cursor.execute(f"UPDATE PETS SET {columns} WHERE pet_id = %s", values)
            return None, True, "Mascota actualizada correctamente"
        except Exception as e:
            logger.error("Error en update_pet: %s", e, exc_info=True)
            return "Error al actualizar la mascota", False, None
        finally:
            cursor.close()

    @staticmethod
    def disable_pet(pet_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE PETS SET pet_status = 1 WHERE pet_id = %s", (pet_id,))
            return None, True, "Mascota desactivada correctamente"
        except Exception as e:
            logger.error("Error en disable_pet: %s", e, exc_info=True)
            return "Error al desactivar la mascota", False, None
        finally:
            cursor.close()

    @staticmethod
    def enable_pet(pet_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE PETS SET pet_status = 2 WHERE pet_id = %s", (pet_id,))
            return None, True, "Mascota activada correctamente"
        except Exception as e:
            logger.error("Error en enable_pet: %s", e, exc_info=True)
            return "Error al activar la mascota", False, None
        finally:
            cursor.close()
