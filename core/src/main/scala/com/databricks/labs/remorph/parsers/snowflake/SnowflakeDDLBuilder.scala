package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate.AddColumn
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.{StringContext => StrContext, _}
import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}

import scala.collection.JavaConverters._
class SnowflakeDDLBuilder
    extends SnowflakeParserBaseVisitor[ir.Catalog]
    with ParserCommon[ir.Catalog]
    with IncompleteParser[ir.Catalog] {

  private val expressionBuilder = new SnowflakeExpressionBuilder

  override protected def wrapUnresolvedInput(unparsedInput: String): ir.Catalog = ir.UnresolvedCatalog(unparsedInput)

  private def extractString(ctx: StrContext): String = {
    ctx.getText.stripPrefix("'").stripSuffix("'")
  }

  override def visitCreateFunction(ctx: CreateFunctionContext): ir.Catalog = {
    val runtimeInfo = ctx match {
      case c if c.JAVA() != null => buildJavaUDF(c)
      case c if c.PYTHON() != null => buildPythonUDF(c)
      case c if c.JAVASCRIPT() != null => ir.JavascriptUDFInfo
      case c if c.SCALA() != null => buildScalaUDF(c)
      case c if c.SQL() != null || c.LANGUAGE() == null => ir.SQLUDFInfo(c.MEMOIZABLE() != null)
    }
    val name = ctx.objectName().getText
    val returnType = DataTypeBuilder.buildDataType(ctx.dataType())
    val parameters = ctx.argDecl().asScala.map(buildParameter)
    val acceptsNullParameters = ctx.CALLED() != null
    val body = buildFunctionBody(ctx.functionDefinition())
    val comment = Option(ctx.commentClause()).map(c => extractString(c.string()))
    ir.CreateInlineUDF(name, returnType, parameters, runtimeInfo, acceptsNullParameters, comment, body)
  }

  private def buildParameter(ctx: ArgDeclContext): ir.FunctionParameter = {
    ir.FunctionParameter(
      name = ctx.argName().getText,
      dataType = DataTypeBuilder.buildDataType(ctx.argDataType().dataType()),
      defaultValue = Option(ctx.argDefaultValueClause())
        .map(_.expr().accept(expressionBuilder)))
  }

  private def buildFunctionBody(ctx: FunctionDefinitionContext): String = (ctx match {
    case c if c.DBL_DOLLAR() != null => c.DBL_DOLLAR().getText.stripPrefix("$$").stripSuffix("$$")
    case c if c.string() != null => extractString(c.string())
  }).trim

  private def buildJavaUDF(ctx: CreateFunctionContext): ir.UDFRuntimeInfo = buildJVMUDF(ctx)(ir.JavaUDFInfo.apply)
  private def buildScalaUDF(ctx: CreateFunctionContext): ir.UDFRuntimeInfo = buildJVMUDF(ctx)(ir.ScalaUDFInfo.apply)

  private def buildJVMUDF(ctx: CreateFunctionContext)(
      ctr: (Option[String], Seq[String], String) => ir.UDFRuntimeInfo): ir.UDFRuntimeInfo = {
    val imports =
      ctx
        .stringList()
        .asScala
        .find(occursBefore(ctx.IMPORTS(), _))
        .map(_.string().asScala.map(extractString))
        .getOrElse(Seq())
    ctr(extractRuntimeVersion(ctx), imports, extractHandler(ctx))
  }
  private def extractRuntimeVersion(ctx: CreateFunctionContext): Option[String] = ctx.string().asScala.collectFirst {
    case c if occursBefore(ctx.RUNTIME_VERSION(), c) => extractString(c)
  }

  private def extractHandler(ctx: CreateFunctionContext): String =
    Option(ctx.HANDLER()).flatMap(h => ctx.string().asScala.find(occursBefore(h, _))).map(extractString).get

  private def buildPythonUDF(ctx: CreateFunctionContext): ir.PythonUDFInfo = {
    val packages =
      ctx
        .stringList()
        .asScala
        .find(occursBefore(ctx.PACKAGES(0), _))
        .map(_.string().asScala.map(extractString))
        .getOrElse(Seq())
    ir.PythonUDFInfo(extractRuntimeVersion(ctx), packages, extractHandler(ctx))
  }

  override def visitCreateTable(ctx: CreateTableContext): ir.Catalog = {
    val tableName = ctx.objectName().getText
    val columns = buildColumnDeclarations(
      ctx
        .createTableClause()
        .columnDeclItemListParen()
        .columnDeclItemList()
        .columnDeclItem()
        .asScala)

    ir.CreateTableCommand(tableName, columns)
  }

  private def buildColumnDeclarations(ctx: Seq[ColumnDeclItemContext]): Seq[ir.ColumnDeclaration] = {
    // According to the grammar, either ctx.fullColDecl or ctx.outOfLineConstraint is non-null.
    val columns = ctx.collect {
      case c if c.fullColDecl() != null => buildColumnDeclaration(c.fullColDecl())
    }
    // An out-of-line constraint may apply to one or many columns
    // When an out-of-line contraint applies to multiple columns,
    // we record a column-name -> constraint mapping for each.
    val outOfLineConstraints: Seq[(String, ir.Constraint)] = ctx.collect {
      case c if c.outOfLineConstraint() != null => buildOutOfLineConstraints(c.outOfLineConstraint())
    }.flatten

    // Finally, for every column, we "inject" the relevant out-of-line constraints
    columns.map { col =>
      val additionalConstraints = outOfLineConstraints.collect {
        case (columnName, constraint) if columnName == col.name => constraint
      }
      col.copy(constraints = col.constraints ++ additionalConstraints)
    }
  }

  private def buildColumnDeclaration(ctx: FullColDeclContext): ir.ColumnDeclaration = {
    val name = ctx.colDecl().columnName().getText
    val dataType = DataTypeBuilder.buildDataType(ctx.colDecl().dataType())
    val constraints = ctx.inlineConstraint().asScala.map(buildInlineConstraint)
    val nullability = if (ctx.nullNotNull().isEmpty) {
      Seq()
    } else {
      Seq(ir.Nullability(!ctx.nullNotNull().asScala.exists(_.NOT() != null)))
    }
    ir.ColumnDeclaration(name, dataType, virtualColumnDeclaration = None, nullability ++ constraints)
  }

  private[snowflake] def buildOutOfLineConstraints(ctx: OutOfLineConstraintContext): Seq[(String, ir.Constraint)] = {
    val columnNames = ctx.columnListInParentheses(0).columnList().columnName().asScala.map(_.getText)
    val repeatForEveryColumnName = List.fill[ir.UnnamedConstraint](columnNames.size)(_)
    val unnamedConstraints = ctx match {
      case c if c.UNIQUE() != null => repeatForEveryColumnName(ir.Unique)
      case c if c.primaryKey() != null => repeatForEveryColumnName(ir.PrimaryKey)
      case c if c.foreignKey() != null =>
        val referencedObject = c.objectName().getText
        val references =
          c.columnListInParentheses(1).columnList().columnName().asScala.map(referencedObject + "." + _.getText)
        references.map(ir.ForeignKey.apply)
      case c => repeatForEveryColumnName(ir.UnresolvedConstraint(c.getText))
    }
    val constraintNameOpt = Option(ctx.id()).map(_.getText)
    val constraints = constraintNameOpt.fold[Seq[ir.Constraint]](unnamedConstraints) { name =>
      unnamedConstraints.map(ir.NamedConstraint(name, _))
    }
    columnNames.zip(constraints)
  }

  private[snowflake] def buildInlineConstraint(ctx: InlineConstraintContext): ir.Constraint = ctx match {
    case c if c.UNIQUE() != null => ir.Unique
    case c if c.primaryKey() != null => ir.PrimaryKey
    case c if c.foreignKey() != null =>
      val references = c.objectName().getText + Option(ctx.columnName()).map("." + _.getText).getOrElse("")
      ir.ForeignKey(references)
    case c => ir.UnresolvedConstraint(c.getText)
  }

  override def visitAlterTable(ctx: AlterTableContext): ir.Catalog = {
    val tableName = ctx.objectName(0).getText
    ctx match {
      case c if c.tableColumnAction() != null =>
        ir.AlterTableCommand(tableName, buildColumnActions(c.tableColumnAction()))
      case c if c.constraintAction() != null =>
        ir.AlterTableCommand(tableName, buildConstraintActions(c.constraintAction()))
      case c => ir.UnresolvedCatalog(c.getText)
    }
  }

  private[snowflake] def buildColumnActions(ctx: TableColumnActionContext): Seq[ir.TableAlteration] = ctx match {
    case c if c.ADD() != null =>
      c.fullColDecl().asScala.map(buildColumnDeclaration).map(AddColumn.apply)
    case c if !c.alterColumnClause().isEmpty =>
      c.alterColumnClause().asScala.map(buildColumnAlterations)
    case c if c.DROP() != null =>
      Seq(ir.DropColumns(c.columnList().columnName().asScala.map(_.getText)))
    case c if c.RENAME() != null =>
      Seq(ir.RenameColumn(c.columnName(0).getText, c.columnName(1).getText))
    case c => Seq(ir.UnresolvedTableAlteration(c.getText))
  }

  private[snowflake] def buildColumnAlterations(ctx: AlterColumnClauseContext): ir.TableAlteration = {
    val columnName = ctx.columnName().getText
    ctx match {
      case c if c.dataType() != null =>
        ir.ChangeColumnDataType(columnName, DataTypeBuilder.buildDataType(c.dataType()))
      case c if c.DROP() != null && c.NULL_() != null =>
        ir.DropConstraint(Some(columnName), ir.Nullability(c.NOT() == null))
      case c if c.NULL_() != null =>
        ir.AddConstraint(columnName, ir.Nullability(c.NOT() == null))
      case c => ir.UnresolvedTableAlteration(c.getText)
    }
  }

  private[snowflake] def buildConstraintActions(ctx: ConstraintActionContext): Seq[ir.TableAlteration] = ctx match {
    case c if c.ADD() != null =>
      buildOutOfLineConstraints(c.outOfLineConstraint()).map(ir.AddConstraint.tupled)
    case c if c.DROP() != null =>
      buildDropConstraints(c)
    case c if c.RENAME() != null =>
      Seq(ir.RenameConstraint(c.id(0).getText, c.id(1).getText))
    case c => Seq(ir.UnresolvedTableAlteration(c.getText))
  }

  private[snowflake] def buildDropConstraints(ctx: ConstraintActionContext): Seq[ir.TableAlteration] = {
    val columnListOpt = Option(ctx.columnListInParentheses())
    val affectedColumns = columnListOpt.map(_.columnList().columnName().asScala.map(_.getText)).getOrElse(Seq())
    ctx match {
      case c if c.primaryKey() != null => dropConstraints(affectedColumns, ir.PrimaryKey)
      case c if c.UNIQUE() != null => dropConstraints(affectedColumns, ir.Unique)
      case c if c.id.size() > 0 => Seq(ir.DropConstraintByName(c.id(0).getText))
      case c => Seq(ir.UnresolvedTableAlteration(ctx.getText))
    }
  }

  private def dropConstraints(affectedColumns: Seq[String], constraint: ir.Constraint): Seq[ir.TableAlteration] = {
    if (affectedColumns.isEmpty) {
      Seq(ir.DropConstraint(None, constraint))
    } else {
      affectedColumns.map(col => ir.DropConstraint(Some(col), constraint))
    }
  }
}
