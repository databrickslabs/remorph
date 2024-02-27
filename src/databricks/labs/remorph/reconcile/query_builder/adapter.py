from databricks.labs.remorph.reconcile.constants import Layer, SourceType
from databricks.labs.remorph.reconcile.query_builder.oracle import OracleQueryBuilder
from databricks.labs.remorph.reconcile.recon_config import Schema, Tables


class QueryBuilderAdapterFactory:

    # TODO add tgt query create method and add other sources
    @staticmethod
    def create(source_type: str, table_conf: Tables, schema: list[Schema]):
        layer = Layer.SOURCE.value
        match source_type.lower():
            case SourceType.ORACLE.value:
                return OracleQueryBuilder(source_type, layer, table_conf, schema)
            case _:
                msg = f"Unsupported source type --> {source_type}"
                raise ValueError(msg)
