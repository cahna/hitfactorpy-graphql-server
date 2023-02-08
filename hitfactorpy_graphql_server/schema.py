from datetime import datetime
from uuid import UUID

import strawberry
from hitfactorpy import enums
from hitfactorpy_sqlalchemy.orm import models
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from strawberry.types import Info

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
        .options(selectinload(models.MatchReport.competitors))
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


@strawberry.type
class Query:
    @strawberry.field
    async def parsed_match_reports(self, info: Info) -> list[ParsedMatchReport]:
        return await get_db_parsed_match_reports_async(info.context.db)

    @strawberry.field
    async def parsed_match_report(self, id: UUID, info: Info) -> ParsedMatchReport:
        return await get_db_parsed_match_report_async(info.context.db, id)


schema = strawberry.Schema(query=Query)
