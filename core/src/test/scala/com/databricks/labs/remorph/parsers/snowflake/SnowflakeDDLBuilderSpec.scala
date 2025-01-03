package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.intermediate._
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.{StringContext => _, _}
import org.antlr.v4.runtime.CommonToken
import org.mockito.Mockito._
import org.scalatest.matchers.should
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

class SnowflakeDDLBuilderSpec
    extends AnyWordSpec
    with SnowflakeParserTestCommon
    with should.Matchers
    with MockitoSugar
    with IRHelpers {

  override protected def astBuilder: SnowflakeDDLBuilder = vc.ddlBuilder

  private def example(query: String, expectedAst: Catalog): Unit = example(query, _.ddlCommand(), expectedAst)

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
          returnType = StringType,
          parameters = Seq(FunctionParameter("x", StringType, None)),
          JavaRuntimeInfo(
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
          returnType = VariantType,
          parameters = Seq(),
          runtimeInfo = PythonRuntimeInfo(
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
          returnType = DoubleType,
          parameters = Seq(FunctionParameter("d", DoubleType, None)),
          runtimeInfo = JavaScriptRuntimeInfo,
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
          returnType = StringType,
          parameters = Seq(FunctionParameter("x", StringType, Some(Literal("foo")))),
          runtimeInfo = ScalaRuntimeInfo(runtimeVersion = Some("2.12"), imports = Seq(), handler = "Echo.echoVarchar"),
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
          returnType = DecimalType(38, 0),
          parameters =
            Seq(FunctionParameter("a", DecimalType(38, 0), None), FunctionParameter("b", DecimalType(38, 0), None)),
          runtimeInfo = SQLRuntimeInfo(memoizable = false),
          acceptsNullParameters = false,
          comment = Some("multiply two numbers"),
          body = "a * b"))
    }

    "translate CREATE TABLE commands" should {
      "CREATE TABLE s.t1 (x VARCHAR)" in {
        example(
          "CREATE TABLE s.t1 (x VARCHAR)",
          CreateTableCommand(name = "s.t1", columns = Seq(ColumnDeclaration("x", StringType, None, Seq()))))
      }
      "CREATE TABLE s.t1 (x VARCHAR UNIQUE)" in {
        example(
          "CREATE TABLE s.t1 (x VARCHAR UNIQUE)",
          CreateTableCommand(name = "s.t1", columns = Seq(ColumnDeclaration("x", StringType, None, Seq(Unique())))))
      }
      "CREATE TABLE s.t1 (x VARCHAR NOT NULL)" in {
        example(
          "CREATE TABLE s.t1 (x VARCHAR NOT NULL)",
          CreateTableCommand("s.t1", Seq(ColumnDeclaration("x", StringType, None, Seq(Nullability(false))))))
      }
      "CREATE TABLE s.t1 (x VARCHAR PRIMARY KEY)" in {
        example(
          "CREATE TABLE s.t1 (x VARCHAR PRIMARY KEY)",
          CreateTableCommand("s.t1", Seq(ColumnDeclaration("x", StringType, None, Seq(PrimaryKey())))))
      }
      "CREATE TABLE s.t1 (x VARCHAR UNIQUE FOREIGN KEY REFERENCES s.t2 (y))" in {
        example(
          "CREATE TABLE s.t1 (x VARCHAR UNIQUE FOREIGN KEY REFERENCES s.t2 (y))",
          CreateTableCommand(
            "s.t1",
            Seq(ColumnDeclaration("x", StringType, None, Seq(Unique(), ForeignKey("", "s.t2.y", "", Seq.empty))))))
      }
      "more complex" in {
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
              ColumnDeclaration("id", StringType, None, Seq(Nullability(false), PrimaryKey())),
              ColumnDeclaration(
                "a",
                StringType,
                None,
                Seq(Unique(), NamedConstraint("fkey", ForeignKey("", "s.t2.x", "", Seq.empty)))),
              ColumnDeclaration(
                "b",
                DecimalType(Some(38), Some(0)),
                None,
                Seq(NamedConstraint("fkey", ForeignKey("", "s.t2.y", "", Seq.empty)))))))
      }

      "CREATE TABLE t1 AS SELECT c1, c2 FROM t2;" in {
        example(
          "CREATE TABLE t1 AS (SELECT * FROM t2);",
          CreateTableParams(
            CreateTableAsSelect("t1", Project(namedTable("t2"), Seq(Star(None))), None, None, None),
            Map.empty[String, Seq[Constraint]],
            Map.empty[String, Seq[GenericOption]],
            Seq.empty[Constraint],
            Seq.empty[Constraint],
            None,
            None))
      }
    }
    "translate ALTER TABLE commands" should {
      "ALTER TABLE s.t1 ADD COLUMN c VARCHAR" in {
        example(
          "ALTER TABLE s.t1 ADD COLUMN c VARCHAR",
          AlterTableCommand("s.t1", Seq(AddColumn(Seq(ColumnDeclaration("c", StringType))))))
      }
      "ALTER TABLE s.t1 ADD CONSTRAINT pk PRIMARY KEY (a, b, c)" in {
        example(
          "ALTER TABLE s.t1 ADD CONSTRAINT pk PRIMARY KEY (a, b, c)",
          AlterTableCommand(
            "s.t1",
            Seq(
              AddConstraint("a", NamedConstraint("pk", PrimaryKey())),
              AddConstraint("b", NamedConstraint("pk", PrimaryKey())),
              AddConstraint("c", NamedConstraint("pk", PrimaryKey())))))
      }
      "ALTER TABLE s.t1 ALTER (COLUMN a TYPE INT)" in {
        example(
          "ALTER TABLE s.t1 ALTER (COLUMN a TYPE INT)",
          AlterTableCommand("s.t1", Seq(ChangeColumnDataType("a", DecimalType(Some(38), Some(0))))))
      }
      "ALTER TABLE s.t1 ALTER (COLUMN a NOT NULL)" in {
        example(
          "ALTER TABLE s.t1 ALTER (COLUMN a NOT NULL)",
          AlterTableCommand("s.t1", Seq(AddConstraint("a", Nullability(false)))))
      }
      "ALTER TABLE s.t1 ALTER (COLUMN a DROP NOT NULL)" in {
        example(
          "ALTER TABLE s.t1 ALTER (COLUMN a DROP NOT NULL)",
          AlterTableCommand("s.t1", Seq(DropConstraint(Some("a"), Nullability(false)))))
      }
      "ALTER TABLE s.t1 DROP COLUMN a" in {
        example("ALTER TABLE s.t1 DROP COLUMN a", AlterTableCommand("s.t1", Seq(DropColumns(Seq("a")))))
      }
      "ALTER TABLE s.t1 DROP PRIMARY KEY" in {
        example("ALTER TABLE s.t1 DROP PRIMARY KEY", AlterTableCommand("s.t1", Seq(DropConstraint(None, PrimaryKey()))))
      }
      "ALTER TABLE s.t1 DROP CONSTRAINT pk" in {
        example("ALTER TABLE s.t1 DROP CONSTRAINT pk", AlterTableCommand("s.t1", Seq(DropConstraintByName("pk"))))
      }
      "ALTER TABLE s.t1 DROP UNIQUE (b, c)" in {
        example(
          "ALTER TABLE s.t1 DROP UNIQUE (b, c)",
          AlterTableCommand("s.t1", Seq(DropConstraint(Some("b"), Unique()), DropConstraint(Some("c"), Unique()))))
      }
      "ALTER TABLE s.t1 RENAME COLUMN a TO aa" in {
        example("ALTER TABLE s.t1 RENAME COLUMN a TO aa", AlterTableCommand("s.t1", Seq(RenameColumn("a", "aa"))))
      }
      "ALTER TABLE s.t1 RENAME CONSTRAINT pk TO pk_t1" in {
        example(
          "ALTER TABLE s.t1 RENAME CONSTRAINT pk TO pk_t1",
          AlterTableCommand("s.t1", Seq(RenameConstraint("pk", "pk_t1"))))
      }
    }

    "translate Unresolved COMMAND" should {
      "ALTER SESSION SET QUERY_TAG = 'TAG'" in {
        example(
          "ALTER SESSION SET QUERY_TAG = 'TAG';",
          UnresolvedCommand(
            ruleText = "ALTER SESSION SET QUERY_TAG = 'TAG'",
            message = "Unknown ALTER command variant",
            ruleName = "alterCommand",
            tokenName = Some("ALTER")))
      }

      "ALTER STREAM mystream SET COMMENT = 'New comment for stream'" in {
        example(
          "ALTER STREAM mystream SET COMMENT = 'New comment for stream';",
          UnresolvedCommand(
            ruleText = "ALTER STREAM mystream SET COMMENT = 'New comment for stream'",
            message = "Unknown ALTER command variant",
            ruleName = "alterCommand",
            tokenName = Some("ALTER")))
      }

      "CREATE STREAM mystream ON TABLE mytable" in {
        example(
          "CREATE STREAM mystream ON TABLE mytable;",
          UnresolvedCommand(
            ruleText = "CREATE STREAM mystream ON TABLE mytable",
            message = "CREATE STREAM UNSUPPORTED",
            ruleName = "createStream",
            tokenName = Some("STREAM")))
      }

      "CREATE TASK t1 SCHEDULE = '30 MINUTE' AS INSERT INTO tbl(ts) VALUES(CURRENT_TIMESTAMP)" in {
        example(
          "CREATE TASK t1 SCHEDULE = '30 MINUTE' AS INSERT INTO tbl(ts) VALUES(CURRENT_TIMESTAMP);",
          UnresolvedCommand(
            ruleText = "CREATE TASK t1 SCHEDULE = '30 MINUTE' AS INSERT INTO tbl(ts) VALUES(CURRENT_TIMESTAMP)",
            message = "CREATE TASK UNSUPPORTED",
            ruleName = "createTask",
            tokenName = Some("TASK")))
      }
    }

    "wrap unknown AST in UnresolvedCommand" in {
      vc.ddlBuilder.visit(parseString("CREATE USER homer", _.createCommand())) shouldBe a[UnresolvedCommand]
    }
  }

  "SnowflakeDDLBuilder.buildOutOfLineConstraint" should {

    "handle unexpected child" in {
      val columnList = parseString("(a, b, c)", _.columnListInParentheses())
      val outOfLineConstraint = mock[OutOfLineConstraintContext]
      when(outOfLineConstraint.columnListInParentheses(0)).thenReturn(columnList)
      val dummyInputTextForOutOfLineConstraint = "dummy"
      when(outOfLineConstraint.getText).thenReturn(dummyInputTextForOutOfLineConstraint)
      val result = vc.ddlBuilder.buildOutOfLineConstraints(outOfLineConstraint)
      result shouldBe Seq(
        "a" -> UnresolvedConstraint(dummyInputTextForOutOfLineConstraint),
        "b" -> UnresolvedConstraint(dummyInputTextForOutOfLineConstraint),
        "c" -> UnresolvedConstraint(dummyInputTextForOutOfLineConstraint))
      verify(outOfLineConstraint).columnListInParentheses(0)
      verify(outOfLineConstraint).UNIQUE()
      verify(outOfLineConstraint).primaryKey()
      verify(outOfLineConstraint).foreignKey()
      verify(outOfLineConstraint).id()
      verify(outOfLineConstraint, times(3)).getText
      verifyNoMoreInteractions(outOfLineConstraint)

    }
  }

  "SnowflakeDDLBuilder.buildInlineConstraint" should {

    "handle unexpected child" in {
      val inlineConstraint = mock[InlineConstraintContext]
      val dummyInputTextForInlineConstraint = "dummy"
      when(inlineConstraint.getText).thenReturn(dummyInputTextForInlineConstraint)
      val result = vc.ddlBuilder.buildInlineConstraint(inlineConstraint)
      result shouldBe UnresolvedConstraint(dummyInputTextForInlineConstraint)
      verify(inlineConstraint).UNIQUE()
      verify(inlineConstraint).primaryKey()
      verify(inlineConstraint).foreignKey()
      verify(inlineConstraint).getText
      verifyNoMoreInteractions(inlineConstraint)
    }
  }
  "SnowflakeDDLBuilder.visitAlter_table" should {
    "handle unexpected child" in {
      val tableName = parseString("s.t1", _.dotIdentifier())
      val alterTable = mock[AlterTableContext]
      val startTok = new CommonToken(ID, "s")
      when(alterTable.dotIdentifier(0)).thenReturn(tableName)
      when(alterTable.getStart).thenReturn(startTok)
      when(alterTable.getStop).thenReturn(startTok)
      when(alterTable.getRuleIndex).thenReturn(SnowflakeParser.RULE_alterTable)
      val result = vc.ddlBuilder.visitAlterTable(alterTable)
      result shouldBe UnresolvedCommand(
        ruleText = "Mocked string",
        message = "Unknown ALTER TABLE variant",
        ruleName = "alterTable",
        tokenName = Some("ID"))
      verify(alterTable).dotIdentifier(0)
      verify(alterTable).tableColumnAction()
      verify(alterTable).constraintAction()
      verify(alterTable).getRuleIndex
      verify(alterTable, times(3)).getStart
      verify(alterTable).getStop
      verifyNoMoreInteractions(alterTable)
    }
  }

  "SnowflakeDDLBuilder.buildColumnActions" should {
    "handle unexpected child" in {
      val tableColumnAction = mock[TableColumnActionContext]
      when(tableColumnAction.alterColumnClause())
        .thenReturn(java.util.Collections.emptyList[AlterColumnClauseContext]())
      val startTok = new CommonToken(ID, "s")
      when(tableColumnAction.getStart).thenReturn(startTok)
      when(tableColumnAction.getStop).thenReturn(startTok)
      when(tableColumnAction.getRuleIndex).thenReturn(SnowflakeParser.RULE_tableColumnAction)
      val result = vc.ddlBuilder.buildColumnActions(tableColumnAction)
      result shouldBe Seq(
        UnresolvedTableAlteration(
          ruleText = "Mocked string",
          message = "Unknown COLUMN action variant",
          ruleName = "tableColumnAction",
          tokenName = Some("ID")))
      verify(tableColumnAction).alterColumnClause()
      verify(tableColumnAction).ADD()
      verify(tableColumnAction).alterColumnClause()
      verify(tableColumnAction).DROP()
      verify(tableColumnAction).RENAME()
      verify(tableColumnAction).getRuleIndex
      verify(tableColumnAction, times(3)).getStart
      verify(tableColumnAction).getStop
      verifyNoMoreInteractions(tableColumnAction)
    }
  }

  "SnowflakeDDLBuilder.buildColumnAlterations" should {
    "handle unexpected child" in {
      val columnName = parseString("a", _.columnName())
      val alterColumnClause = mock[AlterColumnClauseContext]
      when(alterColumnClause.columnName()).thenReturn(columnName)
      val startTok = new CommonToken(ID, "s")
      when(alterColumnClause.getStart).thenReturn(startTok)
      when(alterColumnClause.getStop).thenReturn(startTok)
      when(alterColumnClause.getRuleIndex).thenReturn(SnowflakeParser.RULE_alterColumnClause)
      val result = vc.ddlBuilder.buildColumnAlterations(alterColumnClause)
      result shouldBe UnresolvedTableAlteration(
        ruleText = "Mocked string",
        message = "Unknown ALTER COLUMN variant",
        ruleName = "alterColumnClause",
        tokenName = Some("ID"))
      verify(alterColumnClause).columnName()
      verify(alterColumnClause).dataType()
      verify(alterColumnClause).DROP()
      verify(alterColumnClause).NULL()
      verify(alterColumnClause).getRuleIndex
      verify(alterColumnClause, times(3)).getStart
      verify(alterColumnClause).getStop
      verifyNoMoreInteractions(alterColumnClause)
    }
  }

  "SnowflakeDDLBuilder.buildConstraintActions" should {
    "handle unexpected child" in {
      val constraintAction = mock[ConstraintActionContext]
      val startTok = new CommonToken(ID, "s")
      when(constraintAction.getStart).thenReturn(startTok)
      when(constraintAction.getStop).thenReturn(startTok)
      when(constraintAction.getRuleIndex).thenReturn(SnowflakeParser.RULE_constraintAction)
      val result = vc.ddlBuilder.buildConstraintActions(constraintAction)
      result shouldBe Seq(
        UnresolvedTableAlteration(
          ruleText = "Mocked string",
          message = "Unknown CONSTRAINT variant",
          ruleName = "constraintAction",
          tokenName = Some("ID")))
      verify(constraintAction).ADD()
      verify(constraintAction).DROP()
      verify(constraintAction).RENAME()
      verify(constraintAction).getRuleIndex
      verify(constraintAction, times(3)).getStart
      verify(constraintAction).getStop
      verifyNoMoreInteractions(constraintAction)
    }
  }

  "SnowflakeDDLBuilder.buildDropConstraints" should {
    "handle unexpected child" in {
      val constraintAction = mock[ConstraintActionContext]
      when(constraintAction.id()).thenReturn(java.util.Collections.emptyList[IdContext])
      val startTok = new CommonToken(ID, "s")
      when(constraintAction.getStart).thenReturn(startTok)
      when(constraintAction.getStop).thenReturn(startTok)
      when(constraintAction.getRuleIndex).thenReturn(SnowflakeParser.RULE_constraintAction)
      val result = vc.ddlBuilder.buildDropConstraints(constraintAction)
      result shouldBe Seq(
        UnresolvedTableAlteration(
          ruleText = "Mocked string",
          message = "Unknown DROP constraint variant",
          ruleName = "constraintAction",
          tokenName = Some("ID")))
      verify(constraintAction).columnListInParentheses()
      verify(constraintAction).primaryKey()
      verify(constraintAction).UNIQUE()
      verify(constraintAction).id()
      verify(constraintAction).getRuleIndex
      verify(constraintAction, times(3)).getStart
      verify(constraintAction).getStop
      verifyNoMoreInteractions(constraintAction)
    }
  }
}
