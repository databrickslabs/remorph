from sqlglot.dialects.teradata import Teradata as org_Teradata
from sqlglot import expressions as exp
from sqlglot.tokens import TokenType

class Teradata(org_Teradata):
    teradata = org_Teradata()

    class Parser(org_Teradata.Parser):
        
        FUNCTION_PARSERS = {
            **org_Teradata.Parser.FUNCTION_PARSERS,
            "TRANSLATE": lambda self: self._parse_translate(self.STRICT_CAST),
        }

        def _parse_translate(self, strict: bool) -> exp.Expression:
            this = self._parse_assignment()

            if not self._match(TokenType.USING):
                self.raise_error("Expected USING in TRANSLATE")

            if self._match_texts(self.CHARSET_TRANSLATORS):
                charset_split = self._prev.text.split("_TO_")
                to = self.expression(exp.CharacterSet, this=charset_split[1])
            else:
                self.raise_error("Expected a character set translator after USING in TRANSLATE")
            
            # return f"TRANSLATE({this} USING {charset_split[0]}_{charset_split[1]} WITH ERROR)"
            return self.expression(exp.Anonymous, this=f"TRANSLATE", expressions=[f"{this} USING {charset_split[0]}_{charset_split[1]} WITH ERROR"])
    class Tokenizer(org_Teradata.Tokenizer):
        KEYWORDS = {
            **org_Teradata.Tokenizer.KEYWORDS,
            'WITH ERROR': 'WITH_ERROR',
            'CLOB': TokenType.STRING,
        }