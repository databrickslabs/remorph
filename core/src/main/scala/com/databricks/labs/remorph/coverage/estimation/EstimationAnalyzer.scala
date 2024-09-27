package com.databricks.labs.remorph.coverage.estimation

import com.databricks.labs.remorph.coverage.EstimationReportRecord
import com.databricks.labs.remorph.discovery.ExecutedQuery
import com.databricks.labs.remorph.parsers.intermediate.{Expression, LogicalPlan, TreeNode}
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.typesafe.scalalogging.LazyLogging
import upickle.default._

import scala.util.control.NonFatal

sealed trait SqlComplexity
object SqlComplexity {
  case object LOW extends SqlComplexity
  case object MEDIUM extends SqlComplexity
  case object COMPLEX extends SqlComplexity
  case object VERY_COMPLEX extends SqlComplexity

  // TODO: Define the scores for each complexity level
  def fromScore(score: Int): SqlComplexity = score match {
    case s if s < 10 => LOW
    case s if s < 20 => MEDIUM
    case s if s < 30 => COMPLEX
    case _ => VERY_COMPLEX
  }

  implicit val rw: ReadWriter[SqlComplexity] = ReadWriter.merge(
    macroRW[SqlComplexity.LOW.type],
    macroRW[SqlComplexity.MEDIUM.type],
    macroRW[SqlComplexity.COMPLEX.type],
    macroRW[SqlComplexity.VERY_COMPLEX.type])
}

case class ComplexityEstimate(complexity: SqlComplexity, statementCount: Int, charCount: Int, lineCount: Int)
case class SourceTextComplexity(lineCount: Int, textLength: Int)

case class EstimationStatistics(
    medianScore: Int,
    meanScore: Double,
    modeScore: Int,
    stdDeviation: Double,
    percentile25: Double,
    percentile50: Double,
    percentile75: Double,
    geometricMeanScore: Double,
    complexity: SqlComplexity)

object EstimationStatistics {
  implicit val rw: ReadWriter[EstimationStatistics] = macroRW
}

class EstimationAnalyzer extends LazyLogging {

  // How much each thing in our analysis discovery costs
  val cost = new RuleDefinitions

  def countStatements(plan: ir.LogicalPlan): Int = 1

  def estimateComplexity(query: ExecutedQuery, plan: ir.LogicalPlan): ComplexityEstimate = {
    val s = sourceTextComplexity(query.source)
    ComplexityEstimate(SqlComplexity.LOW, countStatements(plan), s.textLength, s.lineCount)
  }

  def evaluateTree(node: TreeNode[_]): Int = {
    evaluateTree(node, logicalPlanEvaluator, expressionEvaluator)
  }

  def evaluateTree(
      node: TreeNode[_],
      logicalPlanVisitor: PartialFunction[LogicalPlan, Int],
      expressionVisitor: PartialFunction[Expression, Int]): Int = {
    if (node == null) return 0 // Return 0 if the node is null (guards against bad IR for the moment - will change)

    node match {
      case lp: LogicalPlan =>
        val currentValue = logicalPlanVisitor.applyOrElse(lp, (_: LogicalPlan) => 0)
        val childrenValue = lp.children.map(child => evaluateTree(child, logicalPlanVisitor, expressionVisitor)).sum
        val expressionsValue = lp.expressions.map(expr => evaluateTree(expr, logicalPlanVisitor, expressionVisitor)).sum
        currentValue + childrenValue + expressionsValue

      case expr: Expression =>
        if (expr.children == null) return 0
        val currentValue = expressionVisitor.applyOrElse(expr, (_: Expression) => 0)
        val childrenValue = expr.children.map(child => evaluateTree(child, logicalPlanVisitor, expressionVisitor)).sum
        currentValue + childrenValue

      case _ =>
        throw new IllegalArgumentException(s"Unsupported node type: ${node.getClass.getSimpleName}")
    }
  }

  /**
   * <p>
   *   Given the raw query text, produce some statistics that are purely derived from the text, rather than
   *   a parsed plan or translation result.
   * </p>
   * <p>
   *   Text complexity is just one component for the overall score of a query, but it can be a good indicator
   *   of how complex the query is in terms of a human translating it. For example, a query with many lines
   *   and a lot of text is likely to take some time to manually translate, even if there are no complex
   *   expressions, UDFs or subqueries. Text length is of little consequence to the transpiler if it is
   *   successful in parsing but there is.
   * </p>
   *
   * @param query the raw text of the query
   * @return a set of statistics about the query text
   */
  def sourceTextComplexity(query: String): SourceTextComplexity = {
    SourceTextComplexity(query.split("\n").length, query.length)
  }

  private def logicalPlanEvaluator: PartialFunction[LogicalPlan, Int] = { case lp: LogicalPlan =>
    try {
      1 // Placeholder
    } catch {
      case NonFatal(_) => 5
    }
  }

  private def expressionEvaluator: PartialFunction[Expression, Int] = { case expr: Expression =>
    // Initial score for any expression
    val initialScore = cost.rules.getOrElse("EXPRESSSION", 1)
    val expressionScore =
      try {
        expr match {
          case ir.ScalarSubquery(relation) =>
            // ScalarSubqueries are a bit more complex than a simple expression and their score
            // is calculated by an addition for the subquery being present, and the sub-query itself
            cost.rules.getOrElse("SUBQUERY", 5) + evaluateTree(relation)

          case uf: ir.UnresolvedFunction =>
            // Unsupported functions are a bit more complex than a simple expression and their score
            // is calculated by an addition for the function being present, and the function itself
            cost.rules.getOrElse("UNSUPPORTED_FUNCTION", 10) + assessFunction(uf)

          case _ => initialScore // Default case for other expressions
        }
      } catch {
        case NonFatal(_) => 5
      }

    // Final score for the expression is the sum of its components
    initialScore + expressionScore
  }

  /**
   * Assess the complexity of an unsupported  function conversion based on our internal knowledge of how
   * the function is used. Some functions indicate data processing that is not supported in Databricks SQL
   * and some will indicate a well-known conversion pattern that is known to be successful.
   * @param func the function definition to analyze
   * @return the conversion complexity score for the function
   */
  private def assessFunction(func: ir.UnresolvedFunction): Int = {
    func match {
      // For instance XML functions are not supported in Databricks SQL and will require manual conversion,
      // which will be a significant amount of work.
      case ir.UnresolvedFunction(name, _, _, _, _) =>
        cost.rules.getOrElse("UNRESOLVED_FUNCTION", 10) + cost.rules.getOrElse(name, 0)

      // All other functions are assumed to be simple verifications
      case _ => 0
    }
  }

  // TODO: Verify these calculations and decide if they are all needed or not. May not harm to keep them around anyway
  // TODO: calculate overall complexity using the stats not just the median score?
  def summarizeComplexity(reportEntries: Seq[EstimationReportRecord]): EstimationStatistics = {
    val scores = reportEntries.map(_.analysisReport.score)

    // Median
    val sortedScores = scores.sorted
    val medianScore = if (sortedScores.size % 2 == 1) {
      sortedScores(sortedScores.size / 2)
    } else {
      val (up, down) = sortedScores.splitAt(sortedScores.size / 2)
      (up.last + down.head) / 2
    }

    // Mean
    val meanScore = scores.sum.toDouble / scores.size

    // Mode
    val modeScore = scores.groupBy(identity).maxBy(_._2.size)._1

    // Standard Deviation
    val mean = scores.sum.toDouble / scores.size
    val variance = scores.map(score => math.pow(score - mean, 2)).sum / scores.size
    val stdDeviation = math.sqrt(variance)

    // Percentiles
    def percentile(p: Double): Double = {
      val k = (p * (sortedScores.size - 1)).toInt
      sortedScores(k)
    }
    val percentile25 = percentile(0.25)
    val percentile50 = percentile(0.50) // Same as median
    val percentile75 = percentile(0.75)

    // Geometric Mean
    val geometricMeanScore = math.pow(scores.map(_.toDouble).product, 1.0 / scores.size)

    EstimationStatistics(
      medianScore,
      meanScore,
      modeScore,
      stdDeviation,
      percentile25,
      percentile50,
      percentile75,
      geometricMeanScore,
      SqlComplexity.fromScore(medianScore))
  }
}
