from unittest.mock import patch

import pytest
from pyspark.sql import Row, SparkSession

from pyspark.testing import assertDataFrameEqual

from databricks.labs.remorph.config import TableRecon
from databricks.labs.remorph.reconcile.exception import ReconciliationException, InvalidInputException
from databricks.labs.remorph.reconcile.execute import recon
from databricks.labs.remorph.reconcile.recon_config import (
    Table,
    ColumnMapping,
    StatusOutput,
    Filters,
    Transformation,
    Thresholds,
)
from tests.integration.test_utils import get_reports


def test_execute_report_type_is_data_with_all_match(request):
    _metadata_config = request.config.reconcile_config.metadata_config
    request.config.reconcile_config.report_type = 'data'
    recon_id = "11111-db-data_with_all_match"
    table_recon = TableRecon(
        source_schema=_metadata_config.schema,
        source_catalog=_metadata_config.catalog,
        target_schema=_metadata_config.schema,
        target_catalog=_metadata_config.catalog,
        tables=[
            Table(
                source_name=request.config.test_config.db_mock_src,
                target_name=request.config.test_config.db_mock_tgt,
                jdbc_reader_options=None,
                select_columns=None,
                drop_columns=["l_tax"],
                join_columns=["l_orderkey", "l_linenumber"],
                column_mapping=[
                    ColumnMapping(source_name="l_orderkey", target_name="l_orderkey_t"),
                    ColumnMapping(source_name="l_partkey", target_name="l_partkey_t"),
                    ColumnMapping(source_name="l_suppkey", target_name="l_suppkey_t"),
                    ColumnMapping(source_name="l_linenumber", target_name="l_linenumber_t"),
                    ColumnMapping(source_name="l_shipmode", target_name="l_shipmode_t"),
                    ColumnMapping(source_name="l_comment", target_name="l_comment_t"),
                ],
                transformations=None,
                thresholds=None,
                filters=Filters(source="l_linenumber=1", target="l_linenumber_t=1"),
            )
        ],
    )
    with patch("databricks.labs.remorph.reconcile.execute.uuid4", return_value=recon_id):
        recon_result = recon(
            ws=request.config.ws,
            spark=SparkSession.getActiveSession(),
            table_recon=table_recon,
            reconcile_config=request.config.reconcile_config,
        )
    assert recon_result.results[0].status == StatusOutput(row=True, column=True, schema=None)
    assert recon_result.results[0].exception_message == ''
    assert (
        recon_result.results[0].source_table_name == f"{_metadata_config.catalog}."
        f"{_metadata_config.schema}."
        f"{request.config.test_config.db_mock_src}"
    )
    assert (
        recon_result.results[0].target_table_name == f"{_metadata_config.catalog}."
        f"{_metadata_config.schema}."
        f"{request.config.test_config.db_mock_tgt}"
    )


def test_execute_report_type_is_all(request):
    _metadata_config = request.config.reconcile_config.metadata_config
    spark = SparkSession.getActiveSession()
    request.config.reconcile_config.report_type = 'all'
    recon_id = "22222-db-data_with_all"
    key_columns = ["l_orderkey", "l_linenumber"]
    table_recon = TableRecon(
        source_schema=_metadata_config.schema,
        source_catalog=_metadata_config.catalog,
        target_schema=_metadata_config.schema,
        target_catalog=_metadata_config.catalog,
        tables=[
            Table(
                source_name=request.config.test_config.db_mock_src,
                target_name=request.config.test_config.db_mock_tgt,
                jdbc_reader_options=None,
                select_columns=None,
                drop_columns=None,
                join_columns=key_columns,
                column_mapping=[
                    ColumnMapping(source_name="l_orderkey", target_name="l_orderkey_t"),
                    ColumnMapping(source_name="l_partkey", target_name="l_partkey_t"),
                    ColumnMapping(source_name="l_suppkey", target_name="l_suppkey_t"),
                    ColumnMapping(source_name="l_linenumber", target_name="l_linenumber_t"),
                    ColumnMapping(source_name="l_shipmode", target_name="l_shipmode_t"),
                    ColumnMapping(source_name="l_comment", target_name="l_comment_t"),
                ],
                transformations=[Transformation(column_name='l_tax', source='CAST(l_tax AS DECIMAL(18, 2))')],
                thresholds=[Thresholds(column_name="l_discount", lower_bound='-10%', upper_bound='10%', type='int')],
                filters=None,
            )
        ],
    )

    with (
        patch("databricks.labs.remorph.reconcile.execute.uuid4", return_value=recon_id),
        pytest.raises(ReconciliationException) as exc_info,
    ):
        recon(
            ws=request.config.ws, spark=spark, table_recon=table_recon, reconcile_config=request.config.reconcile_config
        )
    assert "Reconciliation failed for one or more tables. Please check the recon metrics for more details." in str(
        exc_info.value
    )

    reports = get_reports(spark, request.config.reconcile_config, recon_id, key_columns)

    assertDataFrameEqual(reports.missing_in_src, spark.createDataFrame([('5', '5')], ['l_orderkey', 'l_linenumber']))
    assertDataFrameEqual(reports.missing_in_tgt, spark.createDataFrame([('4', '4')], ['l_orderkey', 'l_linenumber']))
    assertDataFrameEqual(reports.mismatch, spark.createDataFrame([('3', '3')], ['l_orderkey', 'l_linenumber']))
    assertDataFrameEqual(
        reports.threshold_mismatch, spark.createDataFrame([('3', '3')], ['l_orderkey_source', 'l_linenumber_source'])
    )
    assert reports.metrics == Row(
        recon_metrics=Row(
            row_comparison=Row(missing_in_source=1, missing_in_target=1),
            column_comparison=Row(
                absolute_mismatch=1, threshold_mismatch=1, mismatch_columns='l_quantity,l_receiptdate'
            ),
            schema_comparison=False,
        )
    )


def test_execute_report_type_is_schema(request):
    _metadata_config = request.config.reconcile_config.metadata_config
    request.config.reconcile_config.report_type = 'schema'
    spark = SparkSession.getActiveSession()
    recon_id = "33333-db-schema"
    table_recon = TableRecon(
        source_schema=_metadata_config.schema,
        source_catalog=_metadata_config.catalog,
        target_schema=_metadata_config.schema,
        target_catalog=_metadata_config.catalog,
        tables=[
            Table(
                source_name=request.config.test_config.db_mock_src,
                target_name=request.config.test_config.db_mock_tgt,
                jdbc_reader_options=None,
                select_columns=None,
                drop_columns=None,
                join_columns=None,
                column_mapping=[
                    ColumnMapping(source_name="l_orderkey", target_name="l_orderkey_t"),
                    ColumnMapping(source_name="l_partkey", target_name="l_partkey_t"),
                    ColumnMapping(source_name="l_suppkey", target_name="l_suppkey_t"),
                    ColumnMapping(source_name="l_linenumber", target_name="l_linenumber_t"),
                    ColumnMapping(source_name="l_shipmode", target_name="l_shipmode_t"),
                    ColumnMapping(source_name="l_comment", target_name="l_comment_t"),
                ],
                transformations=[Transformation(column_name='l_tax', source='CAST(l_tax AS DECIMAL(18, 2))')],
                thresholds=[Thresholds(column_name="l_discount", lower_bound='-10%', upper_bound='10%', type='int')],
                filters=None,
            )
        ],
    )

    with (
        patch("databricks.labs.remorph.reconcile.execute.uuid4", return_value=recon_id),
        pytest.raises(ReconciliationException) as exc_info,
    ):
        recon(
            ws=request.config.ws, spark=spark, table_recon=table_recon, reconcile_config=request.config.reconcile_config
        )
    assert "Reconciliation failed for one or more tables. Please check the recon metrics for more details." in str(
        exc_info.value
    )

    reports = get_reports(spark, request.config.reconcile_config, recon_id)

    assertDataFrameEqual(
        reports.schema_validation,
        spark.createDataFrame(
            [('l_tax', 'double', 'decimal(18,2)', 'false')],
            ['source_column', 'source_datatype', 'databricks_datatype', 'is_valid'],
        ),
    )


def test_execute_report_type_is_row(request, caplog):
    _metadata_config = request.config.reconcile_config.metadata_config
    request.config.reconcile_config.report_type = 'row'
    recon_id = "44444-db-row"
    spark = SparkSession.getActiveSession()
    key_columns = ["l_orderkey", "l_linenumber"]
    table_recon = TableRecon(
        source_schema=_metadata_config.schema,
        source_catalog=_metadata_config.catalog,
        target_schema=_metadata_config.schema,
        target_catalog=_metadata_config.catalog,
        tables=[
            Table(
                source_name=request.config.test_config.db_mock_src,
                target_name=request.config.test_config.db_mock_tgt,
                jdbc_reader_options=None,
                select_columns=None,
                drop_columns=None,
                join_columns=key_columns,
                column_mapping=[
                    ColumnMapping(source_name="l_orderkey", target_name="l_orderkey_t"),
                    ColumnMapping(source_name="l_partkey", target_name="l_partkey_t"),
                    ColumnMapping(source_name="l_suppkey", target_name="l_suppkey_t"),
                    ColumnMapping(source_name="l_linenumber", target_name="l_linenumber_t"),
                    ColumnMapping(source_name="l_shipmode", target_name="l_shipmode_t"),
                    ColumnMapping(source_name="l_comment", target_name="l_comment_t"),
                ],
                transformations=[Transformation(column_name='l_tax', source='CAST(l_tax AS DECIMAL(18, 2))')],
                thresholds=[Thresholds(column_name="l_discount", lower_bound='-10%', upper_bound='10%', type='int')],
                filters=None,
            )
        ],
    )

    with (
        patch("databricks.labs.remorph.reconcile.execute.uuid4", return_value=recon_id),
        pytest.raises(ReconciliationException) as exc_info,
    ):
        recon(
            ws=request.config.ws, spark=spark, table_recon=table_recon, reconcile_config=request.config.reconcile_config
        )
    assert "Reconciliation failed for one or more tables. Please check the recon metrics for more details." in str(
        exc_info.value
    )

    reports = get_reports(spark, request.config.reconcile_config, recon_id, key_columns)

    assertDataFrameEqual(
        reports.missing_in_src, spark.createDataFrame([('3', '3'), ('5', '5')], ['l_orderkey', 'l_linenumber'])
    )
    assertDataFrameEqual(
        reports.missing_in_tgt, spark.createDataFrame([('3', '3'), ('4', '4')], ['l_orderkey', 'l_linenumber'])
    )
    assert reports.mismatch is None
    assert reports.threshold_mismatch is None
    assert reports.schema_validation.isEmpty()
    assert reports.metrics == Row(
        recon_metrics=Row(
            row_comparison=Row(missing_in_source=2, missing_in_target=2),
            column_comparison=None,
            schema_comparison=None,
        )
    )
    assert "Threshold comparison is ignored for 'row' report type" in caplog.text


def test_execute_fail_for_tables_not_available(request):
    _metadata_config = request.config.reconcile_config.metadata_config
    request.config.reconcile_config.report_type = 'all'
    recon_id = "44444-db-table-not-found"
    spark = SparkSession.getActiveSession()
    table_recon = TableRecon(
        source_schema=_metadata_config.schema,
        source_catalog=_metadata_config.catalog,
        target_schema=_metadata_config.schema,
        target_catalog=_metadata_config.catalog,
        tables=[
            Table(
                source_name="remorph_src_unknown",
                target_name="remorph_tgt_unknown",
                jdbc_reader_options=None,
                select_columns=None,
                drop_columns=None,
                join_columns=["id"],
                column_mapping=None,
                transformations=None,
                thresholds=None,
                filters=None,
            )
        ],
    )

    with (
        patch("databricks.labs.remorph.reconcile.execute.uuid4", return_value=recon_id),
        pytest.raises(ReconciliationException) as exc_info,
    ):
        recon(
            ws=request.config.ws, spark=spark, table_recon=table_recon, reconcile_config=request.config.reconcile_config
        )

        assert (
            "[TABLE_OR_VIEW_NOT_FOUND] The table or view `remorph_integration_test`.`test`.`remorph_src_unknown`"
            "cannot be found"
        ) in str(exc_info.value)


def test_execute_report_type_is_data_with_all_without_keys(request):
    _metadata_config = request.config.reconcile_config.metadata_config
    request.config.reconcile_config.report_type = 'data'
    recon_id = "66666-db-data_with_all_match"
    table_recon = TableRecon(
        source_schema=_metadata_config.schema,
        source_catalog=_metadata_config.catalog,
        target_schema=_metadata_config.schema,
        target_catalog=_metadata_config.catalog,
        tables=[
            Table(
                source_name=request.config.test_config.db_mock_src,
                target_name=request.config.test_config.db_mock_tgt,
                jdbc_reader_options=None,
                select_columns=None,
                drop_columns=["l_tax"],
                join_columns=None,
                column_mapping=[
                    ColumnMapping(source_name="l_orderkey", target_name="l_orderkey_t"),
                    ColumnMapping(source_name="l_partkey", target_name="l_partkey_t"),
                    ColumnMapping(source_name="l_suppkey", target_name="l_suppkey_t"),
                    ColumnMapping(source_name="l_linenumber", target_name="l_linenumber_t"),
                    ColumnMapping(source_name="l_shipmode", target_name="l_shipmode_t"),
                    ColumnMapping(source_name="l_comment", target_name="l_comment_t"),
                ],
                transformations=None,
                thresholds=None,
                filters=Filters(source="l_linenumber=1", target="l_linenumber_t=1"),
            )
        ],
    )
    with (
        patch("databricks.labs.remorph.reconcile.execute.uuid4", return_value=recon_id),
        pytest.raises(InvalidInputException) as exc_info,
    ):
        recon(
            ws=request.config.ws,
            spark=SparkSession.getActiveSession(),
            table_recon=table_recon,
            reconcile_config=request.config.reconcile_config,
        )
    assert "target table in source layer --> Join Columns are compulsory for data type" in str(exc_info.value)
