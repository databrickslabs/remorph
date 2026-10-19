import pytest

from databricks.labs.lakebridge.reconcile.fingerprint.columns import counterpart_type_of, pair_detection_columns
from databricks.labs.lakebridge.reconcile.fingerprint.query_builders.redshift import RedshiftFingerprintQueryBuilder
from databricks.labs.lakebridge.reconcile.fingerprint.spark_target import serialize_target_column_sql
from databricks.labs.lakebridge.reconcile.recon_config import Schema


def test_pair_detection_columns_attaches_counterpart_types():
    source = [Schema("`a`", "double precision", '"a"'), Schema("`b`", "int", '"b"')]
    target = [Schema("`a`", "decimal(18,2)", "`a`"), Schema("`b`", "bigint", "`b`")]

    paired_source, paired_target = pair_detection_columns(source, target)

    assert [counterpart_type_of(c) for c in paired_source] == ["decimal(18,2)", "bigint"]
    assert [counterpart_type_of(c) for c in paired_target] == ["double precision", "int"]
    assert [c.data_type for c in paired_source] == ["double precision", "int"]
    assert [c.data_type for c in paired_target] == ["decimal(18,2)", "bigint"]


def test_counterpart_type_of_plain_schema_is_none():
    assert counterpart_type_of(Schema("`a`", "int", '"a"')) is None


@pytest.mark.parametrize("source_type, target_type", [("double precision", "decimal(18,2)"), ("timestamp", "string")])
def test_type_divergent_pair_is_not_pinned_on_either_side(source_type, target_type):
    source_sql = RedshiftFingerprintQueryBuilder().serialize_column("`c`", source_type, target_type)
    target_sql = serialize_target_column_sql("c", target_type, source_type)

    assert "DECIMAL(38,10)" not in source_sql
    assert "DECIMAL(38,10)" not in target_sql
    assert "DATE_FORMAT" not in target_sql
