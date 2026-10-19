"""Unit tests for OPT-A-1 — the typed schema layer behind ``fingerprint_metrics_struct_sql``."""

from __future__ import annotations

import dataclasses

import pytest

from databricks.labs.lakebridge.reconcile import recon_capture as rc
from databricks.labs.lakebridge.reconcile.fingerprint.metadata import FingerprintRunMetadata
from databricks.labs.lakebridge.reconcile.recon_capture import (
    FP_METRICS_STRUCT_FIELDS,
    render_fp_metrics_value,
)
from tests.unit.reconcile.fingerprint._fixtures import FP_METRICS_FIELD_ORDER

_ALLOWED_SQL_TYPES = {"bool", "bigint", "bigint_or_null", "string_or_null"}


def test_schema_declares_thirteen_fields_in_dataclass_order():
    assert len(FP_METRICS_STRUCT_FIELDS) == 13, (
        f"Expected 13 fp_metrics fields, got {len(FP_METRICS_STRUCT_FIELDS)}. "
        "If you added a field, update this assertion AND verify the dataclass declaration."
    )

    schema_attrs = [attr for (_sql_field, attr, _sql_type) in FP_METRICS_STRUCT_FIELDS]
    dataclass_attrs = [f.name for f in dataclasses.fields(FingerprintRunMetadata)]

    for attr in schema_attrs:
        assert attr in dataclass_attrs, (
            f"Schema declares attribute {attr!r} that is NOT on FingerprintRunMetadata. "
            "Either remove from schema or add to the dataclass."
        )


def test_schema_field_names_unique():
    sql_field_names = [sql_field for (sql_field, _attr, _sql_type) in FP_METRICS_STRUCT_FIELDS]
    assert len(sql_field_names) == len(
        set(sql_field_names)
    ), f"Duplicate sql_field_name in FP_METRICS_STRUCT_FIELDS: {sql_field_names!r}"

    schema_attrs = [attr for (_sql_field, attr, _sql_type) in FP_METRICS_STRUCT_FIELDS]
    assert len(schema_attrs) == len(
        set(schema_attrs)
    ), f"Duplicate dataclass attribute in FP_METRICS_STRUCT_FIELDS: {schema_attrs!r}"


def test_schema_only_uses_allowed_sql_types():
    for sql_field, attr, sql_type in FP_METRICS_STRUCT_FIELDS:
        assert sql_type in _ALLOWED_SQL_TYPES, (
            f"Schema entry {sql_field!r} (attr={attr!r}) declares unsupported sql_type "
            f"{sql_type!r}. Allowed: {sorted(_ALLOWED_SQL_TYPES)!r}."
        )


def test_render_bool_emits_lowercase_sql_literal():
    assert render_fp_metrics_value(True, "bool") == "true"
    assert render_fp_metrics_value(False, "bool") == "false"
    assert render_fp_metrics_value(1, "bool") == "true"
    assert render_fp_metrics_value(0, "bool") == "false"


def test_render_bigint_emits_explicit_cast():
    assert render_fp_metrics_value(0, "bigint") == "cast(0 as bigint)"
    assert render_fp_metrics_value(2_097_152, "bigint") == "cast(2097152 as bigint)"


def test_render_bigint_or_null_handles_none():
    assert render_fp_metrics_value(None, "bigint_or_null") == "cast(NULL as bigint)"
    assert render_fp_metrics_value(0, "bigint_or_null") == "cast(0 as bigint)"
    assert render_fp_metrics_value(100_000_000, "bigint_or_null") == "cast(100000000 as bigint)"


def test_render_string_or_null_handles_none_and_quotes_scrub():
    assert render_fp_metrics_value(None, "string_or_null") == "cast(NULL as string)"
    assert render_fp_metrics_value("MATCH", "string_or_null") == "'MATCH'"
    assert render_fp_metrics_value("bad'reason\"here", "string_or_null") == "'badreasonhere'"


def test_render_unknown_sql_type_raises():
    with pytest.raises(ValueError, match="Unsupported sql_type"):
        render_fp_metrics_value(42, "int")
    with pytest.raises(ValueError, match="Unsupported sql_type"):
        render_fp_metrics_value("foo", "varchar")
    with pytest.raises(ValueError, match="Unsupported sql_type"):
        render_fp_metrics_value(None, "")


def test_render_bigint_or_null_rejects_non_none_non_int():
    with pytest.raises(AssertionError, match="bigint_or_null field expected"):
        render_fp_metrics_value("not-a-number", "bigint_or_null")


def test_render_bigint_rejects_stringy_value():
    with pytest.raises(AssertionError, match="bigint field expected"):
        render_fp_metrics_value("100", "bigint")


def test_struct_sql_field_order_pinned_by_schema():
    actual_order = tuple(sql_field for (sql_field, _attr, _t) in FP_METRICS_STRUCT_FIELDS)
    assert actual_order == FP_METRICS_FIELD_ORDER, (
        "Field order drifted in FP_METRICS_STRUCT_FIELDS. Reordering is a Delta "
        "schema-positional break for existing recon_metrics rows. Confirm intent."
    )


def test_render_helper_is_module_level_not_method():
    assert callable(rc.render_fp_metrics_value)
    assert rc.render_fp_metrics_value(True, "bool") == "true"


def test_schema_attrs_match_dataclass_fields_one_to_one():
    schema_attrs = {attr for (_sql_field, attr, _t) in FP_METRICS_STRUCT_FIELDS}
    dataclass_attrs = {f.name for f in dataclasses.fields(FingerprintRunMetadata)}

    missing_in_schema = dataclass_attrs - schema_attrs
    assert not missing_in_schema, (
        f"Dataclass attributes missing from FP_METRICS_STRUCT_FIELDS: {sorted(missing_in_schema)!r}. "
        "Either add to the schema, or document why the field is intentionally non-persistent."
    )

    extra_in_schema = schema_attrs - dataclass_attrs
    assert not extra_in_schema, (
        f"Schema references non-existent dataclass attributes: {sorted(extra_in_schema)!r}. "
        "Remove from schema or add to FingerprintRunMetadata."
    )
