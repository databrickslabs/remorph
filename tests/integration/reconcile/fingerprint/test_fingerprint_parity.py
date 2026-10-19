"""Integration parity tests for the fingerprint pre-check."""

import dataclasses
import logging

import pytest
from databricks.sdk.service.catalog import SchemaInfo

from databricks.labs.lakebridge.config import ReconcileConfig, TableRecon
from databricks.labs.lakebridge.reconcile.fingerprint.metadata import INELIGIBLE_FLAG_DISABLED
from databricks.labs.lakebridge.reconcile.normalize_recon_config_service import NormalizeReconConfigService
from databricks.labs.lakebridge.reconcile.recon_config import Table
from databricks.labs.lakebridge.reconcile.recon_output_config import DataReconcileOutput
from databricks.labs.lakebridge.reconcile.trigger_recon_service import TriggerReconService

logger = logging.getLogger(__name__)


def _run_recon_one(ws, spark, recon_config: ReconcileConfig, table_conf: Table, *, fingerprint: bool):
    cfg = dataclasses.replace(recon_config, reconcile_optimizer=fingerprint)
    reconciler, _capture = TriggerReconService.create_recon_dependencies(ws, spark, cfg)
    normalized = NormalizeReconConfigService(reconciler.source, reconciler.target).normalize_recon_table_config(
        table_conf
    )
    _schema_out, data_out, _dur, fp_meta = TriggerReconService.do_recon_one(
        reconciler, cfg, normalized, recon_id="fingerprint-parity-test"
    )
    return data_out, fp_meta


def _assert_counts_equal(fp_out: DataReconcileOutput, legacy_out: DataReconcileOutput) -> None:
    assert (
        fp_out.mismatch_count == legacy_out.mismatch_count
    ), f"mismatch_count: fingerprint={fp_out.mismatch_count} legacy={legacy_out.mismatch_count}"
    assert (
        fp_out.missing_in_src_count == legacy_out.missing_in_src_count
    ), f"missing_in_src_count: fingerprint={fp_out.missing_in_src_count} legacy={legacy_out.missing_in_src_count}"
    assert (
        fp_out.missing_in_tgt_count == legacy_out.missing_in_tgt_count
    ), f"missing_in_tgt_count: fingerprint={fp_out.missing_in_tgt_count} legacy={legacy_out.missing_in_tgt_count}"


@pytest.mark.timeout(func_only=True)
def test_fingerprint_parity_matches_legacy_redshift(
    ws,
    spark,
    redshift_recon_config: ReconcileConfig,
    redshift_recon_table_config: TableRecon,
) -> None:
    table_conf = redshift_recon_table_config.tables[0]

    off_out, off_meta = _run_recon_one(ws, spark, redshift_recon_config, table_conf, fingerprint=False)
    on_out, on_meta = _run_recon_one(ws, spark, redshift_recon_config, table_conf, fingerprint=True)

    _assert_counts_equal(on_out, off_out)

    assert on_meta.eligible is True
    assert on_meta.verdict in {"MATCH", "MISMATCH"}, f"unexpected verdict {on_meta.verdict!r}"
    assert on_meta.fallback_to_full_pipeline is False, "fingerprint fell back to the legacy pipeline"

    assert off_meta.eligible is False
    assert off_meta.ineligibility_reason == INELIGIBLE_FLAG_DISABLED


@pytest.mark.timeout(func_only=True)
def test_fingerprint_parity_detects_same_mismatch_after_target_mutation(
    ws,
    spark,
    recon_schema: SchemaInfo,
    redshift_recon_config: ReconcileConfig,
    redshift_recon_table_config: TableRecon,
) -> None:
    table_conf = redshift_recon_table_config.tables[0]
    target_fqn = f"{recon_schema.catalog_name}.{recon_schema.name}.{table_conf.target_name}"

    spark.sql(f"UPDATE {target_fqn} SET carat = carat + 1.0 WHERE color = 'E' AND clarity = 'SI2'")

    off_out, _off_meta = _run_recon_one(ws, spark, redshift_recon_config, table_conf, fingerprint=False)
    on_out, on_meta = _run_recon_one(ws, spark, redshift_recon_config, table_conf, fingerprint=True)

    _assert_counts_equal(on_out, off_out)
    assert on_out.mismatch_count >= 1, "expected at least the mutated row to mismatch"

    assert on_meta.eligible is True
    assert on_meta.verdict == "MISMATCH"
    assert on_meta.fallback_to_full_pipeline is False
