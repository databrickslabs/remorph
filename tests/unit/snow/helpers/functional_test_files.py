class FunctionalTestFile:
    """A single test case with the required options"""

    def __init__(self, databricks_sql: str, source: str, test_name: str):
        self.databricks_sql = databricks_sql
        self.source = source
        self.test_name = test_name
