from sqlglot import ParseError
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
# Removed the dictionary as we are now categorizing as failures aka Hallucinations
expected_exceptions: dict[str, type[SqlglotError]] = {}
