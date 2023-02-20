from dataclasses import dataclass
from typing import TYPE_CHECKING, Union

import strawberry
from sqlalchemy.ext.asyncio import AsyncSession

# from sqlalchemy.orm import load_only, selectinload
from strawberry.dataloader import DataLoader
from strawberry.fastapi import BaseContext

from ..actions import get_competitors, get_match_report_summaries, get_stage_scores, get_stages

if TYPE_CHECKING:
    from .types import (
        ParsedMatchReportCompetitor,
        ParsedMatchReportStage,
        ParsedMatchReportStageScore,
        ParsedMatchReportSummary,
    )


def _make_match_report_summary_loader(db: AsyncSession):
    from .types import ParsedMatchReportSummary

    async def loader_fn(keys: list[strawberry.ID]) -> list[Union[ParsedMatchReportSummary, ValueError]]:
        match_report_summary_models = await get_match_report_summaries(db, id_in=list(map(str, keys)))
        match_report_summaries = list(map(ParsedMatchReportSummary.from_orm, match_report_summary_models))
        lookup = {m.id: m for m in match_report_summaries}
        return [lookup.get(k, ValueError(f"no MatchReport with id={k}")) for k in keys]

    return loader_fn


def _make_stage_score_loader(db: AsyncSession):
    from .types import ParsedMatchReportStageScore

    async def loader_fn(keys: list[strawberry.ID]) -> list[Union[ParsedMatchReportStageScore, ValueError]]:
        stage_score_models = await get_stage_scores(db, id_in=list(map(str, keys)))
        stage_scores = list(map(ParsedMatchReportStageScore.from_orm, stage_score_models))
        lookup = {m.id: m for m in stage_scores}
        return [lookup.get(k, ValueError(f"no ParsedMatchReportStageScore with id={k}")) for k in keys]

    return loader_fn


def _make_competitor_loader(db: AsyncSession):
    from .types import ParsedMatchReportCompetitor

    async def loader_fn(keys: list[strawberry.ID]) -> list[Union[ParsedMatchReportCompetitor, ValueError]]:
        competitor_models = await get_competitors(db, id_in=list(map(str, keys)))
        competitors = list(map(ParsedMatchReportCompetitor.from_orm, competitor_models))
        lookup = {m.id: m for m in competitors}
        return [lookup.get(k, ValueError(f"no ParsedMatchReportCompetitor with id={k}")) for k in keys]

    return loader_fn


def _make_stage_loader(db: AsyncSession):
    from .types import ParsedMatchReportStage

    async def loader_fn(keys: list[strawberry.ID]) -> list[Union[ParsedMatchReportStage, ValueError]]:
        stage_models = await get_stages(db, id_in=list(map(str, keys)))
        stages = list(map(ParsedMatchReportStage.from_orm, stage_models))
        lookup = {m.id: m for m in stages}
        return [lookup.get(k, ValueError(f"no ParsedMatchReportStage with id={k}")) for k in keys]

    return loader_fn


@dataclass(frozen=True)
class HitFactorDataLoaders:
    match_report_summary: DataLoader[strawberry.ID, "ParsedMatchReportSummary"]
    stage_score: DataLoader[strawberry.ID, "ParsedMatchReportStageScore"]
    competitor: DataLoader[strawberry.ID, "ParsedMatchReportCompetitor"]
    stage: DataLoader[strawberry.ID, "ParsedMatchReportStage"]

    @staticmethod
    def build(db: AsyncSession) -> "HitFactorDataLoaders":
        match_report_summary_loader = DataLoader(load_fn=_make_match_report_summary_loader(db))
        stage_score_loader = DataLoader(load_fn=_make_stage_score_loader(db))
        competitor_loader = DataLoader(load_fn=_make_competitor_loader(db))
        stage_loader = DataLoader(load_fn=_make_stage_loader(db))
        return HitFactorDataLoaders(
            match_report_summary=match_report_summary_loader,
            stage_score=stage_score_loader,
            competitor=competitor_loader,
            stage=stage_loader,
        )


class HitFactorRequestContext(BaseContext):
    def __init__(self, db: AsyncSession, data_loaders: HitFactorDataLoaders):
        self.db = db
        self.data_loaders = data_loaders
