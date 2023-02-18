from typing import Any, cast
from uuid import UUID

import strawberry
from hitfactorpy_sqlalchemy.orm import models
from sqlalchemy import select
from sqlalchemy.orm import load_only, selectinload
from sqlalchemy_utils.functions import is_loaded
from strawberry.types import Info

from ..utils import get_query_statement, get_selection_info
from .context import HitFactorRequestContext
from .types import CompetitorSummary, ParsedMatchReport, ParsedMatchReportSummary, StageSummary

# from .relay.types import Connection, Edge, PageInfo
# from .relay.utils import encode_cursor


@strawberry.type
class Query:
    @strawberry.field
    async def parsed_match_report_summary(
        self, info: Info[HitFactorRequestContext, Any], id: strawberry.ID
    ) -> ParsedMatchReportSummary | None:
        return await info.context.data_loaders.match_report_summary.load(id)

    @strawberry.field
    async def parsed_match_report_summaries(
        self, info: Info[HitFactorRequestContext, Any]
    ) -> list[ParsedMatchReportSummary]:
        stmt = (
            select(models.MatchReport)
            .options(selectinload(models.MatchReport.competitors).load_only("id", "member_number"))
            .options(selectinload(models.MatchReport.stages).load_only("id", "name"))
            .options(selectinload(models.MatchReport.stage_scores).load_only("id"))
        )
        result = await info.context.db.execute(stmt)
        match_reports: list[models.MatchReport] = result.scalars().all()
        return [
            ParsedMatchReportSummary(
                id=strawberry.ID(str(mr.id)),
                name=mr.name,
                date=mr.date,
                created=mr.created,
                updated=mr.updated,
                match_level=mr.match_level,
                competitor_count=len(mr.competitors),
                competitor_ids=[CompetitorSummary(id=c.id, member_number=c.member_number) for c in mr.competitors],
                stage_count=len(mr.stages),
                stage_ids=[StageSummary(id=s.id, name=s.name) for s in mr.stages],
                stage_score_count=len(mr.stage_scores),
            )
            for mr in match_reports
        ]

    @strawberry.field
    async def parsed_match_reports(self, info: Info[HitFactorRequestContext, Any]) -> list[ParsedMatchReport]:
        dl = info.context.data_loaders
        stmt = get_query_statement(models.MatchReport, info)
        result = await info.context.db.execute(stmt)
        match_reports: list[models.MatchReport] = result.scalars().all()

        for match_report in match_reports:
            dl.match_reports.prime(cast(UUID, match_report.id), match_report)
            if is_loaded(match_report, "competitors"):
                for competitor in match_report.competitors:
                    dl.competitors.prime(competitor.id, competitor)
            if is_loaded(match_report, "stages"):
                for stage in match_report.stages:
                    dl.stages.prime(stage.id, stage)
            if is_loaded(match_report, "stage_scores"):
                for stage_score in match_report.stage_scores:
                    dl.stage_scores.prime(stage_score.id, stage_score)
        return match_reports

    @strawberry.field
    async def parsed_match_report(self, info: Info[HitFactorRequestContext, Any], id: UUID) -> ParsedMatchReport | None:
        stmt = get_query_statement(models.MatchReport, info).filter(models.MatchReport.id == id).limit(1)
        result = await info.context.db.execute(stmt)
        if match_report := result.scalar_one_or_none():
            info.context.data_loaders.match_reports.prime(id, match_report)
            return match_report  # type: ignore
        return None

    # @strawberry.field
    # async def parsed_match_reports_relay(
    #     self,
    #     info: Info[HitFactorRequestContext, Any],
    #     first: int = 10,
    #     after: str | None = None
    # ) -> Connection[ParsedMatchReport]:
    #     dl = info.context.data_loaders
    #     stmt = get_query_statement(models.MatchReport, info)
    #     result = await info.context.db.execute(stmt)
    #     match_reports = result.scalars().all()

    #     for match_report in match_reports:
    #         dl.match_reports.prime(match_report.id, match_report)
    #         if is_loaded(match_report, 'competitors'):
    #             for competitor in match_report.competitors:
    #                 dl.competitors.prime(competitor.id, competitor)
    #         if is_loaded(match_report, 'stages'):
    #             for stage in match_report.stages:
    #                 dl.stages.prime(stage.id, stage)
    #         if is_loaded(match_report, 'stage_scores'):
    #             for stage_score in match_report.stage_scores:
    #                 dl.stage_scores.prime(stage_score.id, stage_score)

    #     if len(match_reports) < first:
    #         next_cursor = None
    #         has_next_page = False
    #     else:
    #         has_next_page = True
    #         next_cursor = encode_cursor("ParsedMatchReport", id=match_reports[-1].id)

    #     edges = [
    #         Edge(
    #             node=cast(ParsedMatchReport, match_report),
    #             cursor=encode_cursor("ParsedMatchReport", id=match_report.id),
    #         )
    #         for match_report in match_reports
    #     ]
    #     if edges:
    #         # we have atleast one edge. Get the cursor
    #         # of the first edge we have.
    #         start_cursor = edges[0].cursor
    #     else:
    #         # We have no edges to work with.
    #         start_cursor = None

    #     if len(edges) > 1:
    #         # We have atleast 2 edges. Get the cursor
    #         # of the last edge we have.
    #         end_cursor = edges[-1].cursor
    #     else:
    #         # We don't have enough edges to work with.
    #         end_cursor = None

    #     has_previous_page = False  # TODO

    #     return Connection(
    #         edges=edges,
    #         page_info=PageInfo(
    #             has_next_page=has_next_page,
    #             has_previous_page=has_previous_page,
    #             start_cursor=start_cursor,
    #             end_cursor=end_cursor,
    #         ),
    #     )
