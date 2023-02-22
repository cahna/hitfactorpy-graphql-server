from typing import Any, NamedTuple

import inflection
from sqlalchemy import select
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import load_only, selectinload
from strawberry.types import Info

from .schema.context import HitFactorRequestContext


class SelectionInfo(NamedTuple):
    columns: list[str]
    relationships: list[str]
    unknown: list[str]


def get_selection_info(model_klass, info: Info) -> SelectionInfo:
    mk = inspect(model_klass)
    db_relations_fields = mk.relationships.keys()
    db_columns_fields = mk.columns.keys()
    selected_columns = []
    selected_relationships = []
    selected_unknown = []
    for field in info.selected_fields[0].selections:
        field_name = inflection.underscore(field.name)  # type: ignore
        if field_name in db_relations_fields:
            selected_relationships.append(field_name)
        elif field_name in db_columns_fields:
            selected_columns.append(field_name)
        else:
            selected_unknown.append(field_name)

    return SelectionInfo(selected_columns, selected_relationships, selected_unknown)


def get_query_statement(db_baseclass_name, info: Info[HitFactorRequestContext, Any]):
    selection_info = get_selection_info(db_baseclass_name, info)
    stmt = select(db_baseclass_name)
    if selection_info.columns:
        stmt = stmt.options(load_only(*selection_info.columns))  # type: ignore
    if selection_info.relationships:
        for relation_field in selection_info.relationships:
            stmt = stmt.options(selectinload(relation_field))  # type: ignore

    return stmt
