package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate.IRHelpers
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}
import org.antlr.v4.runtime.tree.RuleNode

import scala.collection.JavaConverters._

class SnowflakeDMLBuilder
    extends SnowflakeParserBaseVisitor[ir.Modification]
    with ParserCommon[ir.Modification]
    with IncompleteParser[ir.Modification]
    with IRHelpers {

  private val expressionBuilder = new SnowflakeExpressionBuilder
  private val relationBuilder = new SnowflakeRelationBuilder

  // This can be used in visitor methods when they detect that they are unable to handle some
  // part of the input, or they are placeholders for a real implementation that has not yet been
  // implemented
  protected override def wrapUnresolvedInput(unparsedInput: RuleNode): ir.Modification =
    ir.UnresolvedModification(getTextFromParserRuleContext(unparsedInput.getRuleContext))

  // The default result is returned when there is no visitor implemented, and we end up visiting terminals
  // or even error nodes (though we should not call the visitor in this system if parsing errors occur).
  protected override def defaultResult(): ir.Modification = {
    ir.UnresolvedModification("Unimplemented visitor returns defaultResult!")
  }

  // This gets called when a visitor is not implemented so the default visitChildren is called. As that sometimes
  // returns more than one result because there is more than one child, we need to aggregate the results here. In
  // fact, we should never rely on this. Here we just protect against returning null, but we should implement the
  // visitor.
  override protected def aggregateResult(aggregate: ir.Modification, nextResult: ir.Modification): ir.Modification =
    // Note that here we are just returning one of the nodes, which avoids returning null so long as they are not BOTH
    // null. This is not correct, but it is a placeholder until we implement the missing visitor,
    // so that we get a warning.
    Option(nextResult).getOrElse(aggregate)

  // Concrete visitors

  override def visitInsertStatement(ctx: InsertStatementContext): ir.Modification = {
    val table = ctx.objectName().accept(relationBuilder)
    val columns = Option(ctx.ids).map(_.asScala).filter(_.nonEmpty).map(_.map(expressionBuilder.visitId))
    val values = ctx match {
      case c if c.queryStatement() != null => c.queryStatement().accept(relationBuilder)
      case c if c.valuesTableBody() != null => c.valuesTableBody().accept(relationBuilder)
    }
    val overwrite = ctx.OVERWRITE() != null
    ir.InsertIntoTable(table, columns, values, None, None, overwrite)
  }

  override def visitDeleteStatement(ctx: DeleteStatementContext): ir.Modification = {
    val target = ctx.tableRef().accept(relationBuilder)
    val where = Option(ctx.predicate()).map(_.accept(expressionBuilder))
    Option(ctx.tablesOrQueries()) match {
      case Some(value) =>
        val relation = relationBuilder.visit(value)
        ir.MergeIntoTable(target, relation, where.getOrElse(ir.Noop), matchedActions = Seq(ir.DeleteAction(None)))
      case None => ir.DeleteFromTable(target, where = where)
    }
  }

  override def visitUpdateStatement(ctx: UpdateStatementContext): ir.Modification = {
    val target = ctx.tableRef().accept(relationBuilder)
    val set = expressionBuilder.visitMany(ctx.setColumnValue())
    val sources =
      Option(ctx.tableSources()).map(t => relationBuilder.visitMany(t.tableSource()).foldLeft(target)(crossJoin))
    val where = Option(ctx.predicate()).map(_.accept(expressionBuilder))
    ir.UpdateTable(target, sources, set, where, None, None)
  }
}
