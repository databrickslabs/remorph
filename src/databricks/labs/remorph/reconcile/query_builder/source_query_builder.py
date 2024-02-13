from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.labs.remorph.reconcile.query_builder.oracle_query_builder import OracleQueryBuildAdapter
from databricks.labs.remorph.reconcile.query_builder.source_query_build_adapter import SourceQueryBuildAdapter
from databricks.labs.remorph.reconcile.recon_config import Tables, Schema


class SourceQueryBuilderFactory:
    @staticmethod
    def create(source_type: str, table_conf: Tables, schema: list[Schema]) -> SourceQueryBuildAdapter:

        match source_type.lower():
            case SourceType.ORACLE.value:
                return OracleQueryBuildAdapter(source_type, table_conf, schema)
            case _:
                msg = f"Unsupported source type --> {source_type}"
                raise ValueError(msg)
