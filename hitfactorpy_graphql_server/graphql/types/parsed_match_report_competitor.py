from ariadne_graphql_modules import DeferredType, ObjectType, gql, convert_case
from hitfactorpy_sqlalchemy.orm import models

from ..enums import PowerFactor, Classification, Division
from ..scalars import UUID

from .parsed_match_report import ParsedMatchReport


class ParsedMatchReportCompetitor(ObjectType):
    __aliases__ = convert_case
    __fields_args__ = convert_case
    __requires__ = [
        UUID,
        Division,
        Classification,
        PowerFactor,
        ParsedMatchReport,
        DeferredType("ParsedMatchReportCompetitor"),
        DeferredType("ParsedMatchReportStage"),
        DeferredType("ParsedMatchReportStageScore"),
    ]
    __schema__ = gql(
        """
        type ParsedMatchReportCompetitor {
            id: UUID!
            match: ParsedMatchReport!
            memberNumber: String
            firstName: String
            lastName: String
            division: Division
            classification: Classification
            powerFactor: PowerFactor
            dq: Boolean
            reentry: Boolean
            stageScores: [ParsedMatchReportStageScore]
        }
        """
    )

    @staticmethod
    def resolve_id(competitor: models.MatchReportCompetitor, *_):
        return competitor.uuid
