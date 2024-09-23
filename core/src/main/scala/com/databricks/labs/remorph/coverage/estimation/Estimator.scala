package com.databricks.labs.remorph.coverage.estimation

import com.databricks.labs.remorph.coverage.connections.SnowflakeConnectionFactory
import com.databricks.labs.remorph.coverage.runners.EnvGetter
import com.databricks.labs.remorph.discovery.SnowflakeQueryHistory
import com.databricks.labs.remorph.parsers.PlanParser
import com.typesafe.scalalogging.LazyLogging
import os.Path

class Estimator extends LazyLogging {

  def run(outputDir: Path, dialect: String, planParser: PlanParser[_]): Unit = {

    logger.info(s"Estimating coverage for $dialect with output to $outputDir")

    val env = new EnvGetter

    val conn = dialect match {
      case "snowflake" =>
        val connFactory = new SnowflakeConnectionFactory(env)
        connFactory.newConnection() // TODO: wrap with closing logic
      case _ => throw new IllegalArgumentException(s"Unsupported dialect: $dialect")
    }
    val snow = new SnowflakeQueryHistory(conn)
    val history = snow.history()
    logger.info(s"Found ${history.queries.size} queries in snowflake history")
  }
}
