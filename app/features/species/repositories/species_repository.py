from app.utils.logger import get_logger
from app.features.species.models.species_schema import CreateSpeciesSchema, FilterSpeciesSchema
from app.features.species.models.species_response import SpeciesResponse

logger = get_logger("species.repository")


class SpeciesRepository:

    @staticmethod
    def find_all_species(filters: FilterSpeciesSchema, connection):
        data = filters.model_dump(exclude_none=True)
        cursor = connection.cursor()
        query = "SELECT species_id, species_name, species_status FROM SPECIES"
        filters_list, values = [], []
        if "status" in data:
            filters_list.append("species_status = %s")
            values.append(data["status"])
        if filters_list:
            query += " WHERE " + " AND ".join(filters_list)
        query += " ORDER BY species_name ASC"
        try:
            cursor.execute(query, values)
            result = cursor.fetchall()
            return None, [SpeciesResponse(species_id=r[0], species_name=r[1], species_status=r[2]) for r in result]
        except Exception as e:
            logger.error("Error en find_all_species: %s", e, exc_info=True)
            return "Error al obtener las especies", None
        finally:
            cursor.close()

    @staticmethod
    def find_species_by_id(species_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT species_id, species_name, species_status FROM SPECIES WHERE species_id = %s",
                (species_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None, None
            return None, SpeciesResponse(species_id=row[0], species_name=row[1], species_status=row[2])
        except Exception as e:
            logger.error("Error en find_species_by_id: %s", e, exc_info=True)
            return "Error al obtener la especie", None
        finally:
            cursor.close()

    @staticmethod
    def find_species_by_name(name: str, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT species_id FROM SPECIES WHERE LOWER(species_name) = LOWER(%s)", (name,)
            )
            return None, cursor.fetchone()
        except Exception as e:
            logger.error("Error en find_species_by_name: %s", e, exc_info=True)
            return "Error al verificar la especie", None
        finally:
            cursor.close()

    @staticmethod
    def create_species(species_data: CreateSpeciesSchema, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO SPECIES (species_name) VALUES (%s)", (species_data.name,)
            )
            return None, True, "Especie creada correctamente"
        except Exception as e:
            logger.error("Error en create_species: %s", e, exc_info=True)
            return "Error al crear la especie", False, None
        finally:
            cursor.close()

    @staticmethod
    def update_species(species_id: int, name: str, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE SPECIES SET species_name = %s WHERE species_id = %s", (name, species_id)
            )
            return None, True, "Especie actualizada correctamente"
        except Exception as e:
            logger.error("Error en update_species: %s", e, exc_info=True)
            return "Error al actualizar la especie", False, None
        finally:
            cursor.close()

    @staticmethod
    def disable_species(species_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE SPECIES SET species_status = 1 WHERE species_id = %s", (species_id,)
            )
            return None, True, "Especie deshabilitada correctamente"
        except Exception as e:
            logger.error("Error en disable_species: %s", e, exc_info=True)
            return "Error al deshabilitar la especie", False, None
        finally:
            cursor.close()

    @staticmethod
    def enable_species(species_id: int, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE SPECIES SET species_status = 2 WHERE species_id = %s", (species_id,)
            )
            return None, True, "Especie habilitada correctamente"
        except Exception as e:
            logger.error("Error en enable_species: %s", e, exc_info=True)
            return "Error al habilitar la especie", False, None
        finally:
            cursor.close()
