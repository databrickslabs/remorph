from sqlglot.dialects.oracle import Oracle as Orc
from sqlglot.tokens import TokenType


class Oracle(Orc):
    # Instantiate Oracle Dialect
    oracle = Orc()

    class Tokenizer(Orc.Tokenizer):
        KEYWORDS = {**Orc.Tokenizer.KEYWORDS, 'LONG': TokenType.TEXT}
