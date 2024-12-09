from sqlglot import ParseError, UnsupportedError
from sqlglot.errors import SqlglotError


class FunctionalTestFile:
    """A single test case with the required options"""

    def __init__(self, databricks_sql: str, source: str, test_name: str, target: str):
        self.databricks_sql = databricks_sql
        self.source = source
        self.test_name = test_name
        self.target = target


class FunctionalTestFileWithExpectedException(FunctionalTestFile):
    """A single test case with the required options and expected exceptions"""

    def __init__(
        self,
        databricks_sql: str,
        source: str,
        test_name: str,
        expected_exception: SqlglotError,
        target: str,
    ):
        self.expected_exception = expected_exception
        super().__init__(databricks_sql, source, test_name, target)


# This dict has the details about which tests have expected exceptions (Either UnsupportedError or ParseError)

expected_exceptions: dict[str, type[SqlglotError]] = {
    'test_regexp_replace_2': ParseError,
    'test_monthname_8': ParseError,
    'test_monthname_9': ParseError,
    'test_regexp_substr_2': ParseError,
    'test_try_cast_3': ParseError,
    'test_array_slice_3': UnsupportedError,
    'test_right_2': ParseError,
    'test_arrayagg_8': ParseError,
    'test_repeat_2': ParseError,
    'test_nvl2_3': ParseError,
    'test_array_contains_2': ParseError,
    'test_iff_2': ParseError,
    'test_nullif_2': ParseError,
    'test_timestampadd_6': ParseError,
    'test_dayname_4': ParseError,
    'test_date_part_2': ParseError,
    'test_approx_percentile_2': ParseError,
    'test_date_trunc_5': ParseError,
    'test_position_2': ParseError,
    'test_split_part_8': ParseError,
    'test_split_part_7': ParseError,
    'test_trunc_2': UnsupportedError,
    'test_to_number_9': UnsupportedError,
    'test_to_number_10': ParseError,
    'test_startswith_2': ParseError,
    'test_regexp_like_2': ParseError,
    'test_left_2': ParseError,
    'test_parse_json_extract_path_text_4': ParseError,
    'test_extract_2': ParseError,
    'test_approx_percentile_5': ParseError,
    'test_approx_percentile_7': ParseError,
}
