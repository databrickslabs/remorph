"""Unit tests for the ``fingerprint_metrics`` SQL projection in ``ReconCapture``."""

import re

from databricks.labs.lakebridge.reconcile.fingerprint.metadata import (
    INELIGIBLE_FILTERS_CONFIGURED,
    FingerprintRunMetadata,
)
from databricks.labs.lakebridge.reconcile.recon_capture import ReconCapture
from tests.unit.reconcile.fingerprint._fixtures import FP_METRICS_FIELD_ORDER as _FIELD_ORDER


def _field_offsets(sql: str) -> list[int]:
    return [sql.index(f"'{name}'") for name in _FIELD_ORDER]


def test_struct_sql_emits_all_eight_fields_in_declared_order():
    metadata = FingerprintRunMetadata(
        eligible=True,
        verdict="MATCH",
        elapsed_ms=42,
        solved_count=3,
        unsolved_sb_count=1,
        total_mismatched_sbs=4,
    )
    sql = ReconCapture.fingerprint_metrics_struct_sql(metadata)
    offsets = _field_offsets(sql)
    assert offsets == sorted(offsets), f"Field order drifted in {sql!r}"


def test_struct_sql_renders_eligible_match_verdict():
    metadata = FingerprintRunMetadata(
        eligible=True, verdict="MATCH", elapsed_ms=120, solved_count=0, unsolved_sb_count=0
    )
    sql = ReconCapture.fingerprint_metrics_struct_sql(metadata)
    assert "'eligible', true" in sql
    assert "'verdict', 'MATCH'" in sql
    assert "'elapsed_ms', cast(120 as bigint)" in sql
    assert "'fallback_to_full_pipeline', false" in sql


def test_struct_sql_renders_ineligible_with_reason():
    metadata = FingerprintRunMetadata.ineligible(INELIGIBLE_FILTERS_CONFIGURED)
    sql = ReconCapture.fingerprint_metrics_struct_sql(metadata)
    assert "'eligible', false" in sql
    assert f"'ineligibility_reason', '{INELIGIBLE_FILTERS_CONFIGURED}'" in sql
    assert "'verdict', cast(NULL as string)" in sql


def test_struct_sql_emits_null_for_none_string_fields():
    metadata = FingerprintRunMetadata(eligible=True, verdict=None)
    sql = ReconCapture.fingerprint_metrics_struct_sql(metadata)
    assert "'verdict', cast(NULL as string)" in sql
    assert "'verdict', 'None'" not in sql
    assert "'ineligibility_reason', cast(NULL as string)" in sql


def test_struct_sql_scrubs_quotes_from_reason_and_verdict():
    metadata = FingerprintRunMetadata(eligible=False, ineligibility_reason="bad'reason\"here", verdict="MIS\"MATCH")
    sql = ReconCapture.fingerprint_metrics_struct_sql(metadata)
    assert "bad'reason" not in sql
    assert 'MIS"MATCH' not in sql
    assert "'ineligibility_reason', 'badreasonhere'" in sql
    assert "'verdict', 'MISMATCH'" in sql


def test_struct_sql_casts_counters_to_bigint():
    metadata = FingerprintRunMetadata(
        eligible=True,
        elapsed_ms=1,
        solved_count=2,
        unsolved_sb_count=3,
        total_mismatched_sbs=4,
        sub_bucket_count=2_097_152,
        bucket_count=2_048,
        target_row_count=100_000_000,
    )
    sql = ReconCapture.fingerprint_metrics_struct_sql(metadata)
    bigint_casts = re.findall(r"cast\(\d+ as bigint\)", sql)
    assert len(bigint_casts) == 7, f"Expected 7 bigint casts, got {bigint_casts!r}"


def test_struct_sql_target_row_count_null_when_static_default_path():
    metadata = FingerprintRunMetadata(
        eligible=True,
        verdict="MATCH",
        sub_bucket_count=1_048_576,
        bucket_count=32_768,
        target_row_count=None,
        row_count_source="static_default",
    )
    sql = ReconCapture.fingerprint_metrics_struct_sql(metadata)
    assert "'target_row_count', cast(NULL as bigint)" in sql
    assert "'row_count_source', 'static_default'" in sql


def test_struct_sql_emits_tier_fields_for_delta_describe_detail_path():
    metadata = FingerprintRunMetadata(
        eligible=True,
        verdict="MATCH",
        sub_bucket_count=4_194_304,
        bucket_count=4_096,
        target_row_count=1_000_000_000,
        row_count_source="delta_describe_detail",
    )
    sql = ReconCapture.fingerprint_metrics_struct_sql(metadata)
    assert "'sub_bucket_count', cast(4194304 as bigint)" in sql
    assert "'bucket_count', cast(4096 as bigint)" in sql
    assert "'target_row_count', cast(1000000000 as bigint)" in sql
    assert "'row_count_source', 'delta_describe_detail'" in sql


def test_struct_sql_default_metadata_emits_zero_tier_and_null_row_count():
    metadata = FingerprintRunMetadata.disabled()
    sql = ReconCapture.fingerprint_metrics_struct_sql(metadata)
    assert "'sub_bucket_count', cast(0 as bigint)" in sql
    assert "'bucket_count', cast(0 as bigint)" in sql
    assert "'target_row_count', cast(NULL as bigint)" in sql
    assert "'row_count_source', cast(NULL as string)" in sql
    assert "'fetch_path', cast(NULL as string)" in sql


def test_struct_sql_emits_fetch_path_v2_for_redshift_split():
    metadata = FingerprintRunMetadata(
        eligible=True,
        verdict="MISMATCH",
        sub_bucket_count=2_097_152,
        bucket_count=2_048,
        target_row_count=100_000_000,
        row_count_source="delta_describe_detail",
        fetch_path="v2_redshift_split",
    )
    sql = ReconCapture.fingerprint_metrics_struct_sql(metadata)
    assert "'fetch_path', 'v2_redshift_split'" in sql


def test_struct_sql_emits_fetch_path_v1_for_legacy_sandwich():
    metadata = FingerprintRunMetadata(
        eligible=True,
        verdict="MISMATCH",
        sub_bucket_count=2_097_152,
        bucket_count=2_048,
        target_row_count=100_000_000,
        row_count_source="delta_describe_detail",
        fetch_path="v1_sandwich",
    )
    sql = ReconCapture.fingerprint_metrics_struct_sql(metadata)
    assert "'fetch_path', 'v1_sandwich'" in sql


def test_struct_sql_match_verdict_emits_null_fetch_path():
    metadata = FingerprintRunMetadata(
        eligible=True,
        verdict="MATCH",
        sub_bucket_count=2_097_152,
        bucket_count=2_048,
        target_row_count=100_000_000,
        row_count_source="delta_describe_detail",
        fetch_path=None,
    )
    sql = ReconCapture.fingerprint_metrics_struct_sql(metadata)
    assert "'fetch_path', cast(NULL as string)" in sql
    assert "'fetch_path', 'None'" not in sql
