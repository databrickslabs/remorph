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

  override def visitQuery_statement(ctx: Query_statementContext): ir.TreeNode = {
    val select = ctx.select_statement().accept(new SnowflakeRelationBuilder)
    buildCTE(ctx.with_expression(), select)
  }

  private def buildCTE(ctx: With_expressionContext, relation: ir.Relation): ir.Relation = {
    if (ctx == null) {
      relation
    } else {
      val ctes = ctx.common_table_expression().asScala.map(_.accept(new SnowflakeRelationBuilder))
      ir.WithCTE(ctes, relation)
    }
  }

}
