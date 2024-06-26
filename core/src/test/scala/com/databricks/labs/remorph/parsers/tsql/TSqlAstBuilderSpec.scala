package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.IRHelpers
import com.databricks.labs.remorph.parsers.intermediate._
import org.mockito.Mockito.{mock, when}
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlAstBuilderSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers with IRHelpers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = new TSqlAstBuilder

  private def example(query: String, expectedAst: TreeNode): Assertion =
    example(query, _.tSqlFile(), expectedAst)

  private def singleQueryExample(query: String, expectedAst: Relation): Assertion =
    example(query, _.tSqlFile(), Batch(Seq(expectedAst)))

  "tsql visitor" should {

    "accept empty input" in {
      example(query = "", expectedAst = Batch(Seq.empty))
    }

    "translate a simple SELECT query" in {
      example(
        query = "SELECT a FROM dbo.table_x",
        expectedAst =
          Batch(Seq(Project(NamedTable("dbo.table_x", Map.empty, is_streaming = false), Seq(simplyNamedColumn("a"))))))

      example(
        query = "SELECT a FROM TABLE",
        expectedAst =
          Batch(Seq(Project(NamedTable("TABLE", Map.empty, is_streaming = false), Seq(simplyNamedColumn("a"))))))
    }

    "translate column aliases" in {
      example(
        query = "SELECT a AS b, J = BigCol FROM dbo.table_x",
        expectedAst = Batch(
          Seq(Project(
            NamedTable("dbo.table_x", Map.empty, is_streaming = false),
            Seq(
              Alias(simplyNamedColumn("a"), Seq(Id("b")), None),
              Alias(simplyNamedColumn("BigCol"), Seq(Id("J")), None))))))
    }

    "accept constants in selects" in {
      example(
        query = "SELECT 42, 65535, 6.4, 0x5A, 2.7E9, 4.24523534425245E10, $40",
        expectedAst = Batch(
          Seq(Project(
            NoTable(),
            Seq(
              Literal(short = Some(42)),
              Literal(integer = Some(65535)),
              Literal(float = Some(6.4f)),
              Literal(string = Some("0x5A")),
              Literal(long = Some(2700000000L)),
              Literal(double = Some(4.24523534425245e10)),
              Money(Literal(string = Some("$40"))))))))
    }

    "translate collation specifiers" in {
      example(
        query = "SELECT a COLLATE Latin1_General_BIN FROM dbo.table_x",
        expectedAst = Batch(
          Seq(
            Project(
              NamedTable("dbo.table_x", Map.empty, is_streaming = false),
              Seq(Collate(simplyNamedColumn("a"), "Latin1_General_BIN"))))))
    }

    "translate table source items with aliases" in {
      example(
        query = "SELECT a FROM dbo.table_x AS t",
        expectedAst = Batch(
          Seq(
            Project(
              TableAlias(NamedTable("dbo.table_x", Map.empty, is_streaming = false), "t"),
              Seq(simplyNamedColumn("a"))))))
    }

    "translate table sources involving *" in {
      example(
        query = "SELECT * FROM dbo.table_x",
        expectedAst = Batch(Seq(Project(NamedTable("dbo.table_x", Map.empty, is_streaming = false), Seq(Star(None))))))

      example(
        query = "SELECT t.*",
        expectedAst = Batch(Seq(Project(NoTable(), Seq(Star(objectName = Some(ObjectReference(Id("t")))))))))

      example(
        query = "SELECT x..b.y.*",
        expectedAst =
          Batch(Seq(Project(NoTable(), Seq(Star(objectName = Some(ObjectReference(Id("x"), Id("b"), Id("y")))))))))

      // TODO: Add tests for OUTPUT clause once implemented - invalid semantics here to force coverage
      example(query = "SELECT INSERTED.*", expectedAst = Batch(Seq(Project(NoTable(), Seq(Inserted(Star(None)))))))
      example(query = "SELECT DELETED.*", expectedAst = Batch(Seq(Project(NoTable(), Seq(Deleted(Star(None)))))))
    }

    "infer a cross join" in {
      example(
        query = "SELECT a, b, c FROM dbo.table_x, dbo.table_y",
        expectedAst = Batch(
          Seq(Project(
            Join(
              NamedTable("dbo.table_x", Map.empty, is_streaming = false),
              NamedTable("dbo.table_y", Map.empty, is_streaming = false),
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
              TableAlias(NamedTable("DBO.TABLE_X", Map(), is_streaming = false), "T1"),
              TableAlias(NamedTable("DBO.TABLE_Y", Map(), is_streaming = false), "T2"),
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
                TableAlias(NamedTable("DBO.TABLE_X", Map(), is_streaming = false), "T1"),
                TableAlias(NamedTable("DBO.TABLE_Y", Map(), is_streaming = false), "T2"),
                Some(Equals(t1aCol, t2aCol)),
                InnerJoin,
                List(),
                JoinDataType(is_left_struct = false, is_right_struct = false)),
              TableAlias(NamedTable("DBO.TABLE_Z", Map(), is_streaming = false), "T3"),
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
                TableAlias(NamedTable("DBO.TABLE_X", Map(), is_streaming = false), "T1"),
                TableAlias(NamedTable("DBO.TABLE_Y", Map(), is_streaming = false), "T2"),
                Some(Equals(t1aCol, t2aCol)),
                InnerJoin,
                List(),
                JoinDataType(is_left_struct = false, is_right_struct = false)),
              TableAlias(NamedTable("DBO.TABLE_Z", Map(), is_streaming = false), "T3"),
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
              TableAlias(NamedTable("DBO.TABLE_X", Map(), is_streaming = false), "T1"),
              TableAlias(NamedTable("DBO.TABLE_Y", Map(), is_streaming = false), "T2"),
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
              TableAlias(NamedTable("DBO.TABLE_X", Map(), is_streaming = false), "T1"),
              TableAlias(NamedTable("DBO.TABLE_Y", Map(), is_streaming = false), "T2"),
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

      val builder = new TSqlRelationBuilder
      val result = builder.translateJoinType(joinOnContextMock)
      result shouldBe UnspecifiedJoin
    }

    "translate simple XML query and values" in {
      example(
        query = "SELECT xmlcolumn.query('/root/child') FROM tab",
        expectedAst = Batch(
          Seq(Project(
            NamedTable("tab", Map(), is_streaming = false),
            Seq(XmlFunction(
              CallFunction("query", Seq(Literal(string = Some("/root/child")))),
              simplyNamedColumn("xmlcolumn")))))))

      example(
        "SELECT xmlcolumn.value('path', 'type') FROM tab",
        expectedAst = Batch(
          Seq(Project(
            NamedTable("tab", Map(), is_streaming = false),
            Seq(XmlFunction(
              CallFunction("value", Seq(Literal(string = Some("path")), Literal(string = Some("type")))),
              simplyNamedColumn("xmlcolumn")))))))

      example(
        "SELECT xmlcolumn.exist('/root/child[text()=\"Some Value\"]') FROM xmltable;",
        expectedAst = Batch(
          Seq(Project(
            NamedTable("xmltable", Map(), is_streaming = false),
            Seq(XmlFunction(
              CallFunction("exist", Seq(Literal(string = Some("/root/child[text()=\"Some Value\"]")))),
              simplyNamedColumn("xmlcolumn")))))))

      // TODO: Add nodes(), modify(), when we complete UPDATE and CROSS APPLY
    }

    "translate all assignments to local variables as select list elements" in {

      example(
        query = "SELECT @a = 1, @b = 2, @c = 3",
        expectedAst = Batch(
          Seq(Project(
            NoTable(),
            Seq(
              Assign(Identifier("@a", isQuoted = false), Literal(short = Some(1))),
              Assign(Identifier("@b", isQuoted = false), Literal(short = Some(2))),
              Assign(Identifier("@c", isQuoted = false), Literal(short = Some(3))))))))

      example(
        query = "SELECT @a += 1, @b -= 2",
        expectedAst = Batch(
          Seq(Project(
            NoTable(),
            Seq(
              Assign(
                Identifier("@a", isQuoted = false),
                Add(Identifier("@a", isQuoted = false), Literal(short = Some(1)))),
              Assign(
                Identifier("@b", isQuoted = false),
                Subtract(Identifier("@b", isQuoted = false), Literal(short = Some(2)))))))))

      example(
        query = "SELECT @a *= 1, @b /= 2",
        expectedAst = Batch(
          Seq(Project(
            NoTable(),
            Seq(
              Assign(
                Identifier("@a", isQuoted = false),
                Multiply(Identifier("@a", isQuoted = false), Literal(short = Some(1)))),
              Assign(
                Identifier("@b", isQuoted = false),
                Divide(Identifier("@b", isQuoted = false), Literal(short = Some(2)))))))))

      example(
        query = "SELECT @a %= myColumn",
        expectedAst = Batch(
          Seq(
            Project(
              NoTable(),
              Seq(Assign(
                Identifier("@a", isQuoted = false),
                Mod(Identifier("@a", isQuoted = false), simplyNamedColumn("myColumn"))))))))

      example(
        query = "SELECT @a &= myColumn",
        expectedAst = Batch(
          Seq(
            Project(
              NoTable(),
              Seq(Assign(
                Identifier("@a", isQuoted = false),
                BitwiseAnd(Identifier("@a", isQuoted = false), simplyNamedColumn("myColumn"))))))))

      example(
        query = "SELECT @a ^= myColumn",
        expectedAst = Batch(
          Seq(
            Project(
              NoTable(),
              Seq(Assign(
                Identifier("@a", isQuoted = false),
                BitwiseXor(Identifier("@a", isQuoted = false), simplyNamedColumn("myColumn"))))))))

      example(
        query = "SELECT @a |= myColumn",
        expectedAst = Batch(
          Seq(
            Project(
              NoTable(),
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
            NamedTable("Employees", Map(), is_streaming = false),
            Seq(
              simplyNamedColumn("EmployeeID"),
              simplyNamedColumn("Name"),
              Alias(
                ScalarSubquery(
                  Project(NamedTable("Employees", Map(), is_streaming = false), Seq(simplyNamedColumn("AvgSalary")))),
                Seq(Id("AverageSalary")),
                None))))))
    }
  }

  "SQL statements should support DISTINCT clauses" in {
    example(
      query = "SELECT DISTINCT * FROM Employees;",
      expectedAst = Batch(
        Seq(
          Project(
            Deduplicate(
              NamedTable("Employees", Map(), is_streaming = false),
              List(),
              all_columns_as_keys = true,
              within_watermark = false),
            Seq(Star(None))))))
    example(
      query = "SELECT DISTINCT a, b AS bb FROM t",
      expectedAst = Batch(
        Seq(Project(
          Deduplicate(
            NamedTable("t", Map(), is_streaming = false),
            List(Id("a"), Id("bb")),
            all_columns_as_keys = false,
            within_watermark = false),
          Seq(simplyNamedColumn("a"), Alias(simplyNamedColumn("b"), Seq(Id("bb")), None))))))
  }

  "Columns specified with dedicated syntax" in {
    example(
      query = "SELECT NEXT VALUE FOR mySequence As nextVal",
      expectedAst = Batch(
        Seq(
          Project(
            NoTable(),
            Seq(Alias(CallFunction("MONOTONICALLY_INCREASING_ID", List.empty), Seq(Id("nextVal")), None))))))

    example(
      query = "SELECT NEXT VALUE FOR var.mySequence As nextVal",
      expectedAst = Batch(
        Seq(
          Project(
            NoTable(),
            Seq(Alias(CallFunction("MONOTONICALLY_INCREASING_ID", List.empty), Seq(Id("nextVal")), None))))))

    example(
      query = "SELECT NEXT VALUE FOR var.mySequence OVER (ORDER BY myColumn) As nextVal ",
      expectedAst = Batch(
        Seq(Project(
          NoTable(),
          Seq(Alias(
            Window(
              CallFunction("ROW_NUMBER", List.empty),
              List.empty,
              List(SortOrder(simplyNamedColumn("myColumn"), AscendingSortDirection, SortNullsUnspecified)),
              None),
            Seq(Id("nextVal")),
            None))))))

  }

  "translate CTE select statements" in {
    example(
      query = "WITH cte AS (SELECT * FROM t) SELECT * FROM cte",
      expectedAst = Batch(
        Seq(WithCTE(
          Seq(CTEDefinition("cte", List.empty, Project(NamedTable("t", Map(), is_streaming = false), Seq(Star(None))))),
          Project(NamedTable("cte", Map(), is_streaming = false), Seq(Star(None)))))))

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
            CTEDefinition(
              "cteTable1",
              Seq(simplyNamedColumn("col1"), simplyNamedColumn("col2"), simplyNamedColumn("col3count")),
              Project(
                NamedTable("Table1", Map(), is_streaming = false),
                Seq(
                  simplyNamedColumn("col1"),
                  simplyNamedColumn("fred"),
                  Alias(CallFunction("COUNT", Seq(simplyNamedColumn("OrderDate"))), Seq(Id("counter")), None)))),
            CTEDefinition(
              "cteTable2",
              Seq(simplyNamedColumn("colx"), simplyNamedColumn("coly"), simplyNamedColumn("colxcount")),
              Project(
                NamedTable("Table2", Map(), is_streaming = false),
                Seq(
                  simplyNamedColumn("col1"),
                  simplyNamedColumn("fred"),
                  Alias(CallFunction("COUNT", Seq(simplyNamedColumn("OrderDate"))), Seq(Id("counter")), None))))),
          Project(
            NamedTable("cteTable", Map(), is_streaming = false),
            Seq(
              simplyNamedColumn("col2"),
              simplyNamedColumn("col1"),
              simplyNamedColumn("col3count"),
              simplyNamedColumn("colx"),
              simplyNamedColumn("coly"),
              simplyNamedColumn("colxcount")))))))
  }

  "parse genericOptions correctly" in {
    // NOTE that we are using the BACKUP DATABASE command to test the generic options as it is the
    // simplest command that has generic options.
    example(
      query = "BACKUP DATABASE mydb TO DISK = 'disk' WITH mount = auto, verbose = default",
      expectedAst = Batch(Seq(BackupDatabase("mydb", Seq("disk"), Map.empty, Seq("MOUNT"), Map.empty))))

    example(
      query = "BACKUP DATABASE mydb TO DISK = 'disk1', DISK = 'disk2' WITH mount = auto, verbose = default",
      expectedAst = Batch(Seq(BackupDatabase("mydb", Seq("disk2", "disk1"), Map.empty, Seq("MOUNT"), Map.empty))))

    example(
      query = "BACKUP DATABASE mydb TO DISK = 'disk1' WITH audit = ON, desCription = 'backup1', FILE_SNAPSHOT OFF",
      expectedAst = Batch(
        Seq(
          BackupDatabase("mydb", Seq("disk1"), Map("AUDIT" -> true, "FILE_SNAPSHOT" -> false), List.empty, Map.empty))))

    example(
      query = "BACKUP DATABASE mydb TO DISK = 'disk1' WITH ON, OFF, AUTO, DEFAULT",
      expectedAst =
        Batch(Seq(BackupDatabase("mydb", Seq("disk1"), Map("ON" -> true, "OFF" -> false), Seq("AUTO"), Map.empty))))

    example(
      query = "BACKUP DATABASE mydb TO DISK 'd1' WITH COPY_ONLY, limit = 77 KB",
      expectedAst = Batch(
        Seq(
          BackupDatabase(
            "mydb",
            Seq("d1"),
            Map("COPY_ONLY" -> true),
            List.empty,
            Map("LIMIT" -> Literal(short = Some(77)))))))
  }

  "translate a SELECT with a TOP clause" in {
    example(
      query = "SELECT TOP 10 * FROM Employees;",
      expectedAst = Batch(
        Seq(
          Project(
            Limit(
              NamedTable("Employees", Map(), is_streaming = false),
              Literal(integer = Some(10)),
              is_percentage = false,
              with_ties = false),
            Seq(Star(None))))))

    example(
      query = "SELECT TOP 10 PERCENT * FROM Employees;",
      expectedAst = Batch(
        Seq(
          Project(
            Limit(
              NamedTable("Employees", Map(), is_streaming = false),
              Literal(integer = Some(10)),
              is_percentage = true,
              with_ties = false),
            Seq(Star(None))))))

    example(
      query = "SELECT TOP 10 PERCENT WITH TIES * FROM Employees;",
      expectedAst = Batch(
        Seq(
          Project(
            Limit(
              NamedTable("Employees", Map(), is_streaming = false),
              Literal(integer = Some(10)),
              is_percentage = true,
              with_ties = true),
            Seq(Star(None))))))
  }

  "translate a SELECT statement with an ORDER BY and OFFSET" in {
    example(
      query = "SELECT * FROM Employees ORDER BY Salary OFFSET 10 ROWS",
      expectedAst = Batch(
        Seq(Project(
          Offset(
            Sort(
              NamedTable("Employees", Map(), is_streaming = false),
              Seq(SortOrder(simplyNamedColumn("Salary"), AscendingSortDirection, SortNullsUnspecified)),
              is_global = false),
            Literal(integer = Some(10))),
          Seq(Star(None))))))

    example(
      query = "SELECT * FROM Employees ORDER BY Salary OFFSET 10 ROWS FETCH NEXT 5 ROWS ONLY",
      expectedAst = Batch(
        Seq(Project(
          Limit(
            Offset(
              Sort(
                NamedTable("Employees", Map(), is_streaming = false),
                Seq(SortOrder(simplyNamedColumn("Salary"), AscendingSortDirection, SortNullsUnspecified)),
                is_global = false),
              Literal(integer = Some(10))),
            Literal(integer = Some(5))),
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
                NamedTable("Employees", Map(), is_streaming = false),
                Seq(SortOrder(simplyNamedColumn("Salary"), AscendingSortDirection, SortNullsUnspecified)),
                is_global = false),
              Literal(integer = Some(10))),
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
                  NamedTable("Employees", Map(), is_streaming = false),
                  List(SortOrder(Column(None, Id("Salary")), AscendingSortDirection, SortNullsUnspecified)),
                  is_global = false),
                Literal(integer = Some(10))),
              Literal(integer = Some(5))),
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
          input = NamedTable("b", Map.empty, is_streaming = false),
          group_type = Pivot,
          grouping_expressions = Seq(CallFunction("SUM", Seq(simplyNamedColumn("a")))),
          pivot =
            Some(Pivot(simplyNamedColumn("c"), Seq(Literal(string = Some("foo")), Literal(string = Some("bar")))))),
        Seq(simplyNamedColumn("a"))))
  }

  "translate a query with UNPIVOT" in {
    singleQueryExample(
      query = "SELECT a FROM b UNPIVOT (c FOR d IN (e, f)) AsSource",
      expectedAst = Project(
        Unpivot(
          input = NamedTable("b", Map.empty, is_streaming = false),
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
          NamedTable("b", Map.empty, is_streaming = false),
          NamedTable("c", Map.empty, is_streaming = false),
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
          NamedTable("b", Map.empty, is_streaming = false),
          NamedTable("c", Map.empty, is_streaming = false),
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
          NamedTable("b", Map.empty, is_streaming = false),
          NamedTable("c", Map.empty, is_streaming = false),
          None,
          CrossApply,
          Seq.empty,
          JoinDataType(is_left_struct = false, is_right_struct = false)),
        Seq(simplyNamedColumn("a"))))
  }

  "parse and ignore IR for the FOR clause in a SELECT statement" in {
    example(
      query = "SELECT * FROM t FOR XML RAW",
      expectedAst = Batch(Seq(Project(NamedTable("t", Map(), is_streaming = false), Seq(Star(None))))))
  }

  "parse and collect the options in the OPTION clause in a SELECT statement" in {
    example(
      query = """SELECT * FROM t FOR XML RAW
            OPTION (
            MAXRECURSION 10,
            OPTIMIZE FOR UNKNOWN,
            SOMETHING ON,
            SOMETHINGELSE OFF,
            SOMEOTHER AUTO,
            SOMEstrOpt = 'STRINGOPTION')""",
      expectedAst = Batch(Seq(Project(NamedTable("t", Map(), is_streaming = false), Seq(Star(None))))))
  }
}
