from fastapi import Depends, FastAPI
from strawberry.fastapi import GraphQLRouter

from .strawberry_context import HitFactorRequestContext


async def get_db():
    from hitfactorpy_sqlalchemy.session import get_sqlalchemy_url, make_async_session

    SessionLocal = make_async_session(get_sqlalchemy_url(scheme="postgresql+asyncpg"))
    async with SessionLocal() as session:
        async with session.begin():
            try:
                yield session
            except:  # noqa: E722
                await session.rollback()
            finally:
                await session.close()


async def hit_factor_request_context_dependency(db=Depends(get_db)) -> HitFactorRequestContext:
    return HitFactorRequestContext(db=db)


async def get_context(
    context=Depends(hit_factor_request_context_dependency),
):
    return context


def make_app():
    from . import __version__ as app_version
    from .schema import schema

    app = FastAPI(
        title="HitFactor API",
        description="Manage practical match reports with GraphQL",
        version=app_version,
    )

    graphql_app = GraphQLRouter(schema, context_getter=get_context)
    app.include_router(graphql_app, prefix="/graphql")

    return app
