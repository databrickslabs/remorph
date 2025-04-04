from sqlglot.dialects import Dialect
from sqlglot.expressions import Cast, Column, Expression, DataType, Trim

from databricks.labs.remorph.recon.normalization.normalizer import Normalizer


class OracleNormalizer(Normalizer):
    def __init__(self, dialect: Dialect, default_normalizations: dict[str, str]):
        super().__init__(dialect, default_normalizations)

    def normalize(self, data_type: DataType, column: Column) -> Expression:
        if data_type.this == DataType.Type.BOOLEAN:
            return self.to_string(column)
        if data_type.this == DataType.Type.UUID:
            return Cast(this=Trim(this=column), to=DataType.build("VARCHAR(36)", dialect=self.dialect))
        if data_type.this == DataType.Type.DATE:
            return self.to_string(column)
        # if TIMESTAMP type
        # convert to a string with 'YYYY-MM-DD HH24:MI:SS.FF6' format
        # if fractional number type
        # convert to a string with FM999.9990 based format based on precision and scale
        return self.apply_default_normalizations(data_type, column)

    def to_string(self, expr: Expression):
        return Cast(this=expr, to=DataType.build("VARCHAR(1024)", dialect=self.dialect))
