package com.databricks.labs.remorph.discovery

import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.parsers.intermediate._
import com.typesafe.scalalogging.LazyLogging

import java.security.MessageDigest
import java.sql.Timestamp
import java.time.Duration
import scala.util.control.NonFatal

object WorkloadType extends Enumeration {
  type WorkloadType = Value
  val ETL, SQL_SERVING, OTHER = Value
}

object QueryType extends Enumeration {
  type QueryType = Value
  val DDL, DML, PROC, OTHER = Value
}

case class Fingerprint(
    timestamp: Timestamp,
    fingerprint: String,
    duration: Duration,
    user: String,
    workloadType: WorkloadType.WorkloadType,
    queryType: QueryType.QueryType)

case class Fingerprints(fingerprints: Seq[Fingerprint]) {
  def uniqueQueries: Int = fingerprints.map(_.fingerprint).distinct.size
}

class Anonymizer(parser: PlanParser[_]) extends LazyLogging {
  private val placeholder = Literal("?", UnresolvedType)

  def apply(history: QueryHistory): Fingerprints = Fingerprints(history.queries.map(fingerprint))

  private[discovery] def fingerprint(query: ExecutedQuery): Fingerprint = {
    try {
      val plan = parser.parse(query.source)
      Fingerprint(query.timestamp, fingerprint(plan), query.duration, query.user, workloadType(plan), queryType(plan))
    } catch {
      case NonFatal(err) =>
        logger.warn(s"Failed to parse query: ${query.source}", err)
        Fingerprint(query.timestamp, "unknown", query.duration, query.user, WorkloadType.OTHER, QueryType.OTHER)
    }
  }

  private def fingerprint(plan: LogicalPlan): String = {
    // replace all literals with a placeholder, that way we can hash the plan
    // without worrying about the actual values. This is a very simple
    // anonymization technique, but it's good enough for our purposes.
    // e.g. ... "LIMIT 500 OFFSET 0" and "LIMIT 100 OFFSET 20" will have
    // the same fingerprint.
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
