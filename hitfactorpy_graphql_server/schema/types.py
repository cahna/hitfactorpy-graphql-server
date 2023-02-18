from datetime import date, datetime
from typing import Any, cast
from uuid import UUID

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
    id: UUID
    member_number: str | None


@strawberry.type
class StageSummary:
    id: UUID
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
    competitor_ids: list[CompetitorSummary]
    stage_count: int
    stage_ids: list[StageSummary]
    stage_score_count: int

    @classmethod
    def from_orm(cls, match_report: models.MatchReport):
        return cls(
            id=strawberry.ID(str(match_report.id)),
            name=match_report.name,
            date=match_report.date,
            created=match_report.created,
            updated=match_report.updated,
            match_level=match_report.match_level,  # type: ignore
            competitor_count=len(match_report.competitors),
            competitor_ids=[
                CompetitorSummary(id=c.id, member_number=c.member_number) for c in match_report.competitors
            ],
            stage_count=len(match_report.stages),
            stage_ids=[StageSummary(id=s.id, name=s.name) for s in match_report.stages],
            stage_score_count=len(match_report.stage_scores),
        )


@strawberry.type
class ParsedMatchReport:
    id: UUID
    name: str | None
    date: date | None
    match_level: MatchLevel | None

    @strawberry.field
    async def competitors(self, info: Info[HitFactorRequestContext, Any]) -> list["ParsedMatchReportCompetitor"]:
        competitor_ids = await info.context.data_loaders.fk_competitors_for_match.load(self.id)
        return cast(
            list["ParsedMatchReportCompetitor"], await info.context.data_loaders.competitors.load_many(competitor_ids)
        )

    @strawberry.field
    async def stages(self, info: Info[HitFactorRequestContext, Any]) -> list["ParsedMatchReportStage"]:
        stage_ids = await info.context.data_loaders.fk_stages_for_match.load(self.id)
        return cast(list["ParsedMatchReportStage"], await info.context.data_loaders.stages.load_many(stage_ids))

    @strawberry.field
    async def stage_scores(self, info: Info[HitFactorRequestContext, Any]) -> list["ParsedMatchReportStageScore"]:
        stage_score_ids = await info.context.data_loaders.fk_stage_scores_for_match.load(self.id)
        return cast(
            list["ParsedMatchReportStageScore"], await info.context.data_loaders.stage_scores.load_many(stage_score_ids)
        )


@strawberry.type
class ParsedMatchReportCompetitor:
    id: UUID
    match_id: strawberry.Private[UUID]
    member_number: str
    first_name: str
    last_name: str
    division: Division
    classification: Classification
    power_factor: PowerFactor
    dq: bool
    reentry: bool

    @strawberry.field
    async def match(self, info: Info[HitFactorRequestContext, Any]) -> ParsedMatchReport:
        return cast(ParsedMatchReport, await info.context.data_loaders.match_reports.load(self.match_id))

    @strawberry.field
    async def stage_scores(self, info: Info[HitFactorRequestContext, Any]) -> list["ParsedMatchReportStageScore"]:
        competitor_score_ids = await info.context.data_loaders.fk_stage_scores_for_competitor.load(self.id)
        return cast(
            list["ParsedMatchReportStageScore"],
            await info.context.data_loaders.stage_scores.load_many(competitor_score_ids),
        )


@strawberry.type
class ParsedMatchReportStage:
    id: UUID
    match_id: strawberry.Private[UUID]
    name: str
    min_rounds: int
    max_points: int
    classifier: bool
    classifier_number: str
    stage_number: int

    @strawberry.field
    async def match(self, info: Info[HitFactorRequestContext, Any]) -> ParsedMatchReport:
        return cast(ParsedMatchReport, await info.context.data_loaders.match_reports.load(self.match_id))

    @strawberry.field
    async def stage_scores(self, info: Info[HitFactorRequestContext, Any]) -> list["ParsedMatchReportStageScore"]:
        stage_score_ids = await info.context.data_loaders.fk_stage_scores_for_stage.load(self.id)
        return cast(
            list["ParsedMatchReportStageScore"], await info.context.data_loaders.stage_scores.load_many(stage_score_ids)
        )


@strawberry.type
class ParsedMatchReportStageScore:
    id: UUID
    match_id: strawberry.Private[UUID]
    competitor_id: strawberry.Private[UUID]
    stage_id: strawberry.Private[UUID]
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
    async def match(self, info: Info[HitFactorRequestContext, Any]) -> ParsedMatchReport:
        return cast(ParsedMatchReport, await info.context.data_loaders.match_reports.load(self.match_id))

    @strawberry.field
    async def competitor(self, info: Info[HitFactorRequestContext, Any]) -> ParsedMatchReportCompetitor:
        return cast(ParsedMatchReportCompetitor, await info.context.data_loaders.competitors.load(self.competitor_id))

    @strawberry.field
    async def stage(self, info: Info[HitFactorRequestContext, Any]) -> ParsedMatchReportStage:
        return cast(ParsedMatchReportStage, await info.context.data_loaders.stages.load(self.stage_id))
