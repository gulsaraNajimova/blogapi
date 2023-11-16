from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.containers import Container
from app.core.dependencies import get_current_user, get_current_superuser
from app.models.users_model import UserModel
from app.schemas.user_schema import EditUserInfo, BaseUser
from app.services.user_service import UserService

users_router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@users_router.patch("/update-user-info", response_model=BaseUser)
@inject
async def update_user_info(user_info: EditUserInfo,
                           current_user: UserModel = Depends(get_current_user),
                           service: UserService = Depends(Provide[Container.user_service])):
    return service.update(id=current_user.id, schema=user_info)


@users_router.delete("/delete-account")
@inject
async def delete_account(current_user: UserModel = Depends(get_current_user),
                         service: UserService = Depends(Provide[Container.user_service])):
    service.delete(current_user.id)
    return "User Successfully Deleted"


# for Admin
@users_router.get("/get-all-users", response_model=List[BaseUser])
@inject
async def get_all_users(skip: int = 0, limit: int = 100,
                        current_user: UserModel = Depends(get_current_superuser),
                        service: UserService = Depends(Provide[Container.user_service])):
    return service.get_all_users(skip, limit)


@users_router.get("/get-user")
@inject
async def get_user(user_id: int, current_user: UserModel = Depends(get_current_superuser),
                   service: UserService = Depends(Provide[Container.user_service])):
    return service.get_by_id(user_id, eager=False)

