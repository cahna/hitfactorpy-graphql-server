from datetime import datetime
from typing import Any
from uuid import UUID

import inflection
import strawberry
from hitfactorpy import enums
from hitfactorpy_sqlalchemy.orm import models
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import load_only, selectinload
from strawberry.dataloader import DataLoader
from strawberry.types import Info

from .strawberry_context import HitFactorRequestContext


def get_only_selected_fields(db_baseclass_name, info):
    db_relations_fields = inspect(db_baseclass_name).relationships.keys()
    selected_fields = [
        inflection.underscore(field.name)
        for field in info.selected_fields[0].selections
        if field.name not in db_relations_fields
    ]
    import pdb

    pdb.set_trace()
    return selected_fields


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
    competitors: list["ParsedMatchReportCompetitor"]
    stages: list["ParsedMatchReportStage"]
    stage_scores: list["ParsedMatchReportStageScore"]


@strawberry.type
class ParsedMatchReportCompetitor:
    id: UUID
    match: ParsedMatchReport
    member_number: str
    first_name: str
    last_name: str
    division: Division
    classification: Classification
    power_factor: PowerFactor
    dq: bool
    reentry: bool
    stage_scores: list["ParsedMatchReportStageScore"]


@strawberry.type
class ParsedMatchReportStage:
    id: UUID
    match: ParsedMatchReport
    name: str
    min_rounds: int
    max_points: int
    classifier: bool
    classifier_number: str
    stage_number: int
    stage_scores: list["ParsedMatchReportStageScore"]


@strawberry.type
class ParsedMatchReportStageScore:
    id: UUID
    match: ParsedMatchReport
    competitor: ParsedMatchReportCompetitor
    stage: ParsedMatchReportStage
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


async def get_db_parsed_match_report_async(db: AsyncSession, id: UUID) -> ParsedMatchReport:
    stmt = (
        select(models.MatchReport)
        .options(
            selectinload(models.MatchReport.competitors),
            selectinload(models.MatchReport.stages),
            selectinload(models.MatchReport.stage_scores),
        )
        .filter(models.MatchReport.uuid == id)
    )
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()
    return report  # type: ignore


async def get_db_parsed_match_reports_async(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[ParsedMatchReport]:
    stmt = select(models.MatchReport).offset(skip).limit(limit)
    result = await db.execute(stmt)
    reports = [r[0] for r in result.fetchall()]
    return reports


def get_query_statement(db_baseclass_name, info: Info[HitFactorRequestContext, Any]):
    db_relations_fields = inspect(db_baseclass_name).relationships.keys()
    selected_scalars = []
    selected_relationships = []
    for field in info.selected_fields[0].selections:
        field_name = inflection.underscore(field.name)  # type: ignore
        if field_name in db_relations_fields:
            selected_relationships.append(field_name)
        else:
            selected_scalars.append(field_name)

    stmt = select(db_baseclass_name)
    if selected_scalars:
        stmt = stmt.options(load_only(*selected_scalars))
    if selected_relationships:
        for relation_field in selected_relationships:
            stmt = stmt.options(selectinload(relation_field))

    return stmt


@strawberry.type
class Query:
    @strawberry.field
    async def parsed_match_reports(self, info: Info[HitFactorRequestContext, Any]) -> list[ParsedMatchReport]:
        import pdb

        pdb.set_trace
        stmt = get_query_statement(models.MatchReport, info)
        result = await info.context.db.execute(stmt)
        return result.scalars().all()  # type: ignore

    @strawberry.field
    async def parsed_match_report(self, id: UUID, info: Info[HitFactorRequestContext, Any]) -> ParsedMatchReport:
        return await get_db_parsed_match_report_async(info.context.db, id)


schema = strawberry.Schema(query=Query)
