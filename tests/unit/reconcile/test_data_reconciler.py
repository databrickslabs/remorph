from pyspark import Row
from pyspark.testing import assertDataFrameEqual

from databricks.labs.remorph.reconcile.recon_config import ReconcileOutput
from databricks.labs.remorph.reconcile.data_reconciler import DataReconciler


def test_compare_data_for_report_all(mock_spark_session):
    source = mock_spark_session.createDataFrame(
        [
            Row(s_suppkey=1, s_nationkey=11, hash_value_recon='1a1'),
            Row(s_suppkey=2, s_nationkey=22, hash_value_recon='2b2'),
            Row(s_suppkey=3, s_nationkey=33, hash_value_recon='3c3'),
            Row(s_suppkey=5, s_nationkey=55, hash_value_recon='5e5'),
        ]
    )
    target = mock_spark_session.createDataFrame(
        [
            Row(s_suppkey=1, s_nationkey=11, hash_value_recon='1a1'),
            Row(s_suppkey=2, s_nationkey=22, hash_value_recon='2b4'),
            Row(s_suppkey=4, s_nationkey=44, hash_value_recon='4d4'),
            Row(s_suppkey=5, s_nationkey=56, hash_value_recon='5e6'),
        ]
    )

    mismatch = mock_spark_session.createDataFrame([Row(s_suppkey=2, s_nationkey=22)])
    missing_in_src = mock_spark_session.createDataFrame(
        [Row(s_suppkey=4, s_nationkey=44), Row(s_suppkey=5, s_nationkey=56)]
    )
    missing_in_tgt = mock_spark_session.createDataFrame(
        [Row(s_suppkey=3, s_nationkey=33), Row(s_suppkey=5, s_nationkey=55)]
    )

    actual = DataReconciler().compare_data(
        source=source, target=target, join_cols=["s_suppkey", "s_nationkey"], report_type="all"
    )
    expected = ReconcileOutput(missing_in_src=missing_in_src, missing_in_tgt=missing_in_tgt, mismatch=mismatch)

    assertDataFrameEqual(actual.mismatch, expected.mismatch)
    assertDataFrameEqual(actual.missing_in_src, expected.missing_in_src)
    assertDataFrameEqual(actual.missing_in_tgt, expected.missing_in_tgt)


def test_compare_data_for_report_hash(mock_spark_session):
    source = mock_spark_session.createDataFrame(
        [
            Row(s_suppkey=1, s_nationkey=11, hash_value_recon='1a1'),
            Row(s_suppkey=2, s_nationkey=22, hash_value_recon='2b2'),
            Row(s_suppkey=3, s_nationkey=33, hash_value_recon='3c3'),
            Row(s_suppkey=5, s_nationkey=55, hash_value_recon='5e5'),
        ]
    )
    target = mock_spark_session.createDataFrame(
        [
            Row(s_suppkey=1, s_nationkey=11, hash_value_recon='1a1'),
            Row(s_suppkey=2, s_nationkey=22, hash_value_recon='2b4'),
            Row(s_suppkey=4, s_nationkey=44, hash_value_recon='4d4'),
            Row(s_suppkey=5, s_nationkey=56, hash_value_recon='5e6'),
        ]
    )

    missing_in_src = mock_spark_session.createDataFrame(
        [Row(s_suppkey=2, s_nationkey=22), Row(s_suppkey=4, s_nationkey=44), Row(s_suppkey=5, s_nationkey=56)]
    )
    missing_in_tgt = mock_spark_session.createDataFrame(
        [Row(s_suppkey=2, s_nationkey=22), Row(s_suppkey=3, s_nationkey=33), Row(s_suppkey=5, s_nationkey=55)]
    )

    actual = DataReconciler().compare_data(
        source=source, target=target, join_cols=["s_suppkey", "s_nationkey"], report_type="hash"
    )
    expected = ReconcileOutput(missing_in_src=missing_in_src, missing_in_tgt=missing_in_tgt, mismatch=None)

    assert actual.mismatch == expected.mismatch
    assertDataFrameEqual(actual.missing_in_src, expected.missing_in_src)
    assertDataFrameEqual(actual.missing_in_tgt, expected.missing_in_tgt)
