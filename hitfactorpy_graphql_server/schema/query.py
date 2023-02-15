from typing import Any
from uuid import UUID

import strawberry
from hitfactorpy_sqlalchemy.orm import models
from strawberry.types import Info

from ..utils import get_query_statement
from .context import HitFactorRequestContext
from .types import ParsedMatchReport


@strawberry.type
class Query:
    @strawberry.field
    async def parsed_match_reports(self, info: Info[HitFactorRequestContext, Any]) -> list[ParsedMatchReport]:
        stmt = get_query_statement(models.MatchReport, info)
        result = await info.context.db.execute(stmt)
        return result.scalars().all()

    @strawberry.field
    async def parsed_match_report(self, info: Info[HitFactorRequestContext, Any], id: UUID) -> ParsedMatchReport:
        return await info.context.data_loaders.match_reports.load(id)  # type: ignore
