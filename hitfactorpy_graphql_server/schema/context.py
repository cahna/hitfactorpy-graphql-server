from dataclasses import dataclass
from uuid import UUID

from hitfactorpy_sqlalchemy.orm import models
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.dataloader import DataLoader
from strawberry.fastapi import BaseContext


def make_loader(db, model_klass):
    async def loader_fn(keys):
        stmt = select(model_klass).filter(model_klass.id.in_(keys))
        result = await db.execute(stmt)
        models = result.scalars().all()
        keyed_models = {m.id: m for m in models}
        return [keyed_models.get(k, ValueError(f"no {model_klass.__name__} with id={k}")) for k in keys]

    return loader_fn


@dataclass(frozen=True)
class HitFactorDataLoaders:
    match_reports: DataLoader[UUID, models.MatchReport]
    stages: DataLoader[UUID, models.MatchReportStage]
    competitors: DataLoader[UUID, models.MatchReportCompetitor]
    stage_scores: DataLoader[UUID, models.MatchReportStageScore]

    @staticmethod
    def build(db: AsyncSession) -> "HitFactorDataLoaders":
        return HitFactorDataLoaders(
            match_reports=DataLoader(load_fn=make_loader(db, models.MatchReport)),
            stages=DataLoader(load_fn=make_loader(db, models.MatchReportStage)),
            competitors=DataLoader(load_fn=make_loader(db, models.MatchReportCompetitor)),
            stage_scores=DataLoader(load_fn=make_loader(db, models.MatchReportStageScore)),
        )


class HitFactorRequestContext(BaseContext):
    def __init__(self, db: AsyncSession, data_loaders: HitFactorDataLoaders):
        self.db = db
        self.data_loaders = data_loaders
