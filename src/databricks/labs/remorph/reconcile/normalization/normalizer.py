from abc import abstractmethod, ABC

from sqlglot import parse_one
from sqlglot.dialects import Dialect
from sqlglot.expressions import Cast, Column, Expression, DataType

from databricks.labs.remorph.reconcile.constants import COLUMN_PLACEHOLDER


class Normalizer(ABC):
    def __init__(
        self,
        dialect: Dialect,
        default_normalizations: dict[str, str],
    ):
        self._dialect = dialect
        self._default_normalizations = self._prep_default_normalizations(default_normalizations)

    @abstractmethod
    def normalize(self, data_type: DataType, column: Column) -> Expression:
        pass

    @property
    def dialect(self) -> Dialect:
        return self._dialect

    def apply_default_normalizations(self, data_type: DataType, column: Column) -> Expression:
        transformation = self._default_normalizations.get(data_type)
        if not transformation:
            return column
        if COLUMN_PLACEHOLDER in transformation:
            return parse_one(transformation.format(column.sql()), dialect=self.dialect)
        return parse_one(transformation, dialect=self.dialect)

    def to_string(self, expr: Expression):
        return Cast(this=expr, to=DataType.Type.TEXT)

    def _prep_default_normalizations(self, default_normalizations: dict[str, str]) -> dict[DataType, str]:
        if not default_normalizations:
            return {}

        normalizations = {}
        for dt, expr in default_normalizations.items():
            data_type = DataType.build(dt, dialect=self.dialect, udt=True)
            normalizations[data_type] = expr
        return normalizations
