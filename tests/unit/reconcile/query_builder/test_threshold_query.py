import re

from databricks.labs.remorph.reconcile.query_builder.threshold_query import (
    ThresholdQueryBuilder,
)
from databricks.labs.remorph.reconcile.recon_config import (
    JdbcReaderOptions,
    Schema,
    Thresholds,
    Transformation,
)


def test_threshold_comparison_query_with_single_threshold(table_conf_with_opts, schema):
    # table conf
    table_conf = table_conf_with_opts
    # schema
    schema, _ = schema
    schema.append(Schema("s_suppdate", "timestamp"))
    comparison_query = ThresholdQueryBuilder(table_conf, schema, "source", "oracle").build_comparison_query()
    assert re.sub(r'\s+', ' ', comparison_query.strip().lower()) == re.sub(
        r'\s+',
        ' ',
        """select coalesce(source.s_acctbal, 0) as s_acctbal_source, coalesce(databricks.s_acctbal,
        0) as s_acctbal_databricks, case when (coalesce(source.s_acctbal, 0) - coalesce(databricks.s_acctbal,
        0)) = 0 then `match` when (coalesce(source.s_acctbal, 0) - coalesce(databricks.s_acctbal, 0)) between 0 and
        100 then `warning` else `failed` end as s_acctbal_match, source.s_nationkey as s_nationkey_source,
        source.s_suppkey as s_suppkey_source from supplier_df_threshold_vw as source inner join
        target_supplier_df_threshold_vw as databricks on source.s_nationkey <=> databricks.s_nationkey and
        source.s_suppkey <=> databricks.s_suppkey where (1 = 1 or 1 = 1) or
        (coalesce(source.s_acctbal, 0) - coalesce(databricks.s_acctbal, 0)) <> 0""".strip().lower(),
    )


def test_threshold_comparison_query_with_multiple_threshold(table_conf_with_opts, schema):
    # table conf
    table_conf = table_conf_with_opts
    table_conf.join_columns = ["s_suppkey", "s_suppdate"]
    table_conf.thresholds = [
        Thresholds(column_name="s_acctbal", lower_bound="5%", upper_bound="-5%", type="float"),
        Thresholds(column_name="s_suppdate", lower_bound="-86400", upper_bound="86400", type="timestamp"),
    ]

    # schema
    schema, _ = schema
    schema.append(Schema("s_suppdate", "timestamp"))

    comparison_query = ThresholdQueryBuilder(table_conf, schema, "target", "databricks").build_comparison_query()
    assert re.sub(r'\s+', ' ', comparison_query.strip().lower()) == re.sub(
        r'\s+',
        ' ',
        """select coalesce(source.s_acctbal, 0) as s_acctbal_source, coalesce(databricks.s_acctbal,
        0) as s_acctbal_databricks, case when (coalesce(source.s_acctbal, 0) - coalesce(databricks.s_acctbal,
        0)) = 0 then `match` when ((coalesce(source.s_acctbal, 0) - coalesce(databricks.s_acctbal,
        0)) / if(databricks.s_acctbal = 0 or databricks.s_acctbal is null, 1, databricks.s_acctbal)) * 100 between 5
        and -5 then `warning` else `failed` end as s_acctbal_match, coalesce(unix_timestamp(source.s_suppdate),
        0) as s_suppdate_source, coalesce(unix_timestamp(databricks.s_suppdate), 0) as s_suppdate_databricks,
        case when (coalesce(unix_timestamp(source.s_suppdate), 0) - coalesce(unix_timestamp(databricks.s_suppdate),
        0)) = 0 then `match` when (coalesce(unix_timestamp(source.s_suppdate), 0) -
        coalesce(unix_timestamp(databricks.s_suppdate), 0)) between -86400 and 86400 then
        `warning` else `failed` end as s_suppdate_match, source.s_suppdate as s_suppdate_source,
        source.s_suppkey as s_suppkey_source from supplier_df_threshold_vw as
        source inner join target_supplier_df_threshold_vw as databricks on source.s_suppdate <=> databricks.s_suppdate and
        source.s_suppkey <=> databricks.s_suppkey where (1 = 1 or 1 = 1) or (coalesce(source.s_acctbal, 0) -
        coalesce(databricks.s_acctbal, 0)) <> 0 or (coalesce(unix_timestamp(source.s_suppdate), 0) -
        coalesce(unix_timestamp(databricks.s_suppdate), 0)) <> 0""".strip().lower(),
    )


def test_build_threshold_query_with_single_threshold(table_conf_with_opts, schema):
    table_conf = table_conf_with_opts
    table_conf.jdbc_reader_options = None
    table_conf.transformations = [
        Transformation(column_name="s_acctbal", source="trim(s_acctbal)", target="trim(s_acctbal)")
    ]
    src_schema, tgt_schema = schema
    src_query = ThresholdQueryBuilder(table_conf, src_schema, "source", "oracle").build_threshold_query()
    target_query = ThresholdQueryBuilder(table_conf, tgt_schema, "target", "databricks").build_threshold_query()
    assert src_query == (
        "SELECT TRIM(s_acctbal) AS s_acctbal, COALESCE(TRIM(s_nationkey), '') AS s_nationkey, "
        "COALESCE(TRIM(s_suppkey), '') AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address = 'a'"
    )
    assert target_query == (
        "SELECT TRIM(s_acctbal) AS s_acctbal, COALESCE(TRIM(s_nationkey_t), '') AS s_nationkey, "
        "COALESCE(TRIM(s_suppkey_t), '') AS s_suppkey FROM :tbl WHERE s_name = 't' AND "
        "s_address_t = 'a'"
    )


def test_build_threshold_query_with_multiple_threshold(table_conf_with_opts, schema):
    table_conf = table_conf_with_opts
    table_conf.jdbc_reader_options = JdbcReaderOptions(
        number_partitions=100, partition_column="s_phone", lower_bound="0", upper_bound="100"
    )
    table_conf.thresholds = [
        Thresholds(column_name="s_acctbal", lower_bound="5%", upper_bound="-5%", type="float"),
        Thresholds(column_name="s_suppdate", lower_bound="-86400", upper_bound="86400", type="timestamp"),
    ]
    table_conf.filters = None
    src_schema, tgt_schema = schema
    src_schema.append(Schema("s_suppdate", "timestamp"))
    tgt_schema.append(Schema("s_suppdate", "timestamp"))
    src_query = ThresholdQueryBuilder(table_conf, src_schema, "source", "oracle").build_threshold_query()
    target_query = ThresholdQueryBuilder(table_conf, tgt_schema, "target", "databricks").build_threshold_query()
    assert src_query == (
        "SELECT COALESCE(TRIM(s_acctbal), '') AS s_acctbal, COALESCE(TRIM(s_nationkey), "
        "'') AS s_nationkey, TRIM(s_phone) AS s_phone, COALESCE(TRIM(s_suppdate), '') AS s_suppdate, "
        "COALESCE(TRIM(s_suppkey), '') AS s_suppkey FROM :tbl"
    )
    assert target_query == (
        "SELECT COALESCE(TRIM(s_acctbal_t), '') AS s_acctbal, COALESCE(TRIM(s_nationkey_t), "
        "'') AS s_nationkey, COALESCE(TRIM(s_suppdate), '') AS s_suppdate, COALESCE(TRIM("
        "s_suppkey_t), '') AS s_suppkey FROM :tbl"
    )
