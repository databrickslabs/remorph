package com.databricks.labs.remorph.coverage.estimation

import com.databricks.labs.remorph.coverage.connections.SnowflakeConnectionFactory
import com.databricks.labs.remorph.coverage.runners.EnvGetter
import com.databricks.labs.remorph.discovery.SnowflakeQueryHistory
import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.parsers.intermediate.{Literal, UnresolvedType}
import com.databricks.labs.remorph.transpilers.Result.{Failure, Success}
import com.databricks.labs.remorph.transpilers.WorkflowStage.{GENERATE, OPTIMIZE, PARSE, PLAN}
import com.databricks.labs.remorph.transpilers.{SourceCode, SqlGenerator}
import com.typesafe.scalalogging.LazyLogging
import os.Path

import java.time.Instant

class Estimator extends LazyLogging {
  private val placeholder = Literal("?", UnresolvedType)
  def run(outputDir: Path, dialect: String, planParser: PlanParser[_]): Unit = {

    val env = new EnvGetter
    val now = Instant.now
    os.makeDir.all(outputDir / "success")
    val resultPath = outputDir / s"${dialect}_${now.getEpochSecond}.jsonl"

    val conn = dialect match {
      case "snowflake" =>
        val connFactory = new SnowflakeConnectionFactory(env)
        connFactory.newConnection()
      case _ => throw new IllegalArgumentException(s"Unsupported dialect: $dialect")
    }
    try {
      val snow = new SnowflakeQueryHistory(conn)
      val history = snow.history()
      logger.info(s"Found ${history.queries.size} queries in snowflake history")

      // TODO: If we want to use the anonymizer to identify only unique queries, then we need to refactor it a little

      // TODO: refactor this to simplify after result sets are built
      var successCount = 0
      history.queries.foreach { query =>
        if (query.source.isEmpty) {
          logger.warn(s"Skipping query with empty source: $query")
        } else {
          val result =
            planParser.parse(SourceCode(query.source, query.user + query.timestamp.toString)).flatMap(planParser.visit)
          result match {
            case Failure(PARSE, errorJson) =>
              logger.warn(s"Failed to parse query: ${query.source} $errorJson")
            case Failure(PLAN, errorJson) =>
              logger.warn(s"Failed to produce plan for query: ${query.source} $errorJson")
            case Success(plan) =>
              val erasedLiterals = plan transformAllExpressions { case _: Literal => placeholder }
              val generator = new SqlGenerator
              val genResult = planParser.optimize(erasedLiterals).flatMap(generator.generate)
              genResult match {
                case Failure(OPTIMIZE, errorJson) =>
                  logger.warn(s"Failed to optimize plan for query: ${query.source} $errorJson")
                case Failure(GENERATE, errorJson) =>
                  logger.warn(s"Failed to generate DB SQL for query: ${query.source} $errorJson")
                case Success(output) =>
                  logger.info(s"Successfully transpiled query: ${query.source}")
                  os.write.over(
                    outputDir / "success" / f"${successCount + 1}%06d_${query.user}_${query.timestamp}.sql",
                    output)
                  successCount += 1
                case _ =>
                  logger.warn(s"Unexpected result from transpilation of query: ${query.source}")
              }
            case _ =>
              logger.warn(s"Unexpected result from transpilation of query: ${query.source}")
          }
        }
      }

      os.write(resultPath, "placeholder for json output")
      logger.info(s"Successfully transpiled $successCount queries")
    } finally {
      conn.close()
    }
  }

}
