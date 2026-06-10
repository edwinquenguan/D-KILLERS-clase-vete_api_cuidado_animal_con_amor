from app.utils.logger import get_logger
from app.features.breeds.models.breeds_schema import CreateBreedSchema, FilterBreedsSchema
from app.features.breeds.models.breeds_response import BreedResponse

logger = get_logger("breeds.repository")


class BreedsRepository:

    @staticmethod
    def find_all_breeds(filters: FilterBreedsSchema, connection):
        data = filters.model_dump(exclude_none=True)
        cursor = connection.cursor()
        query = """
        SELECT b.breed_id, b.species_id, s.species_name, b.breed_name, b.breed_status
        FROM BREEDS AS b
        INNER JOIN SPECIES AS s ON b.species_id = s.species_id
        """
        filters_list, values = [], []
        if "species_id" in data:
            filters_list.append("b.species_id = %s")
            values.append(data["species_id"])
        if "status" in data:
            filters_list.append("b.breed_status = %s")
            values.append(data["status"])
        if filters_list:
            query += " WHERE " + " AND ".join(filters_list)
        query += " ORDER BY s.species_name ASC, b.breed_name ASC"
        try:
            cursor.execute(query, values)
            result = cursor.fetchall()
            return None, [BreedResponse(breed_id=r[0], species_id=r[1], species_name=r[2], breed_name=r[3], breed_status=r[4]) for r in result]
        except Exception as e:
            logger.error("Error en find_all_breeds: %s", e, exc_info=True)
            return "Error al obtener las razas", None
        finally:
            cursor.close()

    @staticmethod
    def find_breed_by_id(breed_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(
                """SELECT b.breed_id, b.species_id, s.species_name, b.breed_name, b.breed_status
                FROM BREEDS AS b INNER JOIN SPECIES AS s ON b.species_id = s.species_id
                WHERE b.breed_id = %s""",
                (breed_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None, None
            return None, BreedResponse(breed_id=row[0], species_id=row[1], species_name=row[2], breed_name=row[3], breed_status=row[4])
        except Exception as e:
            logger.error("Error en find_breed_by_id: %s", e, exc_info=True)
            return "Error al obtener la raza", None
        finally:
            cursor.close()

    @staticmethod
    def create_breed(breed_data: CreateBreedSchema, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO BREEDS (species_id, breed_name) VALUES (%s, %s)",
                (breed_data.species_id, breed_data.name)
            )
            return None, True, "Raza creada correctamente"
        except Exception as e:
            logger.error("Error en create_breed: %s", e, exc_info=True)
            return "Error al crear la raza", False, None
        finally:
            cursor.close()

    @staticmethod
    def update_breed(breed_id: int, name: str, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE BREEDS SET breed_name = %s WHERE breed_id = %s", (name, breed_id))
            return None, True, "Raza actualizada correctamente"
        except Exception as e:
            logger.error("Error en update_breed: %s", e, exc_info=True)
            return "Error al actualizar la raza", False, None
        finally:
            cursor.close()

    @staticmethod
    def disable_breed(breed_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE BREEDS SET breed_status = 1 WHERE breed_id = %s", (breed_id,))
            return None, True, "Raza deshabilitada correctamente"
        except Exception as e:
            logger.error("Error en disable_breed: %s", e, exc_info=True)
            return "Error al deshabilitar la raza", False, None
        finally:
            cursor.close()

    @staticmethod
    def enable_breed(breed_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE BREEDS SET breed_status = 2 WHERE breed_id = %s", (breed_id,))
            return None, True, "Raza habilitada correctamente"
        except Exception as e:
            logger.error("Error en enable_breed: %s", e, exc_info=True)
            return "Error al habilitar la raza", False, None
        finally:
            cursor.close()
