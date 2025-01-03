package com.databricks.labs.remorph

import com.databricks.labs.remorph.intermediate.UncaughtException

import scala.util.control.NonFatal

package object generators {

  implicit class CodeInterpolator(sc: StringContext) extends TransformationConstructors {
    def code(args: Any*): Transformation[String] = {

      args
        .map {
          case tba: Transformation[_] => tba.asInstanceOf[Transformation[String]]
          case x => ok(x.toString)
        }
        .sequence
        .flatMap { a =>
          val stringParts = sc.parts.iterator
          val arguments = a.iterator
          var failureOpt: Option[Transformation[String]] = None
          val sb = new StringBuilder()
          try {
            sb.append(StringContext.treatEscapes(stringParts.next()))
          } catch {
            case NonFatal(e) =>
              failureOpt = Some(lift(KoResult(WorkflowStage.GENERATE, UncaughtException(e))))
          }
          while (failureOpt.isEmpty && arguments.hasNext) {
            try {
              sb.append(arguments.next())
              sb.append(StringContext.treatEscapes(stringParts.next()))
            } catch {
              case NonFatal(e) =>
                failureOpt = Some(lift(KoResult(WorkflowStage.GENERATE, UncaughtException(e))))
            }
          }
          failureOpt.getOrElse(ok(sb.toString()))
        }
    }
  }

  implicit class TBAOps(sql: Transformation[String]) {
    def nonEmpty: Transformation[Boolean] = sql.map(_.nonEmpty)
    def isEmpty: Transformation[Boolean] = sql.map(_.isEmpty)
  }

  implicit class TBASeqOps(tbas: Seq[Transformation[String]]) extends TransformationConstructors {

    def mkCode: Transformation[String] = mkCode("", "", "")

    def mkCode(sep: String): Transformation[String] = mkCode("", sep, "")

    def mkCode(start: String, sep: String, end: String): Transformation[String] = {
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
    def sequence: Transformation[Seq[String]] =
      tbas.foldLeft(ok(Seq.empty[String])) { case (agg, item) =>
        for {
          aggSeq <- agg
          i <- item
        } yield aggSeq :+ i
      }
  }
}
