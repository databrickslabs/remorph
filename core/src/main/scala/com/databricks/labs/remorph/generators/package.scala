package com.databricks.labs.remorph

import com.databricks.labs.remorph.intermediate.UncaughtException

import scala.util.control.NonFatal

package object generators {

  implicit class TBAInterpolator(sc: StringContext) extends TransformationConstructors[Phase] {
    def code(args: Any*): Transformation[Phase, String] = {

      args
        .map {
          case tba: Transformation[_, _] => tba.asInstanceOf[Transformation[Phase, String]]
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

  implicit class TBAOps(sql: Transformation[Phase, String]) {
    def nonEmpty: Transformation[Phase, Boolean] = sql.map(_.nonEmpty)
    def isEmpty: Transformation[Phase, Boolean] = sql.map(_.isEmpty)
  }

  implicit class TBASeqOps(tbas: Seq[Transformation[Phase, String]]) extends TransformationConstructors[Phase] {

    def mkCode: Transformation[Phase, String] = mkCode("", "", "")

    def mkCode(sep: String): Transformation[Phase, String] = mkCode("", sep, "")

    def mkCode(start: String, sep: String, end: String): Transformation[Phase, String] = {
      tbas.sequence.map(_.mkString(start, sep, end))
    }

    /**
     * Combine multiple Transformation[RemorphContext, String] into a Transformation[ RemorphContext, Seq[String] ].
     * The resulting Transformation will run each individual Transformation in sequence, accumulating all the effects
     * along the way.
     *
     * For example, when a Transformation in the input Seq modifies the state, TBAs that come after it in the input
     * Seq will see the modified state.
     */
    def sequence: Transformation[Phase, Seq[String]] =
      tbas.foldLeft(ok(Seq.empty[String])) { case (agg, item) =>
        for {
          aggSeq <- agg
          i <- item
        } yield aggSeq :+ i
      }
  }
}
