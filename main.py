from fastapi import FastAPI, status
from routers.blog import blog_router
from routers.users import users_router
from routers.auth import auth_router
from routers.comments import comment_router

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"detail": "Service is working!"}


app.include_router(auth_router)
app.include_router(blog_router)
app.include_router(comment_router)
app.include_router(users_router)