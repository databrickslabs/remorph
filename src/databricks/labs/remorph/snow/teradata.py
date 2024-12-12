from sqlglot.dialects.teradata import Teradata as org_Teradata
from sqlglot import expressions as exp
from sqlglot.tokens import TokenType
from databricks.labs.remorph.snow import local_expression


def translate(self, expr: local_expression.Translate) -> str:
    with_error = "WITH ERROR" if expr.args.get("with_error") else ""
    from_ = expr.args.get("from").this if isinstance(expr.args.get("from"),exp.CharacterSet) else ""
    to = expr.args.get("to").this if isinstance(expr.args.get("to"),exp.CharacterSet) else ""
    return f"TRANSLATE({self.sql(expr.this)} USING {from_}_TO_{to} {with_error})"

class Teradata(org_Teradata):
    teradata = org_Teradata()

    class Parser(org_Teradata.Parser):
        KEYWORDS = {
            **org_Teradata.Tokenizer.KEYWORDS,
            'CLOB': TokenType.STRING,
        }

        FUNCTION_PARSERS = {
            **org_Teradata.Parser.FUNCTION_PARSERS,
            "TRANSLATE": lambda self: self._parse_translate(False),
        }

        def _parse_translate(self, strict: bool) -> exp.Expression:
            this = self._parse_assignment()

            if not self._match(TokenType.USING):
                self.raise_error("Expected USING in TRANSLATE")

            if not self._match_texts(self.CHARSET_TRANSLATORS):
                self.raise_error("Expected a character set translator after USING in TRANSLATE")

            charset_split = self._prev.text.split("_TO_")
            _from = self.expression(exp.CharacterSet, this=charset_split[0])
            to = self.expression(exp.CharacterSet, this=charset_split[1])
            with_error = self._match_text_seq("WITH", "ERROR")
            return self.expression(
                local_expression.Translate,
                **{
                    "this": this,
                    "from": _from,
                    "to": to,
                    "with_error": with_error,
                },
            )

    class Generator(org_Teradata.Generator):
        TYPE_MAPPING = {
            **org_Teradata.Generator.TYPE_MAPPING,
            exp.DataType.Type.TEXT: "CLOB",
        }
        TRANSFORMS = {
            **org_Teradata.Generator.TRANSFORMS,
            local_expression.Translate: translate,
        }