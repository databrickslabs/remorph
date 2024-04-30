import re

from databricks.labs.remorph.reconcile.query_builder.threshold_query import (
    ThresholdQueryBuilder,
)
from databricks.labs.remorph.reconcile.recon_config import Schema, Thresholds


def test_threshold_comparison_query_with_one_threshold(table_conf_with_opts, schema):
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
        100 then `warning` else `failed` end as s_acctbal_match, source.s_suppkey as s_suppkey_source from 
        supplier_df_threshold_vw as source inner join target_supplier_df_threshold_vw as databricks on 
        source.s_suppkey <=> databricks.s_suppkey where (1 = 1 or 1 = 1) or (coalesce(source.s_acctbal, 0) - 
        coalesce(databricks.s_acctbal, 0)) <> 0""".strip().lower(),
    )


def test_threshold_comparison_query_with_dual_threshold(table_conf_with_opts, schema):
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
