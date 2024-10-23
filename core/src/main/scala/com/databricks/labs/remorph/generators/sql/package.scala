package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.intermediate.{RemorphError, UncaughtException}
import com.databricks.labs.remorph.{KoResult, OkResult, PartialResult, RemorphContext, TBA, TBAS, WorkflowStage}

import scala.collection.mutable.ListBuffer
import scala.util.control.NonFatal

package object sql {

  type SQL = TBA[RemorphContext, String]

  implicit class SQLInterpolator(sc: StringContext) extends TBAS[RemorphContext] {
    def sql(args: Any*): TBA[RemorphContext, String] = {

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
            case failure: KoResult => return lift(failure)
            case other => sb.append(StringContext.treatEscapes(other.toString))
          }
          sb.append(StringContext.treatEscapes(stringParts.next()))
        } catch {
          case NonFatal(e) =>
            return lift(KoResult(WorkflowStage.GENERATE, UncaughtException(e)))
        }
      }
      if (errors.isEmpty) {
        lift(OkResult(sb.toString))
      } else if (errors.size == 1) {
        lift(PartialResult(sb.toString(), errors.head))
      } else {
        lift(PartialResult(sb.toString, errors.reduce(RemorphError.merge)))
      }
    }
  }

  implicit class SqlOps(sql: SQL) {
    def nonEmpty: TBA[RemorphContext, Boolean] = sql.map(_.nonEmpty)
    def isEmpty: TBA[RemorphContext, Boolean] = sql.map(_.isEmpty)
  }

  implicit class TBASeqOps(tbas: Seq[TBA[RemorphContext, String]]) extends TBAS[RemorphContext] {

    def mkSql: TBA[RemorphContext, String] = mkSql("", "", "")

    def mkSql(sep: String): TBA[RemorphContext, String] = mkSql("", sep, "")

    def mkSql(start: String, sep: String, end: String): TBA[RemorphContext, String] = {

      if (tbas.isEmpty) {
        sql"$start$end"
      } else {
        val separatedItems = tbas.tail.foldLeft[TBA[RemorphContext, String]](tbas.head) { case (agg, item) =>
          sql"$agg$sep$item"
        }
        sql"$start$separatedItems$end"
      }
    }

    def sequence: TBA[RemorphContext, Seq[String]] =
      tbas.foldLeft(ok(Seq.empty[String])) { case (agg, item) =>
        for {
          aggSeq <- agg
          i <- item
        } yield aggSeq :+ i
      }
  }
}
