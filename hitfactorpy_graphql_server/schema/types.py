from datetime import date, datetime
from typing import Any, cast

import strawberry
from hitfactorpy import enums
from hitfactorpy_sqlalchemy.orm import models
from strawberry.types import Info

from .context import HitFactorRequestContext

Division = strawberry.enum(enums.Division)  # type: ignore
Classification = strawberry.enum(enums.Classification)  # type: ignore
MatchLevel = strawberry.enum(enums.MatchLevel)  # type: ignore
PowerFactor = strawberry.enum(enums.PowerFactor)  # type: ignore


@strawberry.type
class CompetitorSummary:
    id: strawberry.ID
    member_number: str | None


@strawberry.type
class StageSummary:
    id: strawberry.ID
    name: str | None


@strawberry.type
class ParsedMatchReportSummary:
    id: strawberry.ID
    name: str | None
    date: date | None
    created: datetime | None
    updated: datetime | None
    match_level: MatchLevel | None
    competitor_count: int
    competitor_summaries: list[CompetitorSummary]
    competitor_ids: strawberry.Private[list[strawberry.ID]]
    stage_count: int
    stage_summaries: list[StageSummary]
    stage_ids: strawberry.Private[list[strawberry.ID]]

    @strawberry.field
    async def competitors(self, info: Info[HitFactorRequestContext, Any]) -> list["ParsedMatchReportCompetitor"]:
        return await info.context.data_loaders.competitor.load_many(self.competitor_ids)

    @strawberry.field
    async def stages(self, info: Info[HitFactorRequestContext, Any]) -> list["ParsedMatchReportStage"]:
        return await info.context.data_loaders.stage.load_many(self.stage_ids)

    @classmethod
    def from_orm(cls, match_report: models.MatchReport) -> "ParsedMatchReportSummary":
        return cls(
            id=strawberry.ID(str(match_report.id)),
            name=match_report.name,
            date=match_report.date,
            created=match_report.created,
            updated=match_report.updated,
            match_level=match_report.match_level,  # type: ignore
            competitor_count=len(match_report.competitors),
            competitor_summaries=[
                CompetitorSummary(id=strawberry.ID(str(c.id)), member_number=c.member_number)
                for c in match_report.competitors
            ],
            competitor_ids=[strawberry.ID(str(c.id)) for c in match_report.competitors],
            stage_count=len(match_report.stages),
            stage_summaries=[StageSummary(id=strawberry.ID(str(s.id)), name=s.name) for s in match_report.stages],
            stage_ids=[strawberry.ID(str(s.id)) for s in match_report.stages],
        )


@strawberry.type
class ParsedMatchReportCompetitor:
    id: strawberry.ID
    member_number: str | None
    first_name: str | None
    last_name: str | None
    division: Division
    classification: Classification
    power_factor: PowerFactor
    dq: bool | None
    reentry: bool | None
    match_id: strawberry.Private[strawberry.ID]
    stage_score_ids: strawberry.Private[list[strawberry.ID]]

    @strawberry.field
    async def match(self, info: Info[HitFactorRequestContext, Any]) -> ParsedMatchReportSummary:
        return await info.context.data_loaders.match_report_summary.load(self.match_id)

    @strawberry.field
    async def stage_scores(self, info: Info[HitFactorRequestContext, Any]) -> list["ParsedMatchReportStageScore"]:
        return await info.context.data_loaders.stage_score.load_many(self.stage_score_ids)

    @classmethod
    def from_orm(cls, competitor: models.MatchReportCompetitor) -> "ParsedMatchReportCompetitor":
        return cls(
            id=strawberry.ID(str(competitor.id)),
            member_number=competitor.member_number,
            first_name=competitor.first_name,
            last_name=competitor.last_name,
            division=cast(Division, competitor.division),
            classification=cast(Classification, competitor.classification),
            power_factor=cast(PowerFactor, competitor.power_factor),
            dq=competitor.dq,
            reentry=competitor.reentry,
            match_id=strawberry.ID(str(competitor.match_id)),
            stage_score_ids=[strawberry.ID(str(stage_score.id)) for stage_score in competitor.stage_scores],
        )


@strawberry.type
class ParsedMatchReportStage:
    id: strawberry.ID
    match_id: strawberry.Private[strawberry.ID]
    name: str
    min_rounds: int
    max_points: int
    classifier: bool
    classifier_number: str
    stage_number: int
    stage_score_ids: strawberry.Private[list[strawberry.ID]]

    @strawberry.field
    async def match(self, info: Info[HitFactorRequestContext, Any]) -> ParsedMatchReportSummary:
        return await info.context.data_loaders.match_report_summary.load(self.match_id)

    @strawberry.field
    async def stage_scores(self, info: Info[HitFactorRequestContext, Any]) -> list["ParsedMatchReportStageScore"]:
        return await info.context.data_loaders.stage_score.load_many(self.stage_score_ids)

    @classmethod
    def from_orm(cls, stage: models.MatchReportStage) -> "ParsedMatchReportStage":
        return cls(
            id=strawberry.ID(str(stage.id)),
            match_id=strawberry.ID(str(stage.match_id)),
            name=cast(str, stage.name),
            min_rounds=cast(int, stage.min_rounds),
            max_points=cast(int, stage.max_points),
            classifier=bool(stage.classifier),
            classifier_number=cast(str, stage.classifier_number),
            stage_number=cast(int, stage.stage_number),
            stage_score_ids=[strawberry.ID(str(stage_score.id)) for stage_score in stage.stage_scores],
        )


@strawberry.type
class ParsedMatchReportStageScore:
    id: strawberry.ID
    match_id: strawberry.Private[strawberry.ID]
    competitor_id: strawberry.Private[strawberry.ID]
    stage_id: strawberry.Private[strawberry.ID]
    dq: bool
    dnf: bool
    a: int
    c: int
    d: int
    m: int
    npm: int
    ns: int
    procedural: int
    late_shot: int
    extra_shot: int
    extra_hit: int
    other_penalty: int

    @strawberry.field
    async def match(self, info: Info[HitFactorRequestContext, Any]) -> ParsedMatchReportSummary:
        return await info.context.data_loaders.match_report_summary.load(self.match_id)

    @strawberry.field
    async def competitor(self, info: Info[HitFactorRequestContext, Any]) -> ParsedMatchReportCompetitor:
        return await info.context.data_loaders.competitor.load(self.competitor_id)

    @strawberry.field
    async def stage(self, info: Info[HitFactorRequestContext, Any]) -> ParsedMatchReportStage:
        return await info.context.data_loaders.stage.load(self.stage_id)

    @classmethod
    def from_orm(cls, stage_score: models.MatchReportStageScore) -> "ParsedMatchReportStageScore":
        return cls(
            id=strawberry.ID(str(stage_score.id)),
            match_id=strawberry.ID(str(stage_score.match_id)),
            competitor_id=strawberry.ID(str(stage_score.competitor_id)),
            stage_id=strawberry.ID(str(stage_score.stage_id)),
            dq=bool(stage_score.dq),
            dnf=bool(stage_score.dnf),
            a=cast(int, stage_score.a),
            c=cast(int, stage_score.c),
            d=cast(int, stage_score.d),
            m=cast(int, stage_score.m),
            npm=cast(int, stage_score.npm),
            ns=cast(int, stage_score.ns),
            procedural=cast(int, stage_score.procedural),
            late_shot=cast(int, stage_score.late_shot),
            extra_shot=cast(int, stage_score.extra_shot),
            extra_hit=cast(int, stage_score.extra_hit),
            other_penalty=cast(int, stage_score.other_penalty),
        )
