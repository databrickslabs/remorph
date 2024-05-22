from databricks.connect import DatabricksSession
from databricks.sdk.retries import retried
from databricks.sdk.errors import NotFound
from datetime import timedelta


@retried(on=[NotFound], timeout=timedelta(minutes=5))
def test_recon_gd(ws):
    spark = DatabricksSession.builder.sdkConfig(ws.config).getOrCreate()
    spark.sql("select 1 as col1, 2 as col2").show(100, False)
    assert 1 == 1
