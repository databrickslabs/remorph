package com.databricks.labs.remorph.support.tsql

import com.databricks.labs.remorph.coverage.runners.EnvGetter
import com.databricks.labs.remorph.discovery.QueryHistoryProvider
import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.parsers.tsql.TSqlPlanParser
import com.databricks.labs.remorph.support.{ConnectionFactory, SupportContext}

class TSqlContext(private val envGetter: EnvGetter) extends SupportContext {
  override def name: String = "tsql"
  override def planParser: PlanParser[_] = new TSqlPlanParser
  override lazy val connectionFactory: ConnectionFactory = new SqlServerConnectionFactory(envGetter)
  override def remoteQueryHistory: QueryHistoryProvider = {
    throw new IllegalArgumentException("query history for SQLServer is not yet implemented")
  }
}
