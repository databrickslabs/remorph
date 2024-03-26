from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    Schema,
    Table,
    Transformation,
)


class QueryConfig:
    def __init__(self, table_conf: Table, schema: list[Schema], layer: str, source: str):
        self._table_conf = table_conf
        self._schema = schema
        self._layer = layer
        self._source = source

    @property
    def source(self):
        return self._source

    @property
    def layer(self):
        return self._layer

    @property
    def schema_dict(self):
        return {v.column_name: v for v in self._schema}

    @property
    def tgt_col_mapping(self):
        return self._table_conf.list_to_dict(ColumnMapping, "target_name")

    @property
    def src_col_mapping(self):
        return self._table_conf.list_to_dict(ColumnMapping, "source_name")

    @property
    def transform_dict(self):
        return self._table_conf.list_to_dict(Transformation, "column_name")

    @property
    def threshold_columns(self) -> set[str]:
        return {thresh.column_name for thresh in self._table_conf.thresholds or []}

    @property
    def join_columns(self) -> set[str]:
        if self._table_conf.join_columns is None:
            return set()
        return set(self._table_conf.join_columns)

    @property
    def select_columns(self) -> set[str]:
        if self._table_conf.select_columns is None:
            cols = {sch.column_name for sch in self._schema}
            return cols if self._layer == "source" else self.get_mapped_columns(self.tgt_col_mapping, cols)
        return set(self._table_conf.select_columns)

    @property
    def partition_column(self) -> set[str]:
        if self._table_conf.jdbc_reader_options and self._layer == "source":
            return {self._table_conf.jdbc_reader_options.partition_column}
        return set()

    @property
    def drop_columns(self) -> set[str]:
        if self._table_conf.drop_columns is None:
            return set()
        return set(self._table_conf.drop_columns)

    @property
    def table_name(self) -> str:
        table_name = self._table_conf.source_name if self._layer == "source" else self._table_conf.target_name
        if self._source == SourceType.ORACLE.value:
            return f"{{schema_name}}.{table_name}"
        return f"{{catalog_name}}.{{schema_name}}.{table_name}"

    @property
    def filter(self) -> str:
        if self._table_conf.filters is None:
            return " 1 = 1 "
        if self._layer == "source":
            return self._table_conf.filters.source
        return self._table_conf.filters.target

    @staticmethod
    def get_mapped_columns(col_mapping: dict[str, ColumnMapping], cols: set[str]) -> set[str]:
        select_columns = set()
        for col in cols:
            select_columns.add(col_mapping.get(col, ColumnMapping(source_name=col, target_name='')).source_name)
        return select_columns
