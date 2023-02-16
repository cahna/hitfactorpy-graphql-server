from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter


def make_app():
    from . import __version__ as app_version
    from .deps import strawberry_context_provider
    from .schema import make_schema

    app = FastAPI(
        title="HitFactor API",
        description="Manage practical match reports with GraphQL",
        version=app_version,
    )
    schema = make_schema()
    graphql_app = GraphQLRouter(schema, context_getter=strawberry_context_provider)
    app.include_router(graphql_app, prefix="/graphql")

    return app
