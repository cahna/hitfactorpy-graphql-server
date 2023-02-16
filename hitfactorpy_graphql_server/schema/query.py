from typing import Any, cast
from uuid import UUID

import strawberry
from hitfactorpy_sqlalchemy.orm import models
from strawberry.types import Info
from sqlalchemy_utils.functions import is_loaded

from ..utils import get_query_statement
from .context import HitFactorRequestContext
from .types import ParsedMatchReport


@strawberry.type
class Query:
    @strawberry.field
    async def parsed_match_reports(self, info: Info[HitFactorRequestContext, Any]) -> list[ParsedMatchReport]:
        dl = info.context.data_loaders
        stmt = get_query_statement(models.MatchReport, info)
        result = await info.context.db.execute(stmt)
        match_reports = result.scalars().all()

        for match_report in match_reports:
            dl.match_reports.prime(match_report.id, match_report)
            if is_loaded(match_report, 'competitors'):
                for competitor in match_report.competitors:
                    dl.competitors.prime(competitor.id, competitor)
            if is_loaded(match_report, 'stages'):
                for stage in match_report.stages:
                    dl.stages.prime(stage.id, stage)
            if is_loaded(match_report, 'stage_scores'):
                for stage_score in match_report.stage_scores:
                    dl.stage_scores.prime(stage_score.id, stage_score)

        return match_reports

    @strawberry.field
    async def parsed_match_report(self, info: Info[HitFactorRequestContext, Any], id: UUID) -> ParsedMatchReport | None:
        stmt = get_query_statement(models.MatchReport, info).filter(models.MatchReport.id == id).limit(1)
        result = await info.context.db.execute(stmt)
        if match_report := result.scalar_one_or_none():
            info.context.data_loaders.match_reports.prime(id, match_report)
            return cast(ParsedMatchReport, match_report)
        return None
