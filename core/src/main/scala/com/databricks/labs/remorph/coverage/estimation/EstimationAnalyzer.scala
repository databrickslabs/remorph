package com.databricks.labs.remorph.coverage.estimation

import com.databricks.labs.remorph.coverage.EstimationReportRecord
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
  def fromScore(score: Double): SqlComplexity = score match {
    case s if s < 10 => LOW
    case s if s < 60 => MEDIUM
    case s if s < 120 => COMPLEX
    case _ => VERY_COMPLEX
  }

  implicit val rw: ReadWriter[SqlComplexity] = ReadWriter.merge(
    macroRW[SqlComplexity.LOW.type],
    macroRW[SqlComplexity.MEDIUM.type],
    macroRW[SqlComplexity.COMPLEX.type],
    macroRW[SqlComplexity.VERY_COMPLEX.type])
}

// TODO: case class ComplexityEstimate(complexity: SqlComplexity, statementCount: Int, charCount: Int, lineCount: Int)
case class SourceTextComplexity(lineCount: Int, textLength: Int)

case class EstimationStatistics(allStats: EstimationStatisticsEntry, successStats: EstimationStatisticsEntry)

object EstimationStatistics {
  implicit val rw: ReadWriter[EstimationStatistics] = macroRW
}

case class EstimationStatisticsEntry(
    medianScore: Int,
    meanScore: Double,
    modeScore: Int,
    stdDeviation: Double,
    percentile25: Double,
    percentile50: Double,
    percentile75: Double,
    geometricMeanScore: Double,
    complexity: SqlComplexity)

object EstimationStatisticsEntry {
  implicit val rw: ReadWriter[EstimationStatisticsEntry] = macroRW
}

class EstimationAnalyzer extends LazyLogging {

  // How much each thing in our analysis discovery costs
  val cost = new RuleDefinitions

  def evaluateTree(node: TreeNode[_]): RuleScore = {
    evaluateTree(node, logicalPlanEvaluator, expressionEvaluator)
  }

  def evaluateTree(
      node: TreeNode[_],
      logicalPlanVisitor: PartialFunction[LogicalPlan, RuleScore],
      expressionVisitor: PartialFunction[Expression, RuleScore]): RuleScore = {

    if (node == null) {
      logger.error("IR_ERROR: Node is null!")
      return RuleScore(
        "IR_ERROR",
        cost.rules.getOrElse("IR_ERROR", 100),
        Seq.empty
      ) // Return default value if the node is null
    }

    node match {
      case lp: LogicalPlan =>
        val currentRuleScore = logicalPlanVisitor.applyOrElse(
          lp,
          (_: LogicalPlan) => RuleScore("IR_ERROR", cost.rules.getOrElse("IR_ERROR", 100), Seq.empty))

        val childrenRuleScores =
          lp.children.map(child => evaluateTree(child, logicalPlanVisitor, expressionVisitor))
        val expressionRuleScores =
          lp.expressions.map(expr => evaluateTree(expr, logicalPlanVisitor, expressionVisitor))

        val childrenValue = childrenRuleScores.map(_.score).sum
        val expressionsValue = expressionRuleScores.map(_.score).sum

        RuleScore(
          currentRuleScore.rule,
          currentRuleScore.score + childrenValue + expressionsValue,
          childrenRuleScores ++ expressionRuleScores)

      case expr: Expression =>
        if (expr.children == null) {
          logger.error("IR_ERROR: Expression has null for children instead of empty list!")
          return RuleScore("IR_ERROR", cost.rules.getOrElse("IR_ERROR", 100), Seq.empty)
        }
        val currentRuleScore = expressionVisitor.applyOrElse(
          expr,
          (_: Expression) => RuleScore("IR_ERROR", cost.rules.getOrElse("IR_ERROR", 100), Seq.empty))
        val childrenRuleScores =
          expr.children.map(child => evaluateTree(child, logicalPlanVisitor, expressionVisitor))
        val childrenValue = childrenRuleScores.map(_.score).sum

        // All expressions have a base cost, plus the cost of the expression itself and its children
        RuleScore(
          "EXPRESSION",
          cost.rules.getOrElse("EXPRESSION", 1) + currentRuleScore.score + childrenValue,
          childrenRuleScores)

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

  private def logicalPlanEvaluator: PartialFunction[LogicalPlan, RuleScore] = { case lp: LogicalPlan =>
    try {
      lp match {
        case ir.UnresolvedCommand(_) =>
          RuleScore("UNSUPPORTED_COMMAND", cost.rules.getOrElse("UNSUPPORTED_COMMAND", 1), Seq.empty)

        case _ =>
          RuleScore(
            "STATEMENT",
            cost.rules.getOrElse("STATEMENT", 1),
            Seq.empty
          ) // Default case for other logical plans
      }

    } catch {
      case NonFatal(_) => RuleScore("IR_ERROR", cost.rules.getOrElse("IR_ERROR", 100), Seq.empty)
    }
  }

  private def expressionEvaluator: PartialFunction[Expression, RuleScore] = { case expr: Expression =>
    try {
      expr match {
        case ir.ScalarSubquery(relation) =>
          // ScalarSubqueries are a bit more complex than a simple expression and their score
          // is calculated by an addition for the subquery being present, and the sub-query itself
          val subqueryScore = evaluateTree(relation)
          RuleScore("SUBQUERY", cost.rules.getOrElse("SUBQUERY", 5) + subqueryScore.score, Seq(subqueryScore))

        case uf: ir.UnresolvedFunction =>
          // Unsupported functions are a bit more complex than a simple expression and their score
          // is calculated by an addition for the function being present, and the function itself
          assessFunction(uf)

        case _ =>
          RuleScore(
            "EXPRESSION",
            cost.rules.getOrElse("EXPRESSION", 1),
            Seq.empty
          ) // Default case for other expressions
      }
    } catch {
      case NonFatal(_) => RuleScore("IR_ERROR", cost.rules.getOrElse("IR_ERROR", 100), Seq.empty)
    }
  }

  /**
   * Assess the complexity of an unsupported  function conversion based on our internal knowledge of how
   * the function is used. Some functions indicate data processing that is not supported in Databricks SQL
   * and some will indicate a well-known conversion pattern that is known to be successful.
   * @param func the function definition to analyze
   * @return the conversion complexity score for the function
   */
  private def assessFunction(func: ir.UnresolvedFunction): RuleScore = {
    func match {
      // For instance XML functions are not supported in Databricks SQL and will require manual conversion,
      // which will be a significant amount of work.
      case ir.UnresolvedFunction(name, _, _, _, _) =>
        RuleScore(
          s"UNRESOLVED_FUNCTION:${name}",
          cost.rules.getOrElse("UNRESOLVED_FUNCTION", 10) + cost.rules.getOrElse(name, 0),
          Seq.empty)
    }
  }

  def summarizeComplexity(reportEntries: Seq[EstimationReportRecord]): EstimationStatistics = {

    // We produce a list fo all scores and a list of all successful transpile scores, which allows to produce
    // statistics on ALL transpilation attempts and at the same time on only successful transpilations. Use case
    // will vary on who is consuming the final reports.
    val scores = reportEntries.map(_.analysisReport.score.score).sorted
    val successScores = reportEntries
      .filter(_.transpilationReport.transpilation_error.isEmpty)
      .map(_.analysisReport.score.score)
      .sorted

    val medianScore = median(scores)
    val meanScore = scores.sum.toDouble / scores.size
    val modeScore = scores.groupBy(identity).maxBy(_._2.size)._1
    val variance = scores.map(score => math.pow(score - meanScore, 2)).sum / scores.size
    val stdDeviation = math.sqrt(variance)
    val percentile25 = percentile(scores, 0.25)
    val percentile50 = percentile(scores, 0.50) // Same as median
    val percentile75 = percentile(scores, 0.75)
    val geometricMeanScore = geometricMean(scores)

    val allStats = EstimationStatisticsEntry(
      medianScore,
      meanScore,
      modeScore,
      stdDeviation,
      percentile25,
      percentile50,
      percentile75,
      geometricMeanScore,
      SqlComplexity.fromScore(geometricMeanScore))

    val successStats = if (successScores.isEmpty) {
      EstimationStatisticsEntry(0, 0, 0, 0, 0, 0, 0, 0, SqlComplexity.LOW)
    } else {
      EstimationStatisticsEntry(
        median(successScores),
        successScores.sum.toDouble / successScores.size,
        successScores.groupBy(identity).maxBy(_._2.size)._1,
        math.sqrt(
          successScores
            .map(score => math.pow(score - (successScores.sum.toDouble / successScores.size), 2))
            .sum / successScores.size),
        percentile(successScores, 0.25),
        percentile(successScores, 0.50), // Same as median
        percentile(successScores, 0.75),
        geometricMean(successScores),
        SqlComplexity.fromScore(geometricMean(successScores)))
    }

    EstimationStatistics(allStats = allStats, successStats = successStats)
  }

  private def percentile(scores: Seq[Int], p: Double): Double = {
    if (scores.isEmpty) {
      0
    } else {
      val k = (p * (scores.size - 1)).toInt
      scores(k)
    }
  }

  private def geometricMean(scores: Seq[Int]): Double = {
    val nonZeroScores = scores.filter(_ != 0)
    if (nonZeroScores.nonEmpty) {
      val logSum = nonZeroScores.map(score => math.log(score.toDouble)).sum
      math.exp(logSum / nonZeroScores.size)
    } else {
      0.0
    }
  }

  def median(scores: Seq[Int]): Int = {
    if (scores.isEmpty) {
      0
    } else if (scores.size % 2 == 1) {
      scores(scores.size / 2)
    } else {
      val (up, down) = scores.splitAt(scores.size / 2)
      (up.last + down.head) / 2
    }
  }

  /**
   * Assigns a conversion complexity score based on how much text is in the query, which is a basic
   * indicator of how much work will be required to manually inspect a query.
   * @param sourceTextComplexity the complexity of the source text
   * @return the score for the complexity of the query
   */
  def assessText(sourceTextComplexity: SourceTextComplexity): Int =
    // TODO: These values are arbitrary and need to be verified in some way
    sourceTextComplexity.lineCount + sourceTextComplexity.textLength match {
      case l if l < 100 => 1
      case l if l < 500 => 5
      case l if l < 1000 => 10
      case l if l < 5000 => 25
      case _ => 50
    }
}
