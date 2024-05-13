package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.tsql.TSqlParser.SelectStatementStandaloneContext
import com.databricks.labs.remorph.parsers.{intermediate => ir}

/**
 * @see
 *   org.apache.spark.sql.catalyst.parser.AstBuilder
 */
class TSqlAstBuilder extends TSqlParserBaseVisitor[ir.TreeNode] {

  // When a node has multiple children, this method is called to aggregate the results and returns
  // the IR that represents the node as a whole.
  // TODO: JI: Because some elements create nodes with multiple children, we need to aggregate them here.
  // In this case it is coming from visiting Batch etc and not doing anything with them
  override protected def aggregateResult(aggregate: ir.TreeNode, nextResult: ir.TreeNode): ir.TreeNode = {
    if (nextResult == null) {
      aggregate
    } else {
      nextResult
    }
  }

  /**
   * Build a complete AST for a select statement.
   * @param ctx
   *   the parse tree
   */
  override def visitSelectStatementStandalone(ctx: SelectStatementStandaloneContext): ir.TreeNode =
    ctx.accept(new TSqlRelationBuilder)
}
