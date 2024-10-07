package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}
import org.antlr.v4.runtime.tree.RuleNode

import scala.collection.JavaConverters.asScalaBufferConverter

/**
 * @see
 *   org.apache.spark.sql.catalyst.parser.AstBuilder
 */
class TSqlAstBuilder(vc: TSqlVisitorCoordinator)
    extends TSqlParserBaseVisitor[ir.LogicalPlan]
    with IncompleteParser[ir.LogicalPlan]
    with ParserCommon[ir.LogicalPlan] {

  // This can be used in visitor methods when they detect that they are unable to handle some
  // part of the input, or they are placeholders for a real implementation that has not yet been
  // implemented
  protected override def wrapUnresolvedInput(unparsedInput: RuleNode): ir.UnresolvedRelation =
    ir.UnresolvedRelation(getTextFromParserRuleContext(unparsedInput.getRuleContext))

  // The default result is returned when there is no visitor implemented, and we end up visiting terminals
  // or even error nodes (though we should not call the visitor in this system if parsing errors occur).
  protected override def defaultResult(): ir.LogicalPlan = {
    ir.UnresolvedRelation("Unimplemented visitor returns defaultResult!")
  }

  // This gets called when a visitor is not implemented so the default visitChildren is called. As that sometimes
  // returns more than one result because there is more than one child, we need to aggregate the results here. In
  // fact, we should never rely on this. Here we just protect against returning null, but we should implement the
  // visitor.
  override protected def aggregateResult(aggregate: ir.LogicalPlan, nextResult: ir.LogicalPlan): ir.LogicalPlan =
    // Note that here we are just returning one of the nodes, which avoids returning null so long as they are not BOTH
    // null. This is not correct, but it is a placeholder until we implement the missing visitor,
    // so that we get a warning.
    Option(nextResult).getOrElse(aggregate)

  override def visitTSqlFile(ctx: TSqlParser.TSqlFileContext): ir.LogicalPlan = {
    Option(ctx.batch()).map(_.accept(this)).getOrElse(ir.Batch(List()))
  }

  override def visitBatch(ctx: TSqlParser.BatchContext): ir.LogicalPlan = {
    val executeBodyBatchPlan = Option(ctx.executeBodyBatch()).map(_.accept(this))
    val sqlClausesPlans = ctx.sqlClauses().asScala.map(_.accept(this)).collect { case p: ir.LogicalPlan => p }

    executeBodyBatchPlan match {
      case Some(plan) => ir.Batch(plan :: sqlClausesPlans.toList)
      case None => ir.Batch(sqlClausesPlans.toList)
    }
  }

  // TODO: Stored procedure calls etc as batch start
  override def visitExecuteBodyBatch(ctx: TSqlParser.ExecuteBodyBatchContext): ir.LogicalPlan =
    ir.UnresolvedRelation(getTextFromParserRuleContext(ctx))

  override def visitSqlClauses(ctx: TSqlParser.SqlClausesContext): ir.LogicalPlan = {
    ctx match {
      case dml if dml.dmlClause() != null => dml.dmlClause().accept(this)
      case cfl if cfl.cflStatement() != null => cfl.cflStatement().accept(this)
      case another if another.anotherStatement() != null => another.anotherStatement().accept(this)
      case ddl if ddl.ddlClause() != null => ddl.ddlClause().accept(vc.ddlBuilder)
      case dbcc if dbcc.dbccClause() != null => dbcc.dbccClause().accept(this)
      case backup if backup.backupStatement() != null => backup.backupStatement().accept(vc.ddlBuilder)
      case coaFunction if coaFunction.createOrAlterFunction() != null =>
        coaFunction.createOrAlterFunction().accept(this)
      case coaProcedure if coaProcedure.createOrAlterProcedure() != null =>
        coaProcedure.createOrAlterProcedure().accept(this)
      case coaTrigger if coaTrigger.createOrAlterTrigger() != null => coaTrigger.createOrAlterTrigger().accept(this)
      case cv if cv.createView() != null => cv.createView().accept(this)
      case go if go.goStatement() != null => go.goStatement().accept(this)
      case _ => ir.UnresolvedRelation(getTextFromParserRuleContext(ctx))
    }
  }

  override def visitDmlClause(ctx: TSqlParser.DmlClauseContext): ir.LogicalPlan = {
    val dml = ctx match {
      case dml if dml.selectStatement() != null =>
        dml.selectStatement().accept(vc.relationBuilder)
      case _ =>
        ctx.accept(vc.dmlBuilder)
    }

    Option(ctx.withExpression())
      .map { withExpression =>
        val ctes = withExpression.commonTableExpression().asScala.map(_.accept(vc.relationBuilder))
        ir.WithCTE(ctes, dml)
      }
      .getOrElse(dml)
  }
}
