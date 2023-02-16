from datetime import datetime
from typing import Any, cast
from uuid import UUID

import strawberry
from hitfactorpy import enums
from hitfactorpy_sqlalchemy.orm import models
from sqlalchemy import select
from strawberry.types import Info

from .context import HitFactorRequestContext

Division = strawberry.enum(enums.Division)  # type: ignore
Classification = strawberry.enum(enums.Classification)  # type: ignore
MatchLevel = strawberry.enum(enums.MatchLevel)  # type: ignore
PowerFactor = strawberry.enum(enums.PowerFactor)  # type: ignore


@strawberry.type
class ParsedMatchReport:
    id: UUID
    name: str
    date: datetime
    match_level: MatchLevel

    @strawberry.field
    async def competitors(self, info: Info[HitFactorRequestContext, Any]) -> list["ParsedMatchReportCompetitor"]:
        stmt = (
            select(models.MatchReportCompetitor.id)
            .select_from(models.MatchReportCompetitor)
            .filter(models.MatchReportCompetitor.match_id == self.id)
        )
        result = await info.context.db.execute(stmt)
        competitor_ids: list[UUID] = result.scalars().all()
        return cast(
            list["ParsedMatchReportCompetitor"], await info.context.data_loaders.competitors.load_many(competitor_ids)
        )

    @strawberry.field
    async def stages(self, info: Info[HitFactorRequestContext, Any]) -> list["ParsedMatchReportStage"]:
        stmt = (
            select(models.MatchReportStage.id)
            .select_from(models.MatchReportStage)
            .filter(models.MatchReportStage.match_id == self.id)
        )
        result = await info.context.db.execute(stmt)
        stage_ids: list[UUID] = result.scalars().all()
        return cast(list["ParsedMatchReportStage"], await info.context.data_loaders.stages.load_many(stage_ids))

    @strawberry.field
    async def stage_scores(self, info: Info[HitFactorRequestContext, Any]) -> list["ParsedMatchReportStageScore"]:
        stmt = (
            select(models.MatchReportStageScore.id)
            .select_from(models.MatchReportStageScore)
            .filter(models.MatchReportStageScore.match_id == self.id)
        )
        result = await info.context.db.execute(stmt)
        stage_score_ids: list[UUID] = result.scalars().all()
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
        stmt = (
            select(models.MatchReportStageScore.id)
            .select_from(models.MatchReportStageScore)
            .filter(models.MatchReportStageScore.competitor_id == self.id)
        )
        result = await info.context.db.execute(stmt)
        stage_score_ids: list[UUID] = result.scalars().all()
        return cast(
            list["ParsedMatchReportStageScore"], await info.context.data_loaders.stage_scores.load_many(stage_score_ids)
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
        stmt = (
            select(models.MatchReportStageScore.id)
            .select_from(models.MatchReportStageScore)
            .filter(models.MatchReportStageScore.stage_id == self.id)
        )
        result = await info.context.db.execute(stmt)
        stage_score_ids: list[UUID] = result.scalars().all()
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
