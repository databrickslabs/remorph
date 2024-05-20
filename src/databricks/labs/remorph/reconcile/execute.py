import logging
from uuid import uuid4

from pyspark.sql import DataFrame, SparkSession
from sqlglot import Dialect

from databricks.labs.remorph.config import DatabaseConfig, TableRecon, get_dialect
from databricks.labs.remorph.reconcile.compare import (
    capture_mismatch_data_and_columns,
    reconcile_data,
)
from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
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


def recon(ws: WorkspaceClient, spark: SparkSession, table_recon: TableRecon, source_dialect: Dialect, report_type: str):
    logger.info(report_type)

    database_config = DatabaseConfig(
        source_catalog=table_recon.source_catalog,
        source_schema=table_recon.source_schema,
        target_catalog=table_recon.target_catalog,
        target_schema=table_recon.target_schema,
    )

    source, target = initialise_data_source(engine=source_dialect, spark=spark, ws=ws, secret_scope="secret_scope")
    schema_comparator = SchemaCompare(spark=spark)

    recon_id = str(uuid4())
    # initialise the Reconciliation
    reconciler = Reconciliation(source, target, database_config, report_type, schema_comparator, source_dialect)

    for table_conf in table_recon.tables:
        src_schema = source.get_schema(
            catalog=database_config.source_catalog, schema=database_config.source_schema, table=table_conf.source_name
        )
        tgt_schema = target.get_schema(
            catalog=database_config.target_catalog, schema=database_config.target_schema, table=table_conf.source_name
        )

        if report_type in {"data", "row"}:
            reconciler.reconcile_data(table_conf=table_conf, src_schema=src_schema, tgt_schema=tgt_schema)
        elif report_type == "schema":
            reconciler.reconcile_schema(table_conf=table_conf, src_schema=src_schema, tgt_schema=tgt_schema)
        elif report_type == "all":
            reconciler.reconcile_data(table_conf=table_conf, src_schema=src_schema, tgt_schema=tgt_schema)
            reconciler.reconcile_schema(table_conf=table_conf, src_schema=src_schema, tgt_schema=tgt_schema)

    return recon_id


def initialise_data_source(ws: WorkspaceClient, spark: SparkSession, engine: Dialect, secret_scope: str):
    source = DataSourceAdapter().create_adapter(engine=engine, spark=spark, ws=ws, secret_scope=secret_scope)
    target = DataSourceAdapter().create_adapter(
        engine=get_dialect("databricks"), spark=spark, ws=ws, secret_scope=secret_scope
    )

    return source, target


def _get_missing_data(reader, sampler, missing_df, catalog, schema, table_name: str) -> DataFrame:
    sample_query = sampler.build_query(missing_df)
    return reader.read_data(
        catalog=catalog,
        schema=schema,
        table=table_name,
        query=sample_query,
        options=None,
    )


class Reconciliation:
    def __init__(
        self,
        source: DataSource,
        target: DataSource,
        database_config: DatabaseConfig,
        report_type: str,
        schema_comparator: SchemaCompare,
        source_engine: Dialect,
    ):
        self._source = source
        self._target = target
        self._report_type = report_type
        self._source_catalog = database_config.source_catalog
        self._source_schema = database_config.source_schema
        self._target_catalog = database_config.target_catalog
        self._target_schema = database_config.target_schema
        self._schema_comparator = schema_comparator
        self._target_engine = get_dialect("databricks")
        self._source_engine = source_engine

    def reconcile_data(self, table_conf: Table, src_schema: list[Schema], tgt_schema: list[Schema]):
        reconcile_output = self._get_reconcile_output(table_conf, src_schema, tgt_schema)
        return self._get_sample_data(table_conf, reconcile_output, src_schema, tgt_schema)

    def reconcile_schema(self, src_schema: list[Schema], tgt_schema: list[Schema], table_conf: Table):
        return self._schema_comparator.compare(src_schema, tgt_schema, self._source_engine, table_conf)

    def _get_reconcile_output(self, table_conf, src_schema, tgt_schema):
        src_hash_query = HashQueryBuilder(table_conf, src_schema, Layer.SOURCE.value, self._source_engine).build_query()
        tgt_hash_query = HashQueryBuilder(table_conf, tgt_schema, Layer.TARGET.value, self._target_engine).build_query()
        src_data = self._source.read_data(
            catalog=self._source_catalog,
            schema=self._source_schema,
            table=table_conf.source_name,
            query=src_hash_query,
            options=table_conf.jdbc_reader_options,
        )
        tgt_data = self._target.read_data(
            catalog=self._target_catalog,
            schema=self._target_schema,
            table=table_conf.target_name,
            query=tgt_hash_query,
            options=table_conf.jdbc_reader_options,
        )

        return reconcile_data(
            source=src_data, target=tgt_data, key_columns=table_conf.join_columns, report_type=self._report_type
        )

    def _get_sample_data(self, table_conf, reconcile_output, src_schema, tgt_schema):
        mismatch = None
        missing_in_src = None
        missing_in_tgt = None

        if (
            reconcile_output.mismatch_count > 0
            or reconcile_output.missing_in_src_count > 0
            or reconcile_output.missing_in_tgt_count > 0
        ):
            src_sampler = SamplingQueryBuilder(table_conf, src_schema, Layer.SOURCE.value, self._source_engine)
            tgt_sampler = SamplingQueryBuilder(table_conf, tgt_schema, Layer.TARGET.value, self._target_engine)
            if reconcile_output.mismatch_count > 0:
                mismatch = self._get_mismatch_data(
                    src_sampler,
                    tgt_sampler,
                    reconcile_output.mismatch.mismatch_df,
                    table_conf.join_columns,
                    table_conf.source_name,
                    table_conf.target_name,
                )

            if reconcile_output.missing_in_src_count > 0:
                missing_in_src = _get_missing_data(
                    self._target,
                    tgt_sampler,
                    reconcile_output.missing_in_src,
                    self._target_catalog,
                    self._target_schema,
                    table_conf.target_name,
                )

            if reconcile_output.missing_in_tgt_count > 0:
                missing_in_tgt = _get_missing_data(
                    self._source,
                    src_sampler,
                    reconcile_output.missing_in_tgt,
                    self._source_catalog,
                    self._source_schema,
                    table_conf.source_name,
                )

        return ReconcileOutput(
            mismatch=mismatch,
            mismatch_count=reconcile_output.mismatch_count,
            missing_in_src_count=reconcile_output.missing_in_src_count,
            missing_in_tgt_count=reconcile_output.missing_in_tgt_count,
            missing_in_src=missing_in_src,
            missing_in_tgt=missing_in_tgt,
        )

    def _get_mismatch_data(self, src_sampler, tgt_sampler, mismatch, key_columns, src_table: str, tgt_table: str):
        src_mismatch_sample_query = src_sampler.build_query(mismatch)
        tgt_mismatch_sample_query = tgt_sampler.build_query(mismatch)

        src_data = self._source.read_data(
            catalog=self._source_catalog,
            schema=self._source_schema,
            table=src_table,
            query=src_mismatch_sample_query,
            options=None,
        )
        tgt_data = self._target.read_data(
            catalog=self._target_catalog,
            schema=self._target_schema,
            table=tgt_table,
            query=tgt_mismatch_sample_query,
            options=None,
        )

        return capture_mismatch_data_and_columns(source=src_data, target=tgt_data, key_columns=key_columns)
