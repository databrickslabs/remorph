from databricks.connect import DatabricksSession


def test_recon_gd(ws):
    spark = DatabricksSession.builder.sdkConfig(ws.config).getOrCreate()
    spark.sql("select 1 as col1, 2 as col2").show(100, False)
    assert 1 == 1
