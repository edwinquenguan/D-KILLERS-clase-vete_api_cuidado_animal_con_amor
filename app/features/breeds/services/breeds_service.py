from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.breeds.repositories.breeds_repository import BreedsRepository
from app.features.breeds.models.breeds_schema import CreateBreedSchema, FilterBreedsSchema, UpdateBreedSchema

logger = get_logger("breeds.service")


class BreedsService:

    @staticmethod
    def get_all_breeds(filters: FilterBreedsSchema):
        connection = get_connection()
        try:
            error, data = BreedsRepository.find_all_breeds(filters, connection)
            if error:
                raise ServiceError(error)
            return None, data
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_all_breeds: %s", e, exc_info=True)
            return "Error al obtener las razas", None
        finally:
            connection.close()

    @staticmethod
    def get_breed_by_id(breed_id: int):
        connection = get_connection()
        try:
            error, breed = BreedsRepository.find_breed_by_id(breed_id, connection)
            if error:
                raise ServiceError(error)
            if not breed:
                raise ServiceError("Raza no encontrada")
            return None, breed
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_breed_by_id: %s", e, exc_info=True)
            return "Error al obtener la raza", None
        finally:
            connection.close()

    @staticmethod
    def create_breed(breed_data: CreateBreedSchema):
        connection = get_connection()
        try:
            error, success, message = BreedsRepository.create_breed(breed_data, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Raza creada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en create_breed: %s", e, exc_info=True)
            return "Error al crear la raza", False, None
        finally:
            connection.close()

    @staticmethod
    def update_breed(breed_id: int, breed_data: UpdateBreedSchema):
        connection = get_connection()
        try:
            error, breed = BreedsRepository.find_breed_by_id(breed_id, connection)
            if error:
                raise ServiceError(error)
            if not breed:
                raise ServiceError("Raza no encontrada")
            if breed_data.name:
                error, success, message = BreedsRepository.update_breed(breed_id, breed_data.name, connection)
                if error or not success:
                    raise ServiceError(error)
            connection.commit()
            return None, True, "Raza actualizada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en update_breed: %s", e, exc_info=True)
            return "Error al actualizar la raza", False, None
        finally:
            connection.close()

    @staticmethod
    def disable_breed(breed_id: int):
        connection = get_connection()
        try:
            error, breed = BreedsRepository.find_breed_by_id(breed_id, connection)
            if error:
                raise ServiceError(error)
            if not breed:
                raise ServiceError("Raza no encontrada")
            error, success, message = BreedsRepository.disable_breed(breed_id, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Raza deshabilitada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en disable_breed: %s", e, exc_info=True)
            return "Error al deshabilitar la raza", False, None
        finally:
            connection.close()

    @staticmethod
    def enable_breed(breed_id: int):
        connection = get_connection()
        try:
            error, breed = BreedsRepository.find_breed_by_id(breed_id, connection)
            if error:
                raise ServiceError(error)
            if not breed:
                raise ServiceError("Raza no encontrada")
            error, success, message = BreedsRepository.enable_breed(breed_id, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Raza habilitada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en enable_breed: %s", e, exc_info=True)
            return "Error al habilitar la raza", False, None
        finally:
            connection.close()
