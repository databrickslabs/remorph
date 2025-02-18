from sqlglot import Dialect
from sqlglot.dialects import Dialects


def get_dialect(name: str) -> Dialect:
    value = Dialect.get(name)
    if isinstance(value, Dialect):
        return value
    if isinstance(value, type(Dialect)):
        return value()
    raise ValueError(f"Can't instantiate dialect from {name}")


def dialect_exists(name: str) -> bool:
    values = {member.value for member in Dialects}
    return name in values


def get_dialect_name(dialect: Dialect) -> str:
    try:
        return Dialects(dialect).value
    except ValueError:
        return "universal"
