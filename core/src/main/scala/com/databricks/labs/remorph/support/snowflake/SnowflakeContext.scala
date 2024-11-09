package com.databricks.labs.remorph.support.snowflake

import com.databricks.labs.remorph.coverage.runners.EnvGetter
import com.databricks.labs.remorph.support.{ConnectionFactory, SupportContext}
import com.databricks.labs.remorph.discovery.{QueryHistoryProvider, SnowflakeQueryHistory}
import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.parsers.snowflake.SnowflakePlanParser

class SnowflakeContext(private val envGetter: EnvGetter) extends SupportContext {
  override def name: String = "snowflake"
  override def planParser: PlanParser[_] = new SnowflakePlanParser
  override lazy val connectionFactory: ConnectionFactory = new SnowflakeConnectionFactory(envGetter)
  override lazy val remoteQueryHistory: QueryHistoryProvider = {
    new SnowflakeQueryHistory(connectionFactory.newConnection())
  }
}
