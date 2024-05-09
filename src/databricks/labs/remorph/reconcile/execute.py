import logging
from pathlib import Path

from sqlglot import Dialects

from databricks.connect import DatabricksSession
from databricks.labs.blueprint.installation import Installation
from databricks.labs.remorph.config import SQLGLOT_DIALECTS, DatabaseConfig, TableRecon
from databricks.labs.remorph.reconcile.compare import (
    capture_mismatch_data_and_columns,
    reconcile_data,
)
from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.connectors.databricks import DatabricksDataSource
from databricks.labs.remorph.reconcile.connectors.source_adapter import (
    DataSourceAdapter,
)
from databricks.labs.remorph.reconcile.constants import Layer
from databricks.labs.remorph.reconcile.query_builder.hash_query import HashQueryBuilder
from databricks.labs.remorph.reconcile.query_builder.sampling_query import (
    SamplingQueryBuilder,
)
from databricks.labs.remorph.reconcile.recon_config import (
    ReconcileOutput,
    Schema,
    Table,
)
from databricks.labs.remorph.reconcile.schema_compare import SchemaCompare
from databricks.sdk import WorkspaceClient

logger = logging.getLogger(__name__)


def recon(recon_conf, ws: WorkspaceClient, source: Dialects, report):
    logger.info(source)
    logger.info(report)

    table_recon = get_config(Path(recon_conf))
    database_config = DatabaseConfig(
        source_catalog=table_recon.source_catalog,
        source_schema=table_recon.source_schema,
        target_catalog=table_recon.target_catalog,
        target_schema=table_recon.target_schema,
    )

    spark = DatabricksSession.builder.sdkConfig(ws.config).getOrCreate()

    source = DataSourceAdapter().create_adapter(engine=source, spark=spark, ws=ws, scope="")
    target = DatabricksDataSource(engine=SQLGLOT_DIALECTS.get("databricks"), spark=spark, ws=ws, scope="")
    schema_comparator = SchemaCompare(spark=spark)

    # initialise the Reconciliation
    reconciler = Reconciliation(source, target, database_config, report, schema_comparator)

    for table_conf in table_recon.tables:
        src_schema = source.get_schema(
            catalog=database_config.source_catalog, schema=database_config.source_schema, table=table_conf.source_name
        )
        tgt_schema = target.get_schema(
            catalog=database_config.target_catalog, schema=database_config.target_schema, table=table_conf.source_name
        )

        if report in {"data", "hash"}:
            reconciler.reconcile_data(table_conf=table_conf, src_schema=src_schema, tgt_schema=tgt_schema)
        elif report == "schema":
            reconciler.reconcile_schema(table_conf=table_conf, src_schema=src_schema, tgt_schema=tgt_schema)
        else:
            reconciler.reconcile_data(table_conf=table_conf, src_schema=src_schema, tgt_schema=tgt_schema)
            reconciler.reconcile_schema(table_conf=table_conf, src_schema=src_schema, tgt_schema=tgt_schema)


class Reconciliation:
    def __init__(
        self,
        source: DataSource,
        target: DataSource,
        database_config: DatabaseConfig,
        report_type: str,
        schema_comparator: SchemaCompare,
    ):
        self._source = source
        self._target = target
        self._report_type = report_type
        self._source_catalog = database_config.source_catalog
        self._source_schema = database_config.source_schema
        self._target_catalog = database_config.target_catalog
        self._target_schema = database_config.target_schema
        self._schema_comparator = schema_comparator

    def reconcile_data(self, table_conf: Table, src_schema: list[Schema], tgt_schema: list[Schema]):
        reconcile_output = self._get_reconcile_output(table_conf, src_schema, tgt_schema)
        return self._get_sample_data(table_conf, reconcile_output, src_schema, tgt_schema)

    def reconcile_schema(self, src_schema, tgt_schema, table_conf):
        return self._schema_comparator.compare(src_schema, tgt_schema, self._source.engine, table_conf)

    def _get_reconcile_output(self, table_conf, src_schema, tgt_schema):
        src_hash_query = HashQueryBuilder(table_conf, src_schema, Layer.SOURCE.value, self._source.engine).build_query()
        tgt_hash_query = HashQueryBuilder(table_conf, tgt_schema, Layer.TARGET.value, self._target.engine).build_query()
        src_data = self._source.read_data(
            catalog=self._source_catalog,
            schema=self._source_schema,
            query=src_hash_query,
            options=table_conf.jdbc_reader_options,
        )
        tgt_data = self._target.read_data(
            catalog=self._target_catalog,
            schema=self._target_schema,
            query=tgt_hash_query,
            options=table_conf.jdbc_reader_options,
        )

        return reconcile_data(
            source=src_data, target=tgt_data, key_columns=table_conf.join_columns, report_type=self._report_type
        )

    def _get_sample_data(self, table_conf, reconcile_output, src_schema, tgt_schema):
        src_sampler = SamplingQueryBuilder(table_conf, src_schema, Layer.SOURCE.value, self._source.engine)
        tgt_sampler = SamplingQueryBuilder(table_conf, tgt_schema, Layer.TARGET.value, self._target.engine)
        src_mismatch_sample_query = src_sampler.build_query(reconcile_output.mismatch)
        tgt_mismatch_sample_query = tgt_sampler.build_query(reconcile_output.mismatch)

        src_data = self._source.read_data(
            catalog=self._source_catalog,
            schema=self._source_schema,
            query=src_mismatch_sample_query,
            options=table_conf.jdbc_reader_options,
        )
        tgt_data = self._target.read_data(
            catalog=self._target_catalog,
            schema=self._target_schema,
            query=tgt_mismatch_sample_query,
            options=table_conf.jdbc_reader_options,
        )

        mismatch_data = capture_mismatch_data_and_columns(
            source=src_data, target=tgt_data, key_columns=table_conf.join_columns
        )
        missing_in_src_sample_query = tgt_sampler.build_query(reconcile_output.missing_in_src)
        missing_in_tgt_sample_query = src_sampler.build_query(reconcile_output.missing_in_tgt)

        return ReconcileOutput(
            mismatch=mismatch_data,
            missing_in_src=missing_in_src_sample_query,
            missing_in_tgt=missing_in_tgt_sample_query,
        )


def get_config(file: Path):
    # Convert the JSON data to the TableRecon dataclass
    return Installation.load_local(type_ref=TableRecon, file=file)
