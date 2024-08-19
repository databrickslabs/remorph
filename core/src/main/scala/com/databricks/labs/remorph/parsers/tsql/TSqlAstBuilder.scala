package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.parsers.intermediate.LogicalPlan
import com.databricks.labs.remorph.parsers.tsql.TSqlParser.DmlClauseContext
import com.databricks.labs.remorph.parsers.{OptionAuto, OptionExpression, OptionOff, OptionOn, OptionString, intermediate => ir}

import scala.collection.JavaConverters.asScalaBufferConverter

/**
 * @see
 *   org.apache.spark.sql.catalyst.parser.AstBuilder
 */
class TSqlAstBuilder extends TSqlParserBaseVisitor[ir.LogicalPlan] {

  private val relationBuilder = new TSqlRelationBuilder
  private val dmlBuilder = new TSqlDMLBuilder
  private val ddlBuilder = new TSqlDDLBuilder

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
  override def visitExecuteBodyBatch(ctx: TSqlParser.ExecuteBodyBatchContext): LogicalPlan =
    ir.UnresolvedRelation(ctx.getText)

  override def visitSqlClauses(ctx: TSqlParser.SqlClausesContext): ir.LogicalPlan = {
    ctx match {
      case dml if dml.dmlClause() != null => dml.dmlClause().accept(this)
      case cfl if cfl.cflStatement() != null => cfl.cflStatement().accept(this)
      case another if another.anotherStatement() != null => another.anotherStatement().accept(this)
      case ddl if ddl.ddlClause() != null => ddl.ddlClause().accept(ddlBuilder)
      case dbcc if dbcc.dbccClause() != null => dbcc.dbccClause().accept(this)
      case backup if backup.backupStatement() != null => backup.backupStatement().accept(ddlBuilder)
      case coaFunction if coaFunction.createOrAlterFunction() != null =>
        coaFunction.createOrAlterFunction().accept(this)
      case coaProcedure if coaProcedure.createOrAlterProcedure() != null =>
        coaProcedure.createOrAlterProcedure().accept(this)
      case coaTrigger if coaTrigger.createOrAlterTrigger() != null => coaTrigger.createOrAlterTrigger().accept(this)
      case cv if cv.createView() != null => cv.createView().accept(this)
      case go if go.goStatement() != null => go.goStatement().accept(this)
      case _ => ir.UnresolvedRelation(ctx.getText)
    }
  }

  override def visitDmlClause(ctx: DmlClauseContext): ir.LogicalPlan = {
    ctx match {
      case insert if insert.insertStatement() != null => insert.insertStatement().accept(relationBuilder)
      case select if select.selectStatementStandalone() != null =>
        select.selectStatementStandalone().accept(relationBuilder)
      case delete if delete.deleteStatement() != null => delete.deleteStatement().accept(relationBuilder)
      case merge if merge.mergeStatement() != null => merge.mergeStatement().accept(relationBuilder)
      case update if update.updateStatement() != null => update.updateStatement().accept(relationBuilder)
      case bulk if bulk.bulkStatement() != null => bulk.bulkStatement().accept(relationBuilder)
      case _ => ir.UnresolvedRelation(ctx.getText)
    }
  }

  override def visitDmlClause(ctx: TSqlParser.DmlClauseContext): ir.LogicalPlan = {
    val dml = ctx match {
      case dml if dml.selectStatement() != null =>
        dml.selectStatement().accept(relationBuilder)
      case _ =>
        ctx.accept(dmlBuilder)
    }

    Option(ctx.withExpression())
      .map { withExpression =>
        val ctes = withExpression.commonTableExpression().asScala.map(_.accept(relationBuilder))
        ir.WithCTE(ctes, dml)
      }
      .getOrElse(dml)
  }
}
