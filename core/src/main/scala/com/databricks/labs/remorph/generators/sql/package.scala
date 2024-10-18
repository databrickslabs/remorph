package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.intermediate.{RemorphError, UncaughtException}
import com.databricks.labs.remorph.{KoResult, OkResult, PartialResult, Result, WorkflowStage}

import scala.collection.mutable.ListBuffer
import scala.util.control.NonFatal

package object sql {

  type SQL = Result[String]

  implicit class SQLInterpolator(sc: StringContext) {
    def sql(args: Any*): SQL = {

      val stringParts = sc.parts.iterator
      val arguments = args.iterator
      val sb = new StringBuilder(StringContext.treatEscapes(stringParts.next()))
      val errors = new ListBuffer[RemorphError]

      while (arguments.hasNext) {
        try {
          arguments.next() match {
            case OkResult(s) => sb.append(StringContext.treatEscapes(s.toString))
            case PartialResult(s, err) =>
              sb.append(StringContext.treatEscapes(s.toString))
              errors.append(err)
            case failure: KoResult => return failure
            case other => sb.append(StringContext.treatEscapes(other.toString))
          }
          sb.append(StringContext.treatEscapes(stringParts.next()))
        } catch {
          case NonFatal(e) =>
            return KoResult(WorkflowStage.GENERATE, UncaughtException(e))
        }
      }
      if (errors.isEmpty) {
        OkResult(sb.toString)
      } else if (errors.size == 1) {
        PartialResult(sb.toString(), errors.head)
      } else {
        PartialResult(sb.toString, errors.reduce(RemorphError.merge))
      }
    }
  }

  implicit class SqlOps(sql: SQL) {
    def nonEmpty: Boolean = sql match {
      case OkResult(str) => str.nonEmpty
      case _ => false
    }
    def isEmpty: Boolean = sql match {
      case OkResult(str) => str.isEmpty
      case _ => false
    }
  }

  implicit class SQLSeqOps(sqls: Seq[SQL]) {

    def mkSql: SQL = mkSql("", "", "")

    def mkSql(sep: String): SQL = mkSql("", sep, "")

    def mkSql(start: String, sep: String, end: String): SQL = {

      if (sqls.isEmpty) {
        sql"$start$end"
      } else {
        val separatedItems = sqls.tail.foldLeft[SQL](sqls.head) { case (agg, item) =>
          sql"$agg$sep$item"
        }
        sql"$start$separatedItems$end"
      }

    }
  }

}
