from abc import ABC

from databricks.labs.remorph.reconcile.connectors.databricks import DatabricksDataSource
from databricks.labs.remorph.reconcile.connectors.oracle import OracleDataSource
from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeDataSource
from databricks.labs.remorph.reconcile.constants import (
    ColumnTransformationType,
    SourceType,
)
from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    Schema,
    Table,
    Transformation,
    TransformRuleMapping,
)


class QueryBuilder(ABC):
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
    def table_conf(self):
        return self._table_conf

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
    def select_columns(self) -> set[str]:
        if self._table_conf.select_columns is None:
            cols = {sch.column_name for sch in self._schema}
            return cols if self._layer == "source" else self._get_mapped_columns(self.tgt_col_mapping, cols)
        return set(self._table_conf.select_columns)

    @property
    def table_name(self) -> str:
        table_name = self._table_conf.source_name if self._layer == "source" else self._table_conf.target_name
        if self._source == SourceType.ORACLE.value:
            return f"{{schema_name}}.{table_name}"
        return f"{{catalog_name}}.{{schema_name}}.{table_name}"

    @staticmethod
    def _get_mapped_columns(col_mapping: dict[str, ColumnMapping], cols: set[str]) -> set[str]:
        select_columns = set()
        for col in cols:
            select_columns.add(col_mapping.get(col, ColumnMapping(source_name=col, target_name='')).source_name)
        return select_columns

    @staticmethod
    def _get_default_transformation_expr(data_source: str, data_type: str) -> str:
        if data_source == SourceType.ORACLE.value:
            return OracleDataSource.oracle_datatype_mapper.get(data_type, ColumnTransformationType.ORACLE_DEFAULT.value)
        if data_source == SourceType.SNOWFLAKE.value:
            return SnowflakeDataSource.snowflake_datatype_mapper.get(
                data_type, ColumnTransformationType.SNOWFLAKE_DEFAULT.value
            )
        if data_source == SourceType.DATABRICKS.value:
            return DatabricksDataSource.databricks_datatype_mapper.get(
                data_type, ColumnTransformationType.DATABRICKS_DEFAULT.value
            )
        msg = f"Unsupported source type --> {data_source}"
        raise ValueError(msg)

    @staticmethod
    def _get_layer_transform(transform_dict: dict[str, Transformation], col: str, layer: str) -> str:
        return transform_dict.get(col).source if layer == "source" else transform_dict.get(col).target

    @staticmethod
    def _get_column_expr(func, col_transform: list[TransformRuleMapping]):
        return [func(transform) for transform in col_transform]

    @staticmethod
    def _get_column_map(col, col_mapping: dict[str, ColumnMapping]) -> str:
        return col_mapping.get(col, ColumnMapping(source_name='', target_name=col)).target_name

    @staticmethod
    def _get_column_alias(layer: str, col: str, col_mapping: dict[str, ColumnMapping]) -> tuple[str, str]:
        if col_mapping and col in col_mapping.keys() and layer == "target":
            col_alias = col_mapping.get(col).source_name
            col_origin = col_mapping.get(col).target_name
        else:
            col_alias = col
            col_origin = col

        return col_origin, col_alias

    def _generate_transform_rule_mapping(self, cols: list[str]) -> list[TransformRuleMapping]:
        # compute custom transformation
        if self.transform_dict:
            cols_with_transform = [col for col in cols if col in self.transform_dict.keys()]
            custom_transform = self._get_custom_transformation(
                cols_with_transform, self.transform_dict, self.src_col_mapping
            )
        else:
            custom_transform = []

        # compute default transformation
        cols_without_transform = [col for col in cols if col not in self.transform_dict.keys()]
        default_transform = self._get_default_transformation(
            cols_without_transform, self.src_col_mapping, self.schema_dict
        )

        transform_rule_mapping = custom_transform + default_transform

        return transform_rule_mapping

    def _get_default_transformation(
        self, cols: list[str], col_mapping: dict[str, ColumnMapping], schema: dict[str, Schema]
    ) -> list[TransformRuleMapping]:
        transform_rule_mapping = []
        for col in cols:
            col_origin = col if self.layer == "source" else self._get_column_map(col, col_mapping)
            col_data_type = schema.get(col_origin).data_type
            transform = self._get_default_transformation_expr(self.source, col_data_type).format(col_origin)

            col_origin, col_alias = self._get_column_alias(self.layer, col, col_mapping)

            transform_rule_mapping.append(TransformRuleMapping(col_origin, transform, col_alias))

        return transform_rule_mapping

    def _get_custom_transformation(
        self, cols: list[str], transform_dict: dict[str, Transformation], col_mapping: dict[str, ColumnMapping]
    ) -> list[TransformRuleMapping]:
        transform_rule_mapping = []
        for col in cols:
            if col in transform_dict.keys():
                transform = self._get_layer_transform(transform_dict, col, self.layer)
            else:
                transform = None

            col_origin, col_alias = self._get_column_alias(self.layer, col, col_mapping)

            transform_rule_mapping.append(TransformRuleMapping(col_origin, transform, col_alias))

        return transform_rule_mapping
