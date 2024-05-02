package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.tsql.TSqlParser.Select_statement_standaloneContext
import com.databricks.labs.remorph.parsers.{intermediate => ir}

import scala.collection.JavaConverters._

/**
 * @see
 *   org.apache.spark.sql.catalyst.parser.AstBuilder
 */
class TSqlAstBuilder extends TSqlParserBaseVisitor[ir.TreeNode] {

  // When a node has multiple children, this method is called to aggregate the results and returns
  // the IR that represents the node as a whole.
  // TODO: JI: This is probably because the grammar is poorly designed. I will get to that later
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

    // [TODO]: Handle Where, Group By, Having, Order By, Limit, Offset
    val tableSources = Option(rawExpression.table_sources())
      .fold[ir.Relation](ir.NoTable())(_.accept(new TSqlRelationBuilder))
    ir.Project(tableSources, columnExpression)
  }
}
