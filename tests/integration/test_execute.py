import pytest
from pyspark.sql.functions import col, expr
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    LongType,
    DecimalType,
    DateType,
    DoubleType,
)
from pyspark.sql import Row
from datetime import datetime
import decimal

from databricks.labs.remorph.config import TableRecon
from databricks.labs.remorph.reconcile.exception import ReconciliationException
from databricks.labs.remorph.reconcile.execute import recon
from databricks.labs.remorph.reconcile.recon_config import (
    Table,
    ColumnMapping,
    StatusOutput,
    Filters,
    Transformation,
    Thresholds,
)


@pytest.fixture
def setup_databricks_src(setup_teardown, spark, test_config):
    src_schema = StructType(
        [
            StructField("l_orderkey", LongType(), True),
            StructField("l_partkey", LongType(), True),
            StructField("l_suppkey", LongType(), True),
            StructField("l_linenumber", IntegerType(), True),
            StructField("l_quantity", DecimalType(18, 2), True),
            StructField("l_extendedprice", DecimalType(18, 2), True),
            StructField("l_discount", DecimalType(18, 2), True),
            StructField("l_tax", DoubleType(), True),
            StructField("l_returnflag", StringType(), True),
            StructField("l_linestatus", StringType(), True),
            StructField("l_shipdate", DateType(), True),
            StructField("l_commitdate", DateType(), True),
            StructField("l_receiptdate", DateType(), True),
            StructField("l_shipinstruct", StringType(), True),
            StructField("l_shipmode", StringType(), True),
            StructField("l_comment", StringType(), True),
        ]
    )

    tgt_schema = StructType(
        [
            StructField("l_orderkey_t", LongType(), True),
            StructField("l_partkey_t", LongType(), True),
            StructField("l_suppkey_t", LongType(), True),
            StructField("l_linenumber_t", IntegerType(), True),
            StructField("l_quantity", DecimalType(18, 2), True),
            StructField("l_extendedprice", DecimalType(18, 2), True),
            StructField("l_discount", DecimalType(18, 2), True),
            StructField("l_tax", DecimalType(18, 2), True),
            StructField("l_returnflag", StringType(), True),
            StructField("l_linestatus", StringType(), True),
            StructField("l_shipdate", DateType(), True),
            StructField("l_commitdate", DateType(), True),
            StructField("l_receiptdate", DateType(), True),
            StructField("l_shipinstruct", StringType(), True),
            StructField("l_shipmode_t", StringType(), True),
            StructField("l_comment_t", StringType(), True),
        ]
    )

    src_data = spark.createDataFrame(
        data=[
            Row(
                l_orderkey=1,
                l_partkey=11,
                l_suppkey=111,
                l_linenumber=1,
                l_quantity=decimal.Decimal("1.0"),
                l_extendedprice=decimal.Decimal("100.0"),
                l_discount=decimal.Decimal("0.1"),
                l_tax=1.0,
                l_returnflag="A",
                l_linestatus="F",
                l_shipdate=datetime.strptime("2019-01-01", "%Y-%m-%d").date(),
                l_commitdate=datetime.strptime("2019-01-05", "%Y-%m-%d").date(),
                l_receiptdate=datetime.strptime("2019-01-04", "%Y-%m-%d").date(),
                l_shipinstruct="DELIVER IN PERSON",
                l_shipmode="MAIL",
                l_comment="test",
            ),
            Row(
                l_orderkey=2,
                l_partkey=22,
                l_suppkey=222,
                l_linenumber=2,
                l_quantity=decimal.Decimal("2.0"),
                l_extendedprice=decimal.Decimal("200.0"),
                l_discount=decimal.Decimal("0.21"),
                l_tax=2.0,
                l_returnflag="A",
                l_linestatus="F",
                l_shipdate=datetime.strptime("2019-02-02", "%Y-%m-%d").date(),
                l_commitdate=datetime.strptime("2019-02-05", "%Y-%m-%d").date(),
                l_receiptdate=datetime.strptime("2019-02-04", "%Y-%m-%d").date(),
                l_shipinstruct="DELIVER IN PERSON",
                l_shipmode="MAIL",
                l_comment="test",
            ),
            Row(
                l_orderkey=3,
                l_partkey=33,
                l_suppkey=333,
                l_linenumber=3,
                l_quantity=decimal.Decimal("33.0"),
                l_extendedprice=decimal.Decimal("300.0"),
                l_discount=decimal.Decimal("0.3"),
                l_tax=3.0,
                l_returnflag="A",
                l_linestatus="F",
                l_shipdate=datetime.strptime("2019-03-01", "%Y-%m-%d").date(),
                l_commitdate=datetime.strptime("2019-03-05", "%Y-%m-%d").date(),
                l_receiptdate=datetime.strptime("2019-03-04", "%Y-%m-%d").date(),
                l_shipinstruct="DELIVER IN PERSON",
                l_shipmode="MAIL",
                l_comment="test",
            ),
            Row(
                l_orderkey=4,
                l_partkey=44,
                l_suppkey=444,
                l_linenumber=4,
                l_quantity=decimal.Decimal("4.0"),
                l_extendedprice=decimal.Decimal("400.0"),
                l_discount=decimal.Decimal("0.4"),
                l_tax=4.0,
                l_returnflag="A",
                l_linestatus="F",
                l_shipdate=datetime.strptime("2019-04-01", "%Y-%m-%d").date(),
                l_commitdate=datetime.strptime("2019-04-05", "%Y-%m-%d").date(),
                l_receiptdate=datetime.strptime("2019-04-04", "%Y-%m-%d").date(),
                l_shipinstruct="DELIVER IN PERSON",
                l_shipmode="MAIL",
                l_comment="test",
            ),
        ],
        schema=src_schema,
    )

    tgt_data = spark.createDataFrame(
        data=[
            Row(
                l_orderkey_t=1,
                l_partkey_t=11,
                l_suppkey_t=111,
                l_linenumber_t=1,
                l_quantity=decimal.Decimal("1.0"),
                l_extendedprice=decimal.Decimal("100.0"),
                l_discount=decimal.Decimal("0.1"),
                l_tax=decimal.Decimal("1.0"),
                l_returnflag="A",
                l_linestatus="F",
                l_shipdate=datetime.strptime("2019-01-01", "%Y-%m-%d").date(),
                l_commitdate=datetime.strptime("2019-01-05", "%Y-%m-%d").date(),
                l_receiptdate=datetime.strptime("2019-01-04", "%Y-%m-%d").date(),
                l_shipinstruct="DELIVER IN PERSON",
                l_shipmode_t="MAIL",
                l_comment_t="test",
            ),
            Row(
                l_orderkey_t=2,
                l_partkey_t=22,
                l_suppkey_t=222,
                l_linenumber_t=2,
                l_quantity_t=decimal.Decimal("2.0"),
                l_extendedprice=decimal.Decimal("200.0"),
                l_discount=decimal.Decimal("0.20"),
                l_tax=decimal.Decimal("2.0"),
                l_returnflag="A",
                l_linestatus="F",
                l_shipdate=datetime.strptime("2019-02-02", "%Y-%m-%d").date(),
                l_commitdate=datetime.strptime("2019-02-05", "%Y-%m-%d").date(),
                l_receiptdate=datetime.strptime("2019-02-04", "%Y-%m-%d").date(),
                l_shipinstruct="DELIVER IN PERSON",
                l_shipmode_t="MAIL",
                l_comment_t="test",
            ),
            Row(
                l_orderkey_t=3,
                l_partkey_t=33,
                l_suppkey_t=333,
                l_linenumber_t=3,
                l_quantity=decimal.Decimal("3.0"),
                l_extendedprice=decimal.Decimal("300.0"),
                l_discount=decimal.Decimal("0.35"),
                l_tax=decimal.Decimal("3.0"),
                l_returnflag="A",
                l_linestatus="F",
                l_shipdate=datetime.strptime("2019-03-01", "%Y-%m-%d").date(),
                l_commitdate=datetime.strptime("2019-03-05", "%Y-%m-%d").date(),
                l_receiptdate=datetime.strptime("2019-03-05", "%Y-%m-%d").date(),
                l_shipinstruct="DELIVER IN PERSON",
                l_shipmode_t="MAIL",
                l_comment_t="test",
            ),
            Row(
                l_orderkey_t=5,
                l_partkey_t=55,
                l_suppkey_t=555,
                l_linenumber_t=5,
                l_quantity=decimal.Decimal("5.0"),
                l_extendedprice=decimal.Decimal("500.0"),
                l_discount=decimal.Decimal("0.5"),
                l_tax=decimal.Decimal("5.0"),
                l_returnflag="A",
                l_linestatus="F",
                l_shipdate=datetime.strptime("2019-04-01", "%Y-%m-%d").date(),
                l_commitdate=datetime.strptime("2019-05-05", "%Y-%m-%d").date(),
                l_receiptdate=datetime.strptime("2019-05-04", "%Y-%m-%d").date(),
                l_shipinstruct="DELIVER IN PERSON",
                l_shipmode_t="MAIL",
                l_comment_t="test",
            ),
        ],
        schema=tgt_schema,
    )

    src_data.write.format("delta").mode("overwrite").saveAsTable(
        f"{test_config.db_mock_catalog}." f"{test_config.db_mock_schema}.{test_config.db_mock_src}"
    )
    tgt_data.write.format("delta").mode("overwrite").saveAsTable(
        f"{test_config.db_mock_catalog}." f"{test_config.db_mock_schema}.{test_config.db_mock_tgt}"
    )


def test_execute_databricks_src_data_match(setup_databricks_src, spark, ws, test_config, reconcile_config):
    table_recon = TableRecon(
        source_schema=test_config.db_mock_schema,
        source_catalog=test_config.db_mock_catalog,
        target_schema=test_config.db_mock_schema,
        target_catalog=test_config.db_mock_catalog,
        tables=[
            Table(
                source_name=test_config.db_mock_src,
                target_name=test_config.db_mock_tgt,
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

    recon_result = recon(ws=ws, spark=spark, table_recon=table_recon, reconcile_config=reconcile_config)
    assert recon_result.results[0].status == StatusOutput(row=True, column=True, schema=True)
    assert recon_result.results[0].exception_message == ''
    assert (
        recon_result.results[0].source_table_name
        == f"{test_config.db_mock_catalog}.{test_config.db_mock_schema}.lineitem_src"
    )
    assert (
        recon_result.results[0].target_table_name
        == f"{test_config.db_mock_catalog}.{test_config.db_mock_schema}.lineitem_tgt"
    )


def test_execute_databricks_src(ws, spark, setup_databricks_src, test_config, reconcile_config):
    table_recon = TableRecon(
        source_schema=test_config.db_mock_schema,
        source_catalog=test_config.db_mock_catalog,
        target_schema=test_config.db_mock_schema,
        target_catalog=test_config.db_mock_catalog,
        tables=[
            Table(
                source_name=test_config.db_mock_src,
                target_name=test_config.db_mock_tgt,
                jdbc_reader_options=None,
                select_columns=None,
                drop_columns=None,
                join_columns=["l_orderkey", "l_linenumber"],
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

    with pytest.raises(ReconciliationException) as excinfo:
        recon(ws=ws, spark=spark, table_recon=table_recon, reconcile_config=reconcile_config)
    assert "Reconciliation failed for one or more tables. Please check the recon metrics for more details." in str(
        excinfo.value
    )

    validation_df = spark.sql(
        f"""SELECT main.start_ts,recon_id,source_type,source_table,target_table,recon_type,status,recon_metrics,
        run_metrics,data as sample_data FROM (SELECT * FROM 
        {test_config.db_mock_catalog}.{test_config.db_mock_schema}.main WHERE main.start_ts = 
        (SELECT MAX(start_ts) FROM {test_config.db_mock_catalog}.{test_config.db_mock_schema}.main)) AS main 
        JOIN {test_config.db_mock_catalog}.{test_config.db_mock_schema}.metrics as metrics ON main.recon_table_id = 
        metrics.recon_table_id LEFT JOIN {test_config.db_mock_catalog}.{test_config.db_mock_schema}.details ON 
        main.recon_table_id = details.recon_table_id ORDER BY main.start_ts desc,
        main.recon_id,main.recon_table_id"""
    )

    schema_validation = (
        validation_df.filter(col('recon_type') == 'schema')
        .select(
            col('status'), expr("filter(sample_data, sch -> sch.source_column = 'l_tax')" "[0] as schema_mismatch")
        )
        .select(
            col('status'),
            col('schema_mismatch.source_column').alias('column_name'),
            col('schema_mismatch.source_datatype').alias('source_datatype'),
            col('schema_mismatch.databricks_datatype').alias('target_datatype'),
            col('schema_mismatch.is_valid').alias('is_valid'),
        )
        .collect()
    )

    missing_in_source = (
        validation_df.filter(col('recon_type') == 'missing_in_source')
        .select(
            col('recon_metrics.row_comparison.missing_in_source').alias('missing_count'),
            col('sample_data').getItem(0).getField('l_linenumber').alias('l_linenumber'),
            col('sample_data').getItem(0).getField('l_orderkey').alias('l_orderkey'),
        )
        .collect()
    )

    missing_in_target = (
        validation_df.filter(col('recon_type') == 'missing_in_target')
        .select(
            col('recon_metrics.row_comparison.missing_in_target').alias('missing_count'),
            col('sample_data').getItem(0).getField('l_linenumber').alias('l_linenumber'),
            col('sample_data').getItem(0).getField('l_orderkey').alias('l_orderkey'),
        )
        .collect()
    )
    mismatch = (
        validation_df.filter(col('recon_type') == 'mismatch')
        .select(
            col('recon_metrics.column_comparison.absolute_mismatch').alias('mismatch_count'),
            col('recon_metrics.column_comparison.mismatch_columns').alias('mismatch_columns'),
            col('sample_data').getItem(0).getField('l_linenumber').alias('l_linenumber'),
            col('sample_data').getItem(0).getField('l_orderkey').alias('l_orderkey'),
        )
        .collect()
    )
    threshold_mismatch = (
        validation_df.filter(col('recon_type') == 'threshold_mismatch')
        .select(
            col('recon_metrics.column_comparison.threshold_mismatch').alias('threshold_mismatch_count'),
            col('sample_data').getItem(0).getField('l_linenumber_source').alias('l_linenumber'),
            col('sample_data').getItem(0).getField('l_orderkey_source').alias('l_orderkey'),
        )
        .collect()
    )

    assert missing_in_source == [Row(missing_count=1, l_linenumber='5', l_orderkey='5')]
    assert missing_in_target == [Row(missing_count=1, l_linenumber='4', l_orderkey='4')]
    assert schema_validation == [
        Row(
            status=False,
            column_name='l_tax',
            source_datatype='double',
            target_datatype='decimal(18,2)',
            is_valid='false',
        )
    ]
    assert mismatch == [
        Row(mismatch_count=1, mismatch_columns="l_quantity,l_receiptdate", l_line_number='3', l_orderkey='3')
    ]
    assert threshold_mismatch == [Row(threshold_mismatch_count=1, l_linenumber='3', l_orderkey='3')]


def test_execute_fail_for_tables_not_available(ws, spark, setup_databricks_src, test_config, reconcile_config):
    table_recon = TableRecon(
        source_schema=test_config.db_mock_schema,
        source_catalog=test_config.db_mock_catalog,
        target_schema=test_config.db_mock_schema,
        target_catalog=test_config.db_mock_catalog,
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

    with pytest.raises(ReconciliationException) as excinfo:
        recon(ws=ws, spark=spark, table_recon=table_recon, reconcile_config=reconcile_config)
    assert (
        "[TABLE_OR_VIEW_NOT_FOUND] The table or view `remorph_integration_test`.`test`.`remorph_src_unknown` "
        "cannot be found"
    ) in str(excinfo.value)
