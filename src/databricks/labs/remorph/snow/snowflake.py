import copy
import re
import typing as t
from typing import ClassVar

from databricks.labs.blueprint.entrypoint import get_logger
from sqlglot import exp, parser
from sqlglot.dialects.dialect import parse_date_delta
from sqlglot.dialects.snowflake import Snowflake
from sqlglot.dialects.snowflake import _parse_to_timestamp as parse_to_timestamp
from sqlglot.errors import ParseError
from sqlglot.helper import seq_get
from sqlglot.tokens import Token, TokenType
from sqlglot.trie import new_trie

from databricks.labs.remorph.snow import local_expression

logger = get_logger(__file__)

""" SF Supported Date and Time Parts:
    https://docs.snowflake.com/en/sql-reference/functions-date-time#label-supported-date-time-parts
    Covers DATEADD, DATEDIFF, DATE_TRUNC, LAST_DAY
"""
DATE_DELTA_INTERVAL = {
    "years": "year",
    "year": "year",
    "yrs": "year",
    "yr": "year",
    "yyyy": "year",
    "yyy": "year",
    "yy": "year",
    "y": "year",
    "quarters": "quarter",
    "quarter": "quarter",
    "qtrs": "quarter",
    "qtr": "quarter",
    "q": "quarter",
    "months": "month",
    "month": "month",
    "mons": "month",
    "mon": "month",
    "mm": "month",
    "weekofyear": "week",
    "week": "week",
    "woy": "week",
    "wy": "week",
    "wk": "week",
    "w": "week",
    "dayofmonth": "day",
    "days": "day",
    "day": "day",
    "dd": "day",
    "d": "day",
}


def _parse_dateadd(args: list) -> exp.DateAdd:
    return exp.DateAdd(this=seq_get(args, 2), expression=seq_get(args, 1), unit=seq_get(args, 0))


def _parse_split_part(args: list) -> local_expression.SplitPart:
    if len(args) != 3:
        err_msg = f"Error Parsing args `{args}`. Number of args must be 3, given {len(args)}"
        raise ParseError(err_msg)
    part_num = seq_get(args, 2)
    if isinstance(part_num, exp.Literal):
        # In Snowflake if the partNumber is 0, it is treated as 1.
        # Please refer to https://docs.snowflake.com/en/sql-reference/functions/split_part
        if part_num.is_int and int(part_num.name) == 0:
            part_num = exp.Literal.number(1)
    else:
        cond = exp.EQ(this=part_num, expression=exp.Literal.number(0))
        part_num = exp.If(this=cond, true=exp.Literal.number(1), false=part_num)
    return local_expression.SplitPart(this=seq_get(args, 0), expression=seq_get(args, 1), partNum=part_num)


def _div0null_to_if(args: list) -> exp.If:
    cond = exp.Or(
        this=exp.EQ(this=seq_get(args, 1), expression=exp.Literal.number(0)),
        expression=exp.Is(this=seq_get(args, 1), expression=exp.NULL),
    )
    true = exp.Literal.number(0)
    false = exp.Div(this=seq_get(args, 0), expression=seq_get(args, 1))
    return exp.If(this=cond, true=true, false=false)


def _parse_json_extract_path_text(args: list) -> local_expression.JsonExtractPathText:
    if len(args) != 2:
        err_message = f"Error Parsing args `{args}`. Number of args must be 2, given {len(args)}"
        raise ParseError(err_message)
    return local_expression.JsonExtractPathText(this=seq_get(args, 0), path_name=seq_get(args, 1))


def _parse_array_contains(args: list) -> exp.ArrayContains:
    if len(args) != 2:
        err_message = f"Error Parsing args `{args}`. Number of args must be 2, given {len(args)}"
        raise ParseError(err_message)
    return exp.ArrayContains(this=seq_get(args, 1), expression=seq_get(args, 0))


def _parse_dayname(args: list) -> local_expression.DateFormat:
    """
        * E, EE, EEE, returns short day name (Mon)
        * EEEE, returns full day name (Monday)
    :param args: node expression
    :return: DateFormat with `E` format
    """
    if len(args) != 1:
        err_message = f"Error Parsing args `{args}`. Number of args must be 1, given {len(args)}"
        raise ParseError(err_message)
    return local_expression.DateFormat(this=seq_get(args, 0), expression=exp.Literal.string("E"))


def _parse_trytonumber(args: list) -> local_expression.TryToNumber:
    if len(args) == 1 or len(args) == 3:
        msg = f"""Error Parsing args `{args}`:
                             * `format` is required
                             * `precision` and `scale` both are required [if specified]
                          """
        raise ParseError(msg)

    if len(args) == 4:
        return local_expression.TryToNumber(
            this=seq_get(args, 0), expression=seq_get(args, 1), precision=seq_get(args, 2), scale=seq_get(args, 3)
        )

    return local_expression.TryToNumber(this=seq_get(args, 0), expression=seq_get(args, 1))


def _parse_monthname(args: list) -> local_expression.DateFormat:
    if len(args) != 1:
        err_message = f"Error Parsing args `{args}`. Number of args must be 1, given {len(args)}"
        raise ParseError(err_message)
    return local_expression.DateFormat(this=seq_get(args, 0), expression=exp.Literal.string("MMM"))


def _parse_object_construct(args: list) -> exp.StarMap | exp.Struct:
    expression = parser.parse_var_map(args)

    if isinstance(expression, exp.StarMap):
        return exp.Struct(expressions=[expression.this])

    return exp.Struct(
        expressions=[t.cast(exp.Condition, k).eq(v) for k, v in zip(expression.keys, expression.values, strict=False)]
    )


def _parse_to_boolean(args: list, *, error=False) -> local_expression.ToBoolean:
    this_arg = seq_get(args, 0)
    return local_expression.ToBoolean(this=this_arg, raise_error=exp.Literal.number(1 if error else 0))


def _parse_tonumber(args: list) -> local_expression.ToNumber:
    if len(args) > 4:
        error_msg = f"""Error Parsing args args:
                          * Number of args cannot be more than `4`, given `{len(args)}`
                          """
        raise ParseError(error_msg)

    if len(args) == 1:
        return local_expression.ToNumber(this=seq_get(args, 0))
    elif len(args) == 3:
        return local_expression.ToNumber(this=seq_get(args, 0), precision=seq_get(args, 1), scale=seq_get(args, 2))
    elif len(args) == 4:
        return local_expression.ToNumber(
            this=seq_get(args, 0), expression=seq_get(args, 1), precision=seq_get(args, 2), scale=seq_get(args, 3)
        )

    return local_expression.ToNumber(this=seq_get(args, 0), expression=seq_get(args, 1))


class Snow(Snowflake):
    # Instantiate Snowflake Dialect
    snowflake = Snowflake()

    class Tokenizer(snowflake.Tokenizer):
        IDENTIFIERS: ClassVar[list[str]] = ['"']

        COMMENTS: ClassVar[list[str]] = ["--", "//", ("/*", "*/")]
        STRING_ESCAPES: ClassVar[list[str]] = ["\\", "'"]

        CUSTOM_TOKEN_MAP: ClassVar[dict] = {
            r"(?i)CREATE\s+OR\s+REPLACE\s+PROCEDURE": TokenType.PROCEDURE,
            r"(?i)var\s+\w+\s+=\s+\w+?": TokenType.VAR,
        }

        KEYWORDS: ClassVar[dict] = {**Snowflake.Tokenizer.KEYWORDS}
        # DEC is not a reserved keyword in Snowflake it can be used as table alias
        KEYWORDS.pop("DEC")

        @classmethod
        def update_keywords(cls, new_key_word_dict):
            cls.KEYWORDS = new_key_word_dict | cls.KEYWORDS

        @classmethod
        def merge_trie(cls, parent_trie, new_trie):
            merged_trie = {}
            logger.debug(f"The Parent Trie is {parent_trie}")
            logger.debug(f"The Input Trie is {new_trie}")
            for key in set(parent_trie.keys()) | set(new_trie.keys()):  # Get all unique keys from both tries
                if key in parent_trie and key in new_trie:  # If the key is in both tries, merge the subtries
                    if isinstance(parent_trie[key], dict) and isinstance(new_trie[key], dict):
                        logger.debug(f"New trie inside the key is {new_trie}")
                        logger.debug(f"Parent trie inside the key is {parent_trie}")
                        merged_trie[key] = cls.merge_trie(parent_trie[key], new_trie[key])
                        logger.debug(f"Merged Trie is {merged_trie}")
                    elif isinstance(parent_trie[key], dict):
                        merged_trie[key] = parent_trie[key]
                    else:
                        merged_trie[key] = new_trie[key]
                elif key in parent_trie:  # If the key is only in trie1, add it to the merged trie
                    merged_trie[key] = parent_trie[key]
                else:  # If the key is only in trie2, add it to the merged trie
                    merged_trie[key] = new_trie[key]
            return merged_trie

        @classmethod
        def update_keyword_trie(
            cls,
            new_trie,
            parent_trie=None,
        ):
            if parent_trie is None:
                parent_trie = cls._KEYWORD_TRIE
            cls.KEYWORD_TRIE = cls.merge_trie(parent_trie, new_trie)

        def match_strings_token_dict(self, string, pattern_dict):
            result_dict = {}
            for pattern in pattern_dict:
                matches = re.finditer(pattern, string, re.MULTILINE | re.IGNORECASE | re.DOTALL)
                for _, match in enumerate(matches, start=1):
                    result_dict[match.group().upper()] = pattern_dict[pattern]
            return result_dict

        def match_strings_list(self, string, pattern_dict):
            result = []
            for pattern in pattern_dict:
                matches = re.finditer(pattern, string, re.MULTILINE | re.IGNORECASE | re.DOTALL)
                for _, match in enumerate(matches, start=1):
                    result.append(match.group().upper())
            return result

        def tokenize(self, sql: str) -> list[Token]:
            """Returns a list of tokens corresponding to the SQL string `sql`."""
            self.reset()
            self.sql = sql
            # Update Keywords
            ref_dict = self.match_strings_token_dict(sql, self.CUSTOM_TOKEN_MAP)
            self.update_keywords(ref_dict)
            # Update Keyword Trie
            custom_trie = new_trie(self.match_strings_list(sql, self.CUSTOM_TOKEN_MAP))
            logger.debug(
                f"The New Trie after adding the REF, VAR and IF ELSE blocks "
                f"based on {self.CUSTOM_TOKEN_MAP}, is \n\n {custom_trie}"
            )
            self.update_keyword_trie(custom_trie)
            logger.debug(f"Updated New Trie is {self.KEYWORD_TRIE}")
            # Parent Code
            self.size = len(sql)
            try:
                self._scan()
            except Exception as e:
                start = self._current - 50
                end = self._current + 50
                start = start if start > 0 else 0
                end = end if end < self.size else self.size - 1
                context = self.sql[start:end]
                msg = f"Error tokenizing '{context}'"
                raise ParseError(msg) from e
            return self.tokens

    class Parser(snowflake.Parser):
        FUNCTIONS: ClassVar[dict] = {
            **Snowflake.Parser.FUNCTIONS,
            "STRTOK_TO_ARRAY": local_expression.Split.from_arg_list,
            "DATE_FROM_PARTS": local_expression.MakeDate.from_arg_list,
            "CONVERT_TIMEZONE": local_expression.ConvertTimeZone.from_arg_list,
            "TRY_TO_DATE": local_expression.TryToDate.from_arg_list,
            "STRTOK": local_expression.StrTok.from_arg_list,
            "SPLIT_PART": _parse_split_part,
            "TIMESTAMPADD": _parse_dateadd,
            "TRY_TO_DECIMAL": _parse_trytonumber,
            "TRY_TO_NUMBER": _parse_trytonumber,
            "TRY_TO_NUMERIC": _parse_trytonumber,
            "DATEADD": parse_date_delta(exp.DateAdd, unit_mapping=DATE_DELTA_INTERVAL),
            "DATEDIFF": parse_date_delta(exp.DateDiff, unit_mapping=DATE_DELTA_INTERVAL),
            "IS_INTEGER": local_expression.IsInteger.from_arg_list,
            "DIV0NULL": _div0null_to_if,
            "JSON_EXTRACT_PATH_TEXT": _parse_json_extract_path_text,
            "BITOR_AGG": local_expression.BitOr.from_arg_list,
            "ARRAY_CONTAINS": _parse_array_contains,
            "DAYNAME": _parse_dayname,
            "BASE64_ENCODE": exp.ToBase64.from_arg_list,
            "BASE64_DECODE_STRING": exp.FromBase64.from_arg_list,
            "TRY_BASE64_DECODE_STRING": exp.FromBase64.from_arg_list,
            "ARRAY_CONSTRUCT_COMPACT": local_expression.ArrayConstructCompact.from_arg_list,
            "ARRAY_INTERSECTION": local_expression.ArrayIntersection.from_arg_list,
            "ARRAY_SLICE": local_expression.ArraySlice.from_arg_list,
            "MONTHNAME": _parse_monthname,
            "MONTH_NAME": _parse_monthname,
            "OBJECT_CONSTRUCT": _parse_object_construct,
            "OBJECT_KEYS": local_expression.ObjectKeys.from_arg_list,
            "TRY_PARSE_JSON": exp.ParseJSON.from_arg_list,
            "TIMEDIFF": parse_date_delta(exp.DateDiff, unit_mapping=DATE_DELTA_INTERVAL),
            "TIMESTAMPDIFF": parse_date_delta(exp.DateDiff, unit_mapping=DATE_DELTA_INTERVAL),
            "TIMEADD": _parse_dateadd,
            "TO_BOOLEAN": lambda args: _parse_to_boolean(args, error=True),
            "TO_DECIMAL": _parse_tonumber,
            "TO_DOUBLE": local_expression.ToDouble.from_arg_list,
            "TO_NUMBER": _parse_tonumber,
            "TO_NUMERIC": _parse_tonumber,
            "TO_OBJECT": local_expression.ToObject.from_arg_list,
            "TO_TIME": parse_to_timestamp,
            "TIMESTAMP_FROM_PARTS": local_expression.TimestampFromParts.from_arg_list,
            "TO_VARIANT": local_expression.ToVariant.from_arg_list,
            "TRY_TO_BOOLEAN": lambda args: _parse_to_boolean(args, error=False),
            "UUID_STRING": local_expression.UUID.from_arg_list,
            "SYSDATE": exp.CurrentTimestamp.from_arg_list,
        }

        FUNCTION_PARSERS: ClassVar[dict] = {
            **Snowflake.Parser.FUNCTION_PARSERS,
        }

        PLACEHOLDER_PARSERS: ClassVar[dict] = {
            **Snowflake.Parser.PLACEHOLDER_PARSERS,
            TokenType.PARAMETER: lambda self: self._parse_parameter(),
        }

        FUNC_TOKENS: ClassVar[dict] = {*Snowflake.Parser.FUNC_TOKENS, TokenType.COLLATE}

        COLUMN_OPERATORS: ClassVar[dict] = {
            **Snowflake.Parser.COLUMN_OPERATORS,
            TokenType.COLON: lambda self, this, path: self._json_column_op(this, path),
        }

        TIMESTAMPS: ClassVar[dict] = Snowflake.Parser.TIMESTAMPS.copy() - {TokenType.TIME}

        RANGE_PARSERS: ClassVar[dict] = {
            **Snowflake.Parser.RANGE_PARSERS,
        }

        ALTER_PARSERS: ClassVar[dict] = {**Snowflake.Parser.ALTER_PARSERS}

        def _parse_types(
            self, *, check_func: bool = False, schema: bool = False, allow_identifiers: bool = True
        ) -> t.Optional[exp.Expression]:  # noqa: UP007
            this = super()._parse_types(check_func=check_func, schema=schema, allow_identifiers=allow_identifiers)
            # https://docs.snowflake.com/en/sql-reference/data-types-numeric Numeric datatype alias
            if (
                isinstance(this, exp.DataType)
                and this.is_type("numeric", "decimal", "number", "integer", "int", "smallint", "bigint")
                and not this.expressions
            ):
                return exp.DataType.build("DECIMAL(38,0)")
            return this

        def _parse_parameter(self) -> local_expression.Parameter:
            wrapped = self._match(TokenType.L_BRACE)
            this = self._parse_var() or self._parse_identifier() or self._parse_primary()
            self._match(TokenType.R_BRACE)
            suffix = ""
            if not self._match(TokenType.SPACE) or self._match(TokenType.DOT):
                suffix = self._parse_var() or self._parse_identifier() or self._parse_primary()

            return self.expression(local_expression.Parameter, this=this, wrapped=wrapped, suffix=suffix)

        def _get_table_alias(self):
            """
            :returns the `table alias` by looping through all the tokens until it finds the `From` token.
            Example:
            * SELECT .... FROM persons p => returns `p`
            * SELECT
                 ....
              FROM
                 dwh.vw_replacement_customer  d  => returns `d`
            """
            # Create a deep copy of Parser to avoid any modifications to original one
            self_copy = copy.deepcopy(self)
            found_from = True if self_copy._match(TokenType.FROM, advance=False) else False
            run = True
            indx = 0
            table_alias = None

            try:
                # iterate through all the tokens if tokens are available
                while self_copy._index < len(self_copy._tokens) and (run or found_from):
                    self_copy._advance()
                    indx += 1
                    found_from = True if self_copy._match(TokenType.FROM, advance=False) else False
                    # stop iterating when all the tokens are parsed
                    if indx == len(self_copy._tokens):
                        run = False
                    # get the table alias when FROM token is found
                    if found_from:
                        """
                        advance to two tokens after FROM, if there are available.
                        Handles (SELECT .... FROM persons p => returns `p`)
                        """
                        if self_copy._index + 2 < len(self_copy._tokens):
                            self_copy._advance(2)
                            table_alias = self_copy._curr.text
                            """
                          * if the table is of format :: `<DB>.<TABLE>` <TABLE_ALIAS>, advance to two more tokens
                            - Handles (`SELECT .... FROM dwh.vw_replacement_customer  d`  => returns d)
                          * if the table is of format :: `<DB>.<SCHEMA>.<TABLE>` <TABLE_ALIAS>, advance to 2 more tokens
                            - Handles (`SELECT .... FROM prod.public.tax_transact tt`  => returns tt)
                            """
                            while table_alias == "." and self_copy._index + 2 < len(self_copy._tokens):
                                self_copy._advance(2)
                                table_alias = self_copy._curr.text
                            break
            except Exception:
                logger.exception("Error while getting table alias.")

            return table_alias

        def _json_column_op(self, this, path):
            """
            Get the `table alias` using _get_table_alias() and it is used to check whether
            to remove `.value` from `<COL>.value`. We need to remove `.value` only if it refers
            to `Lateral View` alias.
            :return: the expression based on the alias.
            """
            table_alias = self._get_table_alias()
            is_name_value = this.name.upper() == "VALUE"
            is_path_value = path.alias_or_name.upper() == "VALUE"

            if isinstance(this, exp.Column) and this.table:
                col_table_alias = this.table.upper()
            elif isinstance(this, local_expression.Bracket) and isinstance(this.this, exp.Column) and this.this.table:
                col_table_alias = this.this.table.upper()
            else:
                col_table_alias = this.name.upper()

            is_table_alias = col_table_alias == table_alias.upper() if table_alias else False

            if not isinstance(this, exp.Bracket) and is_name_value:
                # If the column is referring to `lateral alias`, remove `.value` reference (not needed in Databricks)
                if table_alias and this.table != table_alias:
                    return self.expression(local_expression.Bracket, this=this.table, expressions=[path])
                """
                    if it is referring to `table_alias`, we need to keep `.value`. See below example:
                    - SELECT f.first, p.c.value.first, p.value FROM persons_struct AS p
                        LATERAL VIEW EXPLODE($p.$c.contact) AS f
                """
                return self.expression(local_expression.Bracket, this=this, expressions=[path])
            elif isinstance(this, local_expression.Bracket) and (is_name_value or is_table_alias):
                return self.expression(local_expression.Bracket, this=this, expressions=[path])
            elif isinstance(path, exp.Literal) and (path or is_path_value):
                return self.expression(local_expression.Bracket, this=this, expressions=[path])
            else:
                return self.expression(exp.Bracket, this=this, expressions=[path])
