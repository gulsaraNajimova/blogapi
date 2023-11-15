from fastapi import FastAPI, status

from app.core.config import configs
from app.core.containers import Container
from app.routers.blog import blog_router
from app.routers.users import users_router
from app.routers.auth import auth_router
from app.routers.comments import comment_router


class AppCreator:
    def __init__(self):
        self.app = FastAPI(
            title=configs.PROJECT_NAME,
            description="Write your blogs; Read others stories; Engage with them through comments!",
            openapi_url=f"{configs.API}/openapi.json",
            version="0.0.1",
        )

        # set db and container
        self.container = Container()
        self.db = self.container.db()
        # self.db.create_database()

        # set routes
        @self.app.get("/")
        def root():
            return "service is working"

        app.include_router(auth_router)
        app.include_router(blog_router)
        app.include_router(comment_router)
        app.include_router(users_router)


app_creator = AppCreator()
app = app_creator.app
db = app_creator.db
container = app_creator.container

