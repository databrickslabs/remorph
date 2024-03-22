from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    Schema,
    Table,
    Transformation,
)


class QueryConfig:
    def __init__(self, table_conf: Table, schema: list[Schema], layer: str, db_type: str):
        self.table_conf = table_conf
        self.schema = schema
        self.layer = layer
        self.db_type = db_type
        self.schema_dict = {v.column_name: v for v in schema}
        self.tgt_column_mapping = table_conf.list_to_dict(ColumnMapping, "target_name")
        self.src_column_mapping = table_conf.list_to_dict(ColumnMapping, "source_name")
        self.transformations_dict = table_conf.list_to_dict(Transformation, "column_name")

    def get_threshold_columns(self):
        return {thresh.column_name for thresh in self.table_conf.thresholds or []}

    def get_join_columns(self):
        if self.table_conf.join_columns is None:
            return set()
        return set(self.table_conf.join_columns)

    def get_select_columns(self):
        if self.table_conf.select_columns is None:
            columns = {sch.column_name for sch in self.schema}
            return columns if self.layer == "source" else self.get_mapped_columns(self.tgt_column_mapping, columns)
        return set(self.table_conf.select_columns)

    def get_partition_column(self):
        if self.table_conf.jdbc_reader_options and self.layer == "source":
            return {self.table_conf.jdbc_reader_options.partition_column}
        return set()

    def get_drop_columns(self):
        if self.table_conf.drop_columns is None:
            return set()
        return set(self.table_conf.drop_columns)

    def get_table_name(self):
        table_name = self.table_conf.source_name if self.layer == "source" else self.table_conf.target_name
        if self.db_type == SourceType.ORACLE.value:
            return "{{schema_name}}.{table_name}".format(  # pylint: disable=consider-using-f-string
                table_name=table_name
            )
        return "{{catalog_name}}.{{schema_name}}.{table_name}".format(  # pylint: disable=consider-using-f-string
            table_name=table_name
        )

    def get_filter(self):
        if self.table_conf.filters is None:
            return " 1 = 1 "
        if self.layer == "source":
            return self.table_conf.filters.source
        return self.table_conf.filters.target

    @staticmethod
    def get_mapped_columns(column_mapping: dict, columns: set[str]) -> set[str]:
        select_columns = set()
        for column in columns:
            select_columns.add(
                column_mapping.get(column, ColumnMapping(source_name=column, target_name='')).source_name
            )
        return select_columns
