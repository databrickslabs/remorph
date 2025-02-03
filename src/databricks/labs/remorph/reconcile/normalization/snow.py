from sqlglot.dialects import Dialect
from sqlglot.expressions import Cast, Column, Expression, DataType

from databricks.labs.remorph.recon.normalization.normalizer import Normalizer


class SnowNormalizer(Normalizer):
    def __init__(self, dialect: Dialect, default_normalizations: dict[str, str]):
        super().__init__(dialect, default_normalizations)

    def normalize(self, data_type: DataType, column: Column) -> Expression:
        if data_type.this == DataType.Type.BOOLEAN:
            return self.to_string(Cast(this=column, to=DataType.Type.INT))
        if data_type.this == DataType.Type.UUID:
            return self.to_string(column)
        if data_type.this == DataType.Type.DATE:
            return self.to_string(column)
        # if TIMESTAMP type
        # convert to a string with 'YYYY-MM-DD HH24:MI:SS.FF6' format
        # if fractional number type
        # convert to a string with CAST(column AS DECIMAL(38, scale))
        return self.apply_default_normalizations(data_type, column)
