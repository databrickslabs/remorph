from __future__ import annotations

from dataclasses import dataclass

from databricks.labs.remorph.reconcile.constants import Constants, SourceType
from databricks.labs.remorph.reconcile.recon_config import TransformRuleMapping, Tables, Schema, Transformation, \
    ColumnMapping
from databricks.labs.remorph.helpers.list_utils import filter_list


@dataclass
class QueryConfig:
    table_transform: list[TransformRuleMapping]

    @classmethod
    def get_comparison_columns(cls, table_conf: Tables, schema: list[Schema]):
        cols_to_be_compared = []
        # get threshold columns
        if table_conf.thresholds:
            threshold_cols = [threshold.column_name for threshold in table_conf.thresholds]
        else:
            threshold_cols = []
        # explicit select columns
        if table_conf.select_columns:
            sel_cols = filter_list(input_list=table_conf.select_columns, remove_list=threshold_cols)
            join_cols = [join.source_name for join in table_conf.join_columns]
            cols_to_be_compared += (sel_cols + join_cols)
        # complete schema is considered here
        else:
            sel_cols = [schema.column_name for schema in schema]
            drop_cols = table_conf.drop_columns
            if drop_cols is None:
                drop_cols = []
            final_sel_cols = filter_list(input_list=sel_cols, remove_list=drop_cols + threshold_cols)
            cols_to_be_compared += final_sel_cols

        return cols_to_be_compared

    @classmethod
    def get_key_columns(cls, table_conf: Tables):
        key_columns = []
        if table_conf.join_columns:
            join_columns = [join.source_name for join in table_conf.join_columns]
            partition_column = table_conf.jdbc_reader_options.partition_column
            if partition_column not in join_columns:
                join_columns.append(partition_column)
            key_columns += join_columns

        return key_columns

    @classmethod
    def add_custom_transformations(cls, table_conf: Tables, cols: list[str], layer: str):
        transformation_dict = table_conf.list_to_dict(Transformation, "column_name")
        alias_mapping_dict = table_conf.list_to_dict(ColumnMapping, "source_name")

        table_transform = []
        if transformation_dict is not None:
            for col in cols:
                transformation_mapping = TransformRuleMapping(col, None, None)
                if alias_mapping_dict is not None and col in alias_mapping_dict.keys():
                    transformation_mapping.alias_name = alias_mapping_dict.get(col).target_name
                if transformation_dict is not None and col in transformation_dict.keys():
                    match layer:
                        case "source":
                            transformation_mapping.transformation = transformation_dict.get(col).source

                        case "target":
                            transformation_mapping.transformation = transformation_dict.get(col).target
                        case _:
                            print("Invalid layer value only source or target is allowed")
                else:
                    transformation_mapping = TransformRuleMapping(col, None, None)
                table_transform.append(transformation_mapping)

        return cls(table_transform)

    @classmethod
    def generate_hash_algorithm(cls, source_type: str,
                                list_expr: list[str]) -> str:
        if source_type == SourceType.DATABRICKS.value or source_type == SourceType.SNOWFLAKE.value:
            hash_expr = "concat(" + ", ".join(list_expr) + ")"
            return (Constants.hash_algorithm_mapping.get(source_type.lower()).get("source")).format(
                hash_expr)
        else:
            hash_expr = " || ".join(list_expr)
            return (Constants.hash_algorithm_mapping.get(source_type.lower()).get("source")).format(
                hash_expr)

    def list_to_dict(self, cls: any, key: str) -> dict[str, any]:
        for _, value in self.__dict__.items():
            if isinstance(value, list):
                if all(isinstance(x, cls) for x in value):
                    return {getattr(v, key): v for v in value}
            else:
                pass
