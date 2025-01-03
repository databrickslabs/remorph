package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.coverage.estimation.{Rule => EstRule, _}
import com.databricks.labs.remorph.discovery.{Fingerprint, QueryType, WorkloadType}
import com.databricks.labs.remorph.intermediate._
import io.circe._
import io.circe.generic.extras.semiauto._
import io.circe.generic.extras.Configuration
import io.circe.syntax._

import java.sql.Timestamp
import java.time.Duration

trait ErrorEncoders {

  implicit val codecConfiguration: Configuration =
    Configuration.default.withSnakeCaseMemberNames

  implicit val singleErrorEncoder: Encoder[SingleError] = Encoder.instance { err =>
    Json.obj("error_code" -> err.getClass.getSimpleName.asJson, "error_message" -> err.msg.asJson)
  }
  implicit val remorphErrorEncoder: Encoder[RemorphError] = Encoder.instance {
    case s: SingleError => Json.arr(s.asJson)
    case m: MultipleErrors => Json.arr(m.errors.map(_.asJson): _*)
  }

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
