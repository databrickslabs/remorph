package com.databricks.labs.remorph.support

import com.databricks.labs.remorph.discovery.QueryHistoryProvider
import com.databricks.labs.remorph.parsers.PlanParser

trait SupportContext {
  def name: String
  def planParser: PlanParser[_]
  def connectionFactory: ConnectionFactory
  def remoteQueryHistory: QueryHistoryProvider
}
