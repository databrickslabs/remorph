package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}
import SnowflakeParser.{StringContext => StrContext, _}

import scala.collection.JavaConverters._
class SnowflakeDDLBuilder
    extends SnowflakeParserBaseVisitor[ir.Command]
    with ParserCommon
    with IncompleteParser[ir.Command] {
  override protected def wrapUnresolvedInput(unparsedInput: String): ir.Command = ir.UnresolvedCommand(unparsedInput)

  private def extractString(ctx: StrContext): String = {
    ctx.getText.stripPrefix("'").stripSuffix("'")
  }

  override def visitCreate_function(ctx: Create_functionContext): ir.Command = {
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

}
