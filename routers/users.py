from fastapi import APIRouter
from schemas.user_schema import EditUserInfo, User

users_router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@users_router.patch("/update-user-info")
async def update_user_info(user_info: EditUserInfo):
    return User


@users_router.delete("/delete-user")
async def delete_user():
    return "User Successfully Deleted"


# for Admin
@users_router.get("/get-all-users")
async def get_all_users():
    pass


@users_router.get("/get-user")
async def get_user():
    pass

