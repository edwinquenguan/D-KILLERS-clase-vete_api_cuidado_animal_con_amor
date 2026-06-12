from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.pets.repositories.pets_repository import PetsRepository
from app.features.pets.models.pets_schema import CreatePetSchema, FilterPetsSchema, RegisterMyPetSchema, UpdatePetSchema

logger = get_logger("pets.service")


class PetsService:

    @staticmethod
    def get_all_pets(filters: FilterPetsSchema):
        connection = get_connection()
        try:
            error, data = PetsRepository.find_all_pets(filters, connection)
            if error:
                raise ServiceError(error)
            return None, data
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_all_pets: %s", e, exc_info=True)
            return "Error al obtener las mascotas", None
        finally:
            connection.close()

    @staticmethod
    def get_my_pets(user_id: int):
        connection = get_connection()
        try:
            error, data = PetsRepository.find_pets_by_user_id(user_id, connection)
            if error:
                raise ServiceError(error)
            return None, data
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_my_pets: %s", e, exc_info=True)
            return "Error al obtener tus mascotas", None
        finally:
            connection.close()

    @staticmethod
    def get_pet_by_id(pet_id: int):
        connection = get_connection()
        try:
            error, pet = PetsRepository.find_pet_by_id(pet_id, connection)
            if error:
                raise ServiceError(error)
            if not pet:
                raise ServiceError("Mascota no encontrada")
            return None, pet
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_pet_by_id: %s", e, exc_info=True)
            return "Error al obtener la mascota", None
        finally:
            connection.close()

    @staticmethod
    def register_my_pet(user_id: int, pet_data: RegisterMyPetSchema):
        connection = get_connection()
        try:
            error, success, message = PetsRepository.create_pet_for_client(user_id, pet_data, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Mascota registrada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en register_my_pet: %s", e, exc_info=True)
            return "Error al registrar la mascota", False, None
        finally:
            connection.close()

    @staticmethod
    def create_pet(pet_data: CreatePetSchema):
        connection = get_connection()
        try:
            error, success, message = PetsRepository.create_pet(pet_data, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Mascota registrada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en create_pet: %s", e, exc_info=True)
            return "Error al registrar la mascota", False, None
        finally:
            connection.close()

    @staticmethod
    def update_pet(pet_id: int, pet_data: UpdatePetSchema):
        connection = get_connection()
        try:
            error, pet = PetsRepository.find_pet_by_id(pet_id, connection)
            if error:
                raise ServiceError(error)
            if not pet:
                raise ServiceError("Mascota no encontrada")
            error, success, message = PetsRepository.update_pet(pet_id, pet_data, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Mascota actualizada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en update_pet: %s", e, exc_info=True)
            return "Error al actualizar la mascota", False, None
        finally:
            connection.close()

    @staticmethod
    def disable_pet(pet_id: int):
        connection = get_connection()
        try:
            error, pet = PetsRepository.find_pet_by_id(pet_id, connection)
            if error:
                raise ServiceError(error)
            if not pet:
                raise ServiceError("Mascota no encontrada")
            error, success, message = PetsRepository.disable_pet(pet_id, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Mascota desactivada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en disable_pet: %s", e, exc_info=True)
            return "Error al desactivar la mascota", False, None
        finally:
            connection.close()

    @staticmethod
    def enable_pet(pet_id: int):
        connection = get_connection()
        try:
            error, pet = PetsRepository.find_pet_by_id(pet_id, connection)
            if error:
                raise ServiceError(error)
            if not pet:
                raise ServiceError("Mascota no encontrada")
            error, success, message = PetsRepository.enable_pet(pet_id, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Mascota activada correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en enable_pet: %s", e, exc_info=True)
            return "Error al activar la mascota", False, None
        finally:
            connection.close()
