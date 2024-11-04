package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.intermediate.procedures.SetVariable
import com.databricks.labs.remorph.parsers.ParserCommon
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.{StringContext => _, _}
import com.databricks.labs.remorph.{intermediate => ir}

class SnowflakeCommandBuilder(override val vc: SnowflakeVisitorCoordinator)
    extends SnowflakeParserBaseVisitor[ir.Command]
    with ParserCommon[ir.Command] {

  // The default result is returned when there is no visitor implemented, and we produce an unresolved
  // object to represent the input that we have no visitor for.
  protected override def unresolved(ruleText: String, message: String): ir.Command =
    ir.UnresolvedCommand(ruleText, message)

  // Concrete visitors

  // TODO: Implement Cursor and Exception for Declare Statements.
  // TODO: Implement Cursor for Let Statements.

  override def visitDeclareWithDefault(ctx: DeclareWithDefaultContext): ir.Command =
    errorCheck(ctx) match {
      case Some(errorResult) => errorResult
      case None =>
        val variableName = ctx.id().accept(vc.expressionBuilder).asInstanceOf[ir.Id]
        val dataType = vc.typeBuilder.buildDataType(ctx.dataType())
        val variableValue = ctx.expr().accept(vc.expressionBuilder)
        ir.CreateVariable(variableName, dataType, Some(variableValue), replace = false)
    }

  override def visitDeclareSimple(ctx: DeclareSimpleContext): ir.Command =
    errorCheck(ctx) match {
      case Some(errorResult) => errorResult
      case None =>
        val variableName = ctx.id().accept(vc.expressionBuilder).asInstanceOf[ir.Id]
        val dataType = vc.typeBuilder.buildDataType(ctx.dataType())
        ir.CreateVariable(variableName, dataType, None, replace = false)
    }

  override def visitDeclareResultSet(ctx: DeclareResultSetContext): ir.Command =
    errorCheck(ctx) match {
      case Some(errorResult) => errorResult
      case None =>
        val variableName = ctx.id().accept(vc.expressionBuilder).asInstanceOf[ir.Id]
        val variableValue = ctx.expr() match {
          case null => None
          case stmt => Some(stmt.accept(vc.expressionBuilder))
        }
        val dataType = ir.StructType(Seq())
        ir.CreateVariable(variableName, dataType, variableValue, replace = false)
    }

  override def visitLetVariableAssignment(ctx: LetVariableAssignmentContext): ir.Command =
    errorCheck(ctx) match {
      case Some(errorResult) => errorResult
      case None =>
        val variableName = ctx.id().accept(vc.expressionBuilder).asInstanceOf[ir.Id]
        val variableValue = ctx.expr().accept(vc.expressionBuilder)

        val variableDataType = variableValue match {
          case s: ir.ScalarSubquery => Some(s.dataType)
          case _ => Option(ctx.dataType()).flatMap(dt => Some(vc.typeBuilder.buildDataType(dt)))
        }
        SetVariable(variableName, variableValue, variableDataType)
    }

  override def visitExecuteTask(ctx: ExecuteTaskContext): ir.Command = {
    ir.UnresolvedCommand(
      ruleText = contextText(ctx),
      message = "Execute Task is not yet supported",
      ruleName = vc.ruleName(ctx),
      tokenName = Some(tokenName(ctx.getStart)))
  }

  override def visitOtherCommand(ctx: OtherCommandContext): ir.Command =
    errorCheck(ctx) match {
      case Some(errorResult) => errorResult
      case None =>
        ctx match {
          case c if c.copyIntoTable != null => c.copyIntoTable.accept(this)
          case c if c.copyIntoLocation != null => c.copyIntoLocation.accept(this)
          case c if c.comment != null => c.comment.accept(this)
          case c if c.commit != null => c.commit.accept(this)
          case e if e.executeImmediate != null => e.executeImmediate.accept(this)
          case e if e.executeTask != null => e.executeTask.accept(this)
          case e if e.explain != null => e.explain.accept(this)
          case g if g.getDml != null => g.getDml.accept(this)
          case g if g.grantOwnership != null => g.grantOwnership.accept(this)
          case g if g.grantToRole != null => g.grantToRole.accept(this)
          case g if g.grantToShare != null => g.grantToShare.accept(this)
          case g if g.grantRole != null => g.grantRole.accept(this)
          case l if l.list != null => l.list.accept(this)
          case p if p.put != null => p.put.accept(this)
          case r if r.remove != null => r.remove.accept(this)
          case r if r.revokeFromRole != null => r.revokeFromRole.accept(this)
          case r if r.revokeFromShare != null => r.revokeFromShare.accept(this)
          case r if r.revokeRole != null => r.revokeRole.accept(this)
          case r if r.rollback != null => r.rollback.accept(this)
          case s if s.set != null => s.set.accept(this)
          case t if t.truncateMaterializedView != null => t.truncateMaterializedView.accept(this)
          case t if t.truncateTable != null => t.truncateTable.accept(this)
          case u if u.unset != null => u.unset.accept(this)
          case c if c.call != null => c.call.accept(this)
          case b if b.beginTxn != null => b.beginTxn.accept(this)
          case d if d.declareCommand != null => d.declareCommand.accept(this)
          case l if l.let != null => l.let.accept(this)
        }
    }
}
