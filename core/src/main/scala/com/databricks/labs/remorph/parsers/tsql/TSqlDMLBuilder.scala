package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.ParserCommon
import com.databricks.labs.remorph.parsers.tsql.TSqlParser.{StringContext => _, _}
import com.databricks.labs.remorph.parsers.tsql.rules.InsertDefaultsAction
import com.databricks.labs.remorph.{intermediate => ir}

import scala.collection.JavaConverters.asScalaBufferConverter
class TSqlDMLBuilder(override val vc: TSqlVisitorCoordinator)
    extends TSqlParserBaseVisitor[ir.Modification]
    with ParserCommon[ir.Modification] {

  // The default result is returned when there is no visitor implemented, and we produce an unresolved
  // object to represent the input that we have no visitor for.
  protected override def unresolved(ruleText: String, message: String): ir.Modification =
    ir.UnresolvedModification(ruleText = ruleText, message = message)

  // Concrete visitors

  override def visitDmlClause(ctx: DmlClauseContext): ir.Modification = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx match {
        // NB: select is handled by the relationBuilder
        case dml if dml.insert() != null => dml.insert.accept(this)
        case dml if dml.delete() != null => dml.delete().accept(this)
        case dml if dml.merge() != null => dml.merge().accept(this)
        case dml if dml.update() != null => dml.update().accept(this)
        case bulk if bulk.bulkStatement() != null => bulk.bulkStatement().accept(this)
        case _ =>
          ir.UnresolvedModification(
            ruleText = contextText(ctx),
            message = s"Unknown DML clause ${ctx.getStart.getText} in TSqlDMLBuilder.visitDmlClause",
            ruleName = vc.ruleName(ctx),
            tokenName = Some(tokenName(ctx.getStart)))
      }
  }

  override def visitMerge(ctx: MergeContext): ir.Modification = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val targetPlan = ctx.ddlObject().accept(vc.relationBuilder)
      val hints = vc.relationBuilder.buildTableHints(Option(ctx.withTableHints()))
      val finalTarget = if (hints.nonEmpty) {
        ir.TableWithHints(targetPlan, hints)
      } else {
        targetPlan
      }

      val mergeCondition = ctx.searchCondition().accept(vc.expressionBuilder)
      val tableSourcesPlan = ctx.tableSources().tableSource().asScala.map(_.accept(vc.relationBuilder))
      // Reduce is safe: Grammar rule for tableSources ensures that there is always at least one tableSource.
      val sourcePlan = tableSourcesPlan.reduceLeft(
        ir.Join(_, _, None, ir.CrossJoin, Seq(), ir.JoinDataType(is_left_struct = false, is_right_struct = false)))

      // We may have a number of when clauses, each with a condition and an action. We keep the ANTLR syntax compact
      // and lean and determine which of the three types of action we have in the whenMatch method based on
      // the presence or absence of syntactical elements NOT and SOURCE as SOURCE can only be used with NOT
      val (matchedActions, notMatchedActions, notMatchedBySourceActions) = Option(ctx.whenMatch())
        .map(_.asScala.foldLeft((List.empty[ir.MergeAction], List.empty[ir.MergeAction], List.empty[ir.MergeAction])) {
          case ((matched, notMatched, notMatchedBySource), m) =>
            val action = buildWhenMatch(m)
            (m.NOT(), m.SOURCE()) match {
              case (null, _) => (action :: matched, notMatched, notMatchedBySource)
              case (_, null) => (matched, action :: notMatched, notMatchedBySource)
              case _ => (matched, notMatched, action :: notMatchedBySource)
            }
        })
        .getOrElse((List.empty, List.empty, List.empty))

      val optionClause = Option(ctx.optionClause).map(_.accept(vc.expressionBuilder))
      val outputClause = Option(ctx.outputClause()).map(buildOutputClause)

      val mergeIntoTable = ir.MergeIntoTable(
        finalTarget,
        sourcePlan,
        mergeCondition,
        matchedActions,
        notMatchedActions,
        notMatchedBySourceActions)

      val withOptions = optionClause match {
        case Some(option) => ir.WithModificationOptions(mergeIntoTable, option)
        case None => mergeIntoTable
      }

      outputClause match {
        case Some(output) => WithOutputClause(withOptions, output)
        case None => withOptions
      }
  }

  private def buildWhenMatch(ctx: WhenMatchContext): ir.MergeAction = {
    val condition = Option(ctx.searchCondition()).map(_.accept(vc.expressionBuilder))
    ctx.mergeAction() match {
      case action if action.DELETE() != null => ir.DeleteAction(condition)
      case action if action.UPDATE() != null => buildUpdateAction(action, condition)
      case action if action.INSERT() != null => buildInsertAction(action, condition)
    }
  }

  private def buildInsertAction(ctx: MergeActionContext, condition: Option[ir.Expression]): ir.MergeAction = {

    ctx match {
      case action if action.DEFAULT() != null => InsertDefaultsAction(condition)
      case _ =>
        val assignments =
          (ctx.cols
            .expression()
            .asScala
            .map(_.accept(vc.expressionBuilder)) zip ctx.vals.expression().asScala.map(_.accept(vc.expressionBuilder)))
            .map { case (col, value) =>
              ir.Assign(col, value)
            }
        ir.InsertAction(condition, assignments)
    }
  }

  private def buildUpdateAction(ctx: MergeActionContext, condition: Option[ir.Expression]): ir.UpdateAction = {
    val setElements = ctx.updateElem().asScala.collect { case elem =>
      elem.accept(vc.expressionBuilder) match {
        case assign: ir.Assign => assign
      }
    }
    ir.UpdateAction(condition, setElements)
  }

  override def visitUpdate(ctx: UpdateContext): ir.Modification = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val target = ctx.ddlObject().accept(vc.relationBuilder)
      val hints = vc.relationBuilder.buildTableHints(Option(ctx.withTableHints()))
      val hintTarget = if (hints.nonEmpty) {
        ir.TableWithHints(target, hints)
      } else {
        target
      }

      val finalTarget = vc.relationBuilder.buildTop(Option(ctx.topClause()), hintTarget)
      val output = Option(ctx.outputClause()).map(buildOutputClause)
      val setElements = ctx.updateElem().asScala.map(_.accept(vc.expressionBuilder))

      val sourceRelation = buildTableSourcesPlan(Option(ctx.tableSources()))
      val where = Option(ctx.updateWhereClause()) map (_.accept(vc.expressionBuilder))
      val optionClause = Option(ctx.optionClause).map(_.accept(vc.expressionBuilder))
      ir.UpdateTable(finalTarget, sourceRelation, setElements, where, output, optionClause)
  }

  override def visitDelete(ctx: DeleteContext): ir.Modification = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val target = ctx.ddlObject().accept(vc.relationBuilder)
      val hints = vc.relationBuilder.buildTableHints(Option(ctx.withTableHints()))
      val finalTarget = if (hints.nonEmpty) {
        ir.TableWithHints(target, hints)
      } else {
        target
      }

      val output = Option(ctx.outputClause()).map(buildOutputClause)
      val sourceRelation = buildTableSourcesPlan(Option(ctx.tableSources()))
      val where = Option(ctx.updateWhereClause()) map (_.accept(vc.expressionBuilder))
      val optionClause = Option(ctx.optionClause).map(_.accept(vc.expressionBuilder))
      ir.DeleteFromTable(finalTarget, sourceRelation, where, output, optionClause)
  }

  private[this] def buildTableSourcesPlan(tableSources: Option[TableSourcesContext]): Option[ir.LogicalPlan] = {
    val sources = tableSources
      .map(_.tableSource().asScala)
      .getOrElse(Seq())
      .map(_.accept(vc.relationBuilder))
    sources.reduceLeftOption(
      ir.Join(_, _, None, ir.CrossJoin, Seq(), ir.JoinDataType(is_left_struct = false, is_right_struct = false)))
  }

  override def visitInsert(ctx: InsertContext): ir.Modification = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val target = ctx.ddlObject().accept(vc.relationBuilder)
      val hints = vc.relationBuilder.buildTableHints(Option(ctx.withTableHints()))
      val finalTarget = if (hints.nonEmpty) {
        ir.TableWithHints(target, hints)
      } else {
        target
      }

      val columns = Option(ctx.expressionList())
        .map(_.expression().asScala.map(_.accept(vc.expressionBuilder)).collect { case col: ir.Column =>
          col.columnName
        })

      val output = Option(ctx.outputClause()).map(buildOutputClause)
      val values = buildInsertStatementValue(ctx.insertStatementValue())
      val optionClause = Option(ctx.optionClause).map(_.accept(vc.expressionBuilder))
      ir.InsertIntoTable(finalTarget, columns, values, output, optionClause)
  }

  private def buildInsertStatementValue(ctx: InsertStatementValueContext): ir.LogicalPlan = {
    Option(ctx) match {
      case Some(context) if context.derivedTable() != null => context.derivedTable().accept(vc.relationBuilder)
      case Some(context) if context.VALUES() != null => DefaultValues()
      case Some(context) => context.executeStatement().accept(vc.relationBuilder)
    }
  }

  private def buildOutputClause(ctx: OutputClauseContext): Output = {
    val outputs = ctx.outputDmlListElem().asScala.map(_.accept(vc.expressionBuilder))
    val target = Option(ctx.ddlObject()).map(_.accept(vc.relationBuilder))
    val columns =
      Option(ctx.columnNameList())
        .map(_.id().asScala.map(id => ir.Column(None, vc.expressionBuilder.buildId(id))))

    // Databricks SQL does not support the OUTPUT clause, but we may be able to translate
    // the clause to SELECT statements executed before or after the INSERT/DELETE/UPDATE/MERGE
    // is executed
    Output(target, outputs, columns)
  }

}
