from ariadne_graphql_modules import DeferredType, ObjectType, gql, convert_case
from hitfactorpy_sqlalchemy.orm import models

from ..scalars import UUID

from .parsed_match_report import ParsedMatchReport
from .parsed_match_report_competitor import ParsedMatchReportCompetitor


class ParsedMatchReportStage(ObjectType):
    __aliases__ = convert_case
    __fields_args__ = convert_case
    __requires__ = [
        UUID,
        ParsedMatchReport,
        ParsedMatchReportCompetitor,
        DeferredType("ParsedMatchReportStageScore"),
    ]
    __schema__ = gql(
        """
        type ParsedMatchReportStage {
            id: UUID!
            match: ParsedMatchReport!
            name: String
            minRounds: Int!
            maxPoints: Int!
            classifier: Boolean!
            classifierNumber: String
            stageNumber: Int
            stageScores: [ParsedMatchReportStageScore]
        }
        """
    )

    # @staticmethod
    # def resolve_id(stage: models.MatchReportStage, *_):
    #     return stage.uuid

    # @staticmethod
    # def resolve_match(stage: models.MatchReportStage, *_):
    #     return stage.match

    # @staticmethod
    # def resolve_name(stage: models.MatchReportStage, *_):
    #     return stage.name

    # @staticmethod
    # def resolve_min_rounds(stage: models.MatchReportStage, *_):
    #     return stage.min_rounds

    # @staticmethod
    # def resolve_max_points(stage: models.MatchReportStage, *_):
    #     return stage.max_points

    # @staticmethod
    # def resolve_classifier(stage: models.MatchReportStage, *_):
    #     return stage.classifier

    # @staticmethod
    # def resolve_classifier_number(stage: models.MatchReportStage, *_):
    #     return stage.classifier_number

    # @staticmethod
    # def resolve_stage_number(stage: models.MatchReportStage, *_):
    #     return stage.stage_number

    # @staticmethod
    # def resolve_stage_scores(stage: models.MatchReportStage, *_):
    #     return stage.stage_scores

