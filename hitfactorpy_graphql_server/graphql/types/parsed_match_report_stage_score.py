from ariadne_graphql_modules import ObjectType, gql, convert_case
from hitfactorpy_sqlalchemy.orm import models

from ..scalars import UUID
from .parsed_match_report import ParsedMatchReport
from .parsed_match_report_competitor import ParsedMatchReportCompetitor
from .parsed_match_report_stage import ParsedMatchReportStage


class ParsedMatchReportStageScore(ObjectType):
    __aliases__ = convert_case
    __fields_args__ = convert_case
    __requires__ = [UUID, ParsedMatchReport, ParsedMatchReportCompetitor, ParsedMatchReportStage]
    __schema__ = gql(
        """
        type ParsedMatchReportStageScore {
            id: UUID!
            match: ParsedMatchReport!
            competitor: ParsedMatchReportCompetitor!
            stage: ParsedMatchReportStage!
            dq: Boolean!
            dnf: Boolean!
            a: Int!
            c: Int!
            d: Int!
            m: Int!
            npm: Int!
            ns: Int!
            procedural: Int!
            lateShot: Int!
            extraShot: Int!
            extraHit: Int!
            otherPenalty: Int!
        }
        """
    )

    # @staticmethod
    # def resolve_id(stage_score: models.MatchReportStageScore, *_):
    #     return stage_score.uuid

    # @staticmethod
    # def resolve_match(stage_score: models.MatchReportStageScore, *_):
    #     return stage_score.match

    # @staticmethod
    # def resolve_stage(stage_score: models.MatchReportStageScore, *_):
    #     return stage_score.stage

    # @staticmethod
    # def resolve_competitor(stage_score: models.MatchReportStageScore, *_):
    #     return stage_score.competitor

    # @staticmethod
    # def resolve_a(stage_score: models.MatchReportStageScore, *_):
    #     return stage_score.a

    # @staticmethod
    # def resolve_c(stage_score: models.MatchReportStageScore, *_):
    #     return stage_score.c

    # @staticmethod
    # def resolve_d(stage_score: models.MatchReportStageScore, *_):
    #     return stage_score.d

    # @staticmethod
    # def resolve_m(stage_score: models.MatchReportStageScore, *_):
    #     return stage_score.m

    # @staticmethod
    # def resolve_ns(stage_score: models.MatchReportStageScore, *_):
    #     return stage_score.ns

    # @staticmethod
    # def resolve_npm(stage_score: models.MatchReportStageScore, *_):
    #     return stage_score.npm

    # @staticmethod
    # def resolve_procedural(stage_score: models.MatchReportStageScore, *_):
    #     return stage_score.procedural
