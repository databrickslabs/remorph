package com.databricks.labs.remorph

import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.parsers.snowflake.SnowflakePlanParser
import com.databricks.labs.remorph.parsers.tsql.TSqlPlanParser
import com.databricks.labs.remorph.queries.ExampleDebugger
import com.databricks.sdk.WorkspaceClient
import com.databricks.sdk.core.DatabricksConfig

trait ApplicationContext {
  def snowflakePlanParser: SnowflakePlanParser = new SnowflakePlanParser
  def tsqlPlanParser: TSqlPlanParser = new TSqlPlanParser
  def planParser(dialect: String): PlanParser[_] = dialect match {
    case "snowflake" => snowflakePlanParser
    case "tsql" => tsqlPlanParser
    case _ => throw new IllegalArgumentException(s"Unsupported dialect: $dialect")
  }
  def connectConfig: DatabricksConfig = new DatabricksConfig()
  def workspaceClient: WorkspaceClient = new WorkspaceClient(connectConfig)
  def prettyPrinter[T](v: T): Unit = pprint.pprintln[T](v)
  def exampleDebugger: ExampleDebugger = new ExampleDebugger(planParser, prettyPrinter)
}
