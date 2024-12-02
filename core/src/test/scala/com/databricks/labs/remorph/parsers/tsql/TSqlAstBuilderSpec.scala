package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.intermediate._
import com.databricks.labs.remorph.parsers.tsql
import com.databricks.labs.remorph.parsers.tsql.rules.TopPercent
import org.mockito.Mockito.{mock, when}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlAstBuilderSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers with IRHelpers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = vc.astBuilder

  private def example(query: String, expectedAst: LogicalPlan): Unit =
    example(query, _.tSqlFile(), expectedAst)

  private def singleQueryExample(query: String, expectedAst: LogicalPlan): Unit =
    example(query, _.tSqlFile(), Batch(Seq(expectedAst)))

  "tsql visitor" should {

    "accept empty child" in {
      example(query = "", expectedAst = Batch(Seq.empty))
    }

    "translate a simple SELECT query" in {
      example(
        query = "SELECT a FROM dbo.table_x",
        expectedAst = Batch(Seq(Project(namedTable("dbo.table_x"), Seq(simplyNamedColumn("a"))))))

      example(
        query = "SELECT a FROM TABLE",
        expectedAst = Batch(Seq(Project(namedTable("TABLE"), Seq(simplyNamedColumn("a"))))))
    }

    "translate column aliases" in {
      example(
        query = "SELECT a AS b, J = BigCol FROM dbo.table_x",
        expectedAst = Batch(
          Seq(
            Project(
              namedTable("dbo.table_x"),
              Seq(Alias(simplyNamedColumn("a"), Id("b")), Alias(simplyNamedColumn("BigCol"), Id("J")))))))
    }

    "accept constants in selects" in {
      example(
        query = "SELECT 42, 65535, 6.4, 0x5A, 2.7E9, 4.24523534425245E10, $40",
        expectedAst = Batch(
          Seq(
            Project(
              NoTable,
              Seq(
                Literal(42),
                Literal(65535),
                Literal(6.4f),
                Literal("0x5A"),
                Literal(2700000000L),
                Literal(4.24523534425245e10),
                Money(StringLiteral("$40")))))))
    }

    "translate collation specifiers" in {
      example(
        query = "SELECT a COLLATE Latin1_General_BIN FROM dbo.table_x",
        expectedAst =
          Batch(Seq(Project(namedTable("dbo.table_x"), Seq(Collate(simplyNamedColumn("a"), "Latin1_General_BIN"))))))
    }

    "translate table source items with aliases" in {
      example(
        query = "SELECT a FROM dbo.table_x AS t",
        expectedAst = Batch(Seq(Project(TableAlias(namedTable("dbo.table_x"), "t"), Seq(simplyNamedColumn("a"))))))
    }

    "translate table sources involving *" in {
      example(
        query = "SELECT * FROM dbo.table_x",
        expectedAst = Batch(Seq(Project(namedTable("dbo.table_x"), Seq(Star(None))))))

      example(
        query = "SELECT t.*",
        expectedAst = Batch(Seq(Project(NoTable, Seq(Star(objectName = Some(ObjectReference(Id("t")))))))))

      example(
        query = "SELECT x..b.y.*",
        expectedAst =
          Batch(Seq(Project(NoTable, Seq(Star(objectName = Some(ObjectReference(Id("x"), Id("b"), Id("y")))))))))

      // TODO: Add tests for OUTPUT clause once implemented - invalid semantics here to force coverage
      example(query = "SELECT INSERTED.*", expectedAst = Batch(Seq(Project(NoTable, Seq(Inserted(Star(None)))))))
      example(query = "SELECT DELETED.*", expectedAst = Batch(Seq(Project(NoTable, Seq(Deleted(Star(None)))))))
    }

    "infer a cross join" in {
      example(
        query = "SELECT a, b, c FROM dbo.table_x, dbo.table_y",
        expectedAst = Batch(
          Seq(Project(
            Join(
              namedTable("dbo.table_x"),
              namedTable("dbo.table_y"),
              None,
              CrossJoin,
              Seq.empty,
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            Seq(simplyNamedColumn("a"), simplyNamedColumn("b"), simplyNamedColumn("c"))))))
    }

    val t1aCol = Column(Some(ObjectReference(Id("T1"))), Id("A"))
    val t2aCol = Column(Some(ObjectReference(Id("T2"))), Id("A"))
    val t3aCol = Column(Some(ObjectReference(Id("T3"))), Id("A"))
    val t1bCol = Column(Some(ObjectReference(Id("T1"))), Id("B"))
    val t2bCol = Column(Some(ObjectReference(Id("T2"))), Id("B"))
    val t3bCol = Column(Some(ObjectReference(Id("T3"))), Id("B"))

    "translate a query with a JOIN" in {

      example(
        query = "SELECT T1.A, T2.B FROM DBO.TABLE_X AS T1 INNER JOIN DBO.TABLE_Y AS T2 ON T1.A = T2.A AND T1.B = T2.B",
        expectedAst = Batch(
          Seq(Project(
            Join(
              TableAlias(namedTable("DBO.TABLE_X"), "T1"),
              TableAlias(namedTable("DBO.TABLE_Y"), "T2"),
              Some(And(Equals(t1aCol, t2aCol), Equals(t1bCol, t2bCol))),
              InnerJoin,
              List(),
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            List(t1aCol, t2bCol)))))
    }
    "translate a query with Multiple JOIN AND Condition" in {

      example(
        query = "SELECT T1.A, T2.B FROM DBO.TABLE_X AS T1 INNER JOIN DBO.TABLE_Y AS T2 ON T1.A = T2.A " +
          "LEFT JOIN DBO.TABLE_Z AS T3 ON T1.A = T3.A AND T1.B = T3.B",
        expectedAst = Batch(
          Seq(Project(
            Join(
              Join(
                TableAlias(namedTable("DBO.TABLE_X"), "T1"),
                TableAlias(namedTable("DBO.TABLE_Y"), "T2"),
                Some(Equals(t1aCol, t2aCol)),
                InnerJoin,
                List(),
                JoinDataType(is_left_struct = false, is_right_struct = false)),
              TableAlias(namedTable("DBO.TABLE_Z"), "T3"),
              Some(And(Equals(t1aCol, t3aCol), Equals(t1bCol, t3bCol))),
              LeftOuterJoin,
              List(),
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            List(t1aCol, t2bCol)))))
    }
    "translate a query with Multiple JOIN OR Conditions" in {
      example(
        query = "SELECT T1.A, T2.B FROM DBO.TABLE_X AS T1 INNER JOIN DBO.TABLE_Y AS T2 ON T1.A = T2.A " +
          "LEFT JOIN DBO.TABLE_Z AS T3 ON T1.A = T3.A OR T1.B = T3.B",
        expectedAst = Batch(
          Seq(Project(
            Join(
              Join(
                TableAlias(namedTable("DBO.TABLE_X"), "T1"),
                TableAlias(namedTable("DBO.TABLE_Y"), "T2"),
                Some(Equals(t1aCol, t2aCol)),
                InnerJoin,
                List(),
                JoinDataType(is_left_struct = false, is_right_struct = false)),
              TableAlias(namedTable("DBO.TABLE_Z"), "T3"),
              Some(Or(Equals(t1aCol, t3aCol), Equals(t1bCol, t3bCol))),
              LeftOuterJoin,
              List(),
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            List(t1aCol, t2bCol)))))
    }
    "translate a query with a RIGHT OUTER JOIN" in {
      example(
        query = "SELECT T1.A FROM DBO.TABLE_X AS T1 RIGHT OUTER JOIN DBO.TABLE_Y AS T2 ON T1.A = T2.A",
        expectedAst = Batch(
          Seq(Project(
            Join(
              TableAlias(namedTable("DBO.TABLE_X"), "T1"),
              TableAlias(namedTable("DBO.TABLE_Y"), "T2"),
              Some(Equals(t1aCol, t2aCol)),
              RightOuterJoin,
              List(),
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            List(t1aCol)))))
    }
    "translate a query with a FULL OUTER JOIN" in {
      example(
        query = "SELECT T1.A FROM DBO.TABLE_X AS T1 FULL OUTER JOIN DBO.TABLE_Y AS T2 ON T1.A = T2.A",
        expectedAst = Batch(
          Seq(Project(
            Join(
              TableAlias(namedTable("DBO.TABLE_X"), "T1"),
              TableAlias(namedTable("DBO.TABLE_Y"), "T2"),
              Some(Equals(t1aCol, t2aCol)),
              FullOuterJoin,
              List(),
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            List(t1aCol)))))
    }

    "cover default case in translateJoinType" in {
      val joinOnContextMock = mock(classOf[TSqlParser.JoinOnContext])

      val outerJoinContextMock = mock(classOf[TSqlParser.OuterJoinContext])

      // Set up the mock to return null for LEFT(), RIGHT(), and FULL()
      when(outerJoinContextMock.LEFT()).thenReturn(null)
      when(outerJoinContextMock.RIGHT()).thenReturn(null)
      when(outerJoinContextMock.FULL()).thenReturn(null)

      when(joinOnContextMock.joinType()).thenReturn(null)

      val joinTypeContextMock = mock(classOf[TSqlParser.JoinTypeContext])
      when(joinTypeContextMock.outerJoin()).thenReturn(outerJoinContextMock)
      when(joinTypeContextMock.INNER()).thenReturn(null)
      when(joinOnContextMock.joinType()).thenReturn(joinTypeContextMock)

      val result = vc.relationBuilder.translateJoinType(joinOnContextMock)
      result shouldBe UnspecifiedJoin
    }

    "translate simple XML query and values" in {
      example(
        query = "SELECT xmlcolumn.query('/root/child') FROM tab",
        expectedAst = Batch(
          Seq(Project(
            namedTable("tab"),
            Seq(tsql
              .TsqlXmlFunction(CallFunction("query", Seq(Literal("/root/child"))), simplyNamedColumn("xmlcolumn")))))))

      example(
        "SELECT xmlcolumn.value('path', 'type') FROM tab",
        expectedAst = Batch(
          Seq(
            Project(
              namedTable("tab"),
              Seq(tsql.TsqlXmlFunction(
                CallFunction("value", Seq(Literal("path"), Literal("type"))),
                simplyNamedColumn("xmlcolumn")))))))

      example(
        "SELECT xmlcolumn.exist('/root/child[text()=\"Some Value\"]') FROM xmltable;",
        expectedAst = Batch(
          Seq(Project(
            namedTable("xmltable"),
            Seq(tsql.TsqlXmlFunction(
              CallFunction("exist", Seq(Literal("/root/child[text()=\"Some Value\"]"))),
              simplyNamedColumn("xmlcolumn")))))))

      // TODO: Add nodes(), modify(), when we complete UPDATE and CROSS APPLY
    }

    "translate all assignments to local variables as select list elements" in {

      example(
        query = "SELECT @a = 1, @b = 2, @c = 3",
        expectedAst = Batch(
          Seq(Project(
            NoTable,
            Seq(
              Assign(Identifier("@a", isQuoted = false), Literal(1)),
              Assign(Identifier("@b", isQuoted = false), Literal(2)),
              Assign(Identifier("@c", isQuoted = false), Literal(3)))))))

      example(
        query = "SELECT @a += 1, @b -= 2",
        expectedAst = Batch(
          Seq(Project(
            NoTable,
            Seq(
              Assign(Identifier("@a", isQuoted = false), Add(Identifier("@a", isQuoted = false), Literal(1))),
              Assign(Identifier("@b", isQuoted = false), Subtract(Identifier("@b", isQuoted = false), Literal(2))))))))

      example(
        query = "SELECT @a *= 1, @b /= 2",
        expectedAst = Batch(
          Seq(Project(
            NoTable,
            Seq(
              Assign(Identifier("@a", isQuoted = false), Multiply(Identifier("@a", isQuoted = false), Literal(1))),
              Assign(Identifier("@b", isQuoted = false), Divide(Identifier("@b", isQuoted = false), Literal(2))))))))

      example(
        query = "SELECT @a %= myColumn",
        expectedAst = Batch(
          Seq(
            Project(
              NoTable,
              Seq(Assign(
                Identifier("@a", isQuoted = false),
                Mod(Identifier("@a", isQuoted = false), simplyNamedColumn("myColumn"))))))))

      example(
        query = "SELECT @a &= myColumn",
        expectedAst = Batch(
          Seq(
            Project(
              NoTable,
              Seq(Assign(
                Identifier("@a", isQuoted = false),
                BitwiseAnd(Identifier("@a", isQuoted = false), simplyNamedColumn("myColumn"))))))))

      example(
        query = "SELECT @a ^= myColumn",
        expectedAst = Batch(
          Seq(
            Project(
              NoTable,
              Seq(Assign(
                Identifier("@a", isQuoted = false),
                BitwiseXor(Identifier("@a", isQuoted = false), simplyNamedColumn("myColumn"))))))))

      example(
        query = "SELECT @a |= myColumn",
        expectedAst = Batch(
          Seq(
            Project(
              NoTable,
              Seq(Assign(
                Identifier("@a", isQuoted = false),
                BitwiseOr(Identifier("@a", isQuoted = false), simplyNamedColumn("myColumn"))))))))
    }
    "translate scalar subqueries as expressions in select list" in {
      example(
        query = """SELECT
                          EmployeeID,
                          Name,
                          (SELECT AvgSalary FROM Employees) AS AverageSalary
                      FROM
                          Employees;""",
        expectedAst = Batch(
          Seq(Project(
            namedTable("Employees"),
            Seq(
              simplyNamedColumn("EmployeeID"),
              simplyNamedColumn("Name"),
              Alias(
                ScalarSubquery(Project(namedTable("Employees"), Seq(simplyNamedColumn("AvgSalary")))),
                Id("AverageSalary")))))))
    }
  }

  "SQL statements should support DISTINCT clauses" in {
    example(
      query = "SELECT DISTINCT * FROM Employees;",
      expectedAst = Batch(
        Seq(
          Project(
            Deduplicate(namedTable("Employees"), List(), all_columns_as_keys = true, within_watermark = false),
            Seq(Star(None))))))
    example(
      query = "SELECT DISTINCT a, b AS bb FROM t",
      expectedAst = Batch(
        Seq(Project(
          Deduplicate(namedTable("t"), List(Id("a"), Id("bb")), all_columns_as_keys = false, within_watermark = false),
          Seq(simplyNamedColumn("a"), Alias(simplyNamedColumn("b"), Id("bb")))))))
  }

  "SELECT NEXT VALUE FOR mySequence As nextVal" in {
    example(
      query = "SELECT NEXT VALUE FOR mySequence As nextVal",
      expectedAst = Batch(
        Seq(Project(NoTable, Seq(Alias(CallFunction("MONOTONICALLY_INCREASING_ID", List.empty), Id("nextVal")))))))
  }

  "SELECT NEXT VALUE FOR var.mySequence As nextVal" in {
    example(
      query = "SELECT NEXT VALUE FOR var.mySequence As nextVal",
      expectedAst = Batch(
        Seq(Project(NoTable, Seq(Alias(CallFunction("MONOTONICALLY_INCREASING_ID", List.empty), Id("nextVal")))))))
  }

  "SELECT NEXT VALUE FOR var.mySequence OVER (ORDER BY myColumn) As nextVal" in {
    example(
      query = "SELECT NEXT VALUE FOR var.mySequence OVER (ORDER BY myColumn) As nextVal ",
      expectedAst = Batch(
        Seq(Project(
          NoTable,
          Seq(Alias(
            Window(
              CallFunction("ROW_NUMBER", List.empty),
              List.empty,
              List(SortOrder(simplyNamedColumn("myColumn"), UnspecifiedSortDirection, SortNullsUnspecified)),
              None),
            Id("nextVal")))))))
  }

  "translate CTE select statements" in {
    example(
      query = "WITH cte AS (SELECT * FROM t) SELECT * FROM cte",
      expectedAst = Batch(
        Seq(
          WithCTE(
            Seq(SubqueryAlias(Project(namedTable("t"), Seq(Star(None))), Id("cte"), List.empty)),
            Project(namedTable("cte"), Seq(Star(None)))))))

    example(
      query = """WITH cteTable1 (col1, col2, col3count)
                AS
                (
                    SELECT col1, fred, COUNT(OrderDate) AS counter
                    FROM Table1
                ),
                cteTable2 (colx, coly, colxcount)
                AS
                (
                    SELECT col1, fred, COUNT(OrderDate) AS counter
                    FROM Table2
                )
                SELECT col2, col1, col3count, colx, coly, colxcount
                FROM cteTable""",
      expectedAst = Batch(
        Seq(WithCTE(
          Seq(
            SubqueryAlias(
              Project(
                namedTable("Table1"),
                Seq(
                  simplyNamedColumn("col1"),
                  simplyNamedColumn("fred"),
                  Alias(CallFunction("COUNT", Seq(simplyNamedColumn("OrderDate"))), Id("counter")))),
              Id("cteTable1"),
              Seq(Id("col1"), Id("col2"), Id("col3count"))),
            SubqueryAlias(
              Project(
                namedTable("Table2"),
                Seq(
                  simplyNamedColumn("col1"),
                  simplyNamedColumn("fred"),
                  Alias(CallFunction("COUNT", Seq(simplyNamedColumn("OrderDate"))), Id("counter")))),
              Id("cteTable2"),
              Seq(Id("colx"), Id("coly"), Id("colxcount")))),
          Project(
            namedTable("cteTable"),
            Seq(
              simplyNamedColumn("col2"),
              simplyNamedColumn("col1"),
              simplyNamedColumn("col3count"),
              simplyNamedColumn("colx"),
              simplyNamedColumn("coly"),
              simplyNamedColumn("colxcount")))))))
  }

  "translate a SELECT with a TOP clause" should {
    "use LIMIT" in {
      example(
        query = "SELECT TOP 10 * FROM Employees;",
        expectedAst = Batch(Seq(Project(Limit(namedTable("Employees"), Literal(10)), Seq(Star(None))))))
    }

    "use TOP PERCENT" in {
      example(
        query = "SELECT TOP 10 PERCENT * FROM Employees;",
        expectedAst = Batch(Seq(Project(TopPercent(namedTable("Employees"), Literal(10)), Seq(Star(None))))))

      example(
        query = "SELECT TOP 10 PERCENT WITH TIES * FROM Employees;",
        expectedAst =
          Batch(Seq(Project(TopPercent(namedTable("Employees"), Literal(10), with_ties = true), Seq(Star(None))))))
    }
  }

  "translate a SELECT statement with an ORDER BY and OFFSET" in {
    example(
      query = "SELECT * FROM Employees ORDER BY Salary OFFSET 10 ROWS",
      expectedAst = Batch(
        Seq(Project(
          Offset(
            Sort(
              namedTable("Employees"),
              Seq(SortOrder(simplyNamedColumn("Salary"), Ascending, SortNullsUnspecified)),
              is_global = false),
            Literal(10)),
          Seq(Star(None))))))

    example(
      query = "SELECT * FROM Employees ORDER BY Salary OFFSET 10 ROWS FETCH NEXT 5 ROWS ONLY",
      expectedAst = Batch(
        Seq(Project(
          Limit(
            Offset(
              Sort(
                namedTable("Employees"),
                Seq(SortOrder(simplyNamedColumn("Salary"), Ascending, SortNullsUnspecified)),
                is_global = false),
              Literal(10)),
            Literal(5)),
          Seq(Star(None))))))
  }

  "translate SELECT with a combination of DISTINCT, ORDER BY, and OFFSET" in {
    example(
      query = "SELECT DISTINCT * FROM Employees ORDER BY Salary OFFSET 10 ROWS",
      expectedAst = Batch(
        Seq(Project(
          Deduplicate(
            Offset(
              Sort(
                namedTable("Employees"),
                Seq(SortOrder(simplyNamedColumn("Salary"), Ascending, SortNullsUnspecified)),
                is_global = false),
              Literal(10)),
            List(),
            all_columns_as_keys = true,
            within_watermark = false),
          Seq(Star(None))))))

    example(
      query = "SELECT DISTINCT * FROM Employees ORDER BY Salary OFFSET 10 ROWS FETCH NEXT 5 ROWS ONLY",
      expectedAst = Batch(
        List(Project(
          Deduplicate(
            Limit(
              Offset(
                Sort(
                  namedTable("Employees"),
                  List(SortOrder(simplyNamedColumn("Salary"), Ascending, SortNullsUnspecified)),
                  is_global = false),
                Literal(10)),
              Literal(5)),
            List(),
            all_columns_as_keys = true,
            within_watermark = false),
          List(Star(None))))))
  }

  "translate a query with PIVOT" in {
    singleQueryExample(
      query = "SELECT a FROM b PIVOT (SUM(a) FOR c IN ('foo', 'bar')) AS Source",
      expectedAst = Project(
        Aggregate(
          child = namedTable("b"),
          group_type = Pivot,
          grouping_expressions = Seq(CallFunction("SUM", Seq(simplyNamedColumn("a")))),
          pivot = Some(Pivot(simplyNamedColumn("c"), Seq(Literal("foo"), Literal("bar"))))),
        Seq(simplyNamedColumn("a"))))
  }

  "translate a query with UNPIVOT" in {
    singleQueryExample(
      query = "SELECT a FROM b UNPIVOT (c FOR d IN (e, f)) AsSource",
      expectedAst = Project(
        Unpivot(
          child = namedTable("b"),
          ids = Seq(simplyNamedColumn("e"), simplyNamedColumn("f")),
          values = None,
          variable_column_name = Id("c"),
          value_column_name = Id("d")),
        Seq(simplyNamedColumn("a"))))
  }

  "translate a query with an explicit CROSS JOIN" in {
    singleQueryExample(
      query = "SELECT a FROM b CROSS JOIN c",
      expectedAst = Project(
        Join(
          namedTable("b"),
          namedTable("c"),
          None,
          CrossJoin,
          Seq.empty,
          JoinDataType(is_left_struct = false, is_right_struct = false)),
        Seq(simplyNamedColumn("a"))))
  }

  "translate a query with an explicit OUTER APPLY" in {
    singleQueryExample(
      query = "SELECT a FROM b OUTER APPLY c",
      expectedAst = Project(
        Join(
          namedTable("b"),
          namedTable("c"),
          None,
          OuterApply,
          Seq.empty,
          JoinDataType(is_left_struct = false, is_right_struct = false)),
        Seq(simplyNamedColumn("a"))))
  }

  "translate a query with an explicit CROSS APPLY" in {
    singleQueryExample(
      query = "SELECT a FROM b CROSS APPLY c",
      expectedAst = Project(
        Join(
          namedTable("b"),
          namedTable("c"),
          None,
          CrossApply,
          Seq.empty,
          JoinDataType(is_left_struct = false, is_right_struct = false)),
        Seq(simplyNamedColumn("a"))))
  }

  "parse and ignore IR for the FOR clause in a SELECT statement" in {
    example(
      query = "SELECT * FROM DAYS FOR XML RAW",
      expectedAst = Batch(Seq(Project(namedTable("DAYS"), Seq(Star(None))))))
  }

  "parse and collect the options in the OPTION clause in a SELECT statement" in {
    example(
      query = """SELECT * FROM t FOR XML RAW
            OPTION (
            MAXRECURSION 10,
            OPTIMIZE [FOR] UNKNOWN,
            SOMETHING ON,
            SOMETHINGELSE OFF,
            SOMEOTHER AUTO,
            SOMEstrOpt = 'STRINGOPTION')""",
      expectedAst = Batch(
        Seq(WithOptions(
          Project(namedTable("t"), Seq(Star(None))),
          Options(
            Map("MAXRECURSION" -> Literal(10), "OPTIMIZE" -> Column(None, Id("FOR", true))),
            Map("SOMESTROPT" -> "STRINGOPTION"),
            Map("SOMETHING" -> true, "SOMETHINGELSE" -> false),
            List("SOMEOTHER"))))))
  }

  "parse and collect table hints for named table select statements in all variants" in {
    example(
      query = "SELECT * FROM t WITH (NOLOCK)",
      expectedAst = Batch(Seq(Project(TableWithHints(namedTable("t"), Seq(FlagHint("NOLOCK"))), Seq(Star(None))))))
    example(
      query = "SELECT * FROM t WITH (FORCESEEK)",
      expectedAst =
        Batch(Seq(Project(TableWithHints(namedTable("t"), Seq(ForceSeekHint(None, None))), Seq(Star(None))))))
    example(
      query = "SELECT * FROM t WITH (FORCESEEK(1 (Col1, Col2)))",
      expectedAst = Batch(
        Seq(
          Project(
            TableWithHints(namedTable("t"), Seq(ForceSeekHint(Some(Literal(1)), Some(Seq(Id("Col1"), Id("Col2")))))),
            Seq(Star(None))))))
    example(
      query = "SELECT * FROM t WITH (INDEX = (Bill, Ted))",
      expectedAst = Batch(
        Seq(Project(TableWithHints(namedTable("t"), Seq(IndexHint(Seq(Id("Bill"), Id("Ted"))))), Seq(Star(None))))))
    example(
      query = "SELECT * FROM t WITH (FORCESEEK, INDEX = (Bill, Ted))",
      expectedAst = Batch(
        Seq(
          Project(
            TableWithHints(namedTable("t"), Seq(ForceSeekHint(None, None), IndexHint(Seq(Id("Bill"), Id("Ted"))))),
            Seq(Star(None))))))
  }

  "translate INSERT statements" in {
    example(
      query = "INSERT INTO t (a, b) VALUES (1, 2)",
      expectedAst = Batch(
        Seq(
          InsertIntoTable(
            namedTable("t"),
            Some(Seq(Id("a"), Id("b"))),
            DerivedRows(Seq(Seq(Literal(1), Literal(2)))),
            None,
            None,
            overwrite = false))))
  }
  "translate INSERT statement with @LocalVar" in {
    example(
      query = "INSERT INTO @LocalVar (a, b) VALUES (1, 2)",
      expectedAst = Batch(
        Seq(
          InsertIntoTable(
            LocalVarTable(Id("@LocalVar")),
            Some(Seq(Id("a"), Id("b"))),
            DerivedRows(Seq(Seq(Literal(1), Literal(2)))),
            None,
            None,
            overwrite = false))))
  }

  "translate insert statements with VALU(pa, irs)" in {
    example(
      query = "INSERT INTO t (a, b) VALUES (1, 2), (3, 4)",
      expectedAst = Batch(
        Seq(
          InsertIntoTable(
            namedTable("t"),
            Some(Seq(Id("a"), Id("b"))),
            DerivedRows(Seq(Seq(Literal(1), Literal(2)), Seq(Literal(3), Literal(4)))),
            None,
            None,
            overwrite = false))))
  }

  "translate insert statements with (OPTIONS)" in {
    example(
      query = "INSERT INTO t WITH (TABLOCK) (a, b) VALUES (1, 2)",
      expectedAst = Batch(
        Seq(InsertIntoTable(
          TableWithHints(namedTable("t"), List(FlagHint("TABLOCK"))),
          Some(Seq(Id("a"), Id("b"))),
          DerivedRows(Seq(Seq(Literal(1), Literal(2)))),
          None,
          None,
          overwrite = false))))
  }

  "translate insert statement with DEFAULT VALUES" in {
    example(
      query = "INSERT INTO t DEFAULT VALUES",
      expectedAst = Batch(Seq(InsertIntoTable(namedTable("t"), None, DefaultValues(), None, None, overwrite = false))))
  }

  "translate INSERT statement with OUTPUT clause" in {
    example(
      query = "INSERT INTO t (a, b) OUTPUT INSERTED.a as a_lias, INSERTED.b INTO Inserted(a, b) VALUES (1, 2)",
      expectedAst = Batch(
        List(InsertIntoTable(
          namedTable("t"),
          Some(List(Id("a"), Id("b"))),
          DerivedRows(List(List(Literal(1), Literal(2)))),
          Some(tsql.Output(
            Some(namedTable("Inserted")),
            List(
              Alias(Column(Some(ObjectReference(Id("INSERTED"))), Id("a")), Id("a_lias")),
              Column(Some(ObjectReference(Id("INSERTED"))), Id("b"))),
            Some(List(simplyNamedColumn("a"), simplyNamedColumn("b"))))),
          None,
          overwrite = false))))
  }

  "translate insert statements with CTE" in {
    example(
      query = "WITH wtab AS (SELECT * FROM t) INSERT INTO t (a, b) select * from wtab",
      expectedAst = Batch(
        Seq(WithCTE(
          Seq(SubqueryAlias(Project(namedTable("t"), Seq(Star(None))), Id("wtab"), List.empty)),
          InsertIntoTable(
            namedTable("t"),
            Some(Seq(Id("a"), Id("b"))),
            Project(namedTable("wtab"), Seq(Star(None))),
            None,
            None,
            overwrite = false)))))
  }

  "translate insert statements with SELECT" in {
    example(
      query = """
           INSERT INTO ConsolidatedRecords (ID, Name)
              SELECT ID, Name
              FROM (
                SELECT ID, Name
                FROM TableA
                  UNION
                SELECT ID, Name
                FROM TableB)
              AS DerivedTable;""",
      expectedAst = Batch(
        Seq(InsertIntoTable(
          namedTable("ConsolidatedRecords"),
          Some(Seq(Id("ID"), Id("Name"))),
          Project(
            TableAlias(
              SetOperation(
                Project(namedTable("TableA"), Seq(simplyNamedColumn("ID"), simplyNamedColumn("Name"))),
                Project(namedTable("TableB"), Seq(simplyNamedColumn("ID"), simplyNamedColumn("Name"))),
                UnionSetOp,
                is_all = false,
                by_name = false,
                allow_missing_columns = false),
              "DerivedTable"),
            Seq(simplyNamedColumn("ID"), simplyNamedColumn("Name"))),
          None,
          None,
          overwrite = false))))
  }

  "should translate UPDATE statements" in {
    example(
      query = "UPDATE t SET a = 1, b = 2",
      expectedAst = Batch(
        Seq(
          UpdateTable(
            NamedTable("t", Map(), is_streaming = false),
            None,
            Seq(Assign(Column(None, Id("a")), Literal(1)), Assign(Column(None, Id("b")), Literal(2))),
            None,
            None,
            None))))

    example(
      query = "UPDATE t SET a = 1, b = 2 OUTPUT INSERTED.a as a_lias, INSERTED.b INTO Inserted(a, b)",
      expectedAst = Batch(
        Seq(UpdateTable(
          NamedTable("t", Map(), is_streaming = false),
          None,
          Seq(Assign(Column(None, Id("a")), Literal(1)), Assign(Column(None, Id("b")), Literal(2))),
          None,
          Some(tsql.Output(
            Some(NamedTable("Inserted", Map(), is_streaming = false)),
            Seq(
              Alias(Column(Some(ObjectReference(Id("INSERTED"))), Id("a")), Id("a_lias")),
              Column(Some(ObjectReference(Id("INSERTED"))), Id("b"))),
            Some(Seq(Column(None, Id("a")), Column(None, Id("b")))))),
          None))))

    example(
      query = "UPDATE t SET a = 1, b = 2 FROM t1 WHERE t.a = t1.a",
      expectedAst = Batch(
        Seq(UpdateTable(
          NamedTable("t", Map(), is_streaming = false),
          Some(NamedTable("t1", Map(), is_streaming = false)),
          Seq(Assign(Column(None, Id("a")), Literal(1)), Assign(Column(None, Id("b")), Literal(2))),
          Some(
            Equals(Column(Some(ObjectReference(Id("t"))), Id("a")), Column(Some(ObjectReference(Id("t1"))), Id("a")))),
          None,
          None))))

    example(
      query = "UPDATE t SET a = 1, udf.Transform(b) FROM t1 WHERE t.a = t1.a OPTION (KEEP PLAN)",
      expectedAst = Batch(
        Seq(UpdateTable(
          NamedTable("t", Map(), is_streaming = false),
          Some(NamedTable("t1", Map(), is_streaming = false)),
          Seq(
            Assign(Column(None, Id("a")), Literal(1)),
            UnresolvedFunction(
              "udf.Transform",
              Seq(Column(None, Id("b"))),
              is_distinct = false,
              is_user_defined_function = true,
              ruleText = "udf.Transform(...)",
              ruleName = "N/A",
              tokenName = Some("N/A"),
              message = "Function udf.Transform is not convertible to Databricks SQL")),
          Some(
            Equals(Column(Some(ObjectReference(Id("t"))), Id("a")), Column(Some(ObjectReference(Id("t1"))), Id("a")))),
          None,
          Some(Options(Map("KEEP" -> Column(None, Id("PLAN"))), Map.empty, Map.empty, List.empty))))))
  }

  "translate DELETE statements" in {
    example(
      query = "DELETE FROM t",
      expectedAst = Batch(Seq(DeleteFromTable(NamedTable("t", Map(), is_streaming = false), None, None, None, None))))

    example(
      query = "DELETE FROM t OUTPUT DELETED.a as a_lias, DELETED.b INTO Deleted(a, b)",
      expectedAst = Batch(
        Seq(DeleteFromTable(
          NamedTable("t", Map(), is_streaming = false),
          None,
          None,
          Some(tsql.Output(
            Some(NamedTable("Deleted", Map(), is_streaming = false)),
            Seq(
              Alias(Column(Some(ObjectReference(Id("DELETED"))), Id("a")), Id("a_lias")),
              Column(Some(ObjectReference(Id("DELETED"))), Id("b"))),
            Some(Seq(Column(None, Id("a")), Column(None, Id("b")))))),
          None))))

    example(
      query = "DELETE FROM t FROM t1 WHERE t.a = t1.a",
      expectedAst = Batch(
        Seq(DeleteFromTable(
          NamedTable("t", Map(), is_streaming = false),
          Some(NamedTable("t1", Map(), is_streaming = false)),
          Some(
            Equals(Column(Some(ObjectReference(Id("t"))), Id("a")), Column(Some(ObjectReference(Id("t1"))), Id("a")))),
          None,
          None))))

    example(
      query = "DELETE FROM t FROM t1 WHERE t.a = t1.a OPTION (KEEP PLAN)",
      expectedAst = Batch(
        Seq(DeleteFromTable(
          NamedTable("t", Map(), is_streaming = false),
          Some(NamedTable("t1", Map(), is_streaming = false)),
          Some(
            Equals(Column(Some(ObjectReference(Id("t"))), Id("a")), Column(Some(ObjectReference(Id("t1"))), Id("a")))),
          None,
          Some(Options(Map("KEEP" -> Column(None, Id("PLAN"))), Map.empty, Map.empty, List.empty))))))
  }

  "translate MERGE statements" in {
    example(
      query = """
          |MERGE INTO t USING s
          | ON t.a = s.a
          | WHEN MATCHED THEN UPDATE SET t.b = s.b
          | WHEN NOT MATCHED THEN INSERT (a, b) VALUES (s.a, s.b)""".stripMargin,
      expectedAst = Batch(
        Seq(MergeIntoTable(
          NamedTable("t", Map(), is_streaming = false),
          NamedTable("s", Map(), is_streaming = false),
          Equals(Column(Some(ObjectReference(Id("t"))), Id("a")), Column(Some(ObjectReference(Id("s"))), Id("a"))),
          Seq(
            UpdateAction(
              None,
              Seq(Assign(
                Column(Some(ObjectReference(Id("t"))), Id("b")),
                Column(Some(ObjectReference(Id("s"))), Id("b")))))),
          Seq(InsertAction(
            None,
            Seq(
              Assign(Column(None, Id("a")), Column(Some(ObjectReference(Id("s"))), Id("a"))),
              Assign(Column(None, Id("b")), Column(Some(ObjectReference(Id("s"))), Id("b")))))),
          List.empty))))
  }

  "translate MERGE statements with options" in {
    example(
      query = """
            |MERGE INTO t USING s
            | ON t.a = s.a
            | WHEN MATCHED THEN UPDATE SET t.b = s.b
            | WHEN NOT MATCHED THEN INSERT (a, b) VALUES (s.a, s.b)
            | OPTION ( KEEPFIXED PLAN, FAST 666, MAX_GRANT_PERCENT = 30, FLAME ON, FLAME OFF, QUICKLY) """.stripMargin,
      expectedAst = Batch(
        Seq(WithModificationOptions(
          MergeIntoTable(
            NamedTable("t", Map(), is_streaming = false),
            NamedTable("s", Map(), is_streaming = false),
            Equals(Column(Some(ObjectReference(Id("t"))), Id("a")), Column(Some(ObjectReference(Id("s"))), Id("a"))),
            Seq(
              UpdateAction(
                None,
                Seq(Assign(
                  Column(Some(ObjectReference(Id("t"))), Id("b")),
                  Column(Some(ObjectReference(Id("s"))), Id("b")))))),
            Seq(InsertAction(
              None,
              Seq(
                Assign(Column(None, Id("a")), Column(Some(ObjectReference(Id("s"))), Id("a"))),
                Assign(Column(None, Id("b")), Column(Some(ObjectReference(Id("s"))), Id("b")))))),
            List.empty),
          Options(
            Map("KEEPFIXED" -> Column(None, Id("PLAN")), "FAST" -> Literal(666), "MAX_GRANT_PERCENT" -> Literal(30)),
            Map(),
            Map("FLAME" -> false, "QUICKLY" -> true),
            List())))))
    example(
      query = """
            |WITH s (a, b, col3count)
            |                AS
            |                (
            |                    SELECT col1, fred, COUNT(OrderDate) AS counter
            |                    FROM Table1
            |                )
            |   MERGE INTO t WITH (NOLOCK, READCOMMITTED) USING s
            |   ON t.a = s.a
            |   WHEN MATCHED THEN UPDATE SET t.b = s.b
            |   WHEN NOT MATCHED BY TARGET THEN DELETE
            |   WHEN NOT MATCHED BY SOURCE THEN INSERT (a, b) VALUES (s.a, s.b)""".stripMargin,
      expectedAst = Batch(
        Seq(WithCTE(
          Seq(SubqueryAlias(
            Project(
              namedTable("Table1"),
              Seq(
                simplyNamedColumn("col1"),
                simplyNamedColumn("fred"),
                Alias(CallFunction("COUNT", Seq(simplyNamedColumn("OrderDate"))), Id("counter")))),
            Id("s"),
            Seq(Id("a"), Id("b"), Id("col3count")))),
          MergeIntoTable(
            TableWithHints(
              NamedTable("t", Map(), is_streaming = false),
              Seq(FlagHint("NOLOCK"), FlagHint("READCOMMITTED"))),
            NamedTable("s", Map(), is_streaming = false),
            Equals(Column(Some(ObjectReference(Id("t"))), Id("a")), Column(Some(ObjectReference(Id("s"))), Id("a"))),
            Seq(
              UpdateAction(
                None,
                Seq(Assign(
                  Column(Some(ObjectReference(Id("t"))), Id("b")),
                  Column(Some(ObjectReference(Id("s"))), Id("b")))))),
            Seq(DeleteAction(None)),
            Seq(InsertAction(
              None,
              Seq(
                Assign(Column(None, Id("a")), Column(Some(ObjectReference(Id("s"))), Id("a"))),
                Assign(Column(None, Id("b")), Column(Some(ObjectReference(Id("s"))), Id("b")))))))))))
  }
}
