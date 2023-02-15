from typing import Any, NamedTuple

import inflection
from sqlalchemy import select
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import load_only, selectinload
from strawberry.types import Info

from .schema.context import HitFactorRequestContext


class SelectionInfo(NamedTuple):
    selected_columns: list[str]
    selected_relationships: list[str]


def get_selection_info(model_klass, info: Info) -> SelectionInfo:
    db_relations_fields = inspect(model_klass).relationships.keys()
    selected_columns = []
    selected_relationships = []
    for field in info.selected_fields[0].selections:
        field_name = inflection.underscore(field.name)  # type: ignore
        if field_name in db_relations_fields:
            selected_relationships.append(field_name)
        else:
            selected_columns.append(field_name)
    return SelectionInfo(selected_columns, selected_relationships)


def get_query_statement(db_baseclass_name, info: Info[HitFactorRequestContext, Any]):
    selection_info = get_selection_info(db_baseclass_name, info)
    stmt = select(db_baseclass_name)
    if selection_info.selected_columns:
        stmt = stmt.options(load_only(*selection_info.selected_columns))
    if selection_info.selected_relationships:
        for relation_field in selection_info.selected_relationships:
            stmt = stmt.options(selectinload(relation_field))

    return stmt
