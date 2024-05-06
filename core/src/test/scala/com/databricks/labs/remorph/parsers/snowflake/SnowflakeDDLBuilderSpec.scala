package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.{StringContext => _, _}
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

  private def example(query: String, expectedAst: Catalog): Assertion = example(query, _.ddl_command(), expectedAst)

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
          columns = Seq(ColumnDeclaration("x", VarCharType(None), None, Seq(Nullability(false))))))

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
            ColumnDeclaration("id", VarCharType(None), None, Seq(Nullability(false), PrimaryKey)),
            ColumnDeclaration(
              "a",
              VarCharType(Some(32)),
              None,
              Seq(Unique, NamedConstraint("fkey", ForeignKey("s.t2.x")))),
            ColumnDeclaration(
              "b",
              DecimalType(Some(38), None),
              None,
              Seq(NamedConstraint("fkey", ForeignKey("s.t2.y")))))))
    }

    "translate ALTER TABLE commands" in {
      example(
        query = "ALTER TABLE s.t1 ADD COLUMN c VARCHAR",
        expectedAst = AlterTableCommand("s.t1", Seq(AddColumn(ColumnDeclaration("c", VarCharType(None))))))

      example(
        query = "ALTER TABLE s.t1 ADD CONSTRAINT pk PRIMARY KEY (a, b, c)",
        expectedAst = AlterTableCommand(
          "s.t1",
          Seq(
            AddConstraint("a", NamedConstraint("pk", PrimaryKey)),
            AddConstraint("b", NamedConstraint("pk", PrimaryKey)),
            AddConstraint("c", NamedConstraint("pk", PrimaryKey)))))

      example(
        query = "ALTER TABLE s.t1 ALTER (COLUMN a TYPE INT)",
        expectedAst = AlterTableCommand("s.t1", Seq(ChangeColumnDataType("a", DecimalType(Some(38), None)))))
      example(
        query = "ALTER TABLE s.t1 ALTER (COLUMN a NOT NULL)",
        expectedAst = AlterTableCommand("s.t1", Seq(AddConstraint("a", Nullability(false)))))
      example(
        query = "ALTER TABLE s.t1 ALTER (COLUMN a DROP NOT NULL)",
        expectedAst = AlterTableCommand("s.t1", Seq(DropConstraint(Some("a"), Nullability(false)))))

      example(
        query = "ALTER TABLE s.t1 DROP COLUMN a",
        expectedAst = AlterTableCommand("s.t1", Seq(DropColumns(Seq("a")))))

      example(
        query = "ALTER TABLE s.t1 DROP PRIMARY KEY",
        expectedAst = AlterTableCommand("s.t1", Seq(DropConstraint(None, PrimaryKey))))
      example(
        query = "ALTER TABLE s.t1 DROP CONSTRAINT pk",
        expectedAst = AlterTableCommand("s.t1", Seq(DropConstraintByName("pk"))))
      example(
        query = "ALTER TABLE s.t1 DROP UNIQUE (b, c)",
        expectedAst =
          AlterTableCommand("s.t1", Seq(DropConstraint(Some("b"), Unique), DropConstraint(Some("c"), Unique))))

      example(
        query = "ALTER TABLE s.t1 RENAME COLUMN a TO aa",
        expectedAst = AlterTableCommand("s.t1", Seq(RenameColumn("a", "aa"))))
      example(
        query = "ALTER TABLE s.t1 RENAME CONSTRAINT pk TO pk_t1",
        expectedAst = AlterTableCommand("s.t1", Seq(RenameConstraint("pk", "pk_t1"))))
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
      val result = astBuilder.buildOutOfLineConstraints(outOfLineConstraint)
      result shouldBe Seq(
        "a" -> UnresolvedConstraint(dummyInputTextForOutOfLineConstraint),
        "b" -> UnresolvedConstraint(dummyInputTextForOutOfLineConstraint),
        "c" -> UnresolvedConstraint(dummyInputTextForOutOfLineConstraint))
      verify(outOfLineConstraint).column_list_in_parentheses(0)
      verify(outOfLineConstraint).UNIQUE()
      verify(outOfLineConstraint).primary_key()
      verify(outOfLineConstraint).foreign_key()
      verify(outOfLineConstraint).id_()
      verify(outOfLineConstraint, times(3)).getText
      verifyNoMoreInteractions(outOfLineConstraint)

    }
  }

  "SnowflakeDDLBuilder.buildInlineConstraint" should {

    "handle unexpected input" in {
      val inlineConstraint = mock[Inline_constraintContext]
      val dummyInputTextForInlineConstraint = "dummy"
      when(inlineConstraint.getText).thenReturn(dummyInputTextForInlineConstraint)
      val result = astBuilder.buildInlineConstraint(inlineConstraint)
      result shouldBe UnresolvedConstraint(dummyInputTextForInlineConstraint)
      verify(inlineConstraint).UNIQUE()
      verify(inlineConstraint).primary_key()
      verify(inlineConstraint).foreign_key()
      verify(inlineConstraint).getText
      verifyNoMoreInteractions(inlineConstraint)

    }
  }

  "SnowflakeDDLBuilder.visitAlter_table" should {
    "handle unexpected input" in {
      val tableName = parseString("s.t1", _.object_name())
      val alterTable = mock[Alter_tableContext]
      when(alterTable.object_name(0)).thenReturn(tableName)
      val dummyTextForAlterTable = "dummy"
      when(alterTable.getText).thenReturn(dummyTextForAlterTable)
      val result = astBuilder.visitAlter_table(alterTable)
      result shouldBe UnresolvedCatalog(dummyTextForAlterTable)
      verify(alterTable).object_name(0)
      verify(alterTable).table_column_action()
      verify(alterTable).constraint_action()
      verify(alterTable).getText
      verifyNoMoreInteractions(alterTable)

    }
  }

  "SnowflakeDDLBuilder.buildColumnActions" should {
    "handle unexpected input" in {
      val tableColumnAction = mock[Table_column_actionContext]
      when(tableColumnAction.alter_column_clause())
        .thenReturn(java.util.Collections.emptyList[Alter_column_clauseContext]())
      val dummyTextForTableColumnAction = "dummy"
      when(tableColumnAction.getText).thenReturn(dummyTextForTableColumnAction)
      val result = astBuilder.buildColumnActions(tableColumnAction)
      result shouldBe Seq(UnresolvedTableAlteration(dummyTextForTableColumnAction))
      verify(tableColumnAction).alter_column_clause()
      verify(tableColumnAction).ADD()
      verify(tableColumnAction).alter_column_clause()
      verify(tableColumnAction).DROP()
      verify(tableColumnAction).RENAME()
      verify(tableColumnAction).getText
      verifyNoMoreInteractions(tableColumnAction)
    }
  }

  "SnowflakeDDLBuilder.buildColumnAlterations" should {
    "handle unexpected input" in {
      val columnName = parseString("a", _.column_name())
      val alterColumnClause = mock[Alter_column_clauseContext]
      when(alterColumnClause.column_name()).thenReturn(columnName)
      val dummyTextForAlterColumnClause = "dummy"
      when(alterColumnClause.getText).thenReturn(dummyTextForAlterColumnClause)
      val result = astBuilder.buildColumnAlterations(alterColumnClause)
      result shouldBe UnresolvedTableAlteration(dummyTextForAlterColumnClause)
      verify(alterColumnClause).column_name()
      verify(alterColumnClause).data_type()
      verify(alterColumnClause).DROP()
      verify(alterColumnClause).NULL_()
      verify(alterColumnClause).getText
      verifyNoMoreInteractions(alterColumnClause)
    }
  }

  "SnowflakeDDLBuilder.buildConstraintActions" should {
    "handle unexpected input" in {
      val constraintAction = mock[Constraint_actionContext]
      val dummyTextForConstraintAction = "dummy"
      when(constraintAction.getText).thenReturn(dummyTextForConstraintAction)
      val result = astBuilder.buildConstraintActions(constraintAction)
      result shouldBe Seq(UnresolvedTableAlteration(dummyTextForConstraintAction))
      verify(constraintAction).ADD()
      verify(constraintAction).DROP()
      verify(constraintAction).RENAME()
      verify(constraintAction).getText
      verifyNoMoreInteractions(constraintAction)
    }
  }

  "SnowflakeDDLBuilder.buildDropConstraints" should {
    "handle unexpected input" in {
      val constraintAction = mock[Constraint_actionContext]
      when(constraintAction.id_()).thenReturn(java.util.Collections.emptyList[Id_Context])
      val dummyTextForConstraintAction = "dummy"
      when(constraintAction.getText).thenReturn(dummyTextForConstraintAction)
      val result = astBuilder.buildDropConstraints(constraintAction)
      result shouldBe Seq(UnresolvedTableAlteration(dummyTextForConstraintAction))
      verify(constraintAction).column_list_in_parentheses()
      verify(constraintAction).primary_key()
      verify(constraintAction).UNIQUE()
      verify(constraintAction).id_()
      verify(constraintAction).getText
      verifyNoMoreInteractions(constraintAction)
    }
  }
}
