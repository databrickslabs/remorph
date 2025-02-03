from sqlglot import parse_one
from sqlglot.dialects import Dialect
from sqlglot.expressions import Cast, Column, Expression, DataType

from databricks.labs.remorph.recon.normalization.normalizer import Normalizer


class DatabricksNormalizer(Normalizer):
    def __init__(self, dialect: Dialect, default_normalizations: dict[str, str]):
        super().__init__(dialect, default_normalizations)

    def normalize(self, data_type: DataType, column: Column) -> Expression:
        if data_type.this == DataType.Type.BOOLEAN:
            return self.to_string(Cast(this=column, to=DataType.Type.INT))
        if data_type.this == DataType.Type.DATE:
            return parse_one(f"date_format({column.sql()}, 'yyyy-MM-dd')", dialect=self.dialect)
        # if TIMESTAMP type
        # convert to a string with 'yyyy-MM-dd HH:mm:ss.SSSSSS' format
        # if fractional number type
        # value = parse_one(f"cast({column.sql()} as decimal(38, {scale}))", dialect=self.dialect)
        # if scale > 0:
        #     value = parse_one(f"format_number({value.sql()}, {scale})", dialect=self.dialect)
        # return parse_one(f"replace({self.to_string(value)}, ',', '')", dialect=self.dialect)
        return self.apply_default_normalizations(data_type, column)
