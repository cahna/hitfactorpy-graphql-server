from ariadne_graphql_modules import EnumType, gql
from hitfactorpy import enums


class MatchLevel(EnumType):
    __enum__ = enums.MatchLevel
    __schema__ = gql(
        """
        enum MatchLevel {
            I
            II
            III
            IV
        }
        """
    )


class Division(EnumType):
    __enum__ = enums.Division
    __schema__ = gql(
        """
        enum Division {
            PCC
            OPEN
            LIMITED
            CARRY_OPTICS
            LIMITED_10
            PRODUCTION
            SINGLE_STACK
            REVOLVER
            UNKNOWN
        }
        """
    )


class PowerFactor(EnumType):
    __enum__ = enums.PowerFactor
    __schema__ = gql(
        """
        enum PowerFactor {
            MAJOR
            MINOR
            UNKNOWN
        }
        """
    )


class Classification(EnumType):
    __enum__ = enums.Classification
    __schema__ = gql(
        """
        enum Classification {
            GM
            M
            A
            B
            C
            D
            U
            UNKNOWN
        }
        """
    )


class Scoring(EnumType):
    __enum__ = enums.Scoring
    __schema__ = gql(
        """
        enum Scoring {
            COMSTOCK
            VIRGINIA
            FIXED_TIME
            CHRONO
            UNKNOWN
        }
        """
    )

"""
By convention, export all types to be merged into the graphql schema here.
"""
types = [
    MatchLevel,
    Division,
    Classification,
    PowerFactor,
    Scoring,
]
