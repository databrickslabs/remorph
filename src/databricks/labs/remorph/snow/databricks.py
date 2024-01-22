import re
from typing import ClassVar

from databricks.labs.blueprint.entrypoint import get_logger
from sqlglot import expressions as exp
from sqlglot.dialects import hive
from sqlglot.dialects.databricks import Databricks
from sqlglot.dialects.dialect import rename_func
from sqlglot.errors import UnsupportedError
from sqlglot.helper import apply_index_offset, csv

from databricks.labs.remorph.snow import local_expression

logger = get_logger(__file__)

VALID_DATABRICKS_TYPES = {
    "BIGINT",
    "BINARY",
    "BOOLEAN",
    "DATE",
    "DECIMAL",
    "DOUBLE",
    "FLOAT",
    "INT",
    "INTERVAL",
    "VOID",
    "SMALLINT",
    "STRING",
    "TIMESTAMP",
    "TINYINT",
    "ARRAY",
    "MAP",
    "STRUCT",
}


def _parm_sfx(self, expression: local_expression.Parameter) -> str:
    this = self.sql(expression, "this")
    this = f"{{{this}}}" if expression.args.get("wrapped") else f"{this}"
    suffix = self.sql(expression, "suffix")
    PARAMETER_TOKEN = "$"  # noqa: N806
    return f"{PARAMETER_TOKEN}{this}{suffix}"


def _lateral_bracket_sql(self, expression: local_expression.Bracket) -> str:
    """Overwrites `sqlglot/generator.py` `bracket_sql()` function
    to convert <TABLE_ALIAS>`[COL_NAME]` to <TABLE_ALIAS>`.COL_NAME`.
    Example: c[val] ==> c.val
    """
    expressions = apply_index_offset(expression.this, expression.expressions, self.dialect.INDEX_OFFSET)
    expressions = [self.sql(e.alias_or_name.strip("'")) for e in expressions]
    # If expression contains space in between encode it in backticks(``):
    # e.g. ref."ID Number" -> ref.`ID Number`.
    expressions_sql = ", ".join(f"`{e}`" if " " in e else e for e in expressions)
    return f"{self.sql(expression, 'this')}.{expressions_sql}"


def _format_create_sql(self, expression: exp.Create) -> str:
    expression = expression.copy()

    # Remove modifiers in order to simplify the schema.  For example, this removes things like "IF NOT EXISTS"
    # from "CREATE TABLE foo IF NOT EXISTS".
    args_to_delete = ["temporary", "transient", "external", "replace", "exists", "unique", "materialized", "properties"]
    for arg_to_delete in args_to_delete:
        if expression.args.get(arg_to_delete):
            del expression.args[arg_to_delete]

    return hive._create_sql(self, expression)


def _curr_ts():
    return "CURRENT_TIMESTAMP()"


def _curr_time():
    return "date_format(current_timestamp(), 'HH:mm:ss')"


def _lateral_view(self, expression: exp.Lateral) -> str:
    str_lateral_view = "LATERAL VIEW"
    str_outer = "OUTER"
    str_explode = "EXPLODE("
    str_pfx = f"{str_lateral_view} {str_explode}"
    str_alias = ")"

    for expr, _, _ in expression.walk(bfs=True, prune=lambda *_: False):
        match expr:
            case exp.Explode():
                if expr.key.upper() != "EXPLODE":
                    continue
                for node, _, _ in expr.walk(bfs=True, prune=lambda *_: False):
                    if not isinstance(node, exp.Kwarg):
                        continue
                    if not isinstance(node.this, exp.Var):
                        continue

                    node_name = str(node.this).upper()
                    match node_name:
                        case "INPUT":
                            # Added if block to handle Dynamic variables `${}`
                            node_expr = f"{node.expression}".replace("@", "$")
                            if "PARSE_JSON" in node_expr:
                                node_expr = node_expr.replace("PARSE_JSON", "FROM_JSON")
                                msg = (
                                    f"***Warning***: you need to explicitly specify "
                                    f"`SCHEMA` for column(s) in `{node_expr}`"
                                )
                                logger.warning(msg)
                            str_pfx = str_pfx + node_expr
                        case "PATH":
                            str_pfx = str_pfx + f".{node.expression}".replace("'", "").replace('"', "`")
                        case "OUTER":
                            str_pfx = str_pfx.replace(str_lateral_view, f"{str_lateral_view} {str_outer}")
                            # [TODO]: Implement for options: RECURSIVE and MODE
            case exp.TableAlias():
                str_alias = str_alias + f" AS {expr.name}"

    return self.sql(str_pfx + str_alias)


# [TODO] Add more datatype coverage https://docs.databricks.com/sql/language-manual/sql-ref-datatypes.html
def _datatype_map(self, expression) -> str:
    if expression.this in [exp.DataType.Type.VARCHAR, exp.DataType.Type.NVARCHAR, exp.DataType.Type.CHAR]:
        return "STRING"
    if expression.this in [exp.DataType.Type.TIMESTAMP, exp.DataType.Type.TIMESTAMPLTZ]:
        return "TIMESTAMP"
    return self.datatype_sql(expression)


def try_to_date(self, expression: local_expression.TryToDate):
    func = "TRY_TO_TIMESTAMP"
    time_format = self.sql(expression, "format")
    if not time_format:
        time_format = hive.Hive.DATE_FORMAT

    ts_result = self.func(func, expression.this, time_format)
    return exp.Date(this=ts_result)


def try_to_number(self, expression: local_expression.TryToNumber):
    func = "TRY_TO_NUMBER"
    precision = self.sql(expression, "precision")
    scale = self.sql(expression, "scale")

    if not precision:
        precision = 38

    if not scale:
        scale = 0

    func_expr = self.func(func, expression.this)
    if expression.expression:
        func_expr = self.func(func, expression.this, expression.expression)

    return f"CAST({func_expr} AS DECIMAL({precision}, {scale}))"


def _list_agg(self, expr: exp.GroupConcat):
    """
    [TODO]
        Handle:
                1. DISTINCT keyword
                2. WITHIN GROUP (ORDER BY )
                3. OVER ( [ PARTITION BY <expr2> ] )
                4. Collation within Order by
        These are supported in Snowflake: [LISTAGG](https://docs.snowflake.com/en/sql-reference/functions/listagg)
    """
    collect_list_expr = self.func("COLLECT_LIST", expr.this)
    return self.func("ARRAY_JOIN", collect_list_expr, expr.args.get("separator"))


def _to_boolean(self: Databricks.Generator, expression: local_expression.ToBoolean) -> str:
    this = self.sql(expression, "this")
    logger.debug(f"Converting {this} to Boolean")
    raise_error = self.sql(expression, "raise_error")
    raise_error_str = "RAISE_ERROR('Invalid parameter type for TO_BOOLEAN')" if bool(int(raise_error)) else "NULL"
    transformed = f"""
    CASE
       WHEN {this} IS NULL THEN NULL
       WHEN TYPEOF({this}) = 'boolean' THEN BOOLEAN({this})
       WHEN TYPEOF({this}) = 'string' THEN
           CASE
               WHEN LOWER({this}) IN ('true', 't', 'yes', 'y', 'on', '1') THEN TRUE
               WHEN LOWER({this}) IN ('false', 'f', 'no', 'n', 'off', '0') THEN FALSE
               ELSE RAISE_ERROR('Boolean value of x is not recognized by TO_BOOLEAN')
               END
       WHEN ISNOTNULL(TRY_CAST({this} AS DOUBLE)) THEN
           CASE
               WHEN ISNAN(CAST({this} AS DOUBLE)) OR CAST({this} AS DOUBLE) = DOUBLE('infinity') THEN
                    RAISE_ERROR('Invalid parameter type for TO_BOOLEAN')
               ELSE CAST({this} AS DOUBLE) != 0.0
               END
       ELSE {raise_error_str}
       END
    """
    return transformed


def _is_integer(self: Databricks.Generator, expression: local_expression.IsInteger) -> str:
    this = self.sql(expression, "this")
    transformed = f"""
    CASE
       WHEN {this} IS NULL THEN NULL
       WHEN {this} RLIKE '^-?[0-9]+$' AND TRY_CAST({this} AS INT) IS NOT NULL THEN TRUE
       ELSE FALSE
       END
    """
    return transformed


def _parse_json_extract_path_text(self: Databricks.Generator, expression: local_expression.JsonExtractPathText) -> str:
    this = self.sql(expression, "this")
    path_name = expression.args["path_name"]
    if path_name.is_string:
        path = f"{self.dialect.QUOTE_START}$.{expression.text('path_name')}{self.dialect.QUOTE_END}"
    else:
        path = f"CONCAT('$.', {self.sql(expression, 'path_name')})"
    return f"GET_JSON_OBJECT({this}, {path})"


def _array_construct_compact(self: Databricks.Generator, expression: local_expression.ArrayConstructCompact) -> str:
    exclude = "ARRAY(NULL)"
    array_expr = f"ARRAY({self.expressions(expression, flat=True)})"
    return f"ARRAY_EXCEPT({array_expr}, {exclude})"


def _array_slice(self: Databricks.Generator, expression: local_expression.ArraySlice) -> str:
    from_expr = self.sql(expression, "from")
    # In Databricks: array indices start at 1 in function `slice(array, start, length)`
    from_expr = 1 if from_expr == "0" else from_expr

    to_expr = self.sql(expression, "to")
    # Convert string expression to number and check if it is negative number
    if int(to_expr) < 0:
        err_message = "In Databricks: function `slice` length must be greater than or equal to 0"
        raise UnsupportedError(err_message)

    func = "SLICE"
    func_expr = self.func(func, expression.this, exp.Literal.number(from_expr), expression.args["to"])
    return func_expr


def _parse_json(self, expr: exp.ParseJSON):
    """
    Converts `PARSE_JSON` function to `FROM_JSON` function.
    Schema is a mandatory argument for Databricks `FROM_JSON` function
    [FROM_JSON](https://docs.databricks.com/en/sql/language-manual/functions/from_json.html)
    Need to explicitly specify the Schema {<COL_NAME>_SCHEMA} in the current execution environment
    """
    expr_this = self.sql(expr, "this")
    column = expr_this.replace("'", "").upper()
    conv_expr = self.func("FROM_JSON", expr_this, f"{{{column}_SCHEMA}}")
    warning_msg = (
        f"***Warning***: you need to explicitly specify `SCHEMA` for `{column}` column in expression: `{conv_expr}`"
    )
    logger.warning(warning_msg)
    return conv_expr


def _to_number(self, expression: local_expression.TryToNumber):
    func = "TO_NUMBER"
    precision = self.sql(expression, "precision")
    scale = self.sql(expression, "scale")

    if not precision:
        precision = 38

    if not scale:
        scale = 0

    func_expr = self.func(func, expression.this)
    if expression.expression:
        func_expr = self.func(func, expression.this, expression.expression)
    else:
        exception_msg = f"""Error Parsing expression {expression}:
                         * `format`: is required in Databricks [mandatory]
                         * `precision` and `scale`: are considered as (38, 0) if not specified.
                      """
        raise UnsupportedError(exception_msg)

    return f"CAST({func_expr} AS DECIMAL({precision}, {scale}))"


def _uuid(self: Databricks.Generator, expression: local_expression.UUID) -> str:
    namespace = self.sql(expression, "this")
    name = self.sql(expression, "name")

    if namespace and name:
        logger.warning("UUID version 5 is not supported currently. Needs manual intervention.")
        return f"UUID({namespace}, {name})"
    else:
        return "UUID()"


class Databricks(Databricks):
    # Instantiate Databricks Dialect
    databricks = Databricks()

    class Generator(databricks.Generator):
        COLLATE_IS_FUNC = True
        # [TODO]: Variant needs to be transformed better, for now parsing to string was deemed as the choice.
        TYPE_MAPPING: ClassVar[dict] = {
            **Databricks.Generator.TYPE_MAPPING,
            exp.DataType.Type.TINYINT: "TINYINT",
            exp.DataType.Type.SMALLINT: "SMALLINT",
            exp.DataType.Type.INT: "INT",
            exp.DataType.Type.BIGINT: "BIGINT",
            exp.DataType.Type.DATETIME: "TIMESTAMP",
            exp.DataType.Type.VARCHAR: "STRING",
            exp.DataType.Type.VARIANT: "STRING",
            exp.DataType.Type.FLOAT: "DOUBLE",
        }

        TRANSFORMS: ClassVar[dict] = {
            **Databricks.Generator.TRANSFORMS,
            # exp.Select: transforms.preprocess([_unqualify_unnest]),
            exp.Create: _format_create_sql,
            exp.DataType: _datatype_map,
            exp.CurrentTimestamp: _curr_ts(),
            exp.CurrentTime: _curr_time(),
            exp.Lateral: _lateral_view,
            exp.GroupConcat: _list_agg,
            exp.FromBase64: rename_func("UNBASE64"),
            local_expression.Parameter: _parm_sfx,
            local_expression.ToBoolean: _to_boolean,
            local_expression.Bracket: _lateral_bracket_sql,
            local_expression.MakeDate: rename_func("MAKE_DATE"),
            local_expression.TryToDate: try_to_date,
            local_expression.TryToNumber: try_to_number,
            local_expression.IsInteger: _is_integer,
            local_expression.JsonExtractPathText: _parse_json_extract_path_text,
            local_expression.BitOr: rename_func("BIT_OR"),
            local_expression.ArrayConstructCompact: _array_construct_compact,
            local_expression.ArrayIntersection: rename_func("ARRAY_INTERSECT"),
            local_expression.ArraySlice: _array_slice,
            local_expression.ObjectKeys: rename_func("JSON_OBJECT_KEYS"),
            exp.ParseJSON: _parse_json,
            local_expression.TimestampFromParts: rename_func("MAKE_TIMESTAMP"),
            local_expression.ToDouble: rename_func("DOUBLE"),
            exp.Rand: rename_func("RANDOM"),
            local_expression.ToVariant: rename_func("TO_JSON"),
            local_expression.ToObject: rename_func("TO_JSON"),
            exp.ToBase64: rename_func("BASE64"),
            local_expression.ToNumber: _to_number,
            local_expression.UUID: _uuid,
        }

        def join_sql(self, expression: exp.Join) -> str:
            """Overwrites `join_sql()` in `sqlglot/generator.py`
            Added logic to handle Lateral View
            """
            op_list = [
                expression.method,
                "GLOBAL" if expression.args.get("global") else None,
                expression.side,
                expression.kind,
                expression.hint if self.JOIN_HINTS else None,
            ]

            op_sql = " ".join(op for op in op_list if op)
            on_sql = self.sql(expression, "on")
            using = expression.args.get("using")

            if not on_sql and using:
                on_sql = csv(*(self.sql(column) for column in using))

            this_sql = self.sql(expression, "this")

            if on_sql:
                on_sql = self.indent(on_sql, skip_first=True)
                space = self.seg(" " * self.pad) if self.pretty else " "
                if using:
                    on_sql = f"{space}USING ({on_sql})"
                else:
                    on_sql = f"{space}ON {on_sql}"
            # Added the below elif block to handle Lateral View clause
            elif not op_sql and isinstance(expression.this, exp.Lateral):
                return f"\n {this_sql}"
            elif not op_sql:
                return f", {this_sql}"

            op_sql = f"{op_sql} JOIN" if op_sql else "JOIN"
            return f"{self.seg(op_sql)} {this_sql}{on_sql}"

        def arrayagg_sql(self, expression: exp.ArrayAgg) -> str:
            # ARRAY_AGG function is available in Spark built-in functions
            """[TODO]
            Have to handle:
                    1. WITHIN GROUP (ORDER BY )
                    2. OVER ( [ PARTITION BY <expr2> ] )
            These are supported in Snowflake: [array_agg](https://docs.snowflake.com/en/sql-reference/functions/array_agg)
            """
            return self.func(
                "ARRAY_AGG",
                expression.this.this if isinstance(expression.this, exp.Order) else expression.this,
            )

        def split_sql(self, expression: local_expression.Split) -> str:
            """
            :param expression: local_expression.Split expression to be parsed
            :return: Converted expression (SPLIT) compatible with Databricks
            """
            delimiter = " "
            # To handle default delimiter
            if expression.expression:
                delimiter = expression.expression.name

            # Parsing logic to handle String and Table columns
            if expression.name and isinstance(expression.name, str):
                expr_name = f"'{expression.name}'"
            else:
                expr_name = expression.args["this"]
            return f"""SPLIT({expr_name},'[{delimiter}]')"""

        def delete_sql(self, expression: exp.Delete) -> str:
            this = self.sql(expression, "this")
            using = self.sql(expression, "using")
            where = self.sql(expression, "where")
            returning = self.sql(expression, "returning")
            limit = self.sql(expression, "limit")
            tables = self.expressions(expression, key="tables")
            tables = f" {tables}" if tables else ""

            if using:
                using = f" USING {using}" if using else ""
                where = where.replace("WHERE", "ON")
            else:
                this = f"FROM {this}" if this else ""

            if self.RETURNING_END:
                expression_sql = f" {this}{using}{where}{returning}{limit}"
            else:
                expression_sql = f"{returning}{this}{where}{limit}"

            if using:
                return self.prepend_ctes(expression, f"MERGE{tables}{expression_sql} WHEN MATCHED THEN DELETE;")
            else:
                return self.prepend_ctes(expression, f"DELETE{tables}{expression_sql}")

        def converttimezone_sql(self, expression: local_expression.ConvertTimeZone):
            func = "CONVERT_TIMEZONE"
            expr = expression.args["tgtTZ"]
            if len(expression.args) == 3 and expression.args.get("this"):
                expr = expression.args["this"]

            expr = f"'{expr.name}'" if isinstance(expr, exp.Cast) else expr

            result = self.func(func, expression.args["srcTZ"], expr)
            if len(expression.args) == 3:
                result = self.func(func, expression.args["srcTZ"], expression.args["tgtTZ"], expr)

            return result

        def strtok_sql(self, expression: local_expression.StrTok) -> str:
            """
            :param expression: local_expression.StrTok expression to be parsed
            :return: Converted expression (SPLIT_PART) compatible with Databricks
            """
            # To handle default delimiter
            if expression.expression:
                delimiter = expression.expression.name
            else:
                delimiter = " "

            # Handle String and Table columns
            if expression.name and isinstance(expression.name, str):
                expr_name = f"'{expression.name}'"
            else:
                expr_name = expression.args["this"]

            # Handle Partition Number
            if len(expression.args) == 3 and expression.args.get("partNum"):
                part_num = expression.args["partNum"]
            else:
                part_num = 1

            return f"SPLIT_PART({expr_name}, '{delimiter}', {part_num})"

        def splitpart_sql(self, expression: local_expression.SplitPart) -> str:
            """
            :param expression: local_expression.SplitPart expression to be parsed
            :return: Converted expression (SPLIT_PART) compatible with Databricks
            """
            expr_name = self.sql(expression.this)
            delimiter = self.sql(expression.expression)
            part_num = self.sql(expression.args["partNum"])
            return f"SPLIT_PART({expr_name}, {delimiter}, {part_num})"

        def transaction_sql(self, expression: exp.Transaction) -> str:  # noqa: ARG002
            """
            Skip begin command
            :param expression:
            :return: Empty string for unsupported operation
            """
            return ""

        def rollback_sql(self, expression: exp.Rollback) -> str:  # noqa: ARG002
            """
            Skip rollback command
            :param expression:
            :return: Empty string for unsupported operation
            """
            return ""

        def commit_sql(self, expression: exp.Rollback) -> str:  # noqa: ARG002
            """
            Skip commit command
            :param expression:
            :return: Empty string for unsupported operation
            """
            return ""

        def command_sql(self, expression: exp.Command) -> str:
            """
            Skip any session, stream, task related commands
            :param expression:
            :return: Empty string for unsupported operations or objects
            """
            filtered_commands = [
                "CREATE",
                "ALTER",
                "DESCRIBE",
                "DROP",
                "SHOW",
                "EXECUTE",
            ]
            ignored_objects = [
                "STREAM",
                "TASK",
                "STREAMS",
                "TASKS",
                "SESSION",
            ]

            command = self.sql(expression, "this").upper()
            expr = expression.text("expression").strip()
            obj = re.split(r"\s+", expr, maxsplit=2)[0].upper() if expr else ""
            if command in filtered_commands and obj in ignored_objects:
                return ""
            return f"{command} {expr}"
