import os
from dataclasses import dataclass
from datetime import datetime
import decimal

import pytest
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    LongType,
    DecimalType,
    DateType,
    DoubleType,
    Row,
)
from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import VolumeType

from databricks.labs.remorph.config import ReconcileConfig, DatabaseConfig, ReconcileMetadataConfig, MorphConfig
from databricks.labs.remorph.helpers import db_sql
from databricks.labs.remorph.helpers.deployment import TableDeployer
from databricks.labs.remorph.install import ReconciliationMetadataSetup, CatalogSetup


@dataclass
class TestConfig:
    db_table_catalog: str
    db_table_schema: str
    db_table_name: str
    db_mock_catalog: str
    db_mock_schema: str
    db_mock_src: str
    db_mock_tgt: str
    db_mock_volume: str


@pytest.fixture(scope="session")
def ws():
    # Use variables from Unified Auth
    # See https://databricks-sdk-py.readthedocs.io/en/latest/authentication.html
    product_name, product_version = None, None
    return WorkspaceClient(host=os.environ["DATABRICKS_HOST"], product=product_name, product_version=product_version)


@pytest.fixture(scope="session")
def spark(ws):
    return DatabricksSession.builder.sdkConfig(ws.config).getOrCreate()


@pytest.fixture(scope="module")
def test_config():
    return TestConfig(
        db_table_catalog="samples",
        db_table_schema="tpch",
        db_table_name="lineitem",
        db_mock_catalog="remorph_integration_test",
        db_mock_schema="test",
        db_mock_src="lineitem_src",
        db_mock_tgt="lineitem_tgt",
        db_mock_volume="test_volume",
    )


@pytest.fixture(scope="module")
def reconcile_config(test_config):
    return ReconcileConfig(
        data_source="databricks",
        report_type="all",
        secret_scope="scope_databricks",
        database_config=DatabaseConfig(
            source_schema=test_config.db_mock_schema,
            target_catalog=test_config.db_mock_catalog,
            target_schema=test_config.db_mock_schema,
            source_catalog=test_config.db_mock_catalog,
        ),
        metadata_config=ReconcileMetadataConfig(
            catalog=test_config.db_mock_catalog, schema=test_config.db_mock_schema, volume=test_config.db_mock_volume
        ),
        job_id="1",
        tables=None,
    )


@pytest.fixture(scope="module")
def metrics_deployer(ws, reconcile_config):
    morph_config = MorphConfig(
        source=reconcile_config.data_source,
        catalog_name=reconcile_config.metadata_config.catalog,
        schema_name=reconcile_config.metadata_config.schema,
    )
    sql_backend = db_sql.get_sql_backend(ws, morph_config)
    return TableDeployer(
        sql_backend,
        reconcile_config.metadata_config.catalog,
        reconcile_config.metadata_config.schema,
    )


@pytest.fixture(scope="module")
def setup_teardown(ws, spark, test_config, reconcile_config, metrics_deployer):
    ReconciliationMetadataSetup(ws, reconcile_config, CatalogSetup(ws), metrics_deployer).run()
    _create_reconcile_volume(w=ws, reconcile=reconcile_config)
    yield
    ws.catalogs.delete(name=test_config.db_mock_catalog, force=True)


def _create_reconcile_volume(w, reconcile):
    all_volumes = w.volumes.list(
        reconcile.metadata_config.catalog,
        reconcile.metadata_config.schema,
    )

    reconcile_volume_exists = False
    for volume in all_volumes:
        if volume.name == reconcile.metadata_config.volume:
            reconcile_volume_exists = True
            print("Reconciliation Volume already exists.")
            break

    if not reconcile_volume_exists:
        print("Creating Reconciliation Volume.")
        w.volumes.create(
            reconcile.metadata_config.catalog,
            reconcile.metadata_config.schema,
            reconcile.metadata_config.volume,
            VolumeType.MANAGED,
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
