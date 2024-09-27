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
class RuleDefinitions {

  // TODO: Maybe we should use a match like we do in FunctionBuilder?

  val rules: Map[String, Int] = Map(
    // We were unable to parse the query at all. This adds a significant amount of work to the conversion, but it is
    // work for the core team, not the user, so are able to filter these out of calculations if desired.
    "PARSE_FAILURE" -> 100,

    // We were able to parse this query, but the logical plan was not generated. This is possibly significant work
    // required from the core team, but it is not necessarily work for the user, so we can filter out these scores
    // from the conversion complexity calculations if desired.
    "PLAN_FAILURE" -> 100,

    // Either the optimizer or the generator failed to produce a result. This is possibly a significant amount of
    // work for the core team, but it is not necessarily work for the user, so we can filter out these scores.
    "TRANSPILE_FAILURE" -> 100,

    // In theory this cannot happen, but it means the toolchain returned some status that we do not understand
    "UNEXPECTED_RESULT" -> 100,

    // An IR error is only flagged when there is something wrong with the IR generation we received. This generally
    // indicates that there is a missing visitor and that the results of visiting some node were null. This is actually
    // a bug in the Remorph code and should be fixed by the core team. This is not work for the user, so we can filter.
    "IR_ERROR" -> 100,

    // Each individual statement in a query is a separate unit of work. This is a low level of work, but it is
    // counted as it will need to be verified in some way.
    "STATEMENT" -> 1,

    // Any expression in the query is a unit of work. This is also low level of work, but it is counted as it will
    // need to be verified in some way.
    "EXPRESSSION" -> 1,

    // Subqueries will tend to add more complexity in human analysis of any query, though there existence does not
    // necessarily mean that it is complex to convert to Databricks SQL. The final score for a sub query is also
    // a function of its component parts.
    "SUBQUERY" -> 5,

    // Unsupported statements and functions etc

    // When we see a function that we do not already support, it either means that this is either a UDF, a function that
    // have not yet been implemented in the transpiler, or a function that is not supported by Databricks SQL at all.
    // This is potentially a significant amount of work to convert, but we will identify functions that we cannot
    // support and provide a higher score for them.
    "UNSUPPORTED_FUNCTION" -> 10,

    // TSQL has functions and constructs that deal with XML that cannot be converted in kind of automated way. These
    // will generally indicate a significant amount of work to convert.
    "OPENXML" -> 25)
}

case class RuleScore(rule: String, score: Int, from: Seq[RuleScore])
object RuleScore {
  implicit val rw: ReadWriter[RuleScore] = macroRW
}
