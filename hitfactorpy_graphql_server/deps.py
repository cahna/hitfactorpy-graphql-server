from fastapi import Depends
from hitfactorpy_sqlalchemy.session import get_sqlalchemy_url, make_async_session

from .config import HitFactorConfig
from .schema.context import HitFactorDataLoaders, HitFactorRequestContext


async def config_provider() -> HitFactorConfig:
    return HitFactorConfig()


async def sqlalchemy_url_provider(config: HitFactorConfig = Depends(config_provider)) -> str:
    return str(config.SQLALCHEMY_POSTGRES_DSN)


async def alembic_url_provider(config: HitFactorConfig = Depends(config_provider)) -> str:
    return str(config.ALEMBIC_POSTGRES_DSN)


async def session_provider(sqlalchemy_url: str = Depends(sqlalchemy_url_provider)):
    SessionLocal = make_async_session(sqlalchemy_url, echo=True)
    async with SessionLocal() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()


async def data_loaders_provider(db=Depends(session_provider)) -> HitFactorDataLoaders:
    return HitFactorDataLoaders.build(db=db)


async def hit_factor_request_context_provider(
    db=Depends(session_provider), data_loaders=Depends(data_loaders_provider)
) -> HitFactorRequestContext:
    return HitFactorRequestContext(db=db, data_loaders=data_loaders)


async def strawberry_context_provider(
    context=Depends(hit_factor_request_context_provider),
):
    return context
