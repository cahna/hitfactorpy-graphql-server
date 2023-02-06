from ariadne_graphql_modules import ObjectType, gql, convert_case
from .types.parsed_match_report import ParsedMatchReport


class ParsedMatchReportQuery(ObjectType):
    __aliases__ = convert_case
    __fields_args__ = convert_case
    __requires__ = [ParsedMatchReport]
    __schema__ = gql(
        """
        type Query {
            parsedMatchReport(id: String!): ParsedMatchReport
            parsedMatchReports: [ParsedMatchReport]
        }
        """
    )

    @staticmethod
    def resolve_parsed_match_report(*_, id: str):
        return None

    @staticmethod
    def resolve_parsed_match_reports(*_):
        from hitfactorpy_sqlalchemy.session import make_sync_session, get_sqlalchemy_url
        Session = make_sync_session(get_sqlalchemy_url())
        with Session() as session:
            import sqlalchemy as sa
            from hitfactorpy_sqlalchemy.orm import models
            stmt = sa.select(models.MatchReport)
            result = session.execute(stmt)
            reports = [r[0] for r in result.fetchall()]
            return reports

"""
By convention, export all types to be merged into the graphql schema here.
"""
types = [ParsedMatchReportQuery]