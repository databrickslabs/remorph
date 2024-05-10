from pyspark import Row

from databricks.labs.remorph.config import SQLGLOT_DIALECTS, DatabaseConfig
from databricks.labs.remorph.reconcile.connectors.mock_data_source import MockDataSource
from databricks.labs.remorph.reconcile.execute import Reconciliation
from databricks.labs.remorph.reconcile.recon_config import ReconcileOutput
from databricks.labs.remorph.reconcile.schema_compare import SchemaCompare


def test_reconcile_data(mock_spark, table_conf_with_opts, schema):
    src_schema, tgt_schema = schema
    source_dataframe_repository = {("catalog1", "schema1",
                                    "SELECT LOWER(SHA2(CONCAT(TRIM(s_address), TRIM(s_name), COALESCE(TRIM("
                                    "s_nationkey), ''), TRIM(s_phone), COALESCE(TRIM(s_suppkey), '')), 256)) AS "
                                    "hash_value_recon, COALESCE(TRIM(s_nationkey), '') AS s_nationkey, COALESCE(TRIM("
                                    "s_suppkey), '') AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address = 'a'"):
        mock_spark.createDataFrame([
            Row(hash_value_recon="a1b", s_nationkey=11, s_suppkey=1),
            Row(hash_value_recon="c2d", s_nationkey=22, s_suppkey=2)]),
    }
    source_schema_repository = {("catalog1", "schema1", "supplier"): src_schema}

    target_dataframe_repository = {("catalog1", "schema1",
                                    "SELECT LOWER(SHA2(CONCAT(TRIM(s_address_t), TRIM(s_name), COALESCE(TRIM(s_nationkey_t), ''), "
                                    "TRIM(s_phone_t), COALESCE(TRIM(s_suppkey_t), '')), 256)) AS hash_value_recon, COALESCE(TRIM("
                                    "s_nationkey_t), '') AS s_nationkey, COALESCE(TRIM(s_suppkey_t), '') AS s_suppkey FROM :tbl WHERE "
                                    "s_name = 't' AND s_address_t = 'a'"): mock_spark.createDataFrame([
        Row(hash_value_recon="a1b", s_nationkey=11, s_suppkey=1),
        Row(hash_value_recon="c2d", s_nationkey=22, s_suppkey=2)])}

    target_schema_repository = {("catalog1", "schema1", "supplier"): tgt_schema}
    database_config = DatabaseConfig(
        source_catalog="catalog1",
        source_schema="schema1",
        target_catalog="catalog1",
        target_schema="schema1",
    )
    schema_comparator = SchemaCompare(mock_spark)
    source = MockDataSource(source_dataframe_repository, source_schema_repository)
    target = MockDataSource(target_dataframe_repository, target_schema_repository)
    actual = Reconciliation(source, target, database_config, "data", schema_comparator,
                            SQLGLOT_DIALECTS.get("databricks")).reconcile_data(table_conf_with_opts, src_schema,
                                                                               tgt_schema)
    expected = ReconcileOutput(mismatch_count=0, missing_in_src_count=0, missing_in_tgt_count=0, missing_in_src=None,
                               missing_in_tgt=None, mismatch=None)

    assert actual == expected
