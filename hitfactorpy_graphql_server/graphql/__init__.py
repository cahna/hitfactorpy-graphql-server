from ariadne_graphql_modules import make_executable_schema


def make_schema():
    from .scalars import types as scalar_types
    from .types import types as object_types
    from .enums import types as enum_types
    from .query import types as query_types

    return make_executable_schema(*scalar_types, *enum_types, *object_types, *query_types)
