package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.tsql.TSqlParser._
import com.databricks.labs.remorph.parsers.tsql.rules.{InsertDefaultsAction, TopPercent}
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.antlr.v4.runtime.ParserRuleContext

import scala.collection.JavaConverters.asScalaBufferConverter

class TSqlRelationBuilder extends TSqlParserBaseVisitor[ir.LogicalPlan] {

  private val expressionBuilder = new TSqlExpressionBuilder

  override def visitCommonTableExpression(ctx: CommonTableExpressionContext): ir.LogicalPlan = {
    val tableName = ctx.id().getText
    // Column list can be empty if the select specifies distinct column names
    val columns =
      Option(ctx.columnNameList())
        .map(_.id().asScala.map(id => ir.Column(None, expressionBuilder.visitId(id))))
        .getOrElse(List.empty)
    val query = ctx.selectStatement().accept(this)
    ir.CTEDefinition(tableName, columns, query)
  }

  override def visitSelectStatementStandalone(ctx: TSqlParser.SelectStatementStandaloneContext): ir.LogicalPlan = {
    val query = ctx.selectStatement().accept(this)
    Option(ctx.withExpression())
      .map { withExpression =>
        val ctes = withExpression.commonTableExpression().asScala.map(_.accept(this))
        ir.WithCTE(ctes, query)
      }
      .getOrElse(query)
  }

  override def visitSelectStatement(ctx: TSqlParser.SelectStatementContext): ir.LogicalPlan = {
    // TODO: The FOR clause of TSQL is not supported in Databricks SQL as XML and JSON are not supported
    //       in the same way. We probably need to raise an error here that can be used by some sort of linter

    // We visit the OptionClause because in the future, we may be able to glean information from it
    // as an aid to migration, however the clause is not used in the AST or translation.
    val query = ctx.queryExpression.accept(this)
    Option(ctx.optionClause) match {
      case Some(optionClause) => ir.WithOptions(query, optionClause.accept(expressionBuilder))
      case None => query
    }
  }

  override def visitQuerySpecification(ctx: TSqlParser.QuerySpecificationContext): ir.LogicalPlan = {

    // TODO: Check the logic here for all the elements of a query specification
    val select = ctx.selectOptionalClauses().accept(this)

    val columns =
      ctx.selectListElem().asScala.map(_.accept(expressionBuilder))
    // Note that ALL is the default so we don't need to check for it
    ctx match {
      case c if c.DISTINCT() != null =>
        ir.Project(buildTop(Option(ctx.topClause()), buildDistinct(select, columns)), columns)
      case _ =>
        ir.Project(buildTop(Option(ctx.topClause()), select), columns)
    }
  }

  private def buildTop(ctxOpt: Option[TSqlParser.TopClauseContext], input: ir.LogicalPlan): ir.LogicalPlan =
    ctxOpt.fold(input) { top =>
      val limit = top.expression().accept(expressionBuilder)
      if (top.PERCENT() != null) {
        TopPercent(input, limit, with_ties = top.TIES() != null)
      } else {
        ir.Limit(input, limit)
      }
    }

  override def visitSelectOptionalClauses(ctx: SelectOptionalClausesContext): ir.LogicalPlan = {
    val from = Option(ctx.fromClause()).map(_.accept(this)).getOrElse(ir.NoTable())
    buildOrderBy(
      ctx.selectOrderByClause(),
      buildHaving(ctx.havingClause(), buildGroupBy(ctx.groupByClause(), buildWhere(ctx.whereClause(), from))))
  }

  private def buildFilter[A](ctx: A, conditionRule: A => ParserRuleContext, input: ir.LogicalPlan): ir.LogicalPlan =
    Option(ctx).fold(input) { c =>
      ir.Filter(input, conditionRule(c).accept(expressionBuilder))
    }

  private def buildHaving(ctx: HavingClauseContext, input: ir.LogicalPlan): ir.LogicalPlan =
    buildFilter[HavingClauseContext](ctx, _.searchCondition(), input)

  private def buildWhere(ctx: WhereClauseContext, from: ir.LogicalPlan): ir.LogicalPlan =
    buildFilter[WhereClauseContext](ctx, _.searchCondition(), from)

  // TODO: We are not catering for GROUPING SETS here, or in Snowflake
  private def buildGroupBy(ctx: GroupByClauseContext, input: ir.LogicalPlan): ir.LogicalPlan = {
    Option(ctx).fold(input) { c =>
      val groupingExpressions =
        c.expression()
          .asScala
          .map(_.accept(expressionBuilder))
      ir.Aggregate(child = input, group_type = ir.GroupBy, grouping_expressions = groupingExpressions, pivot = None)
    }
  }

  private def buildOrderBy(ctx: SelectOrderByClauseContext, input: ir.LogicalPlan): ir.LogicalPlan = {
    Option(ctx).fold(input) { c =>
      val sortOrders = c.orderByClause().orderByExpression().asScala.map { orderItem =>
        val expression = orderItem.expression(0).accept(expressionBuilder)
        // orderItem.expression(1) is COLLATE - we will not support that, but should either add a comment in the
        // translated source or raise some kind of linting alert.
        if (orderItem.DESC() == null) {
          ir.SortOrder(expression, ir.Ascending, ir.SortNullsUnspecified)
        } else {
          ir.SortOrder(expression, ir.Descending, ir.SortNullsUnspecified)
        }
      }
      val sorted = ir.Sort(input, sortOrders, is_global = false)

      // Having created the IR for ORDER BY, we now need to apply any OFFSET, and then any FETCH
      if (ctx.OFFSET() != null) {
        val offset = ir.Offset(sorted, ctx.expression(0).accept(expressionBuilder))
        if (ctx.FETCH() != null) {
          ir.Limit(offset, ctx.expression(1).accept(expressionBuilder))
        } else {
          offset
        }
      } else {
        sorted
      }
    }
  }

  override def visitFromClause(ctx: FromClauseContext): ir.LogicalPlan = {
    val tableSources = ctx.tableSources().tableSource().asScala.map(_.accept(this))
    // The tableSources seq cannot be empty (as empty FROM clauses are not allowed
    tableSources match {
      case Seq(tableSource) => tableSource
      case sources =>
        sources.reduce(
          ir.Join(_, _, None, ir.CrossJoin, Seq(), ir.JoinDataType(is_left_struct = false, is_right_struct = false)))
    }
  }

  private def buildDistinct(from: ir.LogicalPlan, columns: Seq[ir.Expression]): ir.LogicalPlan = {
    val columnNames = columns.collect {
      case ir.Column(_, c) => Seq(c)
      case ir.Alias(_, a, _) => a
      // Note that the ir.Star(None) is not matched so that we set all_columns_as_keys to true
    }.flatten
    ir.Deduplicate(from, columnNames, all_columns_as_keys = columnNames.isEmpty, within_watermark = false)
  }

  override def visitTableName(ctx: TableNameContext): ir.NamedTable = {
    val linkedServer = Option(ctx.linkedServer).map(_.getText)
    val ids = ctx.ids.asScala.map(_.getText).mkString(".")
    val fullName = linkedServer.fold(ids)(ls => s"$ls..$ids")
    ir.NamedTable(fullName, Map.empty, is_streaming = false)
  }

  override def visitTableSource(ctx: TableSourceContext): ir.LogicalPlan = {
    val left = ctx.tableSourceItem().accept(this)
    ctx match {
      case c if c.joinPart() != null => c.joinPart().asScala.foldLeft(left)(buildJoinPart)
    }
  }

  override def visitTableSourceItem(ctx: TableSourceItemContext): ir.LogicalPlan = {
    val tsiElement = ctx.tsiElement().accept(this)

    // Assemble any table hints, though we do nothing with them for now
    val hints = buildTableHints(Option(ctx.withTableHints()))

    // If we have column aliases, they are applied here first
    val tsiElementWithAliases = Option(ctx.columnAliasList())
      .map { aliasList =>
        val aliases = aliasList.columnAlias().asScala.map(id => buildColumnAlias(id))
        ColumnAliases(tsiElement, aliases)
      }
      .getOrElse(tsiElement)

    val relation = if (hints.nonEmpty) {
      ir.TableWithHints(tsiElementWithAliases, hints)
    } else {
      tsiElementWithAliases
    }

    // Then any table alias is applied to the source
    Option(ctx.asTableAlias())
      .map(alias => ir.TableAlias(relation, alias.id.getText))
      .getOrElse(relation)
  }

  // Table hints arrive syntactically as a () delimited list of options and, in the
  // case of deprecated hint syntax, as a list of generic options without (). Here,
  // we build a single map from both sources, either or both of which may be empty.
  // In true TSQL style, some of the hints have non-orthodox syntax, and must be handled
  // directly.
  private def buildTableHints(ctx: Option[WithTableHintsContext]): Seq[ir.TableHint] = {
    ctx.map(_.tableHint().asScala.map(buildHint).toList).getOrElse(Seq.empty)
  }

  private def buildHint(ctx: TableHintContext): ir.TableHint = {
    ctx match {
      case index if index.INDEX() != null =>
        ir.IndexHint(index.expressionList().expression().asScala.map { expr =>
          expr.accept(expressionBuilder) match {
            case column: ir.Column => column.columnName
            case other => other
          }
        })
      case force if force.FORCESEEK() != null =>
        val name = Option(force.expression()).map(_.accept(expressionBuilder))
        val columns = Option(force.columnNameList()).map(_.id().asScala.map(_.accept(expressionBuilder)))
        ir.ForceSeekHint(name, columns)
      case _ =>
        val option = expressionBuilder.optionBuilder.buildOption(ctx.genericOption())
        ir.FlagHint(option.id)
    }
  }

  private def buildColumnAlias(ctx: TSqlParser.ColumnAliasContext): ir.Id = {
    ctx match {
      case c if c.id() != null => expressionBuilder.visitId(c.id())
      case _ => ir.Id(expressionBuilder.removeQuotes(ctx.getText))
    }
  }

  override def visitTsiNamedTable(ctx: TsiNamedTableContext): ir.LogicalPlan =
    ctx.tableName().accept(this)

  override def visitTsiDerivedTable(ctx: TsiDerivedTableContext): ir.LogicalPlan = {
    ctx.derivedTable().accept(this)
  }

  override def visitDerivedTable(ctx: DerivedTableContext): ir.LogicalPlan = {
    val result = if (ctx.tableValueConstructor() != null) {
      ctx.tableValueConstructor().accept(this)
    } else {
      ctx.subquery().accept(this)
    }
    result
  }

  override def visitTableValueConstructor(ctx: TableValueConstructorContext): ir.LogicalPlan = {
    val rows = ctx.tableValueRow().asScala.map(buildValueRow)
    DerivedRows(rows)
  }

  private def buildValueRow(ctx: TableValueRowContext): Seq[ir.Expression] = {
    ctx.expressionList().expression().asScala.map(_.accept(expressionBuilder))
  }

  override def visitMergeStatement(ctx: MergeStatementContext): ir.LogicalPlan = {
    val merge = ctx.merge().accept(this)
    Option(ctx.withExpression())
      .map { withExpression =>
        val ctes = withExpression.commonTableExpression().asScala.map(_.accept(this))
        ir.WithCTE(ctes, merge)
      }
      .getOrElse(merge)
  }

  override def visitMerge(ctx: MergeContext): ir.LogicalPlan = {

    val targetPlan = ctx.ddlObject().accept(this)
    val hints = buildTableHints(Option(ctx.withTableHints()))
    val finalTarget = if (hints.nonEmpty) {
      ir.TableWithHints(targetPlan, hints)
    } else {
      targetPlan
    }

    val mergeCondition = ctx.searchCondition().accept(expressionBuilder)
    val tableSourcesPlan = ctx.tableSources().tableSource().asScala.map(_.accept(this))
    val sourcePlan = tableSourcesPlan.tail.foldLeft(tableSourcesPlan.head)(
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

    val optionClause = Option(ctx.optionClause).map(_.accept(expressionBuilder))
    val outputClause = Option(ctx.outputClause()).map(_.accept(this))

    val mergeIntoTable = ir.MergeIntoTable(
      finalTarget,
      sourcePlan,
      mergeCondition,
      matchedActions,
      notMatchedActions,
      notMatchedBySourceActions)

    val withOptions = optionClause match {
      case Some(option) => ir.WithOptions(mergeIntoTable, option)
      case None => mergeIntoTable
    }

    outputClause match {
      case Some(output) => WithOutputClause(withOptions, output)
      case None => withOptions
    }
  }

  private def buildWhenMatch(ctx: WhenMatchContext): ir.MergeAction = {
    val condition = Option(ctx.searchCondition()).map(_.accept(expressionBuilder))
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
            .map(_.accept(expressionBuilder)) zip ctx.vals.expression().asScala.map(_.accept(expressionBuilder)))
            .map { case (col, value) =>
              ir.Assign(col, value)
            }
        ir.InsertAction(condition, assignments)
    }
  }

  private def buildUpdateAction(ctx: MergeActionContext, condition: Option[ir.Expression]): ir.UpdateAction = {
    val setElements = ctx.updateElem().asScala.collect { case elem =>
      elem.accept(expressionBuilder) match {
        case assign: ir.Assign => assign
      }
    }
    ir.UpdateAction(condition, setElements)
  }

  override def visitUpdateStatement(ctx: UpdateStatementContext): ir.LogicalPlan = {
    val update = ctx.update().accept(this)
    Option(ctx.withExpression())
      .map { withExpression =>
        val ctes = withExpression.commonTableExpression().asScala.map(_.accept(this))
        ir.WithCTE(ctes, update)
      }
      .getOrElse(update)
  }

  override def visitUpdate(ctx: UpdateContext): ir.LogicalPlan = {
    val target = ctx.ddlObject().accept(this)
    val hints = buildTableHints(Option(ctx.withTableHints()))
    val hintTarget = if (hints.nonEmpty) {
      ir.TableWithHints(target, hints)
    } else {
      target
    }

    val finalTarget = buildTop(Option(ctx.topClause()), hintTarget)
    val output = Option(ctx.outputClause()).map(_.accept(this))
    val setElements = ctx.updateElem().asScala.map(_.accept(expressionBuilder))

    val tableSourcesOption = Option(ctx.tableSources()).map(_.tableSource().asScala.map(_.accept(this)))
    val sourceRelation = tableSourcesOption.map { tableSources =>
      tableSources.tail.foldLeft(tableSources.head)(
        ir.Join(_, _, None, ir.CrossJoin, Seq(), ir.JoinDataType(is_left_struct = false, is_right_struct = false)))
    }

    val where = Option(ctx.updateWhereClause()) map (_.accept(expressionBuilder))
    val optionClause = Option(ctx.optionClause).map(_.accept(expressionBuilder))
    ir.UpdateTable(finalTarget, sourceRelation, setElements, where, output, optionClause)
  }

  override def visitDeleteStatement(ctx: DeleteStatementContext): ir.LogicalPlan = {
    val delete = ctx.delete().accept(this)
    Option(ctx.withExpression())
      .map { withExpression =>
        val ctes = withExpression.commonTableExpression().asScala.map(_.accept(this))
        ir.WithCTE(ctes, delete)
      }
      .getOrElse(delete)
  }

  override def visitDelete(ctx: DeleteContext): ir.LogicalPlan = {
    val target = ctx.ddlObject().accept(this)
    val hints = buildTableHints(Option(ctx.withTableHints()))
    val finalTarget = if (hints.nonEmpty) {
      ir.TableWithHints(target, hints)
    } else {
      target
    }

    val output = Option(ctx.outputClause()).map(_.accept(this))
    val tableSourcesOption = Option(ctx.tableSources()).map(_.tableSource().asScala.map(_.accept(this)))
    val sourceRelation = tableSourcesOption.map { tableSources =>
      tableSources.tail.foldLeft(tableSources.head)(
        ir.Join(_, _, None, ir.CrossJoin, Seq(), ir.JoinDataType(is_left_struct = false, is_right_struct = false)))
    }

    val where = Option(ctx.updateWhereClause()) map (_.accept(expressionBuilder))
    val optionClause = Option(ctx.optionClause).map(_.accept(expressionBuilder))
    ir.DeleteFromTable(finalTarget, sourceRelation, where, output, optionClause)
  }

  override def visitInsertStatement(ctx: InsertStatementContext): ir.LogicalPlan = {
    val insert = ctx.insert().accept(this)
    Option(ctx.withExpression())
      .map { withExpression =>
        val ctes = withExpression.commonTableExpression().asScala.map(_.accept(this))
        ir.WithCTE(ctes, insert)
      }
      .getOrElse(insert)
  }

  override def visitInsert(ctx: InsertContext): ir.LogicalPlan = {
    val target = ctx.ddlObject().accept(this)
    val hints = buildTableHints(Option(ctx.withTableHints()))
    val finalTarget = if (hints.nonEmpty) {
      ir.TableWithHints(target, hints)
    } else {
      target
    }

    val columns = Option(ctx.expressionList())
      .map(_.expression().asScala.map(_.accept(expressionBuilder)).collect { case col: ir.Column => col.columnName })

    val output = Option(ctx.outputClause()).map(_.accept(this))
    val values = ctx.insertStatementValue().accept(this)
    val optionClause = Option(ctx.optionClause).map(_.accept(expressionBuilder))
    ir.InsertIntoTable(finalTarget, columns, values, output, optionClause, overwrite = false)
  }

  override def visitInsertStatementValue(ctx: InsertStatementValueContext): ir.LogicalPlan = {
    Option(ctx) match {
      case Some(context) if context.derivedTable() != null => context.derivedTable().accept(this)
      case Some(context) if context.VALUES() != null => DefaultValues()
      case Some(context) => context.executeStatement().accept(this)
    }
  }

  override def visitOutputClause(ctx: OutputClauseContext): ir.LogicalPlan = {
    val outputs = ctx.outputDmlListElem().asScala.map(_.accept(expressionBuilder))
    val target = ctx.ddlObject().accept(this)
    val columns =
      Option(ctx.columnNameList())
        .map(_.id().asScala.map(id => ir.Column(None, expressionBuilder.visitId(id))))

    // Databricks SQL does not support the OUTPUT clause, but we may be able to translate
    // the clause to SELECT statements executed before or after the INSERT/DELETE/UPDATE/MERGE
    // is executed
    Output(target, outputs, columns)
  }

  override def visitDdlObject(ctx: DdlObjectContext): ir.LogicalPlan = {
    ctx match {
      case tableName if tableName.tableName() != null => tableName.tableName().accept(this)
      case localId if localId.LOCAL_ID() != null => ir.LocalVarTable(ir.Id(localId.LOCAL_ID().getText))
      // TODO: OPENROWSET and OPENQUERY
      case _ => ir.UnresolvedRelation(ctx.getText)
    }
  }

  private def buildJoinPart(left: ir.LogicalPlan, ctx: JoinPartContext): ir.LogicalPlan = {
    ctx match {
      case c if c.joinOn() != null => buildJoinOn(left, c.joinOn())
      case c if c.crossJoin() != null => buildCrossJoin(left, c.crossJoin())
      case c if c.apply() != null => buildApply(left, c.apply())
      case c if c.pivot() != null => buildPivot(left, c.pivot())
      case _ => buildUnpivot(left, ctx.unpivot()) // Only case left
    }
  }

  private def buildUnpivot(left: ir.LogicalPlan, ctx: UnpivotContext): ir.LogicalPlan = {
    val unpivotColumns = ctx
      .unpivotClause()
      .fullColumnNameList()
      .fullColumnName()
      .asScala
      .map(_.accept(expressionBuilder))
    val variableColumnName = expressionBuilder.visitId(ctx.unpivotClause().id(0))
    val valueColumnName = expressionBuilder.visitId(ctx.unpivotClause().id(1))
    ir.Unpivot(
      child = left,
      ids = unpivotColumns,
      values = None,
      variable_column_name = variableColumnName,
      value_column_name = valueColumnName)
  }

  private def buildPivot(left: ir.LogicalPlan, ctx: PivotContext): ir.LogicalPlan = {
    // Though the pivotClause allows expression, it must be a function call and we require
    // correct source code to be given to remorph.
    val aggregateFunction = ctx.pivotClause().expression().accept(expressionBuilder)
    val column = ctx.pivotClause().fullColumnName().accept(expressionBuilder)
    val values = ctx.pivotClause().columnAliasList().columnAlias().asScala.map(c => buildLiteral(c.getText))
    ir.Aggregate(
      child = left,
      group_type = ir.Pivot,
      grouping_expressions = Seq(aggregateFunction),
      pivot = Some(ir.Pivot(column, values)))
  }

  private def buildLiteral(str: String): ir.Literal =
    ir.Literal(string = Some(removeQuotesAndBrackets(str)))

  private def buildApply(left: ir.LogicalPlan, ctx: ApplyContext): ir.LogicalPlan = {
    val rightRelation = ctx.tableSourceItem().accept(this)
    ir.Join(
      left,
      rightRelation,
      None,
      if (ctx.CROSS() != null) ir.CrossApply else ir.OuterApply,
      Seq.empty,
      ir.JoinDataType(is_left_struct = false, is_right_struct = false))
  }

  private def buildCrossJoin(left: ir.LogicalPlan, ctx: CrossJoinContext): ir.LogicalPlan = {
    val rightRelation = ctx.tableSourceItem().accept(this)
    ir.Join(
      left,
      rightRelation,
      None,
      ir.CrossJoin,
      Seq.empty,
      ir.JoinDataType(is_left_struct = false, is_right_struct = false))
  }

  private def buildJoinOn(left: ir.LogicalPlan, ctx: JoinOnContext): ir.Join = {
    val rightRelation = ctx.tableSource().accept(this)
    val joinCondition = ctx.searchCondition().accept(expressionBuilder)

    ir.Join(
      left,
      rightRelation,
      Some(joinCondition),
      translateJoinType(ctx),
      Seq.empty,
      ir.JoinDataType(is_left_struct = false, is_right_struct = false))
  }

  private[tsql] def translateJoinType(ctx: JoinOnContext): ir.JoinType = ctx.joinType() match {
    case jt if jt == null || jt.outerJoin() == null || jt.INNER() != null => ir.InnerJoin
    case jt if jt.outerJoin().LEFT() != null => ir.LeftOuterJoin
    case jt if jt.outerJoin().RIGHT() != null => ir.RightOuterJoin
    case jt if jt.outerJoin().FULL() != null => ir.FullOuterJoin
    case _ => ir.UnspecifiedJoin
  }

  private def removeQuotesAndBrackets(str: String): String = {
    val quotations = Map('\'' -> "'", '"' -> "\"", '[' -> "]", '\\' -> "\\")
    str match {
      case s if s.length < 2 => s
      case s =>
        quotations.get(s.head).fold(s) { closingQuote =>
          if (s.endsWith(closingQuote)) {
            s.substring(1, s.length - 1)
          } else {
            s
          }
        }
    }
  }
}
