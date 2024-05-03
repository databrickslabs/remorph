package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.{Inline_constraintContext, Out_of_line_constraintContext}
import org.mockito.Mockito._
import org.scalatest.Assertion
import org.scalatest.matchers.should
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

class SnowflakeDDLBuilderSpec
    extends AnyWordSpec
    with SnowflakeParserTestCommon
    with should.Matchers
    with MockitoSugar {

  override protected def astBuilder: SnowflakeDDLBuilder = new SnowflakeDDLBuilder

  private def example(query: String, expectedAst: Catalog): Assertion = example(query, _.create_command(), expectedAst)

  "SnowflakeCommandBuilder" should {
    "translate Java UDF create command" in {

      val javaCode = """class TestFunc {
                       |  public static String echoVarchar(String x) {
                       |    return x;
                       |  }
                       |}""".stripMargin

      example(
        query = s"""
          |CREATE OR REPLACE FUNCTION echo_varchar(x varchar)
          |RETURNS VARCHAR
          |LANGUAGE JAVA
          |CALLED ON NULL INPUT
          |IMPORTS = ('@~/some-dir/some-lib.jar')
          |HANDLER = 'TestFunc.echoVarchar'
          |AS
          |'$javaCode';
          |""".stripMargin,
        expectedAst = CreateInlineUDF(
          name = "echo_varchar",
          returnType = VarCharType(None),
          parameters = Seq(FunctionParameter("x", VarCharType(None), None)),
          JavaUDFInfo(
            runtimeVersion = None,
            imports = Seq("@~/some-dir/some-lib.jar"),
            handler = "TestFunc.echoVarchar"),
          acceptsNullParameters = true,
          comment = None,
          body = javaCode))

    }

    "translate Python UDF create command" in {
      val pythonCode = """import numpy as np
                         |import pandas as pd
                         |import xgboost as xgb
                         |def udf():
                         |    return [np.__version__, pd.__version__, xgb.__version__]
                         |""".stripMargin

      example(
        query = s"""CREATE OR REPLACE FUNCTION py_udf()
                  |  RETURNS VARIANT
                  |  LANGUAGE PYTHON
                  |  RUNTIME_VERSION = '3.8'
                  |  PACKAGES = ('numpy','pandas','xgboost==1.5.0')
                  |  HANDLER = 'udf'
                  |AS $$$$
                  |$pythonCode
                  |$$$$;""".stripMargin,
        expectedAst = CreateInlineUDF(
          name = "py_udf",
          returnType = UnparsedType(),
          parameters = Seq(),
          runtimeInfo = PythonUDFInfo(
            runtimeVersion = Some("3.8"),
            packages = Seq("numpy", "pandas", "xgboost==1.5.0"),
            handler = "udf"),
          acceptsNullParameters = false,
          comment = None,
          body = pythonCode.trim))
    }

    "translate JavaScript UDF create command" in {
      val javascriptCode = """if (D <= 0) {
                             |    return 1;
                             |  } else {
                             |    var result = 1;
                             |    for (var i = 2; i <= D; i++) {
                             |      result = result * i;
                             |    }
                             |    return result;
                             |  }""".stripMargin
      example(
        query = s"""CREATE OR REPLACE FUNCTION js_factorial(d double)
                  |  RETURNS double
                  |  LANGUAGE JAVASCRIPT
                  |  STRICT
                  |  COMMENT = 'Compute factorial using JavaScript'
                  |  AS '
                  |  $javascriptCode
                  |  ';""".stripMargin,
        expectedAst = CreateInlineUDF(
          name = "js_factorial",
          returnType = DoubleType(),
          parameters = Seq(FunctionParameter("d", DoubleType(), None)),
          runtimeInfo = JavascriptUDFInfo,
          acceptsNullParameters = false,
          comment = Some("Compute factorial using JavaScript"),
          body = javascriptCode))
    }

    "translate Scala UDF create command" in {
      val scalaCode = """class Echo {
                        |  def echoVarchar(x : String): String = {
                        |    return x
                        |  }
                        |}""".stripMargin

      example(
        query = s"""CREATE OR REPLACE FUNCTION echo_varchar(x VARCHAR DEFAULT 'foo')
                  |  RETURNS VARCHAR
                  |  LANGUAGE SCALA
                  |  CALLED ON NULL INPUT
                  |  RUNTIME_VERSION = '2.12'
                  |  HANDLER='Echo.echoVarchar'
                  |  AS
                  |  $$$$
                  |  $scalaCode
                  |  $$$$;""".stripMargin,
        expectedAst = CreateInlineUDF(
          name = "echo_varchar",
          returnType = VarCharType(None),
          parameters = Seq(FunctionParameter("x", VarCharType(None), Some(Literal(string = Some("foo"))))),
          runtimeInfo = ScalaUDFInfo(runtimeVersion = Some("2.12"), imports = Seq(), handler = "Echo.echoVarchar"),
          acceptsNullParameters = true,
          comment = None,
          body = scalaCode))
    }

    "translate SQL UDF create command" in {
      example(
        query = """CREATE FUNCTION multiply1 (a number, b number)
                  |  RETURNS number
                  |  COMMENT='multiply two numbers'
                  |  AS 'a * b';""".stripMargin,
        expectedAst = CreateInlineUDF(
          name = "multiply1",
          returnType = DecimalType(None, None),
          parameters = Seq(
            FunctionParameter("a", DecimalType(None, None), None),
            FunctionParameter("b", DecimalType(None, None), None)),
          runtimeInfo = SQLUDFInfo(memoizable = false),
          acceptsNullParameters = false,
          comment = Some("multiply two numbers"),
          body = "a * b"))
    }

    "translate CREATE TABLE commands" in {
      example(
        query = "CREATE TABLE s.t1 (x VARCHAR)",
        expectedAst =
          CreateTableCommand(name = "s.t1", columns = Seq(ColumnDeclaration("x", VarCharType(None), None, Seq()))))

      example(
        query = "CREATE TABLE s.t1 (x VARCHAR UNIQUE)",
        expectedAst = CreateTableCommand(
          name = "s.t1",
          columns = Seq(ColumnDeclaration("x", VarCharType(None), None, Seq(Unique)))))

      example(
        query = "CREATE TABLE s.t1 (x VARCHAR NOT NULL)",
        expectedAst = CreateTableCommand(
          name = "s.t1",
          columns = Seq(ColumnDeclaration("x", VarCharType(None), None, Seq(NotNull)))))

      example(
        query = "CREATE TABLE s.t1 (x VARCHAR PRIMARY KEY)",
        expectedAst = CreateTableCommand(
          name = "s.t1",
          columns = Seq(ColumnDeclaration("x", VarCharType(None), None, Seq(PrimaryKey)))))

      example(
        query = "CREATE TABLE s.t1 (x VARCHAR UNIQUE FOREIGN KEY REFERENCES s.t2 (y))",
        expectedAst = CreateTableCommand(
          name = "s.t1",
          columns = Seq(ColumnDeclaration("x", VarCharType(None), None, Seq(Unique, ForeignKey("s.t2.y"))))))

      example(
        query = """CREATE TABLE s.t1 (
            |  id VARCHAR PRIMARY KEY NOT NULL,
            |  a VARCHAR(32) UNIQUE,
            |  b INTEGER,
            |  CONSTRAINT fkey FOREIGN KEY (a, b) REFERENCES s.t2 (x, y)
            |)
            |""".stripMargin,
        expectedAst = CreateTableCommand(
          name = "s.t1",
          columns = Seq(
            ColumnDeclaration("id", VarCharType(None), None, Seq(NotNull, PrimaryKey)),
            ColumnDeclaration("a", VarCharType(Some(32)), None, Seq(Unique, ForeignKey("s.t2.x"))),
            ColumnDeclaration("b", DecimalType(Some(38), None), None, Seq(ForeignKey("s.t2.y"))))))
    }

    "wrap unknown AST in UnresolvedCatalog" in {
      astBuilder.visit(parseString("CREATE USER homer", _.create_command())) shouldBe a[UnresolvedCatalog]
    }
  }

  "SnowflakeDDLBuilder.buildOutOfLineConstraint" should {

    "handle unexpected input" in {
      val columnList = parseString("(a, b, c)", _.column_list_in_parentheses())
      val outOfLineConstraint = mock[Out_of_line_constraintContext]
      when(outOfLineConstraint.column_list_in_parentheses(0)).thenReturn(columnList)
      val dummyInputTextForOutOfLineConstraint = "dummy"
      when(outOfLineConstraint.getText).thenReturn(dummyInputTextForOutOfLineConstraint)
      val result = astBuilder.buildOutOfLineConstraint(outOfLineConstraint)
      result shouldBe Seq(
        "a" -> UnresolvedConstraint(dummyInputTextForOutOfLineConstraint),
        "b" -> UnresolvedConstraint(dummyInputTextForOutOfLineConstraint),
        "c" -> UnresolvedConstraint(dummyInputTextForOutOfLineConstraint))
    }
  }

  "SnowflakeDDLBuilder.buildInlineConstraint" should {

    "handle unexpected input" in {
      val inlineConstraint = mock[Inline_constraintContext]
      val dummyInputTextForInlineConstraint = "dummy"
      when(inlineConstraint.getText).thenReturn(dummyInputTextForInlineConstraint)
      val result = astBuilder.buildInlineConstraint(inlineConstraint)
      result shouldBe UnresolvedConstraint(dummyInputTextForInlineConstraint)
    }
  }

}
