from typing import cast
from uuid import UUID

from hitfactorpy_sqlalchemy.orm import models
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


def select_match_report_summaries():
    return (
        select(models.MatchReport)
        .options(selectinload(models.MatchReport.competitors).load_only("id", "member_number"))
        .options(selectinload(models.MatchReport.stages).load_only("id", "name"))
        .options(selectinload(models.MatchReport.stage_scores).load_only("id"))
    )


async def get_match_report_summaries(
    db: AsyncSession, id_in: list[UUID | str] | None = None
) -> list[models.MatchReport]:
    stmt = select_match_report_summaries()
    if id_in:
        stmt = stmt.filter(models.MatchReport.id.in_(id_in))  # type: ignore
    result = await db.execute(stmt)
    return cast(list[models.MatchReport], result.scalars().all())


async def get_stage_scores(
    db: AsyncSession, id_in: list[UUID | str] | None = None
) -> list[models.MatchReportStageScore]:
    stmt = select(models.MatchReportStageScore)
    if id_in:
        stmt = stmt.filter(models.MatchReportStageScore.id.in_(id_in))  # type: ignore
    result = await db.execute(stmt)
    return cast(list[models.MatchReportStageScore], result.scalars().all())


async def get_competitors(
    db: AsyncSession, id_in: list[UUID | str] | None = None
) -> list[models.MatchReportCompetitor]:
    stmt = select(models.MatchReportCompetitor).options(  # type: ignore
        selectinload(models.MatchReportCompetitor.stage_scores).load_only("id")
    )
    if id_in:
        stmt = stmt.filter(models.MatchReportCompetitor.id.in_(id_in))  # type: ignore
    result = await db.execute(stmt)
    return cast(list[models.MatchReportCompetitor], result.scalars().all())


async def get_stages(db: AsyncSession, id_in: list[UUID | str] | None = None) -> list[models.MatchReportStage]:
    stmt = select(models.MatchReportStage).options(  # type: ignore
        selectinload(models.MatchReportStage.stage_scores).load_only("id"),
    )
    if id_in:
        stmt = stmt.filter(models.MatchReportStage.id.in_(id_in))  # type: ignore
    result = await db.execute(stmt)
    return cast(list[models.MatchReportStage], result.scalars().all())
