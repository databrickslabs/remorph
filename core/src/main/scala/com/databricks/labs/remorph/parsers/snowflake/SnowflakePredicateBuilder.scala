package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.{NotYetImplemented, UnexpectedParserOutput, intermediate => ir}
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._

class SnowflakePredicateBuilder extends SnowflakeParserBaseVisitor[ir.Predicate] {
  override def visitExpr(ctx: ExprContext): ir.Predicate = {

    def buildComparison(left: ir.Expression, right: ir.Expression, op: Comparison_operatorContext): ir.Predicate = {
      if (op.EQ() != null) {
        ir.Equals(left, right)
      } else if (op.NE() != null || op.LTGT() != null) {
        ir.NotEquals(left, right)
      } else if (op.GT() != null) {
        ir.GreaterThan(left, right)
      } else if (op.LT() != null) {
        ir.LesserThan(left, right)
      } else if (op.GE() != null) {
        ir.GreaterThanOrEqual(left, right)
      } else if (op.LE() != null) {
        ir.LesserThanOrEqual(left, right)
      } else {
        throw UnexpectedParserOutput("Comparison operator is expected to be one of [=, !=, <>, >, <, >=, <=]")
      }
    }

    if (ctx.AND() != null) {
      val left = ctx.expr(0).accept(this)
      val right = ctx.expr(1).accept(this)
      ir.And(left, right)
    } else if (ctx.OR() != null) {
      val left = ctx.expr(0).accept(this)
      val right = ctx.expr(1).accept(this)
      ir.Or(left, right)
    } else if (ctx.comparison_operator() != null) {
      val left = ctx.expr(0).accept(new SnowflakeExpressionBuilder)
      val right = ctx.expr(1).accept(new SnowflakeExpressionBuilder)
      buildComparison(left, right, ctx.comparison_operator())
    } else {
      throw NotYetImplemented("Only predicate combinators among [AND, OR] are accepted thus far")
    }
  }

  override def visitSearch_condition(ctx: Search_conditionContext): ir.Predicate = {
    val pred = ctx.predicate().accept(this)
    // TODO: investigate why NOT() is a list here
    if (ctx.NOT().size() > 0) {
      ir.Not(pred)
    } else {
      pred
    }
  }

}
