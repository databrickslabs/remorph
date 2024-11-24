package com.databricks.labs.remorph

import com.databricks.labs.remorph.coverage.estimation.{EstimationAnalyzer, Estimator, JsonEstimationReporter, SummaryEstimationReporter}
import com.databricks.labs.remorph.coverage.runners.EnvGetter
import com.databricks.labs.remorph.coverage.{CoverageTest, EstimationReport}
import com.databricks.labs.remorph.discovery.{FileQueryHistory, QueryHistoryProvider}
import com.databricks.labs.remorph.generators.orchestration.FileSetGenerator
import com.databricks.labs.remorph.queries.ExampleDebugger
import com.databricks.labs.remorph.support.SupportContext
import com.databricks.labs.remorph.support.snowflake.SnowflakeContext
import com.databricks.labs.remorph.support.tsql.TSqlContext
import com.databricks.labs.remorph.transpilers._
import com.databricks.sdk.WorkspaceClient
import com.databricks.sdk.core.DatabricksConfig

import java.io.File
import java.time.Instant

trait ApplicationContext {
  def flags: Map[String, String]

  def envGetter: EnvGetter = new EnvGetter()

  private lazy val supportContext: SupportContext = flags.get("dialect") match {
    case Some("snowflake") => new SnowflakeContext(envGetter)
    case Some("tsql") => new TSqlContext(envGetter)
    case Some(unknown) => throw new IllegalArgumentException(s"--dialect=$unknown is not supported")
    case None => throw new IllegalArgumentException("--dialect is required")
  }

  lazy val queryHistoryProvider: QueryHistoryProvider = flags.get("source-queries") match {
    case Some(folder) => new FileQueryHistory(new File(folder).toPath)
    case None => supportContext.remoteQueryHistory
  }

  protected val now = Instant.now

  def connectConfig: DatabricksConfig = new DatabricksConfig()

  def workspaceClient: WorkspaceClient = new WorkspaceClient(connectConfig)

  def prettyPrinter[T](v: T): Unit = pprint.pprintln[T](v)

  def exampleDebugger: ExampleDebugger =
    new ExampleDebugger(supportContext.planParser, prettyPrinter, supportContext.name)

  def coverageTest: CoverageTest = new CoverageTest

  def estimator: Estimator = new Estimator(queryHistoryProvider, supportContext.planParser, new EstimationAnalyzer())

  def jsonEstimationReporter(
      outputDir: os.Path,
      preserveQueries: Boolean,
      estimate: EstimationReport): JsonEstimationReporter =
    new JsonEstimationReporter(outputDir, preserveQueries, estimate)

  def consoleEstimationReporter(outputDir: os.Path, estimate: EstimationReport): SummaryEstimationReporter =
    new SummaryEstimationReporter(outputDir, estimate)

  private def sqlGenerator: SqlGenerator = new SqlGenerator

  private def pySparkGenerator: PySparkGenerator = new PySparkGenerator

  def fileSetGenerator: FileSetGenerator =
    new FileSetGenerator(supportContext.planParser, sqlGenerator, pySparkGenerator)
}
