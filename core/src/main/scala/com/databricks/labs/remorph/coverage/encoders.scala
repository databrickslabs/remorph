package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.coverage.estimation.{Rule => EstRule, _}
import com.databricks.labs.remorph.discovery.{Fingerprint, QueryType, WorkloadType}
import com.databricks.labs.remorph.intermediate._
import io.circe._
import io.circe.generic.extras.semiauto._
import io.circe.generic.extras.Configuration
import io.circe.syntax._

import java.io.{PrintWriter, StringWriter}
import java.sql.Timestamp
import java.time.Duration

trait ErrorEncoders {

  implicit val codecConfiguration: Configuration =
    Configuration.default.withDiscriminator("$type").withSnakeCaseMemberNames

  implicit val throwableEncoder: Encoder[Throwable] = Encoder.instance { t =>
    val sw = new StringWriter()
    t.printStackTrace(new PrintWriter(sw))
    Json.obj(
      "class" -> t.getClass.getSimpleName.asJson,
      "message" -> Option(t.getMessage).asJson,
      "stack_trace" -> sw.toString.asJson)
  }

  implicit val expressionEncoder: Encoder[Expression] = Encoder.instance(e => e.getClass.getSimpleName.asJson)
  implicit val parsingErrorEncoder: Encoder[ParsingError] = deriveConfiguredEncoder
  implicit val parsingErrorsEncoder: Encoder[ParsingErrors] = deriveConfiguredEncoder
  implicit val unexpectedNodeEncoder: Encoder[UnexpectedNode] = deriveConfiguredEncoder
  implicit val unexpectedTableAlterationEncoder: Encoder[UnexpectedTableAlteration] = deriveConfiguredEncoder
  implicit val unsupportedGroupTypeEncoder: Encoder[UnsupportedGroupType] = deriveConfiguredEncoder
  implicit val unsupportedDataTypeEncoder: Encoder[UnsupportedDataType] = deriveConfiguredEncoder
  implicit val wrongNumberOfArgumentsEncoder: Encoder[WrongNumberOfArguments] = deriveConfiguredEncoder
  implicit val unsupportedArgumentsEncoder: Encoder[UnsupportedArguments] = deriveConfiguredEncoder
  implicit val unsupportedDateTimePartEncoder: Encoder[UnsupportedDateTimePart] = deriveConfiguredEncoder
  implicit val planGenerationFailureEncoder: Encoder[PlanGenerationFailure] = deriveConfiguredEncoder
  implicit val transpileFailureEncoder: Encoder[TranspileFailure] = deriveConfiguredEncoder
  implicit val uncaughtExceptionEncoder: Encoder[UncaughtException] = deriveConfiguredEncoder
  implicit val unexpectedOutputEncoder: Encoder[UnexpectedOutput] = deriveConfiguredEncoder
  implicit val incoherentStateEncoder: Encoder[IncoherentState] = Encoder.instance { is =>
    Json.obj(
      "$type" -> "IncoherentState".asJson,
      "current_phase" -> is.currentPhase.getClass.getSimpleName.asJson,
      "expected_phase" -> is.expectedPhase.getSimpleName.asJson)
  }
  implicit val singleErrorEncoder: Encoder[SingleError] = deriveConfiguredEncoder
  implicit val remorphErrorsEncoder: Encoder[RemorphErrors] = deriveConfiguredEncoder
  implicit val multipleErrorsEncoder: Encoder[MultipleErrors] = deriveConfiguredEncoder
  implicit val remorphErrorEncoder: Encoder[RemorphError] = deriveConfiguredEncoder

}

trait EstimationReportEncoders extends ErrorEncoders {

  implicit val sqlComplexityEncoder: Encoder[SqlComplexity] = deriveConfiguredEncoder
  implicit val parseFailStatsEncoder: Encoder[ParseFailStats] = deriveConfiguredEncoder
  implicit val estimationStatisticsEntryEncoder: Encoder[EstimationStatisticsEntry] = deriveConfiguredEncoder
  implicit val estimationStatisticsEncoder: Encoder[EstimationStatistics] = deriveConfiguredEncoder

  implicit val timestampEncoder: Encoder[Timestamp] = Encoder.instance(t => t.getTime.asJson)
  implicit val durationEncoder: Encoder[Duration] = Encoder.instance(d => d.toMillis.asJson)
  implicit val workloadTypeEncoder: Encoder[WorkloadType.WorkloadType] = Encoder.instance(wt => wt.toString.asJson)
  implicit val queryTypeEncoder: Encoder[QueryType.QueryType] = Encoder.instance(qt => qt.toString.asJson)

  implicit val ruleEncoder: Encoder[EstRule] = deriveConfiguredEncoder
  implicit val ruleScoreEncoder: Encoder[RuleScore] = Encoder.instance(score => Json.obj("rule" -> score.rule.asJson))

  implicit val fingerPrintEncoder: Encoder[Fingerprint] = deriveConfiguredEncoder
  implicit val estimationAnalysisReportEncoder: Encoder[EstimationAnalysisReport] = deriveConfiguredEncoder
  implicit val estimationTranspilationReportEncoder: Encoder[EstimationTranspilationReport] = deriveConfiguredEncoder
  implicit val estimationReportRecordEncoder: Encoder[EstimationReportRecord] = deriveConfiguredEncoder
  implicit val estimationReportEncoder: Encoder[EstimationReport] = deriveConfiguredEncoder
}
