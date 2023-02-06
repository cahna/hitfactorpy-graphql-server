from ariadne_graphql_modules import DeferredType, ObjectType, gql, convert_case
from hitfactorpy_sqlalchemy.orm import models

from ..enums import MatchLevel
from ..scalars import UUID


class ParsedMatchReport(ObjectType):
    __aliases__ = convert_case
    __fields_args__ = convert_case
    __requires__ = [
        UUID,
        MatchLevel,
        DeferredType("ParsedMatchReportCompetitor"),
        DeferredType("ParsedMatchReportStage"),
        DeferredType("ParsedMatchReportStageScore"),
    ]
    __schema__ = gql(
        """
        type ParsedMatchReport {
            id: UUID!
            name: String
            matchLevel: MatchLevel
            competitors: [ParsedMatchReportCompetitor]
            stages: [ParsedMatchReportStage]
            stageScores: [ParsedMatchReportStageScore]
        }
        """
    )

    @staticmethod
    def resolve_id(report: models.MatchReport, *_):
        return report.uuid

    # @staticmethod
    # def resolve_name(report: models.MatchReport, *_):
    #     return report.name

    # @staticmethod
    # def resolve_match_level(report: models.MatchReport, *_):
    #     return report.match_level

    # @staticmethod
    # def resolve_competitors(report: models.MatchReport, *_):
    #     return report.competitors

    # @staticmethod
    # def resolve_stages(report: models.MatchReport, *_):
    #     return report.stages

    # @staticmethod
    # def resolve_stage_scores(report: models.MatchReport, *_):
    #     return report.stage_scores
