from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.labs.remorph.reconcile.query_builder.oracle_query_builder import OracleQueryBuilder
from databricks.labs.remorph.reconcile.recon_config import Tables, Schema


class QueryBuilderAdapterFactory:

    @staticmethod
    def generate_query(source_type: str, layer: str, table_conf: Tables, schema: list[Schema]):
        match source_type.lower():
            case SourceType.ORACLE.value:
                return OracleQueryBuilder(layer, table_conf, schema)
            case _:
                msg = f"Unsupported source type --> {source_type}"
                raise ValueError(msg)
