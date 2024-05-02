package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
import com.databricks.labs.remorph.parsers.{intermediate => ir}

import scala.collection.JavaConverters._

/**
 * @see
 *   org.apache.spark.sql.catalyst.parser.AstBuilder
 */
class SnowflakeAstBuilder extends SnowflakeParserBaseVisitor[ir.TreeNode] {

  // TODO investigate why this is needed
  override protected def aggregateResult(aggregate: ir.TreeNode, nextResult: ir.TreeNode): ir.TreeNode = {
    if (nextResult == null) {
      aggregate
    } else {
      nextResult
    }
  }

  override def visitBatch(ctx: BatchContext): ir.TreeNode = {
    ir.Batch(ctx.sql_command().asScala.map(_.accept(this)).collect { case p: ir.Plan => p })
  }

  override def visitQuery_statement(ctx: Query_statementContext): ir.TreeNode = {
    val select = ctx.select_statement().accept(new SnowflakeRelationBuilder)
    val withCTE = buildCTE(ctx.with_expression(), select)
    ctx.set_operators().asScala.foldLeft(withCTE)(buildSetOperator)

  }

  override def visitDdl_command(ctx: Ddl_commandContext): ir.TreeNode =
    ctx.accept(new SnowflakeDDLBuilder)

  private def buildCTE(ctx: With_expressionContext, relation: ir.Relation): ir.Relation = {
    if (ctx == null) {
      return relation
    }
    val ctes = ctx.common_table_expression().asScala.map(_.accept(new SnowflakeRelationBuilder))
    ir.WithCTE(ctes, relation)
  }

  private def buildSetOperator(left: ir.Relation, ctx: Set_operatorsContext): ir.Relation = {
    val right = ctx.select_statement().accept(new SnowflakeRelationBuilder)
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

}
