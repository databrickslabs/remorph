package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.intermediate.{RemorphError, UncaughtException}
import com.databricks.labs.remorph._

import scala.collection.mutable.ListBuffer
import scala.util.control.NonFatal

package object py {

  type Python = Result[String]

  implicit class PythonInterpolator(sc: StringContext) {
    def py(args: Any*): Python = {

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

  implicit class PythonOps(Python: Python) {
    def nonEmpty: Boolean = Python match {
      case OkResult(str) => str.nonEmpty
      case _ => false
    }
    def isEmpty: Boolean = Python match {
      case OkResult(str) => str.isEmpty
      case _ => false
    }
  }

  implicit class PythonSeqOps(Pythons: Seq[Python]) {
    def mkPython(sep: String): Python = mkPython("", sep, "")

    def mkPython(start: String, sep: String, end: String): Python = {
      if (Pythons.isEmpty) {
        py"$start$end"
      } else {
        val separatedItems = Pythons.tail.foldLeft[Python](Pythons.head) { case (agg, item) =>
          py"$agg$sep$item"
        }
        py"$start$separatedItems$end"
      }
    }
  }
}
