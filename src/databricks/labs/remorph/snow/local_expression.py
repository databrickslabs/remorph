from typing import ClassVar

from sqlglot.expressions import Condition, Expression, Func


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


class TryToNumber(Func):
    arg_types: ClassVar[dict] = {"this": True, "expression": True, "precision": False, "scale": False}
    _sql_names: ClassVar[dict] = ["TRY_TO_DECIMAL", "TRY_TO_NUMBER", "TRY_TO_NUMERIC"]
