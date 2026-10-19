"""Shared helpers for the trigger-recon tests."""

from unittest.mock import MagicMock

from databricks.labs.lakebridge.config import (
    ReconcileConfig,
    SourceConnectionConfig,
    TargetConnectionConfig,
)


def make_reconcile_config(*, report_type: str = "data", source: str = "redshift", **extra) -> ReconcileConfig:
    return ReconcileConfig(
        report_type=report_type,
        source=SourceConnectionConfig(dialect=source, catalog="dev", schema="src", uc_connection_name="conn"),
        target=TargetConnectionConfig(catalog="tc", schema="ts"),
        metadata_config=MagicMock(),
        **extra,
    )
