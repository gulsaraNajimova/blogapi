from fastapi import APIRouter
from app.schemas.auth_schema import SignInInfo, SignUpInfo


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.post("/sign-in")
async def sign_in(user_info: SignInInfo):
    return user_info


@auth_router.post("sign-up")
async def sign_up(user_info: SignUpInfo):
    return user_info


@auth_router.get("/me")
async def get_me():
    pass

