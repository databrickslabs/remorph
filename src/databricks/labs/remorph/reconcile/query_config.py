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
        self._schema_dict = {v.column_name: v for v in schema}
        self._tgt_col_mapping = table_conf.list_to_dict(ColumnMapping, "target_name")
        self._src_col_mapping = table_conf.list_to_dict(ColumnMapping, "source_name")
        self._transform_dict = table_conf.list_to_dict(Transformation, "column_name")

    def get_table_conf(self):
        return self._table_conf

    def get_schema(self):
        return self._schema

    def get_source(self):
        return self._source

    def get_layer(self):
        return self._layer

    def get_schema_dict(self):
        return self._schema_dict

    def get_tgt_col_mapping(self):
        return self._tgt_col_mapping

    def get_src_col_mapping(self):
        return self._src_col_mapping

    def get_transform_dict(self):
        return self._transform_dict

    def get_threshold_columns(self) -> set[str]:
        return {thresh.column_name for thresh in self._table_conf.thresholds or []}

    def get_join_columns(self) -> set[str]:
        if self._table_conf.join_columns is None:
            return set()
        return set(self._table_conf.join_columns)

    def get_select_columns(self) -> set[str]:
        if self._table_conf.select_columns is None:
            cols = {sch.column_name for sch in self._schema}
            return cols if self._layer == "source" else self.get_mapped_columns(self._tgt_col_mapping, cols)
        return set(self._table_conf.select_columns)

    def get_partition_column(self) -> set[str]:
        if self._table_conf.jdbc_reader_options and self._layer == "source":
            return {self._table_conf.jdbc_reader_options.partition_column}
        return set()

    def get_drop_columns(self) -> set[str]:
        if self._table_conf.drop_columns is None:
            return set()
        return set(self._table_conf.drop_columns)

    def get_table_name(self) -> str:
        table_name = self._table_conf.source_name if self._layer == "source" else self._table_conf.target_name
        if self._source == SourceType.ORACLE.value:
            return f"{{schema_name}}.{table_name}"
        return f"{{catalog_name}}.{{schema_name}}.{table_name}"

    def get_filter(self) -> str:
        if self._table_conf.filters is None:
            return " 1 = 1 "
        if self._layer == "source":
            return self._table_conf.filters.source
        return self._table_conf.filters.target

    @staticmethod
    def get_mapped_columns(col_mapping: dict, cols: set[str]) -> set[str]:
        select_columns = set()
        for col in cols:
            select_columns.add(col_mapping.get(col, ColumnMapping(source_name=col, target_name='')).source_name)
        return select_columns
