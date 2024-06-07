package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.intermediate.Relation
import com.databricks.labs.remorph.parsers.tsql.TSqlParser._
import com.databricks.labs.remorph.parsers.{intermediate => ir}

import scala.collection.JavaConverters.asScalaBufferConverter

class TSqlRelationBuilder extends TSqlParserBaseVisitor[ir.Relation] {

  private val expressionBuilder = new TSqlExpressionBuilder

  override def visitCommonTableExpression(ctx: CommonTableExpressionContext): Relation = {
    val tableName = ctx.id().getText
    // Column list can be empty if the select specifies distinct column names
    val columns =
      Option(ctx.columnNameList()).map(_.id().asScala.map(id => ir.Column(id.getText))).getOrElse(List.empty)
    val query = ctx.selectStatement().accept(this)
    ir.CTEDefinition(tableName, columns, query)
  }

  override def visitSelectStatementStandalone(ctx: TSqlParser.SelectStatementStandaloneContext): ir.Relation = {
    val query = ctx.selectStatement().accept(this)
    Option(ctx.withExpression())
      .map { withExpression =>
        val ctes = withExpression.commonTableExpression().asScala.map(_.accept(this))
        ir.WithCTE(ctes, query)
      }
      .getOrElse(query)
  }

  override def visitSelectStatement(ctx: TSqlParser.SelectStatementContext): ir.Relation = {
    // TODO: val orderByClause = Option(ctx.selectOrderByClause).map(_.accept(this))
    // TODO: val forClause = Option(ctx.forClause).map(_.accept(this))
    // TODO: val optionClause = Option(ctx.optionClause).map(_.accept(this))

    ctx.queryExpression.accept(this)
  }

  override def visitQuerySpecification(ctx: TSqlParser.QuerySpecificationContext): ir.Relation = {

    // TODO: Process all the other elements of a query specification

    val columns =
      ctx.selectListElem().asScala.map(_.accept(expressionBuilder))
    val from = Option(ctx.tableSources()).map(_.accept(this)).getOrElse(ir.NoTable)
    // Note that ALL is the default so we don't need to check for it
    ctx match {
      case c if c.DISTINCT() != null =>
        buildDistinct(from, columns)
      case _ =>
        ir.Project(from, columns)
    }
  }

  private def buildDistinct(from: ir.Relation, columns: Seq[ir.Expression]): ir.Relation = {
    val columnNames = columns.collect {
      case ir.Column(c) => Seq(c)
      case ir.Alias(_, a, _) => a
      // Note that the ir.Star(None) is not matched so that we set all_columns_as_keys to true
    }.flatten
    ir.Project(
      ir.Deduplicate(from, columnNames, all_columns_as_keys = columnNames.isEmpty, within_watermark = false),
      columns)
  }

  override def visitTableName(ctx: TableNameContext): ir.NamedTable = {
    val linkedServer = Option(ctx.linkedServer).map(_.getText)
    val ids = ctx.ids.asScala.map(_.getText).mkString(".")
    val fullName = linkedServer.fold(ids)(ls => s"$ls..$ids")
    ir.NamedTable(fullName, Map.empty, is_streaming = false)
  }

  /**
   * Note that SELECT a, b, c FROM x, y, z is equivalent to SELECT a, b, c FROM x CROSS JOIN y CROSS JOIN z
   * @param ctx
   *   the parse tree
   */
  override def visitTableSources(ctx: TSqlParser.TableSourcesContext): ir.Relation = {
    val relations = ctx.tableSource().asScala.toList.map(_.accept(this)).collect { case r: ir.Relation => r }
    relations match {
      case head :: tail =>
        tail.foldLeft(head)((acc, relation) =>
          ir.Join(
            acc,
            relation,
            None,
            ir.CrossJoin,
            Seq.empty,
            ir.JoinDataType(is_left_struct = false, is_right_struct = false)))
      case _ => ir.NoTable
    }
  }

  override def visitTableSource(ctx: TableSourceContext): ir.Relation = {
    val left = ctx.tableSourceItem().accept(this)
    ctx match {
      case c if c.joinPart() != null => c.joinPart().asScala.foldLeft(left)(buildJoin)
    }
  }

  // TODO: note that not all table source items have fullTableName
  override def visitTableSourceItem(ctx: TableSourceItemContext): ir.Relation =
    Option(ctx.asTableAlias())
      .map(alias => ir.TableAlias(ctx.tableName().accept(this), alias.id.getText))
      .getOrElse(ctx.tableName().accept(this))

  private[tsql] def translateJoinType(ctx: JoinOnContext): ir.JoinType = ctx.joinType() match {
    case jt if jt == null || jt.outerJoin() == null || jt.INNER() != null => ir.InnerJoin
    case jt if jt.outerJoin().LEFT() != null => ir.LeftOuterJoin
    case jt if jt.outerJoin().RIGHT() != null => ir.RightOuterJoin
    case jt if jt.outerJoin().FULL() != null => ir.FullOuterJoin
    case _ => ir.UnspecifiedJoin
  }

  private def buildJoin(left: ir.Relation, right: JoinPartContext): ir.Join = {
    val joinExpression = right.joinOn()
    val rightRelation = joinExpression.tableSource().accept(this)
    val joinCondition = joinExpression.searchCondition().accept(expressionBuilder)

    ir.Join(
      left,
      rightRelation,
      Some(joinCondition),
      translateJoinType(joinExpression),
      Seq.empty,
      ir.JoinDataType(is_left_struct = false, is_right_struct = false))
  }
}
