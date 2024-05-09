package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.tsql.TSqlParser.SelectStatementStandaloneContext
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

  override def visitSelectStatementStandalone(ctx: SelectStatementStandaloneContext): ir.TreeNode = {
    val rawExpression = ctx.selectStatement().queryExpression().querySpecification()
    val columnExpression = rawExpression
      .selectList()
      .selectListElem()
      .asScala
      .map(_.accept(new TSqlExpressionBuilder))

    // [TODO]: Handle Where, Group By, Having, Order By, Limit, Offset
    val tableSources = Option(rawExpression.tableSources())
      .fold[ir.Relation](ir.NoTable())(_.accept(new TSqlRelationBuilder))
    ir.Project(tableSources, columnExpression)
  }
}
