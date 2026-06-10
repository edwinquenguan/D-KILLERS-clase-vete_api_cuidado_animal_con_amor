from fastapi import HTTPException
from app.features.owners.services.owners_service import OwnersService
from app.features.owners.models.owners_schema import CreateOwnerSchema, FilterOwnersSchema, UpdateOwnerSchema


class OwnersController:

    @staticmethod
    def get_all_owners(filters: FilterOwnersSchema):
        error, data = OwnersService.get_all_owners(filters)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def get_owner_by_id(owner_id: int):
        error, data = OwnersService.get_owner_by_id(owner_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"data": data}

    @staticmethod
    def create_owner(owner_data: CreateOwnerSchema):
        error, success, message = OwnersService.create_owner(owner_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def update_owner(owner_id: int, owner_data: UpdateOwnerSchema):
        error, success, message = OwnersService.update_owner(owner_id, owner_data)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def disable_owner(owner_id: int):
        error, success, message = OwnersService.disable_owner(owner_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"success": success, "message": message}

    @staticmethod
    def enable_owner(owner_id: int):
        error, success, message = OwnersService.enable_owner(owner_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return {"success": success, "message": message}
