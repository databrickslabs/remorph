import json
import logging
from io import StringIO

from databricks.labs.remorph.helpers.execution_time import timeit
from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.constants import (
    ColumnTransformationType,
    Constants,
    SourceType,
)
from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    Schema,
    TableRecon,
    Tables,
    Transformation,
    TransformRuleMapping,
)

logger = logging.getLogger(__name__)


@timeit
def recon(recon_conf, conn_profile, source, report):
    logger.info(recon_conf)
    logger.info(conn_profile)
    logger.info(source)
    logger.info(report)

    with open(recon_conf, 'r', encoding="utf-8") as f:
        data = json.load(f)

    # Convert the JSON data to the TableRecon dataclass
    table_recon = TableRecon.from_dict(data)

    for tables_conf in table_recon.tables:
        reconcile = Reconciliation(source, report)
        reconcile.compare_schemas(tables_conf, "schema", "catalog")
        reconcile.compare_data(tables_conf, "schema", "catalog")


class Reconciliation:
    def __init__(self, source: DataSource, target: DataSource):
        self.source = source
        self.target = target

    def compare_schemas(self, table_conf: Tables, schema_name: str, catalog_name: str) -> bool:
        source_schema = self.source.get_schema(table_conf.source_name, schema_name, catalog_name)
        target_schema = self.target.get_schema(table_conf.target_name, schema_name, catalog_name)
        return source_schema == target_schema

    def compare_data(self, table_conf: Tables, schema_name: str, catalog_name: str) -> bool:
        source_query = ""  # implement query builder
        target_query = ""  # implement query builder
        source_data = self.source.read_data(table_conf.source_name, schema_name, catalog_name, source_query)
        target_data = self.target.read_data(table_conf.target_name, schema_name, catalog_name, target_query)
        print(source_data.printSchema())
        print(target_data.printSchema())

        # implement hash comparison
        # implement mismatch data
        # implement missing in source
        # implement missing in target
        # implement threshold comparison
        return False  # implement data comparison logic


def build_query(table_conf: Tables, schema: list[Schema], layer: str, source: str) -> str:
    schema_info = {getattr(v, "column_name"): v for v in schema}

    hash_columns, key_columns = _get_column_list(table_conf, schema, layer)
    col_transformation = generate_transformation_rule_mapping(hash_columns, schema_info, table_conf, source, layer)

    hash_columns_expr = [
        TransformRuleMapping.get_column_expression_without_alias(trans) for trans in col_transformation
    ]

    hash_expr = generate_hash_algorithm(source, hash_columns_expr)

    key_column_expr = [
        TransformRuleMapping.get_column_expression_with_alias(trans)
        for trans in col_transformation
        if trans.column_name in key_columns
    ]

    table_name = table_conf.source_name if layer == "source" else table_conf.target_name

    query_filter = getattr(table_conf.filters, layer) if table_conf.filters else " 1 = 1"

    # construct select query
    select_query = _construct_hash_query(table_name, query_filter, hash_expr, key_column_expr)

    return select_query


def generate_transformation_rule_mapping(columns, schema, table_conf, source, layer):
    transformations_dict = table_conf.list_to_dict(Transformation, "column_name")
    column_mapping_dict = table_conf.list_to_dict(ColumnMapping, "target_name")

    transformation_rule_mapping = []
    for column in columns:
        if column in transformations_dict.keys():
            transformation = getattr(transformations_dict.get(column), layer)
        else:
            column_data_type = schema.get(column).data_type
            transformation = _get_default_transformation(source, column_data_type).format(column)

        if column in column_mapping_dict.keys():
            column_alias = column_mapping_dict.get(column).source_name
        else:
            column_alias = column

        transformation_rule_mapping.append(TransformRuleMapping(column, transformation, column_alias))

    return transformation_rule_mapping


def _get_column_list(table_conf, schema, layer):
    if layer == "source":
        join_columns = {col.source_name for col in table_conf.join_columns}
    else:
        join_columns = {col.target_name for col in table_conf.join_columns}

    if table_conf.select_columns is None:
        select_columns = {sch.column_name for sch in schema}
    else:
        select_columns = set(table_conf.select_columns)

    if table_conf.jdbc_reader_options:
        partition_column = {table_conf.jdbc_reader_options.partition_column}
    else:
        partition_column = set()

    # Combine all column names
    all_columns = join_columns | select_columns | partition_column

    # Remove threshold and drop columns
    threshold_columns = {thresh.column_name for thresh in table_conf.thresholds or []}
    drop_columns = set(table_conf.drop_columns or [])
    hash_columns = all_columns - threshold_columns - drop_columns
    key_columns = join_columns | partition_column

    return hash_columns, key_columns


def _get_default_transformation(source, data_type):
    match source:
        case "oracle":
            return oracle_datatype_mapper.get(data_type, ColumnTransformationType.ORACLE_DEFAULT.value)
        case "snowflake":
            return snowflake_datatype_mapper.get(data_type, ColumnTransformationType.SNOWFLAKE_DEFAULT.value)
        case "databricks":
            return databricks_datatype_mapper.get(data_type, ColumnTransformationType.DATABRICKS_DEFAULT.value)
        case _:
            msg = f"Unsupported source type --> {source}"
            raise ValueError(msg)


def generate_hash_algorithm(source: str, list_expr: list[str]) -> str:
    if source in {SourceType.DATABRICKS.value, SourceType.SNOWFLAKE.value}:
        hash_expr = "concat(" + ", ".join(list_expr) + ")"
    else:
        hash_expr = " || ".join(list_expr)

    return (Constants.hash_algorithm_mapping.get(source.lower()).get("source")).format(hash_expr)


def _construct_hash_query(table_name, query_filter, hash_expr, key_column_expr):
    sql_query = StringIO()
    sql_query.write(f"select {hash_expr} as {Constants.hash_column_name}, ")

    # add join column
    sql_query.write(",".join(key_column_expr))
    sql_query.write(f" from {table_name} where {query_filter}")

    select_query = sql_query.getvalue()
    sql_query.close()
    return select_query


oracle_datatype_mapper = {
    "date": "coalesce(trim(to_char({},'YYYY-MM-DD')),'')",
}
snowflake_datatype_mapper = {}
databricks_datatype_mapper = {}
