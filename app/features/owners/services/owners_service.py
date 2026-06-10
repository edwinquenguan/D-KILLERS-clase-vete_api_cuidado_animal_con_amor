from app.utils.logger import get_logger
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.features.owners.repositories.owners_repository import OwnersRepository
from app.features.owners.models.owners_schema import CreateOwnerSchema, FilterOwnersSchema, UpdateOwnerSchema

logger = get_logger("owners.service")


class OwnersService:

    @staticmethod
    def get_all_owners(filters: FilterOwnersSchema):
        connection = get_connection()
        try:
            error, owners = OwnersRepository.find_all_owners(filters, connection)
            if error:
                raise ServiceError(error)
            return None, owners
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_all_owners: %s", e, exc_info=True)
            return "Error al obtener los propietarios", None
        finally:
            connection.close()

    @staticmethod
    def get_owner_by_id(owner_id: int):
        connection = get_connection()
        try:
            error, owner = OwnersRepository.find_owner_by_id(owner_id, connection)
            if error:
                raise ServiceError(error)
            if not owner:
                raise ServiceError("Propietario no encontrado")
            return None, owner
        except ServiceError as e:
            return e.message, None
        except Exception as e:
            logger.error("Error en get_owner_by_id: %s", e, exc_info=True)
            return "Error al obtener el propietario", None
        finally:
            connection.close()

    @staticmethod
    def create_owner(owner_data: CreateOwnerSchema):
        connection = get_connection()
        try:
            error, existing = OwnersRepository.find_owner_by_email(owner_data.email, connection)
            if error:
                raise ServiceError(error)
            if existing:
                raise ServiceError("Ya existe un propietario registrado con este correo electrónico")
            error, success, message = OwnersRepository.create_owner(owner_data, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Propietario creado correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en create_owner: %s", e, exc_info=True)
            return "Error al crear el propietario", False, None
        finally:
            connection.close()

    @staticmethod
    def update_owner(owner_id: int, owner_data: UpdateOwnerSchema):
        connection = get_connection()
        try:
            error, owner = OwnersRepository.find_owner_by_id(owner_id, connection)
            if error:
                raise ServiceError(error)
            if not owner:
                raise ServiceError("Propietario no encontrado")
            error, success, message = OwnersRepository.update_owner(owner_id, owner_data, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Propietario actualizado correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en update_owner: %s", e, exc_info=True)
            return "Error al actualizar el propietario", False, None
        finally:
            connection.close()

    @staticmethod
    def disable_owner(owner_id: int):
        connection = get_connection()
        try:
            error, owner = OwnersRepository.find_owner_by_id(owner_id, connection)
            if error:
                raise ServiceError(error)
            if not owner:
                raise ServiceError("Propietario no encontrado")
            error, success, message = OwnersRepository.disable_owner(owner_id, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Propietario deshabilitado correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en disable_owner: %s", e, exc_info=True)
            return "Error al deshabilitar el propietario", False, None
        finally:
            connection.close()

    @staticmethod
    def enable_owner(owner_id: int):
        connection = get_connection()
        try:
            error, owner = OwnersRepository.find_owner_by_id(owner_id, connection)
            if error:
                raise ServiceError(error)
            if not owner:
                raise ServiceError("Propietario no encontrado")
            error, success, message = OwnersRepository.enable_owner(owner_id, connection)
            if error or not success:
                raise ServiceError(error)
            connection.commit()
            return None, True, "Propietario habilitado correctamente"
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None
        except Exception as e:
            connection.rollback()
            logger.error("Error en enable_owner: %s", e, exc_info=True)
            return "Error al habilitar el propietario", False, None
        finally:
            connection.close()
