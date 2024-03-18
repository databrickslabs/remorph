from enum import Enum, auto


class AutoName(Enum):
    """
    This class is used to auto generate the enum values based on the name of the enum in lower case

    Reference: https://docs.python.org/3/howto/enum.html#enum-advanced-tutorial
    """

    @staticmethod
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


class SourceDriver(Enum):
    ORACLE = "oracle.jdbc.driver.OracleDriver"
    SNOWFLAKE = "net.snowflake.client.jdbc.SnowflakeDriver"


class ColumnTransformationType(Enum):
    ORACLE_DATE = "coalesce(trim(to_char({},'YYYY-MM-DD')),'')"
    ORACLE_DEFAULT = "coalesce(trim({}),'')"
    DATABRICKS_DEFAULT = "coalesce(trim({}),'')"
    SNOWFLAKE_DEFAULT = "coalesce(trim({}),'')"


class HashAlgorithm(Enum):
    DATABRICKS_SHA_256 = "sha2({},256)"
    DATABRICKS_SHA_512 = "sha2({},512)"
    DATABRICKS_MD5 = "MD5({})"
    SNOWFLAKE_SHA_256 = "sha2({},256)"
    SNOWFLAKE_SHA_512 = "sha2({},512)"
    SNOWFLAKE_MD5 = "HASH({},'MD5')"
    ORACLE_SHA_256 = "lower(RAWTOHEX(STANDARD_HASH({}, 'SHA256')))"
    ORACLE_SHA_512 = "lower(RAWTOHEX(STANDARD_HASH({}, 'SHA512')))"
    ORACLE_MD5 = "lower(RAWTOHEX(STANDARD_HASH({}, 'MD5')))"


class ReportType(AutoName):
    DATA = "data"
    SCHEMA = "schema"
    HASH = "hash"
    ALL = "all"


class ThresholdMode(AutoName):
    PERCENTILE = "percentile"
    ABSOLUTE = "absolute"


class ThresholdMatchType(AutoName):
    INTEGER = "integer"
    TIMESTAMP = "timestamp"


class Constants:
    hash_column_name = "hash_value__recon"
    hash_algorithm_mapping = {  # noqa RUF012
        SourceType.SNOWFLAKE.value: {
            "source": HashAlgorithm.SNOWFLAKE_SHA_256.value,
            "target": HashAlgorithm.DATABRICKS_SHA_256.value,
        },
        SourceType.ORACLE.value: {
            "source": HashAlgorithm.ORACLE_SHA_256.value,
            "target": HashAlgorithm.DATABRICKS_SHA_256.value,
        },
        SourceType.DATABRICKS.value: {
            "source": HashAlgorithm.DATABRICKS_SHA_256.value,
            "target": HashAlgorithm.DATABRICKS_SHA_256.value,
        },
    }
