from fastapi import Depends

from .schema.context import HitFactorDataLoaders, HitFactorRequestContext


async def session_provider():
    from hitfactorpy_sqlalchemy.session import get_sqlalchemy_url, make_async_session

    SessionLocal = make_async_session(get_sqlalchemy_url(scheme="postgresql+asyncpg"))
    async with SessionLocal() as session:
        async with session.begin():
            try:
                yield session
            # except:  # noqa: E722
            #     await session.rollback()
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
