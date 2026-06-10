from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.species.repositories.species_repository import SpeciesRepository
from app.features.species.models.species_schema import CreateSpeciesSchema, FilterSpeciesSchema, UpdateSpeciesSchema

logger = get_logger("species.service")


class SpeciesService:

    @staticmethod
    def get_all_species(filters: FilterSpeciesSchema):
        connection = get_connection()
        try:
            error, data = SpeciesRepository.find_all_species(filters, connection)
            if error:
                raise ServiceError(error)
            return None, data
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_all_species: %s", e, exc_info=True)
            return "Error al obtener las especies", None
        finally:
            connection.close()

    @staticmethod
    def get_species_by_id(species_id: int):
        connection = get_connection()
        try:
            error, species = SpeciesRepository.find_species_by_id(species_id, connection)
            if error:
                raise ServiceError(error)
            if not species:
                raise ServiceError("Especie no encontrada")
            return None, species
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_species_by_id: %s", e, exc_info=True)
            return "Error al obtener la especie", None
        finally:
            connection.close()

    @staticmethod
    def create_species(species_data: CreateSpeciesSchema):
        connection = get_connection()
        try:
            error, existing = SpeciesRepository.find_species_by_name(species_data.name, connection)
            if error:
                raise ServiceError(error)
            if existing:
                raise ServiceError("Ya existe una especie con ese nombre")
            error, success, message = SpeciesRepository.create_species(species_data, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Especie creada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en create_species: %s", e, exc_info=True)
            return "Error al crear la especie", False, None
        finally:
            connection.close()

    @staticmethod
    def update_species(species_id: int, species_data: UpdateSpeciesSchema):
        connection = get_connection()
        try:
            error, species = SpeciesRepository.find_species_by_id(species_id, connection)
            if error:
                raise ServiceError(error)
            if not species:
                raise ServiceError("Especie no encontrada")
            if species_data.name:
                error, success, message = SpeciesRepository.update_species(species_id, species_data.name, connection)
                if error or not success:
                    raise ServiceError(error)
            connection.commit()
            return None, True, "Especie actualizada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en update_species: %s", e, exc_info=True)
            return "Error al actualizar la especie", False, None
        finally:
            connection.close()

    @staticmethod
    def disable_species(species_id: int):
        connection = get_connection()
        try:
            error, species = SpeciesRepository.find_species_by_id(species_id, connection)
            if error:
                raise ServiceError(error)
            if not species:
                raise ServiceError("Especie no encontrada")
            error, success, message = SpeciesRepository.disable_species(species_id, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Especie deshabilitada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en disable_species: %s", e, exc_info=True)
            return "Error al deshabilitar la especie", False, None
        finally:
            connection.close()

    @staticmethod
    def enable_species(species_id: int):
        connection = get_connection()
        try:
            error, species = SpeciesRepository.find_species_by_id(species_id, connection)
            if error:
                raise ServiceError(error)
            if not species:
                raise ServiceError("Especie no encontrada")
            error, success, message = SpeciesRepository.enable_species(species_id, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Especie habilitada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en enable_species: %s", e, exc_info=True)
            return "Error al habilitar la especie", False, None
        finally:
            connection.close()
