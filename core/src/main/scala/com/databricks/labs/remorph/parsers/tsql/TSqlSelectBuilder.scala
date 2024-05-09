package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{intermediate => ir}

/**
 * This visitor is responsible for building the IR for a SELECT statement.
 *
 * It utilizes specialized visitors for the sub-elements of a SELECT statement, such as a column, a relation, etc.
 */
class TSqlSelectBuilder extends TSqlParserBaseVisitor[ir.TreeNode] {

  override def visitSelectStatementStandalone(ctx: TSqlParser.SelectStatementStandaloneContext): ir.TreeNode = {

    // TODO: Process ctx.WithExpression
    ctx.selectStatement().accept(this)
    // val tableSources = Option(rawExpression.tableSources()).fold[ir.Relation](ir.NoTable())
    // (_.accept(new TSqlRelationBuilder))
  }

  override def visitSelectStatement(ctx: TSqlParser.SelectStatementContext): ir.TreeNode = {
    // TODO: val orderByClause = Option(ctx.selectOrderByClause).map(_.accept(this))
    // TODO: val forClause = Option(ctx.forClause).map(_.accept(this))
    // TODO: val optionClause = Option(ctx.optionClause).map(_.accept(this))

    ctx.queryExpression.accept(this)
  }

  override def visitQuerySpecification(ctx: TSqlParser.QuerySpecificationContext): ir.TreeNode = {

    // TODO: Process all the other elements of a query specification

    val columns = ctx.selectList.accept(new TSqlColumnBuilder).asInstanceOf[ir.ExpressionList].expressions
    val from = Option(ctx.tableSources()).map(_.accept(new TSqlRelationBuilder)).getOrElse(ir.NoTable())

    ir.Project(from, columns)
  }

}
