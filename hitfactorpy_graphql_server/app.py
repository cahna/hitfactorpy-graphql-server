from pathlib import Path
from ariadne import EnumType, QueryType, make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL

from hitfactorpy.enums import Classification, PowerFactor, Division, Scoring, MatchLevel
import os

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

type_defs = load_schema_from_path(str(ROOT_DIR / "schema.graphql"))
enum_classification = EnumType("Classification", Classification)
enum_power_factor = EnumType("PowerFactor", PowerFactor)
enum_division = EnumType("Division", Division)
enum_scoring = EnumType("Scoring", Scoring)
enum_match_level = EnumType("MatchLevel", MatchLevel)

query = QueryType()


@query.field("parsedMatchReports")
def resolve_parsed_match_reports(*_):
    return {"data": [{"name": "test", "matchLevel": MatchLevel.I}]}


schema = make_executable_schema(
    type_defs, query, enum_classification, enum_power_factor, enum_division, enum_scoring, enum_match_level
)
app = GraphQL(schema, debug=True)
