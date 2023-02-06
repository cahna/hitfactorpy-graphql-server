from ariadne.asgi import GraphQL

from .graphql import make_schema



schema = make_schema()
app = GraphQL(schema, debug=True)
