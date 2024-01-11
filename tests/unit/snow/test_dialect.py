import unittest

from sqlglot import ErrorLevel, UnsupportedError, parse_one, transpile

from databricks.labs.remorph.snow.databricks import Databricks
from databricks.labs.remorph.snow.snowflake import Snow


def _normalize_string(s: str) -> str:
    # Remove indentations and convert to lowercase
    lines = [line.strip() for line in s.splitlines()]
    return " ".join(lines).lower().strip()


class Validator(unittest.TestCase):
    dialect = None

    def get_dialect(self, input_dialect):
        if input_dialect == "databricks":
            return Databricks
        elif input_dialect == "snowflake":
            return Snow
        else:
            return input_dialect

    def parse_one(self, sql):
        return parse_one(sql, read=self.get_dialect(self.dialect))

    def validate_identity(self, sql, *, write_sql=None, pretty=False):
        expression = self.parse_one(sql)
        self.assertEqual(write_sql or sql, expression.sql(dialect=self.get_dialect(self.dialect), pretty=pretty))
        return expression

    def validate_all_transpiled(self, sql, *, read=None, write=None, pretty=False):
        """
        Validate that:
        1. Everything in `read` transpiles to `sql`
        2. `sql` transpiles to everything in `write`

        Args:
            sql (str): Main SQL expression
            read (dict): Mapping of dialect -> SQL
            write (dict): Mapping of dialect -> SQL
            pretty (bool): prettify both read and write
        """
        expression = self.parse_one(sql) if sql else None

        for read_dialect, read_sql in (read or {}).items():
            with self.subTest(f"{read_dialect} -> {sql}"):
                transpiled_sql = transpile(
                    read_sql, read=self.get_dialect(self.dialect), write=Databricks, pretty=pretty, error_level=None
                )[0]
                self.assertEqual(
                    _normalize_string(transpiled_sql),
                    _normalize_string(sql),
                    msg=f"-> *sql* `{sql}`,\n-> *read_dialect* `{read_dialect},"
                    f"\n-> *transpiled_sql* `{transpiled_sql}`\n",
                )

        for write_dialect, write_sql in (write or {}).items():
            with self.subTest(f"{sql} -> {write_dialect}"):
                if write_sql is UnsupportedError:
                    with self.assertRaises(UnsupportedError):
                        if expression:
                            expression.sql(write_dialect, unsupported_level=ErrorLevel.RAISE)
                else:
                    transpiled_sql = transpile(
                        write_sql, read=Snow, write=self.get_dialect(write_dialect), pretty=pretty, error_level=None
                    )[0]
                    self.assertEqual(
                        _normalize_string(transpiled_sql),
                        _normalize_string(sql),
                        msg=f"-> *sql* `{sql}`,\n-> *write_dialect* `{write_dialect},"
                        f"\n-> *transpiled_sql* `{transpiled_sql}`\n",
                    )

    def validate_all(self, sql, *, read=None, write=None, pretty=False, identify=False):
        """
        Validate that:
        1. Everything in `read` transpiles to `sql`
        2. `sql` transpiles to everything in `write`

        Args:
            sql (str): Main SQL expression
            read (dict): Mapping of dialect -> SQL
            write (dict): Mapping of dialect -> SQL
            pretty (bool): prettify both read and write
            identify (bool): quote identifiers in both read and write
        """
        expression = self.parse_one(sql)

        for read_dialect, read_sql in (read or {}).items():
            with self.subTest(f"{read_dialect} -> {sql}"):
                parsed_sql = parse_one(sql=read_sql, read=read_dialect).sql(
                    self.get_dialect(self.dialect),
                    unsupported_level=ErrorLevel.IGNORE,
                    pretty=pretty,
                    identify=identify,
                )
                self.assertEqual(
                    _normalize_string(parsed_sql),
                    _normalize_string(sql),
                    msg=f"-> *sql* `{sql}`,\n-> *read_dialect* `{read_dialect},\n-> *parsed_sql* `{parsed_sql}`\n",
                )

        for write_dialect, write_sql in (write or {}).items():
            with self.subTest(f"{sql} -> {write_dialect}"):
                if write_sql is UnsupportedError:
                    with self.assertRaises(UnsupportedError):
                        expression.sql(write_dialect, unsupported_level=ErrorLevel.RAISE)
                else:
                    expr_sql = expression.sql(
                        self.get_dialect(write_dialect),
                        unsupported_level=ErrorLevel.IGNORE,
                        pretty=pretty,
                        identify=identify,
                    )
                    self.assertEqual(
                        _normalize_string(expr_sql),
                        _normalize_string(write_sql),
                        msg=f"-> *write_sql* `{write_sql}`,\n-> *write_dialect* `{write_dialect},"
                        f"\n-> *expr_sql* `{expr_sql}`\n",
                    )
