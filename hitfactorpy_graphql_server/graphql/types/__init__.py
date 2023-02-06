from .parsed_match_report import ParsedMatchReport
from .parsed_match_report_competitor import ParsedMatchReportCompetitor
from .parsed_match_report_stage import ParsedMatchReportStage
from .parsed_match_report_stage_score import ParsedMatchReportStageScore

"""
By convention, export all types to be merged into the graphql schema here.
"""
types = [
    ParsedMatchReport,
    ParsedMatchReportCompetitor,
    ParsedMatchReportStage,
    ParsedMatchReportStageScore,
]
