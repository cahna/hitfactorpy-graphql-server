from typing import Callable
from uuid import UUID

import strawberry
from hitfactorpy_sqlalchemy.orm import models
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, selectinload
from sqlalchemy.sql.selectable import Select
from sqlalchemy_utils.functions import is_loaded


def select_match_report_summaries(extend_select: Callable[[Select], Select] | None = None):
    stmt = (
        select(models.MatchReport)
        .options(selectinload(models.MatchReport.competitors).load_only("id", "member_number"))
        .options(selectinload(models.MatchReport.stages).load_only("id", "name"))
        .options(selectinload(models.MatchReport.stage_scores).load_only("id"))
    )
    if extend_select:
        stmt = extend_select(stmt)
    return stmt


async def get_match_report_summaries(
    db: AsyncSession, id_in: list[UUID | str] | None = None
) -> list[models.MatchReport]:
    _filter = (lambda s: s.filter(models.MatchReport.id.in_(id_in))) if id_in else None
    result = await db.execute(select_match_report_summaries(_filter))
    return result.scalars().all()
