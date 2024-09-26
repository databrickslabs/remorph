package com.databricks.labs.remorph.discovery

import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.parsers.intermediate._
import com.databricks.labs.remorph.transpilers.WorkflowStage.PARSE
import com.databricks.labs.remorph.transpilers.{Result, SourceCode}
import com.typesafe.scalalogging.LazyLogging
import upickle.default._

import java.security.MessageDigest
import java.sql.Timestamp
import java.time.Duration

object WorkloadType extends Enumeration {
  type WorkloadType = Value
  val ETL, SQL_SERVING, OTHER = Value

  implicit val rw: ReadWriter[WorkloadType] =
    readwriter[String].bimap[WorkloadType](_.toString, str => WorkloadType.withName(str))
}

object QueryType extends Enumeration {
  type QueryType = Value
  val DDL, DML, PROC, OTHER = Value

  implicit val rw: ReadWriter[QueryType] =
    readwriter[String].bimap[QueryType](_.toString, str => QueryType.withName(str))
}

case class Fingerprint(
    timestamp: Timestamp,
    fingerprint: String,
    duration: Duration,
    user: String,
    workloadType: WorkloadType.WorkloadType,
    queryType: QueryType.QueryType) {}

object Fingerprint {
  implicit val rw: ReadWriter[Fingerprint] = macroRW
  implicit val timestampRW: ReadWriter[Timestamp] =
    readwriter[Long].bimap[Timestamp](ts => ts.getTime, millis => new Timestamp(millis))
  implicit val durationRW: ReadWriter[Duration] =
    readwriter[Long].bimap[Duration](duration => duration.toMillis, millis => Duration.ofMillis(millis))
}

case class Fingerprints(fingerprints: Seq[Fingerprint]) {
  def uniqueQueries: Int = fingerprints.map(_.fingerprint).distinct.size
}

class Anonymizer(parser: PlanParser[_]) extends LazyLogging {
  private val placeholder = Literal("?", UnresolvedType)

  def apply(history: QueryHistory): Fingerprints = Fingerprints(history.queries.map(fingerprint))
  def apply(query: ExecutedQuery, plan: LogicalPlan): Fingerprint = fingerprint(query, plan)
  def apply(query: ExecutedQuery): Fingerprint = fingerprint(query)
  def apply(plan: LogicalPlan): String = fingerprint(plan)

  private[discovery] def fingerprint(query: ExecutedQuery): Fingerprint = {
    parser.parse(SourceCode(query.source)).flatMap(parser.visit) match {
      case Result.Failure(PARSE, errorJson) =>
        logger.warn(s"Failed to parse query: ${query.source} $errorJson")
        Fingerprint(query.timestamp, "unknown", query.duration, query.user, WorkloadType.OTHER, QueryType.OTHER)
      case Result.Failure(_, errorJson) =>
        logger.warn(s"Failed to produce plan from query: ${query.source} $errorJson")
        Fingerprint(query.timestamp, "unknown", query.duration, query.user, WorkloadType.OTHER, QueryType.OTHER)
      case Result.Success(plan) =>
        Fingerprint(query.timestamp, fingerprint(plan), query.duration, query.user, workloadType(plan), queryType(plan))
    }
  }

  /**
   * Create a fingerprint for a query and its plan, when the plan is already produced
   * @param query The executed query
   * @param plan The logical plan
   * @return A fingerprint representing the query plan
   */
  private[discovery] def fingerprint(query: ExecutedQuery, plan: LogicalPlan): Fingerprint = {
    Fingerprint(query.timestamp, fingerprint(plan), query.duration, query.user, workloadType(plan), queryType(plan))
  }

  /**
   * <p>
   *   Provide a generic hash for the given plan
   * </p>
   * <p>
   *   Before hashing the plan, we replace all literals with a placeholder. This way we can hash the plan
   *   without worrying about the actual values and will generate the same hash code for queries that only
   *   differ by literal values.
   * </p>
   * <p>
   *   This is a very simple anonymization technique, but it's good enough for our purposes.
   *   e.g. ... "LIMIT 500 OFFSET 0" and "LIMIT 100 OFFSET 20" will have
   *   the same fingerprint.
   * </p>
   *
   * @param plan The plan we want a hash code for
   * @return The hash string for the query with literals replaced by placeholders
   */
  private def fingerprint(plan: LogicalPlan): String = {

    val erasedLiterals = plan transformAllExpressions { case _: Literal =>
      placeholder
    }
    val code = erasedLiterals.asCode
    val digest = MessageDigest.getInstance("SHA-1")
    digest.update(code.getBytes)
    digest.digest().map("%02x".format(_)).mkString
  }

  private def workloadType(plan: LogicalPlan): WorkloadType.WorkloadType = {
    plan match {
      case Batch(Seq(_: Project)) => WorkloadType.SQL_SERVING
      case Batch(Seq(_: CreateTableCommand)) => WorkloadType.ETL
      case Batch(Seq(_: UpdateTable)) => WorkloadType.ETL
      case Batch(Seq(_: DeleteFromTable)) => WorkloadType.ETL
      case Batch(Seq(_: MergeIntoTable)) => WorkloadType.ETL

      case _ => WorkloadType.OTHER
    }
  }

  private def queryType(plan: LogicalPlan): QueryType.QueryType = {
    plan match {
      case Batch(Seq(_: CreateTableCommand)) => QueryType.DDL
      case Batch(Seq(_: AlterTableCommand)) => QueryType.DDL
      case Batch(Seq(_: DropTempView)) => QueryType.DDL
      case Batch(Seq(_: DropGlobalTempView)) => QueryType.DDL
      case Batch(Seq(_: Drop)) => QueryType.DDL

      case Batch(Seq(_: Project)) => QueryType.DML
      case Batch(Seq(_: InsertIntoTable)) => QueryType.DML
      case Batch(Seq(_: UpdateTable)) => QueryType.DML
      case Batch(Seq(_: DeleteFromTable)) => QueryType.DML
      case Batch(Seq(_: MergeIntoTable)) => QueryType.DML

      case _ => QueryType.OTHER
    }
  }
}
