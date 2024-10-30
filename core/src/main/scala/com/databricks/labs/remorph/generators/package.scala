package com.databricks.labs.remorph

import com.databricks.labs.remorph.intermediate.UncaughtException

import scala.util.control.NonFatal

package object generators {

  implicit class TBAInterpolator(sc: StringContext) extends TBAS[RemorphContext] {
    def tba(args: Any*): TBA[RemorphContext, String] = {

      args
        .map {
          case tba: TBA[_, _] => tba.asInstanceOf[TBA[RemorphContext, String]]
          case x => ok(x.toString)
        }
        .sequence
        .map { a =>
          val stringParts = sc.parts.iterator
          val arguments = a.iterator
          val sb = new StringBuilder(StringContext.treatEscapes(stringParts.next()))
          while (arguments.hasNext) {
            try {
              sb.append(StringContext.treatEscapes(arguments.next()))
              sb.append(StringContext.treatEscapes(stringParts.next()))
            } catch {
              case NonFatal(e) =>
                return lift(KoResult(WorkflowStage.GENERATE, UncaughtException(e)))
            }
          }
          sb.toString()

        }
    }
  }

  implicit class TBAOps(sql: TBA[RemorphContext, String]) {
    def nonEmpty: TBA[RemorphContext, Boolean] = sql.map(_.nonEmpty)
    def isEmpty: TBA[RemorphContext, Boolean] = sql.map(_.isEmpty)
  }

  implicit class TBASeqOps(tbas: Seq[TBA[RemorphContext, String]]) extends TBAS[RemorphContext] {

    def mkTba: TBA[RemorphContext, String] = mkTba("", "", "")

    def mkTba(sep: String): TBA[RemorphContext, String] = mkTba("", sep, "")

    def mkTba(start: String, sep: String, end: String): TBA[RemorphContext, String] = {
      tbas.sequence.map(_.mkString(start, sep, end))
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
