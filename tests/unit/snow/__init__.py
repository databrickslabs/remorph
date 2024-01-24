import pytest
from sqlglot import ErrorLevel, UnsupportedError
from sqlglot import parse_one as sqlglot_parse_one
from sqlglot import transpile

from databricks.labs.remorph.snow.databricks import Databricks
from databricks.labs.remorph.snow.snowflake import Snow


def _normalize_string(s: str) -> str:
    # Remove indentations and convert to lowercase
    lines = [line.strip() for line in s.splitlines()]
    return " ".join(lines).lower().strip()


@pytest.fixture(scope="session")
def dialect_context():
    dialect = Databricks

    def get_dialect(input_dialect=None):
        if input_dialect == "databricks":
            return Databricks
        elif input_dialect == "snowflake":
            return Snow
        else:
            return input_dialect

    def parse_one(sql):
        return sqlglot_parse_one(sql, read=dialect)

    def validate_source_transpile(databricks_sql, *, source=None, pretty=False):
        for source_dialect, source_sql in (source or {}).items():
            actual_sql = _normalize_string(
                transpile(
                    source_sql, read=get_dialect(source_dialect), write=Databricks, pretty=pretty, error_level=None
                )[0]
            )

            expected_sql = _normalize_string(databricks_sql)

            error_msg = f"""-> *target_sql* `{expected_sql}` is not matching with\
                                    \n-> *transpiled_sql* `{actual_sql}`\
                                    \n-> for *source_dialect* `{source_dialect}\
                                 """

            assert expected_sql == actual_sql, error_msg

    def validate_target_transpile(input_sql, *, target=None, pretty=False):
        expression = parse_one(input_sql) if input_sql else None
        for target_dialect, target_sql in (target or {}).items():
            if target_sql is UnsupportedError:
                with pytest.raises(UnsupportedError):
                    if expression:
                        expression.sql(target_dialect, unsupported_level=ErrorLevel.RAISE)
            else:
                actual_sql = _normalize_string(
                    transpile(
                        target_sql, read=Snow, write=get_dialect(target_dialect), pretty=pretty, error_level=None
                    )[0]
                )

                expected_sql = _normalize_string(input_sql)

                error_msg = f"""-> *target_sql* `{expected_sql}` is not matching with\
                                    \n-> *transpiled_sql* `{actual_sql}`\
                                    \n-> for *target_dialect* `{target_dialect}\
                                 """

                assert expected_sql == actual_sql, error_msg

    return validate_source_transpile, validate_target_transpile
