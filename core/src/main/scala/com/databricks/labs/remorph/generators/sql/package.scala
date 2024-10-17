package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.intermediate.UncaughtException
import com.databricks.labs.remorph.{Result, WorkflowStage}

import scala.util.control.NonFatal

package object sql {

  type SQL = Result[String]

  implicit class SQLInterpolator(sc: StringContext) {
    def sql(args: Any*): SQL = {

      val stringParts = sc.parts.iterator
      val arguments = args.iterator
      val sb = new StringBuilder(StringContext.treatEscapes(stringParts.next()))

      while (arguments.hasNext) {
        try {
          arguments.next() match {
            case Result.Success(s) => sb.append(StringContext.treatEscapes(s.toString))
            case failure: Result.Failure => return failure
            case other => sb.append(StringContext.treatEscapes(other.toString))
          }
          sb.append(StringContext.treatEscapes(stringParts.next()))
        } catch {
          case NonFatal(e) =>
            return Result.Failure(WorkflowStage.GENERATE, UncaughtException(e))
        }
      }

      Result.Success(sb.toString)
    }
  }

  implicit class SqlOps(sql: SQL) {
    def nonEmpty: Boolean = sql match {
      case Result.Success(str) => str.nonEmpty
      case _ => false
    }
    def isEmpty: Boolean = sql match {
      case Result.Success(str) => str.isEmpty
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
