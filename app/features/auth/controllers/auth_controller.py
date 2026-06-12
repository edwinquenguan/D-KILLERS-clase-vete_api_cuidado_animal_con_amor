from fastapi import HTTPException, Request, Response
from pydantic import EmailStr

from app.features.auth.models.auth_model import RegisterClientModel, VerifyRoleModel
from app.features.auth.services.auth_service import AuthService
from app.features.users.services.users_service import UsersService


class AuthController:
    @staticmethod
    def login(email: str, password: str, response: Response):
        error, success, message, user_data = AuthService.login(
            email, password, response
        )

        if error or not success:
            raise HTTPException(
                status_code=401, detail="Credenciales invalidas"
            )

        return {
            "success": success,
            "message": message,
            "data": user_data,
        }

    @staticmethod
    def refresh_tokens(request: Request, response: Response):
        error, success, message = AuthService.refresh_tokens(
            request, response
        )

        if error or not success:
            raise HTTPException(
                status_code=401, detail=error
            )

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def verify_roles(body: VerifyRoleModel, payload: dict):
        error, success = AuthService.verify_roles(
            body, payload
        )

        if error or not success:
            raise HTTPException(status_code=401, detail="No autorizado")

        return {
            "success": success
        }

    @staticmethod
    def logout(response: Response):
        error, success, message = AuthService.logout(
            response
        )

        if error or not success:
            raise HTTPException(status_code=401, detail=error)

        return {
            "success": success,
            "message": message
        }

    @staticmethod
    def get_current_user(payload: dict):
        user_id = int(payload["user_id"])
        error, users = UsersService.get_user_by_id(user_id)
        if error or not users:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        u = users[0]
        return {
            "data": {
                "user_id": u.id,
                "name": f"{u.name} {u.first_surname}",
                "email": u.email,
                "role": payload["role"],
            }
        }

    @staticmethod
    def register_client(data: RegisterClientModel, response: Response):
        error, success, message, user_data = AuthService.register_client(data, response)
        if error or not success:
            raise HTTPException(status_code=400, detail=error or "Error al registrar")
        return {"success": True, "message": message, "data": user_data}

    @staticmethod
    async def recover_password(email: EmailStr):
        success, message = AuthService.recover_password(
            email
        )

        return {
            "success": success,
            "message": message
        }
