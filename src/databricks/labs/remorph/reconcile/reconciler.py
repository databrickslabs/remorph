from typing import Tuple

from databricks.labs.remorph.reconcile.compare import capture_mismatch_data_and_columns, reconcile_data
from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.constants import Layer
from databricks.labs.remorph.reconcile.query_builder.hash_query import HashQueryBuilder
from databricks.labs.remorph.reconcile.query_builder.sampling_query import SamplingQueryBuilder
from databricks.labs.remorph.reconcile.recon_config import Table, Schema, ReconcileOutput


class Reconciler:

    def __init__(self, source: DataSource, target: DataSource, table_conf: Table, report_type: str):
        self._source = source
        self._target = target
        self._table_conf = table_conf
        self._source_table = self._table_conf.source_name
        self._target_table = self._table_conf.target_name
        self._report_type = report_type

    def reconcile_data(self):
        src_schema, tgt_schema = self._extract_schema()
        self._execute_data_reconcile(src_schema, tgt_schema)

    def reconcile_schema(self):
        src_schema, tgt_schema = self._extract_schema()
        raise NotImplementedError

    def _extract_schema(self) -> Tuple[list[Schema], list[Schema]]:
        src_schema = self._source.get_schema(table=self._source_table)
        tgt_schema = self._target.get_schema(table=self._target_table)

        return src_schema, tgt_schema

    def _execute_data_reconcile(self, src_schema: list[Schema], tgt_schema: list[Schema]):
        reconcile_output = self._get_reconcile_output(src_schema, tgt_schema)
        return self._get_sample_data(src_schema, tgt_schema, reconcile_output)

    def _get_reconcile_output(self, src_schema, tgt_schema):
        src_query = HashQueryBuilder(self._table_conf, src_schema, Layer.SOURCE.value,
                                     self._source.engine).build_query()
        tgt_query = HashQueryBuilder(self._table_conf, tgt_schema, Layer.TARGET.value,
                                     self._target.engine).build_query()

        src_data = self._source.read_data(query=src_query, options=self._table_conf.jdbc_reader_options)
        tgt_data = self._target.read_data(query=tgt_query, options=self._table_conf.jdbc_reader_options)

        return reconcile_data(source=src_data, target=tgt_data, key_columns=self._table_conf.join_columns,
                              report_type=self._report_type)

    def _get_sample_data(self, src_schema: list[Schema], tgt_schema: list[Schema], reconcile_output):
        src_sampler = SamplingQueryBuilder(self._table_conf, src_schema, Layer.SOURCE.value, self._source.engine)
        tgt_sampler = SamplingQueryBuilder(self._table_conf, tgt_schema, Layer.TARGET.value, self._target.engine)
        src_mismatch_sample_query = src_sampler.build_query(reconcile_output.mismatch)
        tgt_mismatch_sample_query = tgt_sampler.build_query(reconcile_output.mismatch)

        src_data = self._source.read_data(query=src_mismatch_sample_query, options=self._table_conf.jdbc_reader_options)
        tgt_data = self._target.read_data(query=tgt_mismatch_sample_query, options=self._table_conf.jdbc_reader_options)

        mismatch_data = capture_mismatch_data_and_columns(source=src_data, target=tgt_data,
                                                          key_columns=self._table_conf.join_columns)
        missing_in_src_sample_query = tgt_sampler.build_query(reconcile_output.missing_in_src)
        missing_in_tgt_sample_query = src_sampler.build_query(reconcile_output.missing_in_tgt)

        return ReconcileOutput(mismatch=mismatch_data,
                               missing_in_src=missing_in_src_sample_query,
                               missing_in_tgt=missing_in_tgt_sample_query)
