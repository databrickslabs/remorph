package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.FunctionBuilder
import com.databricks.labs.remorph.parsers.intermediate._
import org.mockito.Mockito.{mock, when}
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

import java.util.Collections

class TSqlAstBuilderSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = new TSqlAstBuilder

  private def example(query: String, expectedAst: TreeNode): Assertion =
    example(query, _.tSqlFile(), expectedAst)

  "tsql visitor" should {

    "accept empty input" in {
      example(query = "", expectedAst = Batch(Seq.empty))
    }

    "translate a simple SELECT query" in {
      example(
        query = "SELECT a FROM dbo.table_x",
        expectedAst = Batch(Seq(Project(NamedTable("dbo.table_x", Map.empty, is_streaming = false), Seq(Column("a"))))))
    }

    "translate column aliases" in {
      example(
        query = "SELECT a AS b, J = BigCol FROM dbo.table_x",
        expectedAst = Batch(
          Seq(
            Project(
              NamedTable("dbo.table_x", Map.empty, is_streaming = false),
              Seq(Alias(Column("a"), Seq("b"), None), Alias(Column("BigCol"), Seq("J"), None))))))
    }

    "accept constants in selects" in {
      example(
        query = "SELECT 42, 6.4, 0x5A, 2.7E9, 4.24523534425245E10, $40",
        expectedAst = Batch(
          Seq(Project(
            NoTable,
            Seq(
              Literal(integer = Some(42)),
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
              Seq(Collate(Column("a"), "Latin1_General_BIN"))))))
    }

    "translate table source items with aliases" in {
      example(
        query = "SELECT a FROM dbo.table_x AS t",
        expectedAst = Batch(
          Seq(Project(TableAlias(NamedTable("dbo.table_x", Map.empty, is_streaming = false), "t"), Seq(Column("a"))))))
    }

    "translate table sources involving *" in {
      example(
        query = "SELECT * FROM dbo.table_x",
        expectedAst = Batch(Seq(Project(NamedTable("dbo.table_x", Map.empty, is_streaming = false), Seq(Star(None))))))
      example(query = "SELECT t.*", expectedAst = Batch(Seq(Project(NoTable, Seq(Star(objectName = Some("t")))))))
      example(
        query = "SELECT x..b.y.*",
        expectedAst = Batch(Seq(Project(NoTable, Seq(Star(objectName = Some("x..b.y")))))))
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
              NamedTable("dbo.table_x", Map.empty, is_streaming = false),
              NamedTable("dbo.table_y", Map.empty, is_streaming = false),
              None,
              CrossJoin,
              Seq.empty,
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            Seq(Column("a"), Column("b"), Column("c"))))))
    }
    "translate a query with a JOIN" in {
      example(
        query = "SELECT T1.A, T2.B FROM DBO.TABLE_X AS T1 INNER JOIN DBO.TABLE_Y AS T2 ON T1.A = T2.A AND T1.B = T2.B",
        expectedAst = Batch(
          Seq(Project(
            Join(
              TableAlias(NamedTable("DBO.TABLE_X", Map(), is_streaming = false), "T1"),
              TableAlias(NamedTable("DBO.TABLE_Y", Map(), is_streaming = false), "T2"),
              Some(And(Equals(Column("T1.A"), Column("T2.A")), Equals(Column("T1.B"), Column("T2.B")))),
              InnerJoin,
              List(),
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            List(Column("T1.A"), Column("T2.B"))))))
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
                Some(Equals(Column("T1.A"), Column("T2.A"))),
                InnerJoin,
                List(),
                JoinDataType(is_left_struct = false, is_right_struct = false)),
              TableAlias(NamedTable("DBO.TABLE_Z", Map(), is_streaming = false), "T3"),
              Some(And(Equals(Column("T1.A"), Column("T3.A")), Equals(Column("T1.B"), Column("T3.B")))),
              LeftOuterJoin,
              List(),
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            List(Column("T1.A"), Column("T2.B"))))))
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
                Some(Equals(Column("T1.A"), Column("T2.A"))),
                InnerJoin,
                List(),
                JoinDataType(is_left_struct = false, is_right_struct = false)),
              TableAlias(NamedTable("DBO.TABLE_Z", Map(), is_streaming = false), "T3"),
              Some(Or(Equals(Column("T1.A"), Column("T3.A")), Equals(Column("T1.B"), Column("T3.B")))),
              LeftOuterJoin,
              List(),
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            List(Column("T1.A"), Column("T2.B"))))))
    }
    "translate a query with a RIGHT OUTER JOIN" in {
      example(
        query = "SELECT T1.A FROM DBO.TABLE_X AS T1 RIGHT OUTER JOIN DBO.TABLE_Y AS T2 ON T1.A = T2.A",
        expectedAst = Batch(
          Seq(Project(
            Join(
              TableAlias(NamedTable("DBO.TABLE_X", Map(), is_streaming = false), "T1"),
              TableAlias(NamedTable("DBO.TABLE_Y", Map(), is_streaming = false), "T2"),
              Some(Equals(Column("T1.A"), Column("T2.A"))),
              RightOuterJoin,
              List(),
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            List(Column("T1.A"))))))
    }
    "translate a query with a FULL OUTER JOIN" in {
      example(
        query = "SELECT T1.A FROM DBO.TABLE_X AS T1 FULL OUTER JOIN DBO.TABLE_Y AS T2 ON T1.A = T2.A",
        expectedAst = Batch(
          Seq(Project(
            Join(
              TableAlias(NamedTable("DBO.TABLE_X", Map(), is_streaming = false), "T1"),
              TableAlias(NamedTable("DBO.TABLE_Y", Map(), is_streaming = false), "T2"),
              Some(Equals(Column("T1.A"), Column("T2.A"))),
              FullOuterJoin,
              List(),
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            List(Column("T1.A"))))))
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
            Seq(XmlFunction(CallFunction("query", Seq(Literal(string = Some("/root/child")))), Column("xmlcolumn")))))))

      example(
        "SELECT xmlcolumn.value('path', 'type') FROM tab",
        expectedAst = Batch(
          Seq(Project(
            NamedTable("tab", Map(), is_streaming = false),
            Seq(XmlFunction(
              CallFunction("value", Seq(Literal(string = Some("path")), Literal(string = Some("type")))),
              Column("xmlcolumn")))))))

      example(
        "SELECT xmlcolumn.exist('/root/child[text()=\"Some Value\"]') FROM xmltable;",
        expectedAst = Batch(
          Seq(Project(
            NamedTable("xmltable", Map(), is_streaming = false),
            Seq(XmlFunction(
              CallFunction("exist", Seq(Literal(string = Some("/root/child[text()=\"Some Value\"]")))),
              Column("xmlcolumn")))))))

      // TODO: Add nodes(), modify(), when we complete UPDATE and CROSS APPLY
    }

    "translate all assignments to local variables as select list elements" in {

      example(
        query = "SELECT @a = 1, @b = 2, @c = 3",
        expectedAst = Batch(
          Seq(Project(
            NoTable,
            Seq(
              Assign(Identifier("@a", isQuoted = false), Literal(integer = Some(1))),
              Assign(Identifier("@b", isQuoted = false), Literal(integer = Some(2))),
              Assign(Identifier("@c", isQuoted = false), Literal(integer = Some(3))))))))

      example(
        query = "SELECT @a += 1, @b -= 2",
        expectedAst = Batch(
          Seq(Project(
            NoTable,
            Seq(
              Assign(
                Identifier("@a", isQuoted = false),
                Add(Identifier("@a", isQuoted = false), Literal(integer = Some(1)))),
              Assign(
                Identifier("@b", isQuoted = false),
                Subtract(Identifier("@b", isQuoted = false), Literal(integer = Some(2)))))))))

      example(
        query = "SELECT @a *= 1, @b /= 2",
        expectedAst = Batch(
          Seq(Project(
            NoTable,
            Seq(
              Assign(
                Identifier("@a", isQuoted = false),
                Multiply(Identifier("@a", isQuoted = false), Literal(integer = Some(1)))),
              Assign(
                Identifier("@b", isQuoted = false),
                Divide(Identifier("@b", isQuoted = false), Literal(integer = Some(2)))))))))

      example(
        query = "SELECT @a %= myColumn",
        expectedAst = Batch(Seq(Project(
          NoTable,
          Seq(
            Assign(Identifier("@a", isQuoted = false), Mod(Identifier("@a", isQuoted = false), Column("myColumn"))))))))

      example(
        query = "SELECT @a &= myColumn",
        expectedAst = Batch(
          Seq(
            Project(
              NoTable,
              Seq(Assign(
                Identifier("@a", isQuoted = false),
                BitwiseAnd(Identifier("@a", isQuoted = false), Column("myColumn"))))))))

      example(
        query = "SELECT @a ^= myColumn",
        expectedAst = Batch(
          Seq(
            Project(
              NoTable,
              Seq(Assign(
                Identifier("@a", isQuoted = false),
                BitwiseXor(Identifier("@a", isQuoted = false), Column("myColumn"))))))))

      example(
        query = "SELECT @a |= myColumn",
        expectedAst = Batch(
          Seq(
            Project(
              NoTable,
              Seq(Assign(
                Identifier("@a", isQuoted = false),
                BitwiseOr(Identifier("@a", isQuoted = false), Column("myColumn"))))))))
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
              Column("EmployeeID"),
              Column("Name"),
              Alias(
                ScalarSubquery(Project(NamedTable("Employees", Map(), is_streaming = false), Seq(Column("AvgSalary")))),
                Seq("AverageSalary"),
                None))))))
    }
  }

  "visitTableSources" should {
    "return NoTable when tableSource is empty" in {
      val mockTableSourcesContext: TSqlParser.TableSourcesContext = mock(classOf[TSqlParser.TableSourcesContext])

      when(mockTableSourcesContext.tableSource())
        .thenReturn(Collections.emptyList().asInstanceOf[java.util.List[TSqlParser.TableSourceContext]])

      val tSqlRelationBuilder = new TSqlRelationBuilder()
      val result = tSqlRelationBuilder.visitTableSources(mockTableSourcesContext)

      result shouldBe NoTable
    }
  }

  "FunctionBuilder" should {

    "remove quotes and brackets from function names" in {
      // Test function name with less than 2 characters
      val result1 = FunctionBuilder.buildFunction("a", Seq())
      result1 match {
        case f: UnresolvedFunction => f.function_name shouldBe "a"
        case _ => fail("Unexpected function type")
      }

      // Test function name with matching quotes
      val result2 = FunctionBuilder.buildFunction("'quoted'", Seq())
      result2 match {
        case f: UnresolvedFunction => f.function_name shouldBe "quoted"
        case _ => fail("Unexpected function type")
      }

      // Test function name with matching brackets
      val result3 = FunctionBuilder.buildFunction("[bracketed]", Seq())
      result3 match {
        case f: UnresolvedFunction => f.function_name shouldBe "bracketed"
        case _ => fail("Unexpected function type")
      }

      // Test function name with matching backslashes
      val result4 = FunctionBuilder.buildFunction("\\backslashed\\", Seq())
      result4 match {
        case f: UnresolvedFunction => f.function_name shouldBe "backslashed"
        case _ => fail("Unexpected function type")
      }

      // Test function name with non-matching quotes
      val result5 = FunctionBuilder.buildFunction("'nonmatching", Seq())
      result5 match {
        case f: UnresolvedFunction => f.function_name shouldBe "'nonmatching"
        case _ => fail("Unexpected function type")
      }
    }
  }
}
