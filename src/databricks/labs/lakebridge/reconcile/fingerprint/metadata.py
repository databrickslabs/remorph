"""Persistence-side metadata for the fingerprint pre-check."""

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from databricks.labs.lakebridge.reconcile.fingerprint.orchestrator import FingerprintResult


class IneligibilityReason(str, Enum):
    """Why a table was skipped by the fingerprint pre-check."""

    FLAG_DISABLED = "flag_disabled"
    UNSUPPORTED_DIALECT = "unsupported_dialect"
    REPORT_TYPE_NOT_DATA = "report_type_not_data"
    NO_JOIN_COLUMNS = "no_join_columns"
    FILTERS_CONFIGURED = "filters_configured"
    TRANSFORMS_CONFIGURED = "transforms_configured"
    COLUMN_THRESHOLDS_CONFIGURED = "column_thresholds_configured"
    TABLE_THRESHOLDS_CONFIGURED = "table_thresholds_configured"
    UNMAPPED_TARGET_COLUMN_MAPPING = "unmapped_target_column_mapping"


INELIGIBLE_FLAG_DISABLED = IneligibilityReason.FLAG_DISABLED.value
INELIGIBLE_UNSUPPORTED_DIALECT = IneligibilityReason.UNSUPPORTED_DIALECT.value
INELIGIBLE_REPORT_TYPE_NOT_DATA = IneligibilityReason.REPORT_TYPE_NOT_DATA.value
INELIGIBLE_NO_JOIN_COLUMNS = IneligibilityReason.NO_JOIN_COLUMNS.value
INELIGIBLE_FILTERS_CONFIGURED = IneligibilityReason.FILTERS_CONFIGURED.value
INELIGIBLE_TRANSFORMS_CONFIGURED = IneligibilityReason.TRANSFORMS_CONFIGURED.value
INELIGIBLE_COLUMN_THRESHOLDS_CONFIGURED = IneligibilityReason.COLUMN_THRESHOLDS_CONFIGURED.value
INELIGIBLE_TABLE_THRESHOLDS_CONFIGURED = IneligibilityReason.TABLE_THRESHOLDS_CONFIGURED.value
INELIGIBLE_UNMAPPED_TARGET_COLUMN_MAPPING = IneligibilityReason.UNMAPPED_TARGET_COLUMN_MAPPING.value


class FetchPath(str, Enum):
    """Stage-2 source-fetch strategy used for one run."""

    V1_SANDWICH = "v1_sandwich"
    V2_REDSHIFT_SPLIT = "v2_redshift_split"


FETCH_PATH_V1_SANDWICH = FetchPath.V1_SANDWICH.value
FETCH_PATH_V2_REDSHIFT_SPLIT = FetchPath.V2_REDSHIFT_SPLIT.value


RunVerdict = Literal["MATCH", "MISMATCH", "FAILED"]


@dataclass(frozen=True)
class FingerprintRunMetadata:
    """Recorded once per (recon_id, table) on recon_metrics."""

    eligible: bool = False
    ineligibility_reason: str | None = None
    verdict: RunVerdict | None = None
    elapsed_ms: int = 0
    solved_count: int = 0
    unsolved_sb_count: int = 0
    total_mismatched_sbs: int = 0
    fallback_to_full_pipeline: bool = False
    sub_bucket_count: int = 0
    bucket_count: int = 0
    target_row_count: int | None = None
    row_count_source: str | None = None
    fetch_path: str | None = None

    @classmethod
    def ineligible(cls, reason: str) -> "FingerprintRunMetadata":
        return cls(eligible=False, ineligibility_reason=reason)

    @classmethod
    def disabled(cls) -> "FingerprintRunMetadata":
        """Default for non-fingerprint reconciles, so the persisted struct stays uniform."""
        return cls(eligible=False, ineligibility_reason=INELIGIBLE_FLAG_DISABLED)

    @classmethod
    def from_result(
        cls,
        result: "FingerprintResult",
        *,
        verdict: RunVerdict,
        fallback_to_full_pipeline: bool = False,
    ) -> "FingerprintRunMetadata":
        """Single-site mapping from detection-side ``FingerprintResult`` to the persisted
        metadata. Adding a new telemetry field is one line here, not three copy-loop edits
        across the orchestrator's MATCH / MISMATCH-fallback / MISMATCH-success branches.
        """
        return cls(
            eligible=True,
            verdict=verdict,
            elapsed_ms=result.detection_elapsed_ms,
            solved_count=result.solved_count,
            unsolved_sb_count=result.unsolved_sb_count,
            total_mismatched_sbs=result.total_mismatched_sbs,
            fallback_to_full_pipeline=fallback_to_full_pipeline,
            sub_bucket_count=result.sub_bucket_count,
            bucket_count=result.bucket_count,
            target_row_count=result.target_row_count,
            row_count_source=result.row_count_source,
            fetch_path=result.fetch_path,
        )

    @classmethod
    def fallback(cls, *, verdict: RunVerdict | None = None) -> "FingerprintRunMetadata":
        """Eligible but no usable ``FingerprintResult`` (precheck declined or raised)."""
        return cls(eligible=True, fallback_to_full_pipeline=True, verdict=verdict)
