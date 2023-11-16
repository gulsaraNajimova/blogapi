from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.core.containers import Container
from app.core.dependencies import get_current_user
from app.models.users_model import UserModel
from app.schemas.auth_schema import SignInInfo, SignUpInfo, SignInResponse, SignUpResponse
from app.services.auth_service import AuthService

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.post("/sign-in", response_model=SignInResponse)
@inject
async def sign_in(sign_in_info: SignInInfo, service: AuthService = Depends(Provide[Container.auth_service])):
    return service.sign_in(sign_in_info)


@auth_router.post("sign-up", response_model=SignUpResponse)
@inject
async def sign_up(sign_up_info: SignUpInfo, service: AuthService = Depends(Provide[Container.auth_service])):
    return service.sign_up(sign_up_info)


@auth_router.get("/me")
async def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

