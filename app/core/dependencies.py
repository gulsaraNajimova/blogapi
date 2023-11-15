from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from jose import jwt
from pydantic import ValidationError

from app.core.config import configs
from app.core.containers import Container
from app.core.exceptions import AuthError
from app.core.security import JWTBearer, ALGORITHM
from app.models.users_model import UserModel
from app.schemas.auth_schema import Payload
from app.services.user_service import UserService


@inject
def get_current_user(
        token: str = Depends(JWTBearer()),
        service: UserService = Depends(Provide[Container.user_service])) -> UserModel:
    try:
        payload = jwt.decode(token, configs.SECRET_KEY, ALGORITHM)
        token_data = Payload(**payload)
    except ValidationError:
        raise AuthError(detail="Could not Validate Credentials")
    current_user = service.get_by_id(token_data.id)
    if not current_user:
        raise AuthError(detail="User not Found")
    return current_user


def get_current_superuser(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    if not current_user.is_superuser:
        raise AuthError(detail="It's not a Super User")
    return current_user

