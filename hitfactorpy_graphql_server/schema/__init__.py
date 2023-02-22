import strawberry
from strawberry.extensions import QueryDepthLimiter

from .query import Query


def make_schema():
    return strawberry.Schema(
        query=Query,
        extensions=[
            QueryDepthLimiter(max_depth=5),
        ],
    )
