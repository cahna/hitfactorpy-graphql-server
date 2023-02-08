from ariadne.asgi import GraphQL
from ariadne.constants import PLAYGROUND_HTML

from fastapi import FastAPI

from .graphql import make_schema

def make_app():
    from . import __version__ as app_version
    app = FastAPI(
        title="HitFactor API",
        description="Manage practical match reports with GraphQL",
        version=app_version,
    )

    # @app.on_event("startup")
    # async def startup():
    #     await data.database.connect()


    # @app.on_event("shutdown")
    # async def shutdown():
    #     await data.database.disconnect()

    schema = make_schema()

    # graphql_app = GraphQL(schema, debug=True)
    # app.mount("/", graphql_app)

    @app.get("/graphql")
    async def graphql_ide():
        return PLAYGROUND_HTML

    @app.route("/graphql", methods=["POST"])
    def graphql_ide():

    return app
