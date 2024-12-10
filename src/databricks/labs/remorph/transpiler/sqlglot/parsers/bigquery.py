import logging
from sqlglot import exp
from sqlglot.helper import seq_get
from sqlglot.dialects.bigquery import BigQuery as bigquery

from databricks.labs.remorph.transpiler.sqlglot import local_expression

logger = logging.getLogger(__name__)

bigquery_to_databricks = {
    "%A": "EEEE",  # Full weekday name
    "%a": "EEE",  # Abbreviated weekday name
    "%B": "MMMM",  # Full month name
    "%b": "MMM",  # Abbreviated month name
    "%C": "yy",  # Century
    "%c": "EEE MMM dd HH:mm:ss yyyy",  # Date and time representation
    "%D": "MM/dd/yy",  # Date in mm/dd/yy
    "%d": "dd",  # Day of the month (2 digits)
    "%e": "d",  # Day of month (single digit without leading zero)
    "%F": "yyyy-MM-dd",  # ISO 8601 date
    "%H": "HH",  # 24-hour clock hour
    "%h": "MMM",  # Abbreviated month name (duplicate of %b in BigQuery)
    "%I": "hh",  # 12-hour clock hour
    "%j": "DDD",  # Day of year
    "%k": "H",  # 24-hour clock without leading zero
    "%l": "h",  # 12-hour clock without leading zero
    "%M": "mm",  # Minute
    "%m": "MM",  # Month (2 digits)
    "%P": "a",  # am/pm in lowercase
    "%p": "a",  # AM/PM in uppercase
    "%Q": "q",  # Quarter
    "%R": "HH:mm",  # Time in HH:mm
    "%S": "ss",  # Second
    "%s": "epoch",  # Seconds since epoch (special handling required)
    "%T": "HH:mm:ss",  # Time in HH:mm:ss
    "%U": "ww",  # Week number of year (Sunday start)
    "%u": "e",  # ISO weekday (Monday start)
    "%V": "ww",  # ISO week number of year
    "%W": "ww",  # Week number (Monday start)
    "%w": "e",  # Weekday (Sunday start)
    "%X": "HH:mm:ss",  # Time representation
    "%x": "MM/dd/yy",  # Date representation
    "%Y": "yyyy",  # Year with century
    "%y": "yy",  # Year without century
    "%Z": "z",  # Time zone name
    "%z": "xxx",  # Time zone offset
    "%%": "%",  # Literal percent
    "%Ez": "xxx",  # RFC 3339 numeric time zone
    "%E*S": "ss.SSSSSS",  # Full fractional seconds
    "%E4Y": "yyyy",  # Four-character years
}


def _parse_format_date(args: list):
    format_element = str(args[0].this)
    if format_element == "%s":
        return exp.StrToUnix(this=seq_get(args, 1))
    if format_element == "%V":
        return exp.Extract(this=exp.Var(this="W"), expression=seq_get(args, 1))
    if format_element == "%u":
        return exp.Extract(this=exp.Var(this="DAYOFWEEK_ISO"), expression=seq_get(args, 1))
    if format_element == "%w":
        return exp.Sub(
            this=exp.Extract(this=exp.Var(this="DAYOFWEEK"), expression=seq_get(args, 1)),
            expression=exp.Literal(this='1', is_string=False),
        )
    if format_element == "%C":
        return exp.Round(
            this=exp.Div(
                this=exp.Extract(this=exp.Var(this="YEAR"), expression=seq_get(args, 1)),
                expression=exp.Literal(this='100', is_string=False),
            )
        )
    databricks_datetime_pattern = (
        bigquery_to_databricks.get(format_element) if format_element in bigquery_to_databricks else format_element
    )
    return local_expression.DateFormat(
        this=seq_get(args, 1), expression=exp.Literal(this=databricks_datetime_pattern, is_string=True)
    )


class BigQuery(bigquery):
    class Parser(bigquery.Parser):
        VALUES_FOLLOWED_BY_PAREN = False

        FUNCTIONS = {
            **bigquery.Parser.FUNCTIONS,
            "FORMAT_DATE": _parse_format_date,
        }

    class Tokenizer(bigquery.Tokenizer):
        KEYWORDS = {
            **bigquery.Tokenizer.KEYWORDS,
        }
