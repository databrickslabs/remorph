package com.databricks.labs.remorph.discovery

import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.intermediate._
import com.databricks.labs.remorph.{KoResult, OkResult, PartialResult, Parsing, WorkflowStage}
import com.typesafe.scalalogging.LazyLogging

import java.security.MessageDigest
import java.sql.Timestamp
import java.time.Duration

object WorkloadType extends Enumeration {
  type WorkloadType = Value
  val ETL, SQL_SERVING, OTHER = Value
}

object QueryType extends Enumeration {
  type QueryType = Value
  val DDL, DML, PROC, OTHER = Value
}

/**
 * A fingerprint is a hash of a query plan that can be used to recognize duplicate queries
 *
 * @param dbQueryHash The hash or id of the query as stored in the database, which can be used to identify the query
 *                    when the queries cannot be stored offsite because of customer data restrictions
 * @param timestamp The timestamp of when this query was executed
 * @param fingerprint The hash of the query plan, rather than the query itself - can be null if we
 *                    cannot parse the query into a digestible plan
 * @param duration how long this query took to execute, which may or may not be an indication of complexity
 * @param user The user who executed the query against the database
 * @param workloadType The type of workload this query represents (e.g. ETL, SQL_SERVING, OTHER)
 * @param queryType The type of query this is (e.g. DDL, DML, PROC, OTHER)
 */
case class Fingerprint(
    dbQueryHash: String,
    timestamp: Timestamp,
    fingerprint: String,
    duration: Duration,
    user: String,
    workloadType: WorkloadType.WorkloadType,
    queryType: QueryType.QueryType) {}

case class Fingerprints(fingerprints: Seq[Fingerprint]) {
  def uniqueQueries: Int = fingerprints.map(_.fingerprint).distinct.size
}

class Anonymizer(parser: PlanParser[_]) extends LazyLogging {
  private val placeholder = Literal("?", UnresolvedType)

  def apply(history: QueryHistory): Fingerprints = Fingerprints(history.queries.map(fingerprint))
  def apply(query: ExecutedQuery, plan: LogicalPlan): Fingerprint = fingerprint(query, plan)
  def apply(query: ExecutedQuery): Fingerprint = fingerprint(query)
  def apply(plan: LogicalPlan): String = fingerprint(plan)
  def apply(query: String): String = fingerprint(query)

  private[discovery] def fingerprint(query: ExecutedQuery): Fingerprint = {
    parser.parse(Parsing(query.source)).flatMap(parser.visit).run(Parsing(query.source)) match {
      case KoResult(WorkflowStage.PARSE, error) =>
        logger.warn(s"Failed to parse query: ${query.source} ${error.msg}")
        Fingerprint(
          query.id,
          query.timestamp,
          fingerprint(query.source),
          query.duration,
          query.user.getOrElse("unknown"),
          WorkloadType.OTHER,
          QueryType.OTHER)
      case KoResult(_, error) =>
        logger.warn(s"Failed to produce plan from query: ${query.source} ${error.msg}")
        Fingerprint(
          query.id,
          query.timestamp,
          fingerprint(query.source),
          query.duration,
          query.user.getOrElse("unknown"),
          WorkloadType.OTHER,
          QueryType.OTHER)
      case PartialResult((_, plan), error) =>
        logger.warn(s"Errors occurred while producing plan from query: ${query.source} ${error.msg}")
        Fingerprint(
          query.id,
          query.timestamp,
          fingerprint(plan),
          query.duration,
          query.user.getOrElse("unknown"),
          workloadType(plan),
          queryType(plan))
      case OkResult((_, plan)) =>
        Fingerprint(
          query.id,
          query.timestamp,
          fingerprint(plan),
          query.duration,
          query.user.getOrElse("unknown"),
          workloadType(plan),
          queryType(plan))
    }
  }

  /**
   * Create a fingerprint for a query and its plan, when the plan is already produced
   * @param query The executed query
   * @param plan The logical plan
   * @return A fingerprint representing the query plan
   */
  private[discovery] def fingerprint(query: ExecutedQuery, plan: LogicalPlan): Fingerprint = {
    Fingerprint(
      query.id,
      query.timestamp,
      fingerprint(plan),
      query.duration,
      query.user.getOrElse("unknown"),
      workloadType(plan),
      queryType(plan))
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

  /**
   * Create a fingerprint for a query, when the plan is not yet, or cannot be produced.
   * <p>
   *   This is a fallback method for when we cannot parse the query into a plan. It will
   *   make a crude attempt to hash the query text itself, taking out literals and numerics.
   *   This gives us a very basic way to identify duplicate queries and not report them as
   *   unparsable if they are just different by a few values from a previous query. In turn,
   *   this gives us a better idea of how many unique unparsable queries we have yet to deal
   *   with, rather than just reporting them all as unparsable and making the core work
   *   seem bigger than it actually is.
   * </p>
   * <p>
   *   We could improve this hash by removing comments and normalizing whitespace perhaps,
   *   but whether we would get any gains from that is debatable
   * </p>
   *
   * @param query The text of the query to parse
   * @return A fingerprint representing the query text
   */
  private def fingerprint(query: String): String = {
    val masked = query
      .replaceAll("\\b\\d+\\b", "42")
      .replaceAll("'[^']*'", "?")
      .replaceAll("\"[^\"]*\"", "?")
      .replaceAll("`[^`]*`", "?")
    val digest = MessageDigest.getInstance("SHA-1")
    digest.update(masked.getBytes)
    digest.digest().map("%02x".format(_)).mkString
  }
}
