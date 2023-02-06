import datetime
import uuid
from ariadne_graphql_modules import ScalarType


class UUID(ScalarType):
    __schema__ = '''
    """
    String UUIDv4
    """
    scalar UUID
    '''

    @staticmethod
    def serialize(value):
        return str(value)

    @staticmethod
    def parse_value(value):
        return uuid.UUID(str(value))


class DateTimeISO8601(ScalarType):
    __schema__ = '''
    """
    DateTime in ISO8601 format (string)
    """
    scalar DateTimeISO8601
    '''

    @staticmethod
    def serialize(value):
        return value.replace(tzinfo=datetime.timezone.utc).isoformat()

    @staticmethod
    def parse_value(value):
        return datetime.datetime.fromisoformat(value)


class DecimalPrecision8Scale2(ScalarType):
    __schema__ = '''
    """
    Decimal with precision=8 and scale=2 (string)
    """
    scalar DecimalPrecision8Scale2
    '''

    @staticmethod
    def serialize(value):
        return str(value)

    @staticmethod
    def parse_value(value):
        return datetime.datetime.fromisoformat(value)


"""
By convention, export all types to be merged into the graphql schema here.
"""
types = [UUID, DateTimeISO8601, DecimalPrecision8Scale2]
