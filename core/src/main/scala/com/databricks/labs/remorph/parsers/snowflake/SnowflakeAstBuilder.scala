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

  override def visitSelect_statement(ctx: Select_statementContext): ir.TreeNode = {
    val select = ctx.select_optional_clauses().accept(new SnowflakeRelationBuilder)
    val relation =
      if (ctx.limit_clause() != null) {
        val limit = ir.Limit(select, ctx.limit_clause().num(0).getText.toInt)
        if (ctx.limit_clause().OFFSET() != null) {
          ir.Offset(limit, ctx.limit_clause().num(1).getText.toInt)
        } else {
          limit
        }
      } else {
        select
      }
    val selectListElements = ctx.select_clause().select_list_no_top().select_list().select_list_elem().asScala
    val expressionVisitor = new SnowflakeExpressionBuilder
    val expressions: Seq[ir.Expression] = selectListElements.map(_.accept(expressionVisitor))
    ir.Project(relation, expressions)
  }

}
