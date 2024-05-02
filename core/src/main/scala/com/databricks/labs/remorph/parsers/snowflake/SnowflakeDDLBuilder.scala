package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}
import SnowflakeParser.{StringContext => StrContext, _}

import scala.collection.JavaConverters._
class SnowflakeDDLBuilder
    extends SnowflakeParserBaseVisitor[ir.Catalog]
    with ParserCommon
    with IncompleteParser[ir.Catalog] {
  override protected def wrapUnresolvedInput(unparsedInput: String): ir.Catalog = ir.UnresolvedCatalog(unparsedInput)

  private def extractString(ctx: StrContext): String = {
    ctx.getText.stripPrefix("'").stripSuffix("'")
  }

  override def visitCreate_function(ctx: Create_functionContext): ir.Catalog = {
    val runtimeInfo = ctx match {
      case c if c.JAVA() != null => buildJavaUDF(c)
      case c if c.PYTHON() != null => buildPythonUDF(c)
      case c if c.JAVASCRIPT() != null => ir.JavascriptUDFInfo
      case c if c.SCALA() != null => buildScalaUDF(c)
      case c if c.SQL() != null || c.LANGUAGE() == null => ir.SQLUDFInfo(c.MEMOIZABLE() != null)
    }
    val name = ctx.object_name().getText
    val returnType = DataTypeBuilder.buildDataType(ctx.data_type())
    val parameters = ctx.arg_decl().asScala.map(buildParameter)
    val acceptsNullParameters = ctx.CALLED() != null
    val body = buildFunctionBody(ctx.function_definition())
    val comment = Option(ctx.comment_clause()).map(c => extractString(c.string()))
    ir.CreateInlineUDF(name, returnType, parameters, runtimeInfo, acceptsNullParameters, comment, body)
  }

  private def buildParameter(ctx: Arg_declContext): ir.FunctionParameter = {
    ir.FunctionParameter(
      name = ctx.arg_name().getText,
      dataType = DataTypeBuilder.buildDataType(ctx.arg_data_type().id_().data_type()),
      defaultValue = Option(ctx.arg_default_value_clause()).map(_.expr().accept(new SnowflakeExpressionBuilder)))
  }

  private def buildFunctionBody(ctx: Function_definitionContext): String = (ctx match {
    case c if c.DBL_DOLLAR() != null => c.DBL_DOLLAR().getText.stripPrefix("$$").stripSuffix("$$")
    case c if c.string() != null => extractString(c.string())
  }).trim

  private def buildJavaUDF(ctx: Create_functionContext): ir.UDFRuntimeInfo = buildJVMUDF(ctx)(ir.JavaUDFInfo.apply)
  private def buildScalaUDF(ctx: Create_functionContext): ir.UDFRuntimeInfo = buildJVMUDF(ctx)(ir.ScalaUDFInfo.apply)

  private def buildJVMUDF(ctx: Create_functionContext)(
      ctr: (Option[String], Seq[String], String) => ir.UDFRuntimeInfo): ir.UDFRuntimeInfo = {
    val imports =
      ctx
        .string_list()
        .asScala
        .find(occursBefore(ctx.IMPORTS(), _))
        .map(_.string().asScala.map(extractString))
        .getOrElse(Seq())
    ctr(extractRuntimeVersion(ctx), imports, extractHandler(ctx))
  }
  private def extractRuntimeVersion(ctx: Create_functionContext): Option[String] = ctx.string().asScala.collectFirst {
    case c if occursBefore(ctx.RUNTIME_VERSION(), c) => extractString(c)
  }

  private def extractHandler(ctx: Create_functionContext): String =
    Option(ctx.HANDLER()).flatMap(h => ctx.string().asScala.find(occursBefore(h, _))).map(extractString).get

  private def buildPythonUDF(ctx: Create_functionContext): ir.PythonUDFInfo = {
    val packages =
      ctx
        .string_list()
        .asScala
        .find(occursBefore(ctx.PACKAGES(0), _))
        .map(_.string().asScala.map(extractString))
        .getOrElse(Seq())
    ir.PythonUDFInfo(extractRuntimeVersion(ctx), packages, extractHandler(ctx))
  }

  override def visitCreate_table(ctx: Create_tableContext): ir.Catalog = {
    val tableName = ctx.object_name().getText
    val columns = buildColumnDeclarations(
      ctx
        .create_table_clause()
        .column_decl_item_list_paren()
        .column_decl_item_list()
        .column_decl_item()
        .asScala)

    ir.CreateTableCommand(tableName, columns)
  }

  private def buildColumnDeclarations(ctx: Seq[Column_decl_itemContext]): Seq[ir.ColumnDeclaration] = {
    val columns = ctx.collect {
      case c if c.full_col_decl() != null => buildColumnDeclaration(c.full_col_decl())
    }
    val outOfLineConstraints = ctx.collect {
      case c if c.out_of_line_constraint() != null => buildOutOfLineConstraint(c.out_of_line_constraint())
    }.flatten

    columns.map { col =>
      val additionalConstraints = outOfLineConstraints.collect {
        case (columnName, constraint) if columnName == col.name => constraint
      }
      col.copy(constraints = col.constraints ++ additionalConstraints)
    }
  }

  private def buildColumnDeclaration(ctx: Full_col_declContext): ir.ColumnDeclaration = {
    val name = ctx.col_decl().column_name().getText
    val dataType = DataTypeBuilder.buildDataType(ctx.col_decl().data_type())
    val constraints = ctx.inline_constraint().asScala.map(buildInlineConstraint)
    val nullability = if (ctx.null_not_null().asScala.exists(_.NOT() != null)) Seq(ir.NotNull) else Seq()
    ir.ColumnDeclaration(name, dataType, virtualColumnDeclaration = None, nullability ++ constraints)
  }

  private def buildOutOfLineConstraint(ctx: Out_of_line_constraintContext): Seq[(String, ir.Constraint)] = {
    val columnNames = ctx.column_list_in_parentheses(0).column_list().column_name().asScala.map(_.getText)
    val constraints = ctx match {
      case c if c.UNIQUE() != null => List.fill(columnNames.size)(ir.Unique)
      case c if c.primary_key() != null => List.fill(columnNames.size)(ir.PrimaryKey)
      case c if c.foreign_key() != null =>
        val referencedObject = c.object_name().getText
        val references =
          c.column_list_in_parentheses(1).column_list().column_name().asScala.map(referencedObject + "." + _.getText)
        references.map(ir.ForeignKey.apply)

    }
    columnNames.zip(constraints)
  }

  private def buildInlineConstraint(ctx: Inline_constraintContext): ir.Constraint = ctx match {
    case c if c.UNIQUE() != null => ir.Unique
    case c if c.primary_key() != null => ir.PrimaryKey
    case c if c.foreign_key() != null =>
      val references = c.object_name().getText + Option(ctx.column_name()).map("." + _.getText).getOrElse("")
      ir.ForeignKey(references)
  }
}
