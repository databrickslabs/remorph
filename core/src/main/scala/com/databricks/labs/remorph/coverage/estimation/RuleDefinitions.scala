package com.databricks.labs.remorph.coverage.estimation

import upickle.default._

/**
 * <p>Defines the rules and their related score for conversion complexity estimation.
 * </p>
 * <p>
 *   The rules are defined as a map of rule name to score, and their descriptions are expected to be
 *   stored somewhere more relevant to the dashboard reporting system (where they can also be subject
 *   to i18n/l10n).
 * </p>
 * <p>
 *   Rules that are matched by the analyzer will be used to calculate the complexity of the query in terms
 *   of how much effort it is to convert it to Databricks SQL and not necessarily how complex the query is in
 *   terms of say execution time or resource requirements. While there are rules to score for the inability
 *   to parse, generate IR and transpile, they are essentially capturing work for the core team rather than
 *   the user/porting team. Such scores can optionally be ruled out of conversion complexity calculations but
 *   are useful to assess the work required from the core Remorph team.
 * </p>
 */
sealed trait Rule {
  def score: Int
  def plusScore(newScore: Int): Rule // Adds the given score to the current score
}
@upickle.implicits.serializeDefaults(true)
object Rule {
  implicit val rw: ReadWriter[Rule] = macroRW
}

/**
 * Transpilation was successful so we can reduce the score, but it is not zero because there will be some
 * effort required to verify the translation.
 */
@upickle.implicits.serializeDefaults(true)
case class SuccessfulTranspileRule(override val score: Int = 5) extends Rule {
  override def plusScore(newScore: Int): SuccessfulTranspileRule = this.copy(score = newScore + this.score)
}
object SuccessfulTranspileRule {
  implicit val rw: ReadWriter[SuccessfulTranspileRule] = macroRW
}

/**
 * We were unable to parse the query at all. This adds a significant amount of work to the conversion, but it is
 * work for the core team, not the user, so are able to filter these out of calculations if desired.
 */
@upickle.implicits.serializeDefaults(true)
case class ParseFailureRule(score: Int = 100) extends Rule {
  override def plusScore(newScore: Int): ParseFailureRule = this.copy(score = newScore + this.score)
}
object ParseFailureRule {
  implicit val rw: ReadWriter[ParseFailureRule] = macroRW
}

/**
 * We were able to parse this query, but the logical plan was not generated. This is possibly significant work
 * required from the core team, but it is not necessarily work for the user, so we can filter out these scores
 * from the conversion complexity calculations if desired.
 */
@upickle.implicits.serializeDefaults(true)
case class PlanFailureRule(score: Int = 100) extends Rule {
  override def plusScore(newScore: Int): PlanFailureRule = this.copy(score = newScore + this.score)
}
object PlanFailureRule {
  implicit val rw: ReadWriter[PlanFailureRule] = macroRW
}

/**
 * Either the optimizer or the generator failed to produce a result. This is possibly a significant amount of
 * work for the core team, but it is not necessarily work for the user, so we can filter out these scores.
 */
@upickle.implicits.serializeDefaults(true)
case class TranspileFailureRule(override val score: Int = 100) extends Rule {
  override def plusScore(newScore: Int): TranspileFailureRule = this.copy(score = newScore + this.score)
}
object TranspileFailureRule {
  implicit val rw: ReadWriter[TranspileFailureRule] = macroRW
}

/**
 * In theory this cannot happen, but it means the toolchain returned some status that we do not understand
 */
@upickle.implicits.serializeDefaults(true)
case class UnexpectedResultRule(override val score: Int = 100) extends Rule {
  override def plusScore(newScore: Int): UnexpectedResultRule = this.copy(score = newScore + this.score)
}
object UnexpectedResultRule {
  implicit val rw: ReadWriter[UnexpectedResultRule] = macroRW
}

/**
 * An IR error is only flagged when there is something wrong with the IR generation we received. This generally
 * indicates that there is a missing visitor and that the results of visiting some node were null. This is actually
 * a bug in the Remorph code and should be fixed by the core team. This is not work for the user, so we can filter.
 */
@upickle.implicits.serializeDefaults(true)
case class IrErrorRule(override val score: Int = 100) extends Rule {
  override def plusScore(newScore: Int): IrErrorRule = this.copy(score = newScore + this.score)
}
object IrErrorRule {
  implicit val rw: ReadWriter[IrErrorRule] = macroRW
}

/**
 * Each individual statement in a query is a separate unit of work. This is a low level of work, but it is
 * counted as it will need to be verified in some way.
 */
@upickle.implicits.serializeDefaults(true)
case class StatementRule(override val score: Int = 1) extends Rule {
  override def plusScore(newScore: Int): StatementRule = this.copy(score = newScore + this.score)
}
object StatementRule {
  implicit val rw: ReadWriter[StatementRule] = macroRW
}

/**
 * Any expression in the query is a unit of work. This is also a low level of work, but it is counted as it will
 * need to be verified in some way.
 */
@upickle.implicits.serializeDefaults(true)
case class ExpressionRule(override val score: Int = 1) extends Rule {
  override def plusScore(newScore: Int): ExpressionRule = this.copy(score = newScore + this.score)
}
object ExpressionRule {
  implicit val rw: ReadWriter[ExpressionRule] = macroRW
}

/**
 * Subqueries will tend to add more complexity in human analysis of any query, though their existence does not
 * necessarily mean that it is complex to convert to Databricks SQL. The final score for a sub query is also
 * a function of its component parts.
 */
@upickle.implicits.serializeDefaults(true)
case class SubqueryRule(override val score: Int = 5) extends Rule {
  override def plusScore(newScore: Int): SubqueryRule = this.copy(score = newScore + this.score)
}
object SubqueryRule {
  implicit val rw: ReadWriter[SubqueryRule] = macroRW
}

// Unsupported statements and functions etc

/**
 * When we see a function that we do not already support, it either means that this is either a UDF,
 * a function that we have not yet been implemented in the transpiler, or a function that is not
 * supported by Databricks SQL at all.
 * This is potentially a significant amount of work to convert, but in some case we will identify the
 * individual functions that we cannot support automatically at all and provide a higher score for them.
 * For instance XML functions in TSQL.
 */
@upickle.implicits.serializeDefaults(true)
case class UnsupportedFunctionRule(override val score: Int = 10, funcName: String) extends Rule {
  override def plusScore(newScore: Int): UnsupportedFunctionRule = this.copy(score = newScore + this.score)
  def resolve(): UnsupportedFunctionRule = this.copy(score = funcName match {

    // TODO: Add scores for the various unresolved functions that we know will be extra complicated to convert
    case "OPENXML" => 25
    case _ => 10
  })
}
object UnsupportedFunctionRule {
  implicit val rw: ReadWriter[UnsupportedFunctionRule] = macroRW
}

/**
 * When we see a command that we do not support, it either means that this is a command that we have not yet
 * implemented or that we can never implement it and it is going to add a lot of complexity to the conversion.
 */
@upickle.implicits.serializeDefaults(true)
case class UnsupportedCommandRule(override val score: Int = 10) extends Rule {
  override def plusScore(newScore: Int): UnsupportedCommandRule = this.copy(score = newScore + this.score)
}
object UnsupportedCommandRule {
  implicit val rw: ReadWriter[UnsupportedCommandRule] = macroRW
}

case class RuleScore(rule: Rule, from: Seq[RuleScore])
object RuleScore {
  implicit val rw: ReadWriter[RuleScore] = macroRW
}
