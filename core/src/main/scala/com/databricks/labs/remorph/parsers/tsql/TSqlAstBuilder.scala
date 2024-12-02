package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.intermediate.LogicalPlan
import com.databricks.labs.remorph.parsers.ParserCommon
import com.databricks.labs.remorph.{intermediate => ir}

import scala.collection.JavaConverters.asScalaBufferConverter

/**
 * @see
 *   org.apache.spark.sql.catalyst.parser.AstBuilder
 */
class TSqlAstBuilder(override val vc: TSqlVisitorCoordinator)
    extends TSqlParserBaseVisitor[ir.LogicalPlan]
    with ParserCommon[ir.LogicalPlan] {

  // The default result is returned when there is no visitor implemented, and we produce an unresolved
  // object to represent the input that we have no visitor for.
  protected override def unresolved(ruleText: String, message: String): ir.LogicalPlan =
    ir.UnresolvedRelation(ruleText = ruleText, message = message)

  // Concrete visitors

  override def visitTSqlFile(ctx: TSqlParser.TSqlFileContext): ir.LogicalPlan = {

    // This very top level visitor does not ignore any valid statements for the batch, instead
    // we prepend any errors to the batch plan, so they are generated first in the output.
    val errors = errorCheck(ctx)
    val batchPlan = Option(ctx.batch()).map(buildBatch).getOrElse(Seq.empty)
    errors match {
      case Some(errorResult) => ir.Batch(errorResult +: batchPlan)
      case None => ir.Batch(batchPlan)
    }
  }

  private def buildBatch(ctx: TSqlParser.BatchContext): Seq[LogicalPlan] = {

    // This very top level visitor does not ignore any valid statements for the batch, instead
    // we prepend any errors to the batch plan, so they are generated first in the output.
    val errors = errorCheck(ctx)
    val executeBodyBatchPlan = Option(ctx.executeBodyBatch()).map(_.accept(this))
    val sqlClausesPlans = ctx.sqlClauses().asScala.map(_.accept(this)).collect { case p: ir.LogicalPlan => p }

    val validStatements = executeBodyBatchPlan match {
      case Some(plan) => plan +: sqlClausesPlans
      case None => sqlClausesPlans
    }
    errors match {
      case Some(errorResult) => errorResult +: validStatements
      case None => validStatements
    }
  }

  // TODO: Stored procedure calls etc as batch start
  override def visitExecuteBodyBatch(ctx: TSqlParser.ExecuteBodyBatchContext): ir.LogicalPlan = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.UnresolvedRelation(
        ruleText = contextText(ctx),
        message = "Execute body batch is not supported yet",
        ruleName = vc.ruleName(ctx),
        tokenName = Some(tokenName(ctx.getStart)))
  }

  override def visitSqlClauses(ctx: TSqlParser.SqlClausesContext): ir.LogicalPlan = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
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
        case _ =>
          ir.UnresolvedRelation(
            ruleText = contextText(ctx),
            message = s"Unknown SQL clause ${ctx.getStart.getText} in TSqlAstBuilder.visitSqlClauses",
            ruleName = vc.ruleName(ctx),
            tokenName = Some(tokenName(ctx.getStart)))
      }
  }

  override def visitDmlClause(ctx: TSqlParser.DmlClauseContext): ir.LogicalPlan = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
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
