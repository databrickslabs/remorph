package com.databricks.labs.remorph.coverage.runners

import com.databricks.connect.DatabricksSession
import com.databricks.sdk.core.DatabricksConfig
import com.databricks.sdk.WorkspaceClient
import com.typesafe.scalalogging.LazyLogging

class DatabricksSQL(env: EnvGetter) extends LazyLogging {
  val config = new DatabricksConfig()
    .setHost(env.get("DATABRICKS_HOST"))
    // TODO: fix envs to use DATABRICKS_CLUSTER_ID
    .setClusterId(env.get("TEST_USER_ISOLATION_CLUSTER_ID"))

  val w = new WorkspaceClient(config)
  logger.info("Ensuring cluster is running")
  w.clusters().ensureClusterIsRunning(config.getClusterId)

  val spark = DatabricksSession.builder().sdkConfig(config).getOrCreate()
  val res = spark.sql("SELECT * FROM samples.tpch.customer LIMIT 10").collect()
  logger.info(s"Tables: ${res.mkString(", ")}")
}
