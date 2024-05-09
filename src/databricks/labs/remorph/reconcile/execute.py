import logging
from functools import cached_property
from pathlib import Path

from databricks.labs.blueprint.installation import Installation
from databricks.labs.remorph.config import DatabaseConfig, TableRecon
from databricks.labs.remorph.reconcile.compare import (
    capture_mismatch_data_and_columns,
    reconcile_data,
)
from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.constants import Layer
from databricks.labs.remorph.reconcile.query_builder.hash_query import HashQueryBuilder
from databricks.labs.remorph.reconcile.query_builder.sampling_query import (
    SamplingQueryBuilder,
)
from databricks.labs.remorph.reconcile.recon_config import ReconcileOutput, Table

logger = logging.getLogger(__name__)


def recon(recon_conf, conn_profile, source, report):
    logger.info(conn_profile)
    logger.info(source)
    logger.info(report)

    table_recon = get_config(Path(recon_conf))


class Reconciliation:
    def __init__(
        self,
        source: DataSource,
        target: DataSource,
        table_conf: Table,
        database_config: DatabaseConfig,
        report_type: str,
    ):
        self._source = source
        self._target = target
        self._table_conf = table_conf
        self._report_type = report_type
        self._source_catalog = database_config.source_catalog
        self._source_schema = database_config.source_schema
        self._target_catalog = database_config.target_catalog
        self._target_schema = database_config.target_schema

    @cached_property
    def src_schema(self):
        return self._source.get_schema(
            catalog=self._source_catalog, schema=self._source_schema, table=self._table_conf.source_name
        )

    @cached_property
    def tgt_schema(self):
        return self._target.get_schema(
            catalog=self._target_catalog, schema=self._target_schema, table=self._table_conf.target_name
        )

    @cached_property
    def src_hash_query(self):
        return HashQueryBuilder(
            self._table_conf, self.src_schema, Layer.SOURCE.value, self._source.engine
        ).build_query()

    @cached_property
    def tgt_hash_query(self):
        return HashQueryBuilder(
            self._table_conf, self.tgt_schema, Layer.TARGET.value, self._target.engine
        ).build_query()

    @cached_property
    def src_sampler(self):
        return SamplingQueryBuilder(self._table_conf, self.src_schema, Layer.SOURCE.value, self._source.engine)

    @cached_property
    def tgt_sampler(self):
        return SamplingQueryBuilder(self._table_conf, self.tgt_schema, Layer.TARGET.value, self._target.engine)

    def reconcile_data(self):
        reconcile_output = self._get_reconcile_output()
        return self._get_sample_data(reconcile_output)

    def reconcile_schema(self):
        raise NotImplementedError

    def _get_reconcile_output(self):
        src_data = self._source.read_data(
            catalog=self._source_catalog,
            schema=self._source_schema,
            query=self.src_hash_query,
            options=self._table_conf.jdbc_reader_options,
        )
        tgt_data = self._target.read_data(
            catalog=self._target_catalog,
            schema=self._target_schema,
            query=self.tgt_hash_query,
            options=self._table_conf.jdbc_reader_options,
        )

        return reconcile_data(
            source=src_data, target=tgt_data, key_columns=self._table_conf.join_columns, report_type=self._report_type
        )

    def _get_sample_data(self, reconcile_output):
        src_mismatch_sample_query = self.src_sampler.build_query(reconcile_output.mismatch)
        tgt_mismatch_sample_query = self.tgt_sampler.build_query(reconcile_output.mismatch)

        src_data = self._source.read_data(
            catalog=self._source_catalog,
            schema=self._source_schema,
            query=src_mismatch_sample_query,
            options=self._table_conf.jdbc_reader_options,
        )
        tgt_data = self._target.read_data(
            catalog=self._target_catalog,
            schema=self._target_schema,
            query=tgt_mismatch_sample_query,
            options=self._table_conf.jdbc_reader_options,
        )

        mismatch_data = capture_mismatch_data_and_columns(
            source=src_data, target=tgt_data, key_columns=self._table_conf.join_columns
        )
        missing_in_src_sample_query = self.tgt_sampler.build_query(reconcile_output.missing_in_src)
        missing_in_tgt_sample_query = self.src_sampler.build_query(reconcile_output.missing_in_tgt)

        return ReconcileOutput(
            mismatch=mismatch_data,
            missing_in_src=missing_in_src_sample_query,
            missing_in_tgt=missing_in_tgt_sample_query,
        )


def get_config(file: Path):
    # Convert the JSON data to the TableRecon dataclass
    return Installation.load_local(type_ref=TableRecon, file=file)
