from datetime import timedelta

import bcrypt
import jwt
from jwt import PyJWTError
from pydantic import EmailStr
from fastapi import Request, Response

from app.core.config import settings
from app.core.database import get_connection
from app.core.exception import ServiceError
from app.core.security import create_access_token, create_refresh_token, set_auth_cookies, verify_password
from app.features.auth.models.auth_model import RegisterClientModel, VerifyRoleModel
from app.features.users.repositories.users_repository import UsersRepository
from app.features.users.services.users_service import UsersService
from app.tasks.email_tasks import recovery_password_email


class AuthService:
    @staticmethod
    def login(email: str, password: str, response: Response):
        try:
            error, user = UsersService.get_user_by_email(email)

            if error or not user:
                raise ServiceError(error)

            # Validación de los parametros recibidos
            verify_password(user[6], password)

            # Tiempo en que expira el token
            expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)

            # Creación del token
            access_token = create_access_token({
                "sub": str(user[1]),
                "role": user[0]
            },
                expires_delta=expires
            )

            refresh_token = create_refresh_token({
                "sub": str(user[1]),
                "role": user[0]
            }
            )

            set_auth_cookies(response, access_token, refresh_token)

            return None, True, "Inicio de sesión exitoso", {
                "user_id": user[1],
                "name": f"{user[2]} {user[3]}",
                "email": user[5],
                "role": user[0],
            }

        except ServiceError as e:
            return e.message, False, "No autorizado", None

    @staticmethod
    def refresh_tokens(request: Request, response: Response):
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise ServiceError("Refresh token no encontrado")

        try:
            payload = jwt.decode(
                refresh_token,
                settings.REFRESH_TOKEN_SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id = payload.get("sub")

            if not user_id:
                raise ServiceError("Refresh token inválido")

        except PyJWTError:
            raise ServiceError(
                "Refresh token expirado o inválido"
            )

        new_access_token = create_access_token({
            "sub": str(user_id),
            "role": payload.get("role")
        },
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
        )

        new_refresh_token = create_refresh_token({
            "sub": user_id,
            "role": payload.get("role")
        })

        set_auth_cookies(response, new_access_token, new_refresh_token)

        return None, True, "Tokens actualizados correctamente"

    @staticmethod
    def verify_roles(body: VerifyRoleModel, payload: dict):
        try:
            user_role = payload.get("role")
            roles = body.roles

            if user_role not in roles:
                raise ServiceError("No autorizado")

            return None, True

        except ServiceError as e:
            return e.message, None

        except Exception as e:
            return "Error al intentar verificar los roles", None

    @staticmethod
    def logout(response: Response):
        try:
            response.delete_cookie(key="access_token", path="/api")
            response.delete_cookie(key="refresh_token",
                                   path="/api/auth/refresh")

            return None, True, "Sesión cerrada exitosamente"

        except Exception as e:
            return "Error al intentar cerrar la sesión", False, None

    @staticmethod
    def register_client(data: RegisterClientModel, response: Response):
        connection = get_connection()
        try:
            error, existing = UsersRepository.find_user_by_email(data.email, connection)
            if existing:
                return "Este correo ya está registrado", False, None, None

            hashed = bcrypt.hashpw(
                data.password.encode("utf-8"), bcrypt.gensalt(rounds=12)
            ).decode("utf-8")

            cursor = connection.cursor()
            cursor.execute(
                """INSERT INTO USERS
                   (rol_id, user_name, user_first_surname, user_second_surname,
                    user_phone, user_email, user_address, user_password, user_city)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (4, data.name, data.first_surname, data.second_surname or "",
                 data.phone, data.email, data.address or "Sin especificar",
                 hashed, data.city)
            )
            cursor.close()

            # Crear entrada en OWNERS si no existe ya (para ligar mascotas y citas)
            cursor2 = connection.cursor()
            cursor2.execute("SELECT owner_id FROM OWNERS WHERE owner_email = %s", (data.email,))
            if not cursor2.fetchone():
                cursor2.execute(
                    """INSERT INTO OWNERS
                       (owner_name, owner_first_surname, owner_second_surname,
                        owner_phone, owner_email, owner_address, owner_city)
                       VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                    (data.name, data.first_surname, data.second_surname or "",
                     data.phone, data.email, data.address or "Sin especificar",
                     data.city)
                )
            cursor2.close()
            connection.commit()

            expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
            error2, user = UsersRepository.find_user_by_email(data.email, connection)
            access_token  = create_access_token({"sub": str(user[1]), "role": user[0]}, expires_delta=expires)
            refresh_token = create_refresh_token({"sub": str(user[1]), "role": user[0]})
            set_auth_cookies(response, access_token, refresh_token)

            return None, True, "Registro exitoso", {
                "user_id": user[1],
                "name": f"{user[2]} {user[3]}",
                "email": user[5],
                "role": user[0],
            }
        except ServiceError as e:
            connection.rollback()
            return e.message, False, None, None
        except Exception:
            connection.rollback()
            return "Error al registrar el usuario", False, None, None
        finally:
            connection.close()

    @staticmethod
    def recover_password(email: EmailStr):
        try:
            error, user = UsersService.get_user_by_email(email)

            if user:
                recovery_password_email.delay(
                    user_email=email,
                    user_name=user[2]
                )

        except Exception:
            pass

        return True, "Correo enviado correctamente"
