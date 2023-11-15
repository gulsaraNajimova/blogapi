from dependency_injector import containers, providers

from app.core.config import configs
from app.core.database import Database
from app.repositories.blog_repository import BlogRepository
from app.repositories.comments_repository import CommentRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.blog_service import BlogService
from app.services.comment_service import CommentService
from app.services.user_service import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.routers.auth",
            "app.routers.blog",
            "app.routers.comments",
            "app.routers.user",
            "app.core.dependencies"
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DATABASE_URI)

    blog_repository = providers.Factory(BlogRepository, session_factory=db.provided.session)
    comments_repository = providers.Factory(CommentRepository, session_factory=db.provided.session)
    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)

    auth_service = providers.Factory(AuthService, repository=user_repository)
    blog_service = providers.Factory(BlogService, repository=blog_repository)
    comment_service = providers.Factory(CommentService, repository=comments_repository)
    user_service = providers.Factory(UserService, repository=user_repository)

