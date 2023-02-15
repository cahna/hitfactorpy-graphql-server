from hitfactorpy_sqlalchemy.orm import models
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect

from sqlalchemy.orm import load_only
from strawberry.dataloader import DataLoader

_MATCH_REPORT = inspect(models.MatchReport)
_MATCH_REPORT_RELATIONS_FIELDS = _MATCH_REPORT.relationships.keys()
_MATCH_REPORT_COLUMNS_FIELDS = _MATCH_REPORT.columns.keys()


def make_match_report_loader(db: AsyncSession) -> DataLoader:
    async def load_match_reports(keys) -> list[models.MatchReport]:
        stmt = select(models.MatchReport).filter(models.MatchReport.id.in_(keys))
        result = await db.execute(stmt)
        match_reports = result.scalars().all()
        keyed_match_reports = {m.uuid: m for m in match_reports}

        def _load(id):
            if report := keyed_match_reports.get(id, None):
                return report
            return ValueError(f"no match report for id={id}")

        return [_load(k) for k in keys]

    return DataLoader(load_fn=load_match_reports)
