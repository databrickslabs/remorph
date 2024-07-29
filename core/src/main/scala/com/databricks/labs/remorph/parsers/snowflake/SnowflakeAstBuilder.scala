package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
import com.databricks.labs.remorph.parsers.{ParserCommon, intermediate => ir}

import scala.collection.JavaConverters._

/**
 * @see
 *   org.apache.spark.sql.catalyst.parser.AstBuilder
 */
class SnowflakeAstBuilder extends SnowflakeParserBaseVisitor[ir.LogicalPlan] with ParserCommon[ir.LogicalPlan] {

  private val relationBuilder = new SnowflakeRelationBuilder
  private val ddlBuilder = new SnowflakeDDLBuilder
  private val dmlBuilder = new SnowflakeDMLBuilder

  // TODO investigate why this is needed
  override protected def aggregateResult(aggregate: ir.LogicalPlan, nextResult: ir.LogicalPlan): ir.LogicalPlan = {
    if (nextResult == null) {
      aggregate
    } else {
      nextResult
    }
  }

  override def visitBatch(ctx: BatchContext): ir.LogicalPlan = {
    ir.Batch(visitMany(ctx.sqlCommand()))
  }

  override def visitQueryStatement(ctx: QueryStatementContext): ir.LogicalPlan = {
    val select = ctx.selectStatement().accept(relationBuilder)
    val withCTE = buildCTE(ctx.withExpression(), select)
    ctx.setOperators().asScala.foldLeft(withCTE)(buildSetOperator)

  }

  override def visitDdlCommand(ctx: DdlCommandContext): ir.LogicalPlan =
    ctx.accept(ddlBuilder)

  private def buildCTE(ctx: WithExpressionContext, relation: ir.LogicalPlan): ir.LogicalPlan = {
    if (ctx == null) {
      return relation
    }
    val ctes = relationBuilder.visitMany(ctx.commonTableExpression())
    ir.WithCTE(ctes, relation)
  }

  private def buildSetOperator(left: ir.LogicalPlan, ctx: SetOperatorsContext): ir.LogicalPlan = {
    val right = ctx.selectStatement().accept(relationBuilder)
    val (isAll, setOp) = ctx match {
      case c if c.UNION() != null =>
        (c.ALL() != null, ir.UnionSetOp)
      case c if c.MINUS_() != null || c.EXCEPT() != null =>
        (false, ir.ExceptSetOp)
      case c if c.INTERSECT() != null =>
        (false, ir.IntersectSetOp)
    }
    ir.SetOperation(left, right, setOp, is_all = isAll, by_name = false, allow_missing_columns = false)
  }

  override def visitDmlCommand(ctx: DmlCommandContext): ir.LogicalPlan = ctx match {
    case c if c.queryStatement() != null => c.queryStatement().accept(this)
    case c => c.accept(dmlBuilder)
  }
}
