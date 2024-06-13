package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.tsql.TSqlParser.{DmlClauseContext, SelectStatementStandaloneContext}
import com.databricks.labs.remorph.parsers.{intermediate => ir}

import scala.collection.JavaConverters.asScalaBufferConverter

/**
 * @see
 *   org.apache.spark.sql.catalyst.parser.AstBuilder
 */
class TSqlAstBuilder extends TSqlParserBaseVisitor[ir.TreeNode] {

  override def visitTSqlFile(ctx: TSqlParser.TSqlFileContext): ir.TreeNode = {
    Option(ctx.batch()).map(_.accept(this)).getOrElse(ir.Batch(List()))
  }

  override def visitBatch(ctx: TSqlParser.BatchContext): ir.TreeNode = {
    // TODO: Rework the tsqlFile rule
    ir.Batch(ctx.sqlClauses().asScala.map(_.accept(this)).collect { case p: ir.Plan => p })
  }

  override def visitSqlClauses(ctx: TSqlParser.SqlClausesContext): ir.TreeNode = {
    // TODO: Implement the rest of the SQL clauses
    ctx.dmlClause().accept(this)
  }

  override def visitDmlClause(ctx: DmlClauseContext): ir.TreeNode = {
    // TODO: Implement the rest of the DML clauses
    ctx.selectStatementStandalone().accept(this)
  }

  /**
   * Build a complete AST for a select statement.
   * @param ctx
   *   the parse tree
   */
  override def visitSelectStatementStandalone(ctx: SelectStatementStandaloneContext): ir.TreeNode =
    ctx.accept(new TSqlRelationBuilder)
}
