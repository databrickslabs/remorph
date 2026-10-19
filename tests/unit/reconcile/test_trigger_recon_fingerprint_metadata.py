"""Unit tests for the FingerprintRunMetadata produced by the trigger service."""

from unittest.mock import MagicMock, patch

import pytest
from pyspark.errors import PySparkException

from databricks.labs.lakebridge.config import ReconcileConfig
from databricks.labs.lakebridge.reconcile.exception import ColumnMismatchException, DataSourceRuntimeException
from databricks.labs.lakebridge.reconcile.fingerprint.exceptions import UnmappedTargetColumnMappingError
from databricks.labs.lakebridge.reconcile.fingerprint.metadata import (
    INELIGIBLE_FILTERS_CONFIGURED,
    INELIGIBLE_FLAG_DISABLED,
    INELIGIBLE_NO_JOIN_COLUMNS,
    INELIGIBLE_UNMAPPED_TARGET_COLUMN_MAPPING,
    INELIGIBLE_UNSUPPORTED_DIALECT,
)
from databricks.labs.lakebridge.reconcile.fingerprint.orchestrator import FingerprintResult
from databricks.labs.lakebridge.reconcile.recon_config import Filters, Table
from databricks.labs.lakebridge.reconcile.recon_output_config import DataReconcileOutput, MismatchOutput
from databricks.labs.lakebridge.reconcile.trigger_recon_service import TriggerReconService
from tests.unit.reconcile._trigger_recon_harness import make_reconcile_config


def _reconciler(report_type: str = "data") -> MagicMock:
    reconciler = MagicMock()
    reconciler.report_type = report_type
    reconciler.source = MagicMock()
    reconciler.target = MagicMock()
    reconciler.spark = MagicMock()
    reconciler.source_engine = MagicMock()
    reconciler.intermediate_persist = MagicMock()
    return reconciler


def _config(*, flag: bool = True, source: str = "redshift") -> ReconcileConfig:
    return make_reconcile_config(report_type="data", source=source, reconcile_optimizer=flag)


def _table(**overrides) -> Table:
    base = {"source_name": "t", "target_name": "t", "join_columns": ["id"]}
    base.update(overrides)
    return Table(**base)  # type: ignore[arg-type]


def _stub_full_pipeline_output() -> DataReconcileOutput:
    return DataReconcileOutput(mismatch_count=999, mismatch=MismatchOutput())


@patch.object(TriggerReconService, "_run_reconcile_data")
def test_flag_disabled_records_flag_disabled_reason(mock_full):
    mock_full.return_value = _stub_full_pipeline_output()

    output, metadata = TriggerReconService.run_fingerprint_or_reconcile_data(
        reconciler=_reconciler(),
        reconcile_config=_config(flag=False),
        table_conf=_table(),
        src_schema=[],
        tgt_schema=[],
    )

    assert metadata.eligible is False
    assert metadata.ineligibility_reason == INELIGIBLE_FLAG_DISABLED
    assert metadata.fallback_to_full_pipeline is False, (
        "Ineligible tables didn't *fall back* — they were never eligible to begin with. "
        "Conflating these would inflate fallback rates in dashboards."
    )
    assert output.mismatch_count == 999
    mock_full.assert_called_once()


@patch.object(TriggerReconService, "_run_reconcile_data")
def test_unsupported_dialect_records_unsupported_reason(mock_full):
    mock_full.return_value = _stub_full_pipeline_output()

    _, metadata = TriggerReconService.run_fingerprint_or_reconcile_data(
        reconciler=_reconciler(),
        reconcile_config=_config(source="snowflake"),
        table_conf=_table(),
        src_schema=[],
        tgt_schema=[],
    )

    assert metadata.ineligibility_reason == INELIGIBLE_UNSUPPORTED_DIALECT
    mock_full.assert_called_once()


@patch.object(TriggerReconService, "_run_reconcile_data")
def test_no_join_columns_records_no_join_columns_reason(mock_full):
    mock_full.return_value = _stub_full_pipeline_output()

    _, metadata = TriggerReconService.run_fingerprint_or_reconcile_data(
        reconciler=_reconciler(),
        reconcile_config=_config(),
        table_conf=Table(source_name="t", target_name="t"),
        src_schema=[],
        tgt_schema=[],
    )

    assert metadata.ineligibility_reason == INELIGIBLE_NO_JOIN_COLUMNS


@patch.object(TriggerReconService, "_run_reconcile_data")
def test_per_table_filter_records_filters_reason(mock_full):
    mock_full.return_value = _stub_full_pipeline_output()

    _, metadata = TriggerReconService.run_fingerprint_or_reconcile_data(
        reconciler=_reconciler(),
        reconcile_config=_config(),
        table_conf=_table(filters=Filters(source="x is not null")),
        src_schema=[],
        tgt_schema=[],
    )

    assert metadata.ineligibility_reason == INELIGIBLE_FILTERS_CONFIGURED


@patch("databricks.labs.lakebridge.reconcile.trigger_recon_service.run_fingerprint_precheck")
def test_eligible_match_records_match_verdict_with_elapsed(mock_precheck):
    mock_precheck.return_value = FingerprintResult(verdict="MATCH", detection_elapsed_ms=137)

    output, metadata = TriggerReconService.run_fingerprint_or_reconcile_data(
        reconciler=_reconciler(),
        reconcile_config=_config(),
        table_conf=_table(),
        src_schema=[],
        tgt_schema=[],
    )

    assert metadata.eligible is True
    assert metadata.verdict == "MATCH"
    assert metadata.elapsed_ms == 137
    assert metadata.fallback_to_full_pipeline is False
    assert output.mismatch_count == 0
    assert output.missing_in_src_count == 0
    assert output.missing_in_tgt_count == 0


@patch("databricks.labs.lakebridge.reconcile.trigger_recon_service.build_mismatch_output")
@patch("databricks.labs.lakebridge.reconcile.trigger_recon_service.run_fingerprint_precheck")
def test_eligible_mismatch_with_rows_records_solver_counters(mock_precheck, mock_build):
    src_rows = MagicMock()
    src_rows.count.return_value = 5
    tgt_rows = MagicMock()
    tgt_rows.count.return_value = 3
    mock_precheck.return_value = FingerprintResult(
        verdict="MISMATCH",
        source_rows=src_rows,
        target_rows=tgt_rows,
        solved_count=4,
        unsolved_sb_count=2,
        total_mismatched_sbs=6,
        detection_elapsed_ms=99,
    )
    mock_build.return_value = DataReconcileOutput(mismatch_count=4, mismatch=MismatchOutput())

    _, metadata = TriggerReconService.run_fingerprint_or_reconcile_data(
        reconciler=_reconciler(),
        reconcile_config=_config(),
        table_conf=_table(),
        src_schema=[],
        tgt_schema=[],
    )

    assert metadata.eligible is True
    assert metadata.verdict == "MISMATCH"
    assert metadata.elapsed_ms == 99
    assert metadata.solved_count == 4
    assert metadata.unsolved_sb_count == 2
    assert metadata.total_mismatched_sbs == 6
    assert metadata.fallback_to_full_pipeline is False


@patch.object(TriggerReconService, "_run_reconcile_data")
@patch("databricks.labs.lakebridge.reconcile.trigger_recon_service.run_fingerprint_precheck")
def test_eligible_mismatch_missing_rows_falls_back_with_metadata(mock_precheck, mock_full):
    mock_precheck.return_value = FingerprintResult(
        verdict="MISMATCH",
        source_rows=None,
        target_rows=None,
        solved_count=1,
        unsolved_sb_count=2,
        total_mismatched_sbs=3,
        detection_elapsed_ms=11,
    )
    mock_full.return_value = _stub_full_pipeline_output()

    output, metadata = TriggerReconService.run_fingerprint_or_reconcile_data(
        reconciler=_reconciler(),
        reconcile_config=_config(),
        table_conf=_table(),
        src_schema=[],
        tgt_schema=[],
    )

    assert metadata.verdict == "MISMATCH"
    assert metadata.fallback_to_full_pipeline is True
    assert metadata.solved_count == 1
    assert metadata.unsolved_sb_count == 2
    assert metadata.total_mismatched_sbs == 3
    assert output.mismatch_count == 999


@patch.object(TriggerReconService, "_run_reconcile_data")
@patch("databricks.labs.lakebridge.reconcile.trigger_recon_service.run_fingerprint_precheck")
def test_eligible_precheck_returns_none_records_fallback(mock_precheck, mock_full):
    mock_precheck.return_value = None
    mock_full.return_value = _stub_full_pipeline_output()

    output, metadata = TriggerReconService.run_fingerprint_or_reconcile_data(
        reconciler=_reconciler(),
        reconcile_config=_config(),
        table_conf=_table(),
        src_schema=[],
        tgt_schema=[],
    )

    assert metadata.eligible is True
    assert metadata.verdict is None
    assert metadata.fallback_to_full_pipeline is True
    assert output.mismatch_count == 999


@patch.object(TriggerReconService, "_run_reconcile_data")
@patch("databricks.labs.lakebridge.reconcile.trigger_recon_service.run_fingerprint_precheck")
def test_eligible_precheck_failure_records_failed_verdict(mock_precheck, mock_full):
    mock_precheck.side_effect = DataSourceRuntimeException("simulated jdbc failure")
    mock_full.return_value = _stub_full_pipeline_output()

    output, metadata = TriggerReconService.run_fingerprint_or_reconcile_data(
        reconciler=_reconciler(),
        reconcile_config=_config(),
        table_conf=_table(),
        src_schema=[],
        tgt_schema=[],
    )

    assert metadata.eligible is True
    assert metadata.verdict == "FAILED"
    assert metadata.fallback_to_full_pipeline is True
    assert output.mismatch_count == 999


@pytest.mark.parametrize(
    "report_type",
    ["data", "all", "row"],
)
@patch.object(TriggerReconService, "_run_reconcile_data")
@patch("databricks.labs.lakebridge.reconcile.trigger_recon_service.run_fingerprint_precheck")
def test_eligible_match_skips_full_pipeline_for_all_data_report_types(mock_precheck, mock_full, report_type):
    mock_precheck.return_value = FingerprintResult(verdict="MATCH", detection_elapsed_ms=1)

    TriggerReconService.run_fingerprint_or_reconcile_data(
        reconciler=_reconciler(report_type=report_type),
        reconcile_config=_config(),
        table_conf=_table(),
        src_schema=[],
        tgt_schema=[],
    )

    mock_full.assert_not_called()


@patch.object(TriggerReconService, "_run_reconcile_data")
@patch("databricks.labs.lakebridge.reconcile.trigger_recon_service.run_fingerprint_precheck")
def test_pyspark_exception_during_precheck_falls_back_with_failed_verdict(mock_precheck, mock_full):
    mock_precheck.side_effect = PySparkException("AnalysisException: column 'foo' does not exist on target Delta table")
    mock_full.return_value = _stub_full_pipeline_output()

    output, metadata = TriggerReconService.run_fingerprint_or_reconcile_data(
        reconciler=_reconciler(),
        reconcile_config=_config(),
        table_conf=_table(),
        src_schema=[],
        tgt_schema=[],
    )

    assert metadata.eligible is True
    assert metadata.verdict == "FAILED"
    assert metadata.fallback_to_full_pipeline is True
    assert output.mismatch_count == 999, "Full-pipeline output (sentinel mismatch_count=999) must be returned"


@pytest.mark.parametrize(
    "unexpected_exc",
    [
        ValueError("solver produced a degenerate power-sum system"),
        KeyError("sub_bucket_id"),
        IndexError("unsolved_sb_ids out of range"),
        ArithmeticError("overflow in d=2 discriminant"),
        RuntimeError("unanticipated fingerprint fault"),
    ],
)
@patch.object(TriggerReconService, "_run_reconcile_data")
@patch("databricks.labs.lakebridge.reconcile.trigger_recon_service.run_fingerprint_precheck")
def test_unenumerated_precheck_exception_fails_open_not_crash(mock_precheck, mock_full, unexpected_exc):
    mock_precheck.side_effect = unexpected_exc
    mock_full.return_value = _stub_full_pipeline_output()

    output, metadata = TriggerReconService.run_fingerprint_or_reconcile_data(
        reconciler=_reconciler(),
        reconcile_config=_config(),
        table_conf=_table(),
        src_schema=[],
        tgt_schema=[],
    )

    assert metadata.eligible is True
    assert metadata.verdict == "FAILED"
    assert metadata.fallback_to_full_pipeline is True
    assert output.mismatch_count == 999, "Unexpected precheck fault must fall back to the full pipeline output"
    mock_full.assert_called_once()


@patch.object(TriggerReconService, "_run_reconcile_data")
@patch("databricks.labs.lakebridge.reconcile.trigger_recon_service.build_mismatch_output")
@patch("databricks.labs.lakebridge.reconcile.trigger_recon_service.run_fingerprint_precheck")
def test_pyspark_exception_during_mismatch_output_falls_back_to_full_pipeline(mock_precheck, mock_build, mock_full):
    mock_precheck.return_value = FingerprintResult(
        verdict="MISMATCH",
        source_rows=MagicMock(),
        target_rows=MagicMock(),
        detection_elapsed_ms=10,
        solved_count=1,
    )
    mock_build.side_effect = PySparkException("AnalysisException: column resolution failed")
    full_output = _stub_full_pipeline_output()
    mock_full.return_value = full_output

    output, metadata = TriggerReconService.run_fingerprint_or_reconcile_data(
        reconciler=_reconciler(),
        reconcile_config=_config(),
        table_conf=_table(),
        src_schema=[],
        tgt_schema=[],
    )

    assert metadata.eligible is True
    assert metadata.verdict == "MISMATCH", (
        "Verdict must reflect the precheck signal, not the build-output failure — "
        "the failure is recorded via fallback_to_full_pipeline=True."
    )
    assert metadata.fallback_to_full_pipeline is True
    assert (
        output is full_output
    ), "Output must come from the full pipeline so the customer still gets a real recon answer."
    mock_full.assert_called_once()


@pytest.mark.parametrize(
    "raised",
    [
        ColumnMismatchException("source and target should have same columns for capturing the mismatch data"),
        KeyError("hash_value_recon"),
        RuntimeError("unexpected build state"),
    ],
    ids=["column_mismatch", "key_error", "runtime_error"],
)
@patch.object(TriggerReconService, "_run_reconcile_data")
@patch("databricks.labs.lakebridge.reconcile.trigger_recon_service.build_mismatch_output")
@patch("databricks.labs.lakebridge.reconcile.trigger_recon_service.run_fingerprint_precheck")
def test_non_spark_exception_during_mismatch_output_falls_back_instead_of_aborting(
    mock_precheck, mock_build, mock_full, raised
):
    mock_precheck.return_value = FingerprintResult(
        verdict="MISMATCH",
        source_rows=MagicMock(),
        target_rows=MagicMock(),
        detection_elapsed_ms=10,
        solved_count=1,
    )
    mock_build.side_effect = raised
    full_output = _stub_full_pipeline_output()
    mock_full.return_value = full_output

    output, metadata = TriggerReconService.run_fingerprint_or_reconcile_data(
        reconciler=_reconciler(),
        reconcile_config=_config(),
        table_conf=_table(),
        src_schema=[],
        tgt_schema=[],
    )

    assert metadata.verdict == "MISMATCH", (
        "Verdict reflects the precheck signal; the build failure is recorded via "
        "fallback_to_full_pipeline=True, not by aborting the job."
    )
    assert metadata.fallback_to_full_pipeline is True
    assert output is full_output, "A non-Spark build failure must still yield the full-pipeline recon answer."
    mock_full.assert_called_once()


@patch.object(TriggerReconService, "_run_reconcile_data")
@patch("databricks.labs.lakebridge.reconcile.trigger_recon_service.build_mismatch_output")
@patch("databricks.labs.lakebridge.reconcile.trigger_recon_service.run_fingerprint_precheck")
def test_control_flow_signal_during_mismatch_output_is_not_swallowed(mock_precheck, mock_build, mock_full):
    mock_precheck.return_value = FingerprintResult(
        verdict="MISMATCH",
        source_rows=MagicMock(),
        target_rows=MagicMock(),
        detection_elapsed_ms=10,
        solved_count=1,
    )
    mock_build.side_effect = KeyboardInterrupt()

    with pytest.raises(KeyboardInterrupt):
        TriggerReconService.run_fingerprint_or_reconcile_data(
            reconciler=_reconciler(),
            reconcile_config=_config(),
            table_conf=_table(),
            src_schema=[],
            tgt_schema=[],
        )

    mock_full.assert_not_called()


@patch.object(TriggerReconService, "_run_reconcile_data")
@patch("databricks.labs.lakebridge.reconcile.trigger_recon_service.run_fingerprint_precheck")
def test_unmapped_target_column_mapping_records_typed_ineligibility(mock_precheck, mock_full):
    mock_precheck.side_effect = UnmappedTargetColumnMappingError(
        "column_mapping target 'tgt_a_typo' (mapped from 'src_a') not found in target schema"
    )
    mock_full.return_value = _stub_full_pipeline_output()

    output, metadata = TriggerReconService.run_fingerprint_or_reconcile_data(
        reconciler=_reconciler(),
        reconcile_config=_config(),
        table_conf=_table(),
        src_schema=[],
        tgt_schema=[],
    )

    assert metadata.eligible is False, "Config-time ineligibility, not a precheck failure"
    assert metadata.ineligibility_reason == INELIGIBLE_UNMAPPED_TARGET_COLUMN_MAPPING
    assert metadata.ineligibility_reason == "unmapped_target_column_mapping"
    assert metadata.verdict is None
    assert metadata.fallback_to_full_pipeline is False, (
        "fallback_to_full_pipeline tracks runtime fallbacks; ineligible runs use the full "
        "pipeline by definition and shouldn't double-count on this flag."
    )
    assert output.mismatch_count == 999, "Full-pipeline output (sentinel mismatch_count=999) must be returned"
