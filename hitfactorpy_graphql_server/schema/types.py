from datetime import datetime
from uuid import UUID

import strawberry
from hitfactorpy import enums

Division = strawberry.enum(enums.Division)  # type: ignore
Classification = strawberry.enum(enums.Classification)  # type: ignore
MatchLevel = strawberry.enum(enums.MatchLevel)  # type: ignore
PowerFactor = strawberry.enum(enums.PowerFactor)  # type: ignore


@strawberry.type
class ParsedMatchReport:
    id: UUID
    name: str
    date: datetime
    match_level: MatchLevel
    competitors: list["ParsedMatchReportCompetitor"]
    stages: list["ParsedMatchReportStage"]
    stage_scores: list["ParsedMatchReportStageScore"]


@strawberry.type
class ParsedMatchReportCompetitor:
    id: UUID
    match: ParsedMatchReport
    member_number: str
    first_name: str
    last_name: str
    division: Division
    classification: Classification
    power_factor: PowerFactor
    dq: bool
    reentry: bool
    stage_scores: list["ParsedMatchReportStageScore"]


@strawberry.type
class ParsedMatchReportStage:
    id: UUID
    match: ParsedMatchReport
    name: str
    min_rounds: int
    max_points: int
    classifier: bool
    classifier_number: str
    stage_number: int
    stage_scores: list["ParsedMatchReportStageScore"]


@strawberry.type
class ParsedMatchReportStageScore:
    id: UUID
    match: ParsedMatchReport
    competitor: ParsedMatchReportCompetitor
    stage: ParsedMatchReportStage
    dq: bool
    dnf: bool
    a: int
    c: int
    d: int
    m: int
    npm: int
    ns: int
    procedural: int
    late_shot: int
    extra_shot: int
    extra_hit: int
    other_penalty: int
