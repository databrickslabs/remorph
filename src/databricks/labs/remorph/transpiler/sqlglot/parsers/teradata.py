from functools import partial

from sqlglot.dialects.teradata import Teradata as SqlglotTeradata
from sqlglot import exp
from sqlglot.tokens import TokenType
from sqlglot.errors import ErrorLevel

from databricks.labs.remorph.transpiler.sqlglot import local_expression

# pylint: disable=protected-access
class Teradata(SqlglotTeradata):
    teradata = SqlglotTeradata()

    class Parser(SqlglotTeradata.Parser):

        STATEMENT_PARSERS = {
            **SqlglotTeradata.Parser.STATEMENT_PARSERS,
            TokenType.CREATE: lambda self: self._parse_create(),
        }

        CONSTRAINT_PARSERS = {
            **SqlglotTeradata.Parser.CONSTRAINT_PARSERS,
            "COMPRESS": lambda self: self._parse_compress(),
        }

        PROPERTY_PARSERS = {
            **SqlglotTeradata.Parser.PROPERTY_PARSERS,
            "MAP": lambda self: self._parse_map_property(),
        }

        FUNCTION_PARSERS = {
            **SqlglotTeradata.Parser.FUNCTION_PARSERS,
            "CASE_N": lambda self: self._parse_case_n(),
        }

        def match_pair_and_advance(self):
            self.error_level = ErrorLevel.WARN
            start, comments = self._prev, self._prev_comments
            replace = start.text.upper() == "REPLACE" or self._match_pair(TokenType.OR, TokenType.REPLACE)
            unique = self._match(TokenType.UNIQUE)
            if self._match_pair(TokenType.TABLE, TokenType.FUNCTION, advance=False):
                self._advance()

            properties, create_token = None, self._match_set(self.CREATABLES) and self._prev
            return unique, replace, start, comments, properties, create_token

        def _initialize_create_variables(self):
            exists = self._parse_exists(not_=True)
            this = None
            expression: exp.Expression | None = None
            indexes = None
            no_schema_binding = None
            begin = None
            end = None
            clone = None
            return exists, this, expression, indexes, no_schema_binding, begin, end, clone

        def _parse_function_body(self, extend_props):
            begin = self._match(TokenType.BEGIN)
            return_ = self._match_text_seq("RETURN")

            if self._match(TokenType.STRING, advance=False):
                expression = self._parse_string()
                extend_props(self._parse_properties())
            else:
                expression = self._parse_statement()

            end = self._match_text_seq("END")

            if return_:
                expression = self.expression(exp.Return, this=expression)

            return begin, expression, end

        def _parse_table_schema(self, extend_props):
            table_parts = self._parse_table_parts(schema=True)

            self._match(TokenType.COMMA)
            extend_props(self._parse_properties(before=True))
            this = self._parse_schema(this=table_parts)
            extend_props(self._parse_properties())
            self._match(TokenType.ALIAS)
            return this

        def extend_props(self, properties, temp_props: exp.Properties | None) -> None:
            if properties and temp_props:
                properties.expressions.extend(temp_props.expressions)
            elif temp_props:
                properties = temp_props

        def _parse_create(self) -> exp.Create | exp.Command:
            unique, replace, start, comments, properties, create_token = self.match_pair_and_advance()

            if not create_token:
                properties = self._parse_properties()
                create_token = self._match_set(self.CREATABLES) and self._prev

                if not properties or not create_token:
                    return self._parse_as_command(start)

            exists, this, expression, indexes, no_schema_binding, begin, end, clone = (
                self._initialize_create_variables()
            )

            extend_props_partial = partial(self.extend_props, properties)

            if create_token.token_type in (TokenType.FUNCTION, TokenType.PROCEDURE):
                this = self._parse_user_defined_function(kind=create_token.token_type)
                extend_props_partial(self._parse_properties())
                self._match(TokenType.ALIAS)
                if not self._match(TokenType.COMMAND):
                    begin, expression, end = self._parse_function_body(extend_props_partial)

                expression = self._parse_as_command(self._prev)

            elif create_token.token_type == TokenType.INDEX:
                this = self._parse_index(index=self._parse_id_var())
            elif create_token.token_type in self.DB_CREATABLES:
                this = self._parse_table_schema(extend_props_partial)
                if not self._match_set(self.DDL_SELECT_TOKENS, advance=False):
                    extend_props_partial(self._parse_properties())

                expression = self._parse_ddl_select()

                if create_token.token_type == TokenType.TABLE:
                    self._parse_table_properties(extend_props_partial)
                    indexes = self._parse_indexes(extend_props_partial)
                elif create_token.token_type == TokenType.VIEW:
                    no_schema_binding = self._match_text_seq("WITH", "NO", "SCHEMA", "BINDING")

                shallow = self._match_text_seq("SHALLOW")
                clone = self._create_clone_if_needed(shallow)
                self._match(TokenType.WITH)

            return self.expression(
                exp.Create,
                comments=comments,
                this=this,
                kind=create_token.text,
                replace=replace,
                unique=unique,
                expression=expression,
                exists=exists,
                properties=properties,
                indexes=indexes,
                no_schema_binding=no_schema_binding,
                begin=begin,
                end=end,
                clone=clone,
            )

        def _parse_table_properties(self, extend_props_partial):
            extend_props_partial(self._parse_properties())

        def _parse_indexes(self, extend_props_partial):
            indexes = []
            while True:
                index = self._parse_index()
                extend_props_partial(self._parse_properties())
                if not index:
                    break
                self._match(TokenType.COMMA)
                indexes.append(index)
            return indexes

        def _create_clone_if_needed(self, shallow):
            if self._match_texts(self.CLONE_KEYWORDS):
                return self._create_copy_clone(shallow)
            return None

        def _create_copy_clone(self, shallow: bool):
            copy = self._prev.text.lower() == "copy"
            clone = self.expression(exp.Clone, this=self._parse_table(schema=True), shallow=shallow, copy=copy)
            return clone

        def _parse_compress(self) -> exp.CompressColumnConstraint:
            if self._match(TokenType.L_PAREN, advance=False):
                return self.expression(exp.CompressColumnConstraint, this=self._parse_wrapped_csv(self._parse_bitwise))
            bitwise_expr = self._parse_bitwise()
            this_expr = bitwise_expr if bitwise_expr else exp.Literal(this=" ", is_string=True)
            return self.expression(exp.CompressColumnConstraint, this=this_expr)

        def _parse_map_property(self) -> local_expression.MapProperty:
            self._match(TokenType.EQ)
            return self.expression(
                local_expression.MapProperty, this="MAP", name=self._parse_var(any_token=False, tokens=[TokenType.VAR])
            )

        def _parse_rangen(self) -> local_expression.RangeN:
            this = self._parse_id_var()
            self._match(TokenType.BETWEEN)
            expressions = self._parse_csv(self._parse_assignment)
            each = self._match_text_seq("EACH") and self._parse_assignment()

            range_spec = []
            while self._match(TokenType.COMMA):
                if self._match(TokenType.VAR) or self._match(TokenType.UNKNOWN):
                    final_option = self._prev.text
                    if self._match_texts(["UNKNOWN", "RANGE"]):
                        final_option = f"{final_option} " + self._prev.text
                        if self._match_texts(["OR", ",", "|"]):
                            final_option = f"{final_option} {self._prev.text} {self._curr.text}"
                            self._advance(1)
                    range_spec.append(final_option)
                else:
                    final_option = self._curr.text
                    self._advance(1)
                    while not self._match(TokenType.COMMA, advance=False) and not self._match(
                        TokenType.R_PAREN, advance=False
                    ):
                        final_option = final_option + " " + self._curr.text
                        self._advance(1)
                    range_spec.append(final_option)

            return self.expression(
                local_expression.RangeN, this=this, expressions=expressions, each=each, range_spec=range
            )

        def _parse_case_n(self) -> local_expression.CaseN:
            list_exp = []
            list_exp.append(self._parse_assignment())
            case_spec = None
            while self._match(TokenType.COMMA):
                if self._match_texts(["NO"]):
                    case_spec = self._process_case_spec()
                elif self._match_texts(["UNKNOWN"]):
                    case_spec = self._prev.text
                else:
                    list_exp.append(self._parse_assignment())

            return self.expression(local_expression.CaseN, this="CASE_N", expression=list_exp, case_spec=case_spec)

        def _process_case_spec(self) -> str:
            case_spec = "NO " + self._curr.text
            self._advance(1)
            if self._match_texts(["OR", ",", "|"]):
                case_spec = f"{case_spec} {self._prev.text} {self._curr.text}"
                self._advance(1)
            return case_spec
