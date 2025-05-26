from dataclasses import dataclass

import pytest


@dataclass
class SamplingQueries:
    target_sampling_query: str


@dataclass
class HashQueries:
    source_hash_query: str
    target_hash_query: str


@dataclass
class MismatchQueries:
    source_mismatch_query: str
    target_mismatch_query: str


@dataclass
class MissingQueries:
    source_missing_query: str
    target_missing_query: str


@dataclass
class ThresholdQueries:
    source_threshold_query: str
    target_threshold_query: str
    threshold_comparison_query: str


@dataclass
class RowQueries:
    source_row_query: str
    target_row_query: str


@dataclass
class RecordCountQueries:
    source_record_count_query: str
    target_record_count_query: str


@dataclass
class QueryStore:
    hash_queries: HashQueries
    mismatch_queries: MismatchQueries
    missing_queries: MissingQueries
    threshold_queries: ThresholdQueries
    row_queries: RowQueries
    record_count_queries: RecordCountQueries
    sampling_queries: SamplingQueries


@pytest.fixture
def setup_metadata_table(mock_spark, report_tables_schema):
    recon_schema, metrics_schema, details_schema = report_tables_schema
    mode = "overwrite"
    mock_spark.createDataFrame(data=[], schema=recon_schema).write.mode(mode).saveAsTable("DEFAULT.MAIN")
    mock_spark.createDataFrame(data=[], schema=metrics_schema).write.mode(mode).saveAsTable("DEFAULT.METRICS")
    mock_spark.createDataFrame(data=[], schema=details_schema).write.mode(mode).saveAsTable("DEFAULT.DETAILS")


@pytest.fixture
def query_store(mock_spark):
    source_hash_query = "SELECT LOWER(SHA2(CONCAT(TRIM(s_address), TRIM(s_name), COALESCE(TRIM(s_nationkey), '_null_recon_'), TRIM(s_phone), COALESCE(TRIM(s_suppkey), '_null_recon_')), 256)) AS hash_value_recon, s_nationkey AS s_nationkey, s_suppkey AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address = 'a'"
    target_hash_query = "SELECT LOWER(SHA2(CONCAT(TRIM(s_address_t), TRIM(s_name), COALESCE(TRIM(s_nationkey_t), '_null_recon_'), TRIM(s_phone_t), COALESCE(TRIM(s_suppkey_t), '_null_recon_')), 256)) AS hash_value_recon, s_nationkey_t AS s_nationkey, s_suppkey_t AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address_t = 'a'"
    source_mismatch_query = "WITH recon AS (SELECT CAST(22 AS number) AS s_nationkey, CAST(2 AS number) AS s_suppkey), src AS (SELECT TRIM(s_address) AS s_address, TRIM(s_name) AS s_name, COALESCE(TRIM(s_nationkey), '_null_recon_') AS s_nationkey, TRIM(s_phone) AS s_phone, COALESCE(TRIM(s_suppkey), '_null_recon_') AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address = 'a') SELECT src.s_address, src.s_name, src.s_nationkey, src.s_phone, src.s_suppkey FROM src INNER JOIN recon AS recon ON src.s_nationkey = recon.s_nationkey AND src.s_suppkey = recon.s_suppkey"
    target_mismatch_query = "WITH recon AS (SELECT 22 AS s_nationkey, 2 AS s_suppkey), src AS (SELECT TRIM(s_address_t) AS s_address, TRIM(s_name) AS s_name, COALESCE(TRIM(s_nationkey_t), '_null_recon_') AS s_nationkey, TRIM(s_phone_t) AS s_phone, COALESCE(TRIM(s_suppkey_t), '_null_recon_') AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address_t = 'a') SELECT src.s_address, src.s_name, src.s_nationkey, src.s_phone, src.s_suppkey FROM src INNER JOIN recon AS recon ON src.s_nationkey = recon.s_nationkey AND src.s_suppkey = recon.s_suppkey"
    source_missing_query = "WITH recon AS (SELECT 44 AS s_nationkey, 4 AS s_suppkey), src AS (SELECT TRIM(s_address_t) AS s_address, TRIM(s_name) AS s_name, COALESCE(TRIM(s_nationkey_t), '_null_recon_') AS s_nationkey, TRIM(s_phone_t) AS s_phone, COALESCE(TRIM(s_suppkey_t), '_null_recon_') AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address_t = 'a') SELECT src.s_address, src.s_name, src.s_nationkey, src.s_phone, src.s_suppkey FROM src INNER JOIN recon AS recon ON src.s_nationkey = recon.s_nationkey AND src.s_suppkey = recon.s_suppkey"
    target_missing_query = "WITH recon AS (SELECT CAST(33 AS number) AS s_nationkey, CAST(3 AS number) AS s_suppkey), src AS (SELECT TRIM(s_address) AS s_address, TRIM(s_name) AS s_name, COALESCE(TRIM(s_nationkey), '_null_recon_') AS s_nationkey, TRIM(s_phone) AS s_phone, COALESCE(TRIM(s_suppkey), '_null_recon_') AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address = 'a') SELECT src.s_address, src.s_name, src.s_nationkey, src.s_phone, src.s_suppkey FROM src INNER JOIN recon AS recon ON src.s_nationkey = recon.s_nationkey AND src.s_suppkey = recon.s_suppkey"
    source_threshold_query = "SELECT s_nationkey AS s_nationkey, s_suppkey AS s_suppkey, s_acctbal AS s_acctbal FROM :tbl WHERE s_name = 't' AND s_address = 'a'"
    target_threshold_query = "SELECT s_nationkey_t AS s_nationkey, s_suppkey_t AS s_suppkey, s_acctbal_t AS s_acctbal FROM :tbl WHERE s_name = 't' AND s_address_t = 'a'"
    threshold_comparison_query = "SELECT COALESCE(source.s_acctbal, 0) AS s_acctbal_source, COALESCE(databricks.s_acctbal, 0) AS s_acctbal_databricks, CASE WHEN (COALESCE(source.s_acctbal, 0) - COALESCE(databricks.s_acctbal, 0)) = 0 THEN 'Match' WHEN (COALESCE(source.s_acctbal, 0) - COALESCE(databricks.s_acctbal, 0)) BETWEEN 0 AND 100 THEN 'Warning' ELSE 'Failed' END AS s_acctbal_match, source.s_nationkey AS s_nationkey_source, source.s_suppkey AS s_suppkey_source FROM source_supplier_df_threshold_vw AS source INNER JOIN target_target_supplier_df_threshold_vw AS databricks ON source.s_nationkey <=> databricks.s_nationkey AND source.s_suppkey <=> databricks.s_suppkey WHERE (1 = 1 OR 1 = 1) OR (COALESCE(source.s_acctbal, 0) - COALESCE(databricks.s_acctbal, 0)) <> 0"
    source_row_query = "SELECT LOWER(SHA2(CONCAT(TRIM(s_address), TRIM(s_name), COALESCE(TRIM(s_nationkey), '_null_recon_'), TRIM(s_phone), COALESCE(TRIM(s_suppkey), '_null_recon_')), 256)) AS hash_value_recon, TRIM(s_address) AS s_address, TRIM(s_name) AS s_name, s_nationkey AS s_nationkey, TRIM(s_phone) AS s_phone, s_suppkey AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address = 'a'"
    target_row_query = "SELECT LOWER(SHA2(CONCAT(TRIM(s_address_t), TRIM(s_name), COALESCE(TRIM(s_nationkey_t), '_null_recon_'), TRIM(s_phone_t), COALESCE(TRIM(s_suppkey_t), '_null_recon_')), 256)) AS hash_value_recon, TRIM(s_address_t) AS s_address, TRIM(s_name) AS s_name, s_nationkey_t AS s_nationkey, TRIM(s_phone_t) AS s_phone, s_suppkey_t AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address_t = 'a'"
    hash_queries = HashQueries(
        source_hash_query=source_hash_query,
        target_hash_query=target_hash_query,
    )
    mismatch_queries = MismatchQueries(
        source_mismatch_query=source_mismatch_query,
        target_mismatch_query=target_mismatch_query,
    )
    missing_queries = MissingQueries(
        source_missing_query=source_missing_query,
        target_missing_query=target_missing_query,
    )
    threshold_queries = ThresholdQueries(
        source_threshold_query=source_threshold_query,
        target_threshold_query=target_threshold_query,
        threshold_comparison_query=threshold_comparison_query,
    )
    row_queries = RowQueries(
        source_row_query=source_row_query,
        target_row_query=target_row_query,
    )
    record_count_queries = RecordCountQueries(
        source_record_count_query="SELECT COUNT(1) AS count FROM :tbl WHERE s_name = 't' AND s_address = 'a'",
        target_record_count_query="SELECT COUNT(1) AS count FROM :tbl WHERE s_name = 't' AND s_address_t = 'a'",
    )
    sampling_queries = SamplingQueries(
        target_sampling_query="SELECT s_address_t AS s_address, s_name AS s_name, s_nationkey_t AS s_nationkey, s_phone_t AS s_phone, s_suppkey_t AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address_t = 'a'"
    )

    return QueryStore(
        hash_queries=hash_queries,
        mismatch_queries=mismatch_queries,
        missing_queries=missing_queries,
        threshold_queries=threshold_queries,
        row_queries=row_queries,
        record_count_queries=record_count_queries,
        sampling_queries=sampling_queries,
    )
