from typing import ClassVar

from sqlglot.dialects.presto import Presto as presto
from sqlglot.tokens import TokenType
from sqlglot import exp
from sqlglot.helper import apply_index_offset, seq_get


def _build_approx_percentile(args: list) -> exp.Expression:
    if len(args) == 4:
        arg3 = seq_get(args, 3)
        try:
            number = float(arg3.this)
            return exp.ApproxQuantile(
                this=seq_get(args, 0),
                weight=seq_get(args, 1),
                quantile=seq_get(args, 2),
                accuracy=exp.Literal(this=f'{int((1/number) * 100)} ', is_string=False),
            )
        except ValueError:
            raise ValueError(f"Expected a string representation of a number for argument 2, but got {arg3.this}")
    if len(args) == 3:
        arg2 = seq_get(args, 2)
        try:
            number = float(arg2.this)
            return exp.ApproxQuantile(
                this=seq_get(args, 0),
                quantile=seq_get(args, 1),
                accuracy=exp.Literal(this=f'{int((1/number) * 100)}', is_string=False)
            )
        except ValueError:
            raise ValueError(f"Expected a string representation of a number for argument 2, but got {arg2.this}")
    return exp.ApproxQuantile.from_arg_list(args)


class Presto(presto):

    class Parser(presto.Parser):
        VALUES_FOLLOWED_BY_PAREN = False

        FUNCTIONS = {
            "APPROX_PERCENTILE": _build_approx_percentile,
        }