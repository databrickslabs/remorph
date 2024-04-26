package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.tsql.TSqlParser._
import com.databricks.labs.remorph.parsers.{intermediate => ir}

import scala.collection.JavaConverters._

/**
 * @see
 *   org.apache.spark.sql.catalyst.parser.AstBuilder
 */
class TSqlAstBuilder extends TSqlParserBaseVisitor[ir.TreeNode] {

  // TODO investigate why this is needed
  override protected def aggregateResult(aggregate: ir.TreeNode, nextResult: ir.TreeNode): ir.TreeNode = {
    if (nextResult == null) {
      aggregate
    } else {
      nextResult
    }
  }

  override def visitSelect_statement_standalone(ctx: Select_statement_standaloneContext): ir.TreeNode = {
    val rawExpression = ctx.select_statement().query_expression().query_specification()
    val columnExpression = rawExpression
      .select_list()
      .select_list_elem()
      .asScala
      .map(_.accept(new TSqlExpressionBuilder))
    val fromTable = rawExpression.table_sources().accept(new TSqlRelationBuilder)

    ir.Project(fromTable, columnExpression)

  }

}
