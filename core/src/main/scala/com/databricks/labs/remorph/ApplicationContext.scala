package com.databricks.labs.remorph

import com.databricks.labs.remorph.coverage.connections.SnowflakeConnectionFactory
import com.databricks.labs.remorph.coverage.estimation.{SummaryEstimationReporter, EstimationAnalyzer, Estimator, JsonEstimationReporter}
import com.databricks.labs.remorph.coverage.runners.EnvGetter
import com.databricks.labs.remorph.coverage.{CoverageTest, EstimationReport}
import com.databricks.labs.remorph.discovery.SnowflakeQueryHistory
import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.parsers.snowflake.SnowflakePlanParser
import com.databricks.labs.remorph.parsers.tsql.TSqlPlanParser
import com.databricks.labs.remorph.queries.ExampleDebugger
import com.databricks.labs.remorph.transpilers.{BaseTranspiler, SnowflakeToDatabricksTranspiler, TSqlToDatabricksTranspiler}
import com.databricks.sdk.WorkspaceClient
import com.databricks.sdk.core.DatabricksConfig

import java.time.Instant

trait ApplicationContext {
  private def snowflakePlanParser: SnowflakePlanParser = new SnowflakePlanParser

  protected val now = Instant.now
  private def tsqlPlanParser: TSqlPlanParser = new TSqlPlanParser

  def planParser(dialect: String): PlanParser[_] = dialect match {
    case "snowflake" => snowflakePlanParser
    case "tsql" => tsqlPlanParser
    case _ => throw new IllegalArgumentException(s"Unsupported dialect: $dialect")
  }

  def transpiler(dialect: String): BaseTranspiler = dialect match {
    case "snowflake" => new SnowflakeToDatabricksTranspiler
    case "tsql" => new TSqlToDatabricksTranspiler
    case _ => throw new IllegalArgumentException(s"Unsupported dialect: $dialect")
  }

  def connectConfig: DatabricksConfig = new DatabricksConfig()

  def workspaceClient: WorkspaceClient = new WorkspaceClient(connectConfig)

  def prettyPrinter[T](v: T): Unit = pprint.pprintln[T](v)

  def exampleDebugger: ExampleDebugger = new ExampleDebugger(planParser, prettyPrinter)

  def coverageTest: CoverageTest = new CoverageTest

  def connectionFactory: SnowflakeConnectionFactory = new SnowflakeConnectionFactory(new EnvGetter)

  def estimator(dialect: String): Estimator =
    new Estimator(
      new SnowflakeQueryHistory(connectionFactory.newConnection()),
      planParser(dialect),
      new EstimationAnalyzer())

  def jsonEstimationReporter(
      outputDir: os.Path,
      preserveQueries: Boolean,
      estimate: EstimationReport): JsonEstimationReporter =
    new JsonEstimationReporter(outputDir, preserveQueries, estimate)

  def consoleEstimationReporter(outputDir: os.Path, estimate: EstimationReport): SummaryEstimationReporter =
    new SummaryEstimationReporter(outputDir, estimate)
}
