package com.databricks.labs.remorph.coverage.estimation

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.typesafe.scalalogging.LazyLogging
import upickle.default._

sealed trait SqlComplexity
object SqlComplexity {
  case object LOW extends SqlComplexity
  case object MEDIUM extends SqlComplexity
  case object COMPLEX extends SqlComplexity
  case object VERY_COMPLEX extends SqlComplexity

  implicit val rw: ReadWriter[SqlComplexity] = ReadWriter.merge(
    macroRW[SqlComplexity.LOW.type],
    macroRW[SqlComplexity.MEDIUM.type],
    macroRW[SqlComplexity.COMPLEX.type],
    macroRW[SqlComplexity.VERY_COMPLEX.type])
}

case class SourceTextComplexity(lineCount: Int, textLength: Int)

class EstimationAnalyzer extends LazyLogging {
  // TODO: We will do this and the rest of the analysis in the next PR
  def countStatements(plan: ir.LogicalPlan): Int = 1

  def estimateComplexity(plan: ir.LogicalPlan): SqlComplexity = SqlComplexity.LOW

  def sourceTextComplexity(query: String): SourceTextComplexity = {
    SourceTextComplexity(query.split("\n").length, query.length)
  }
}
