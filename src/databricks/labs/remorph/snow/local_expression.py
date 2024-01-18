from typing import ClassVar

from sqlglot.expressions import AggFunc, Condition, Expression, Func


class Parameter(Expression):
    arg_types: ClassVar[dict] = {"this": True, "wrapped": False, "suffix": False}


class Collate(Func):
    arg_types: ClassVar[dict] = {"this": True, "expressions": True}


class Bracket(Condition):
    arg_types: ClassVar[dict] = {"this": True, "expressions": True}


class Split(Func):
    """
    Redefined Split(sqlglot/expression) class with expression: False to handle default delimiter
    Please refer the test case `test_strtok_to_array` -> `select STRTOK_TO_ARRAY('my text is divided')`
    """

    arg_types: ClassVar[dict] = {"this": True, "expression": False, "limit": False}


class MakeDate(Func):
    arg_types: ClassVar[dict] = {"this": True, "expression": False, "zone": False}


class ConvertTimeZone(Func):
    arg_types: ClassVar[dict] = {"srcTZ": True, "tgtTZ": True, "this": False}


class TryToDate(Func):
    arg_types: ClassVar[dict] = {"this": True, "format": False}


class SplitPart(Func):
    arg_types: ClassVar[dict] = {"this": True, "expression": False, "partNum": False}


class StrTok(Func):
    arg_types: ClassVar[dict] = {"this": True, "expression": False, "partNum": False}


class TryToNumber(Func):
    arg_types: ClassVar[dict] = {"this": True, "expression": True, "precision": False, "scale": False}
    _sql_names: ClassVar[dict] = ["TRY_TO_DECIMAL", "TRY_TO_NUMBER", "TRY_TO_NUMERIC"]


class DateFormat(Func):
    arg_types: ClassVar[dict] = {"this": True, "expression": False}


class IsInteger(Func):
    pass


class JsonExtractPathText(Func):
    arg_types: ClassVar[dict] = {"this": True, "path_name": True}


class BitOr(AggFunc):
    pass


class ArrayConstructCompact(Func):
    arg_types: ClassVar[dict] = {"expressions": False}
    is_var_len_args = True


class ArrayIntersection(Func):
    arg_types: ClassVar[dict] = {"this": True, "expression": True}


class ArraySlice(Func):
    arg_types: ClassVar[dict] = {"this": True, "from": True, "to": True}


class ObjectKeys(Func):
    arg_types: ClassVar[dict] = {"this": True}


class ToBoolean(Func):
    arg_types: ClassVar[dict] = {"this": True, "raise_error": False}


class ToDouble(Func):
    pass


class ToObject(Func):
    pass


class ToNumber(Func):
    arg_types: ClassVar[dict] = {"this": True, "expression": False, "precision": False, "scale": False}
    _sql_names: ClassVar[list] = ["TO_DECIMAL", "TO_NUMBER", "TO_NUMERIC"]


class TimestampFromParts(Func):
    arg_types: ClassVar[dict] = {
        "this": True,
        "expression": True,
        "day": True,
        "hour": True,
        "min": True,
        "sec": True,
        "nanosec": False,
        "Zone": False,
    }


class ToVariant(Func):
    pass


class UUID(Func):
    arg_types: ClassVar[dict] = {"this": False, "name": False}
