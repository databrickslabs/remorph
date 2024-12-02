package com.databricks.labs.remorph.coverage.estimation

import com.databricks.labs.remorph.coverage.EstimationReportRecord
import com.databricks.labs.remorph.intermediate.{ParsingErrors}
import com.databricks.labs.remorph.{intermediate => ir}
import com.typesafe.scalalogging.LazyLogging

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
}

case class SourceTextComplexity(lineCount: Int, textLength: Int)

case class ParseFailStats(ruleNameCounts: Map[String, Int], tokenNameCounts: Map[String, Int])

case class EstimationStatistics(
    allStats: EstimationStatisticsEntry,
    successStats: EstimationStatisticsEntry,
    pfStats: ParseFailStats)

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

class EstimationAnalyzer extends LazyLogging {

  def evaluateTree(node: ir.TreeNode[_]): RuleScore = {
    evaluateTree(node, logicalPlanEvaluator, expressionEvaluator)
  }

  def evaluateTree(
      node: ir.TreeNode[_],
      logicalPlanVisitor: PartialFunction[ir.LogicalPlan, RuleScore],
      expressionVisitor: PartialFunction[ir.Expression, RuleScore]): RuleScore = {

    node match {

      case lp: ir.LogicalPlan =>
        val currentRuleScore =
          logicalPlanVisitor.applyOrElse(lp, (_: ir.LogicalPlan) => RuleScore(IrErrorRule(), Seq.empty))

        val childrenRuleScores =
          lp.children.map(child => evaluateTree(child, logicalPlanVisitor, expressionVisitor))
        val expressionRuleScores =
          lp.expressions.map(expr => evaluateTree(expr, logicalPlanVisitor, expressionVisitor))

        val childrenValue = childrenRuleScores.map(_.rule.score).sum
        val expressionsValue = expressionRuleScores.map(_.rule.score).sum

        RuleScore(
          currentRuleScore.rule.plusScore(childrenValue + expressionsValue),
          childrenRuleScores ++ expressionRuleScores)

      case expr: ir.Expression =>
        val currentRuleScore =
          expressionVisitor.applyOrElse(expr, (_: ir.Expression) => RuleScore(IrErrorRule(), Seq.empty))
        val childrenRuleScores =
          expr.children.map(child => evaluateTree(child, logicalPlanVisitor, expressionVisitor))
        val childrenValue = childrenRuleScores.map(_.rule.score).sum

        // All expressions have a base cost, plus the cost of the ir.Expression itself and its children
        RuleScore(currentRuleScore.rule.plusScore(childrenValue), childrenRuleScores)

      case _ =>
        throw new IllegalArgumentException(s"Unsupported node type: ${node.getClass.getSimpleName}")
    }
  }

  /**
   * <p>
   *   Given the raw query text, produce some statistics that are purely derived from the text, rather than
   *   a parsed plan or translation
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

  private def logicalPlanEvaluator: PartialFunction[ir.LogicalPlan, RuleScore] = { case lp: ir.LogicalPlan =>
    try {
      lp match {
        case ir.UnresolvedCommand(_, _, _, _) =>
          RuleScore(UnsupportedCommandRule(), Seq.empty)

        // TODO: Add scores for other logical plans that add more complexity then a simple statement
        case _ =>
          RuleScore(StatementRule(), Seq.empty) // Default case for other logical plans
      }

    } catch {
      case NonFatal(_) => RuleScore(IrErrorRule(), Seq.empty)
    }
  }

  private def expressionEvaluator: PartialFunction[ir.Expression, RuleScore] = { case expr: ir.Expression =>
    try {
      expr match {
        case ir.ScalarSubquery(relation) =>
          // ScalarSubqueries are a bit more complex than a simple ir.Expression and their score
          // is calculated by an addition for the subquery being present, and the sub-query itself
          val subqueryRelationScore = evaluateTree(relation)
          RuleScore(SubqueryRule().plusScore(subqueryRelationScore.rule.score), Seq(subqueryRelationScore))

        case uf: ir.UnresolvedFunction =>
          // Unsupported functions are a bit more complex than a simple ir.Expression and their score
          // is calculated by an addition for the function being present, and the function itself
          assessFunction(uf)

        // TODO: Add specific rules for things that are more complicated than simple expressions such as
        //       UDFs or CASE statements - also cater for all the different Unresolved[type] classes
        case _ =>
          RuleScore(ExpressionRule(), Seq.empty) // Default case for straightforward expressions
      }
    } catch {
      case NonFatal(_) => RuleScore(IrErrorRule(), Seq.empty)
    }
  }

  /**
   * Assess the complexity of an unsupported function conversion based on our internal knowledge of how
   * the function is used. Some functions indicate data processing that is not supported in Databricks SQL
   * and some will indicate a well-known conversion pattern that is known to be successful.
   * @param func the function definition to analyze
   * @return the conversion complexity score for the function
   */
  private def assessFunction(func: ir.UnresolvedFunction): RuleScore = {
    func match {
      // For instance XML functions are not supported in Databricks SQL and will require manual conversion,
      // which will be a significant amount of work.
      case af: ir.UnresolvedFunction =>
        RuleScore(UnsupportedFunctionRule(funcName = af.function_name).resolve(), Seq.empty)
    }
  }

  def summarizeComplexity(reportEntries: Seq[EstimationReportRecord]): EstimationStatistics = {

    // We produce a list of all scores and a list of all successful transpile scores, which allows to produce
    // statistics on ALL transpilation attempts and at the same time on only successful transpilations. Use case
    // will vary on who is consuming the final reports.
    val scores = reportEntries.map(_.analysisReport.score.rule.score).sorted
    val successScores = reportEntries
      .filter(_.transpilationReport.transpiled_statements > 0)
      .map(_.analysisReport.score.rule.score)
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

    EstimationStatistics(allStats, successStats, assessParsingFailures(reportEntries))
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

  /**
   * Find all the report entries where parsing_error is not null, and accumulate the number of times
   * each ruleName and tokenName appears in the errors. This will give us an idea of which rules and
   * tokens, if implemented correctly would have the most impact on increasing the success rate of the
   * parser for the given sample of queries.
   *
   * @param reportEntries the list of all report records
   */
  def assessParsingFailures(reportEntries: Seq[EstimationReportRecord]): ParseFailStats = {
    val ruleNameCounts = scala.collection.mutable.Map[String, Int]().withDefaultValue(0)
    val tokenNameCounts = scala.collection.mutable.Map[String, Int]().withDefaultValue(0)

    reportEntries.foreach(err =>
      err.transpilationReport.parsing_error match {
        case Some(e: ParsingErrors) =>
          e.errors.foreach(e => {
            val ruleName = e.ruleName
            val tokenName = e.offendingTokenName
            ruleNameCounts(ruleName) += 1
            tokenNameCounts(tokenName) += 1
          })
        case _ => // No errors
      })

    val topRuleNames = ruleNameCounts.toSeq.sortBy(-_._2).take(10).toMap
    val topTokenNames = tokenNameCounts.toSeq.sortBy(-_._2).take(10).toMap

    ParseFailStats(topRuleNames, topTokenNames)
  }

}
