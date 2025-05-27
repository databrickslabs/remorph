from pyspark import Row

from databricks.labs.remorph.reconcile.recon_config import AggregateRule
from databricks.labs.remorph.reconcile.recon_output_config import DataReconcileOutput, MismatchOutput


def expected_reconcile_output_dict(spark_session):
    count_reconcile_output = DataReconcileOutput(
        mismatch_count=1,
        missing_in_src_count=1,
        missing_in_tgt_count=1,
        mismatch=MismatchOutput(
            mismatch_columns=None,
            mismatch_df=spark_session.createDataFrame(
                [
                    Row(
                        source_count_s_name=11,
                        target_count_s_name=9,
                        source_group_by_s_nationkey=12,
                        target_group_by_s_nationkey=12,
                        match_count_s_name=False,
                        match_group_by_s_nationkey=True,
                        agg_data_match=False,
                    )
                ]
            ),
        ),
        missing_in_src=spark_session.createDataFrame([Row(target_count_s_name=76, target_group_by_s_nationkey=14)]),
        missing_in_tgt=spark_session.createDataFrame([Row(source_count_s_name=21, source_group_by_s_nationkey=13)]),
    )

    sum_reconcile_output = DataReconcileOutput(
        mismatch_count=1,
        missing_in_src_count=1,
        missing_in_tgt_count=1,
        mismatch=MismatchOutput(
            mismatch_columns=None,
            mismatch_df=spark_session.createDataFrame(
                [
                    Row(
                        source_sum_s_acctbal=23,
                        target_sum_s_acctbal=43,
                        source_group_by_s_nationkey=12,
                        target_group_by_s_nationkey=12,
                        match_sum_s_acctbal=False,
                        match_group_by_s_nationkey=True,
                        agg_data_match=False,
                    )
                ]
            ),
        ),
        missing_in_src=spark_session.createDataFrame([Row(target_sum_s_acctbal=348, target_group_by_s_nationkey=14)]),
        missing_in_tgt=spark_session.createDataFrame([Row(source_sum_s_acctbal=112, source_group_by_s_nationkey=13)]),
    )

    return {"count": count_reconcile_output, "sum": sum_reconcile_output}


def expected_rule_output():
    count_rule_output = AggregateRule(
        agg_type="count",
        agg_column="s_name",
        group_by_columns=["s_nationkey"],
        group_by_columns_as_str="s_nationkey",
    )

    sum_rule_output = AggregateRule(
        agg_type="sum",
        agg_column="s_acctbal",
        group_by_columns=["s_nationkey"],
        group_by_columns_as_str="s_nationkey",
    )

    return {"count": count_rule_output, "sum": sum_rule_output}
