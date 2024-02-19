from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.labs.remorph.reconcile.query_builder.databricks_query_builder import DatabricksQueryBuilder
from databricks.labs.remorph.reconcile.query_builder.oracle_query_builder import OracleQueryBuilder
from databricks.labs.remorph.reconcile.recon_config import Tables, Schema


class QueryBuilderAdapterFactory:

    @staticmethod
    def generate_src_query(source_type: str, table_conf: Tables, schema: list[Schema]):
        layer = "source"
        match source_type.lower():
            case SourceType.ORACLE.value:
                return OracleQueryBuilder(layer, table_conf, schema)
            case SourceType.DATABRICKS.value:
                return DatabricksQueryBuilder(layer, table_conf, schema)
            case _:
                msg = f"Unsupported source type --> {source_type}"
                raise ValueError(msg)

    @staticmethod
    def generate_tgt_query(table_conf, schema: list[Schema]):
        return DatabricksQueryBuilder("target", table_conf, schema)
