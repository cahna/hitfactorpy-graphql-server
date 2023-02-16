from collections import defaultdict
from dataclasses import dataclass
from typing import Tuple
from uuid import UUID

from hitfactorpy_sqlalchemy.orm import models
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.dataloader import DataLoader
from strawberry.fastapi import BaseContext


def make_model_loader(db, model_klass):
    async def loader_fn(keys):
        stmt = select(model_klass).filter(model_klass.id.in_(keys))
        result = await db.execute(stmt)
        models = result.scalars().all()
        keyed_models = {m.id: m for m in models}
        return [keyed_models.get(k, ValueError(f"no {model_klass.__name__} with id={k}")) for k in keys]

    return loader_fn


def make_fk_stage_scores_for_stage_loader(db):
    async def loader_fn(keys) -> list[list[UUID]]:
        stmt = select(models.MatchReportStageScore.stage_id, models.MatchReportStageScore.id).filter(
            models.MatchReportStageScore.stage_id.in_(keys)
        )
        result = await db.execute(stmt)
        stage_score_ids: list[Tuple[UUID, UUID]] = result.fetchall()
        stage_scores_for_stage = defaultdict(list)
        for (stage_id, stage_score_id) in stage_score_ids:
            stage_scores_for_stage[stage_id].append(stage_score_id)
        return [stage_scores_for_stage[k] for k in keys]

    return loader_fn


def make_fk_stage_scores_for_competitor_loader(db):
    async def loader_fn(keys) -> list[list[UUID]]:
        stmt = select(models.MatchReportStageScore.competitor_id, models.MatchReportStageScore.id).filter(
            models.MatchReportStageScore.competitor_id.in_(keys)
        )
        result = await db.execute(stmt)
        stage_score_ids: list[Tuple[UUID, UUID]] = result.fetchall()
        stage_scores_for_competitor = defaultdict(list)
        for (competitor_id, stage_score_id) in stage_score_ids:
            stage_scores_for_competitor[competitor_id].append(stage_score_id)
        return [stage_scores_for_competitor[k] for k in keys]

    return loader_fn


def make_fk_competitors_for_match_loader(db):
    async def loader_fn(keys) -> list[list[UUID]]:
        stmt = select(models.MatchReportCompetitor.match_id, models.MatchReportCompetitor.id).filter(
            models.MatchReportCompetitor.match_id.in_(keys)
        )
        result = await db.execute(stmt)
        result_tuples: list[Tuple[UUID, UUID]] = result.fetchall()
        competitors_for_match = defaultdict(list)
        for (match_id, competitor_id) in result_tuples:
            competitors_for_match[match_id].append(competitor_id)
        return [competitors_for_match[k] for k in keys]

    return loader_fn


def make_fk_stages_for_match_loader(db):
    async def loader_fn(keys) -> list[list[UUID]]:
        stmt = select(models.MatchReportStage.match_id, models.MatchReportStage.id).filter(
            models.MatchReportStage.match_id.in_(keys)
        )
        result = await db.execute(stmt)
        result_tuples: list[Tuple[UUID, UUID]] = result.fetchall()
        stages_for_match = defaultdict(list)
        for (match_id, stage_id) in result_tuples:
            stages_for_match[match_id].append(stage_id)
        return [stages_for_match[k] for k in keys]

    return loader_fn


def make_fk_stage_scores_for_match_loader(db):
    async def loader_fn(keys) -> list[list[UUID]]:
        stmt = select(models.MatchReportStageScore.match_id, models.MatchReportStageScore.id).filter(
            models.MatchReportStageScore.match_id.in_(keys)
        )
        result = await db.execute(stmt)
        result_tuples: list[Tuple[UUID, UUID]] = result.fetchall()
        stage_scores_for_match = defaultdict(list)
        for (match_id, stage_score_id) in result_tuples:
            stage_scores_for_match[match_id].append(stage_score_id)
        return [stage_scores_for_match[k] for k in keys]

    return loader_fn


@dataclass(frozen=True)
class HitFactorDataLoaders:
    match_reports: DataLoader[UUID, models.MatchReport]
    stages: DataLoader[UUID, models.MatchReportStage]
    competitors: DataLoader[UUID, models.MatchReportCompetitor]
    stage_scores: DataLoader[UUID, models.MatchReportStageScore]
    fk_stage_scores_for_stage: DataLoader[UUID, list[UUID]]
    fk_stage_scores_for_competitor: DataLoader[UUID, list[UUID]]
    fk_competitors_for_match: DataLoader[UUID, list[UUID]]
    fk_stages_for_match: DataLoader[UUID, list[UUID]]
    fk_stage_scores_for_match: DataLoader[UUID, list[UUID]]

    @staticmethod
    def build(db: AsyncSession) -> "HitFactorDataLoaders":
        return HitFactorDataLoaders(
            match_reports=DataLoader(load_fn=make_model_loader(db, models.MatchReport)),
            stages=DataLoader(load_fn=make_model_loader(db, models.MatchReportStage)),
            competitors=DataLoader(load_fn=make_model_loader(db, models.MatchReportCompetitor)),
            stage_scores=DataLoader(load_fn=make_model_loader(db, models.MatchReportStageScore)),
            fk_stage_scores_for_stage=DataLoader(load_fn=make_fk_stage_scores_for_stage_loader(db)),
            fk_stage_scores_for_competitor=DataLoader(load_fn=make_fk_stage_scores_for_competitor_loader(db)),
            fk_competitors_for_match=DataLoader(load_fn=make_fk_competitors_for_match_loader(db)),
            fk_stages_for_match=DataLoader(load_fn=make_fk_stages_for_match_loader(db)),
            fk_stage_scores_for_match=DataLoader(load_fn=make_fk_stage_scores_for_match_loader(db)),
        )


class HitFactorRequestContext(BaseContext):
    def __init__(self, db: AsyncSession, data_loaders: HitFactorDataLoaders):
        self.db = db
        self.data_loaders = data_loaders
