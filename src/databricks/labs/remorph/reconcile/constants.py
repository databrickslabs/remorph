from enum import Enum, auto


class AutoName(Enum):
    """
    This class is used to auto generate the enum values based on the name of the enum in lower case

    Reference: https://docs.python.org/3/howto/enum.html#enum-advanced-tutorial
    """

    @staticmethod
    # pylint: disable-next=bad-dunder-name
    def _generate_next_value_(name, start, count, last_values):  # noqa ARG004
        return name.lower()


class SourceType(AutoName):
    SNOWFLAKE = auto()
    NETEZZA = auto()
    ORACLE = auto()
    DATABRICKS = auto()


class Layer(AutoName):
    SOURCE = auto()
    TARGET = auto()


class ThresholdMode(AutoName):
    PERCENTAGE = "percentage"
    ABSOLUTE = "absolute"
    NUMBER_ABSOLUTE = "number_absolute"
    NUMBER_PERCENTAGE = "number_percentage"
    DATETIME = "datetime"
