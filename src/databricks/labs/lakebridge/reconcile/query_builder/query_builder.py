import dataclasses
import logging


from databricks.labs.lakebridge.reconcile.exception import InvalidInputException
from databricks.labs.lakebridge.reconcile.recon_config import ColumnType, TableMapping, Aggregate, Layer

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Column:
    table: str | None
    name: str
    alias: str | None = None
    transform: str | None = None
    quoted = False

    def sql(self) -> str:
        if self.transform and self.transform != self.name and self.transform != self.alias:
            if not self.alias:
                raise ValueError(f"Missing alias for column: {self}")
            return f"{self.transform} AS {self.alias}"
        if self.alias and self.alias != self.name:
            return f"{self.name} AS {self.alias}"
        return self.name


class QueryBuilder:

    @classmethod
    def for_dialect(cls, table_mapping: TableMapping, column_types: list[ColumnType], layer: Layer, _dialect: str):
        # TODO for now
        return QueryBuilder(table_mapping, column_types, layer)

    def __init__(
        self,
        table_mapping: TableMapping,
        column_types: list[ColumnType],
        layer: Layer,
    ):
        self._table_mapping = table_mapping
        self._column_types = column_types
        self._layer = layer

    @property
    def layer(self) -> Layer:
        return self._layer

    @property
    def column_types(self) -> list[ColumnType]:
        return self._column_types

    @property
    def table_mapping(self) -> TableMapping:
        return self._table_mapping

    @property
    def select_columns(self) -> set[str]:
        return self.table_mapping.get_select_columns(self._column_types, self._layer)

    @property
    def threshold_columns(self) -> set[str]:
        return self.table_mapping.get_threshold_columns(self._layer)

    @property
    def join_columns(self) -> set[str] | None:
        return self.table_mapping.get_join_columns(self._layer)

    @property
    def drop_columns(self) -> set[str]:
        return self._table_mapping.get_drop_columns(self._layer)

    @property
    def partition_column(self) -> set[str]:
        return self._table_mapping.get_partition_column(self._layer)

    @property
    def filter(self) -> str | None:
        return self._table_mapping.get_filter(self._layer)

    @property
    def aggregates(self) -> list[Aggregate] | None:
        return self.table_mapping.aggregates

    @property
    def user_transformations(self) -> dict[str, str]:
        return self._table_mapping.get_transformation_dict(self._layer)

    @property
    def default_transformations(self) -> dict[str, list[str]]:
        return {"default": ["TRIM($column$)", "COALESCE($column$, '_null_recon_')"]}

    @property
    def hash_transform(self) -> str:
        return "SHA2($column$, 256)"

    def _validate(self, field: set[str] | list[str] | None, message: str):
        if field is None:
            message = f"Exception for {self.table_mapping.target_name} target table in {self.layer} layer --> {message}"
            logger.error(message)
            raise InvalidInputException(message)

    def _apply_user_transformation(self, column: Column) -> Column:
        # don't transform already transformed columns
        if column.transform:
            return column
        user_transformations = self.user_transformations or {}
        transform = user_transformations.get(column.alias, None)
        if not transform:
            transform = user_transformations.get(column.name, None)
        return dataclasses.replace(column, transform=transform)

    def _apply_default_transformation(self, column: Column) -> Column:
        # don't transform already transformed columns
        if column.transform:
            return column
        # ensure we have transforms to apply for column type
        if not self.default_transformations:
            return column
        column_types: list[ColumnType] = list(filter(lambda col: col.column_name == column.name, self._column_types))
        if not column_types:
            return column
        data_type = column_types[0].data_type
        transformations = self.default_transformations.get(data_type, self.default_transformations.get("default", None))
        if not transformations:
            return column
        # apply transforms
        transform = column.name
        for transformation in transformations:
            transform = transformation.replace("$column$", transform)
        return dataclasses.replace(column, transform=transform)

    def build_count_query(self) -> str:
        return f"SELECT COUNT(1) AS count FROM :tbl WHERE {self.filter}"

    def build_hash_query(self, report_type: str) -> str:
        if report_type != 'row':
            self._validate(self.join_columns, f"Join Columns are compulsory for {report_type} type")

        join_columns: set[str] = self.join_columns or set()

        hash_cols: list[str] = list((join_columns | self.select_columns) - self.threshold_columns - self.drop_columns)
        hash_cols_with_alias = [
            Column(table=None, name=col, alias=self.table_mapping.get_layer_tgt_to_src_col_mapping(col, self.layer))
            for col in hash_cols
        ]
        # in case if we have column mapping, we need to sort the target columns
        # in the same order as source columns to get the same hash value
        hash_cols_with_alias_sorted = sorted(hash_cols_with_alias, key=lambda column: column.alias or column.name)
        hash_cols_with_user_transform = [self._apply_user_transformation(col) for col in hash_cols_with_alias_sorted]
        hash_cols_with_default_transform = [self._apply_default_transformation(col) for col in hash_cols_with_user_transform]
        hash_col_with_concat = f"CONCAT({', '.join(col.transform or col.name for col in hash_cols_with_default_transform)})"
        hash_col_with_hash = self.hash_transform.replace("$column$", hash_col_with_concat)
        hash_col_with_lower = f"LOWER({hash_col_with_hash}) AS hash_value_recon"

        key_cols = hash_cols if report_type == "row" else sorted(join_columns | self.partition_column)
        key_cols_with_alias = [
            Column(table=None, name=col, alias=self.table_mapping.get_layer_tgt_to_src_col_mapping(col, self.layer))
            for col in key_cols
        ]
        key_cols_with_transform = [self._apply_user_transformation(col) for col in key_cols_with_alias]

        columns_to_select = [hash_col_with_lower] + [col.sql() for col in key_cols_with_transform]
        sql = f"SELECT {', '.join(columns_to_select)} FROM :tbl" + (f" WHERE {self.filter}" if self.filter else "")
        logger.info(f"Hash Query for {self.layer}: {sql}")
        return sql
