from typing import ClassVar

from sqlglot.dialects.oracle import Oracle as Orc
from sqlglot.tokens import TokenType


class Oracle(Orc):
    # Instantiate Oracle Dialect
    oracle = Orc()

    class Tokenizer(Orc.Tokenizer):
        def __init__(self):
            super().__init__()
            self.KEYWORDS: ClassVar[dict] = {**Orc.Tokenizer.KEYWORDS, 'LONG': TokenType.TEXT}
