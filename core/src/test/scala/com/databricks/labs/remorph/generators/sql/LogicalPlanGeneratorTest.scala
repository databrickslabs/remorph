package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.{GeneratorContext, GeneratorTestCommon}
import com.databricks.labs.remorph.{Generating, intermediate => ir}
import org.scalatest.wordspec.AnyWordSpec

class LogicalPlanGeneratorTest extends AnyWordSpec with GeneratorTestCommon[ir.LogicalPlan] with ir.IRHelpers {

  protected val expressionGenerator = new ExpressionGenerator()
  protected val optionGenerator = new OptionGenerator(expressionGenerator)
  override protected val generator = new LogicalPlanGenerator(expressionGenerator, optionGenerator)

  override protected def initialState(plan: ir.LogicalPlan) =
    Generating(optimizedPlan = plan, currentNode = plan, ctx = GeneratorContext(generator))
  "Project" should {
    "transpile to SELECT" in {
      ir.Project(namedTable("t1"), Seq(ir.Id("c1"))) generates "SELECT c1 FROM t1"
      ir.Project(namedTable("t1"), Seq(ir.Star(None))) generates "SELECT * FROM t1"
      ir.Project(ir.NoTable, Seq(ir.Literal(1))) generates "SELECT 1"
    }

    "transpile to SELECT with COMMENTS" in {
      ir.WithOptions(
        ir.Project(namedTable("t"), Seq(ir.Star(None))),
        ir.Options(
          Map("MAXRECURSION" -> ir.Literal(10), "OPTIMIZE" -> ir.Column(None, ir.Id("FOR", caseSensitive = true))),
          Map("SOMESTROPT" -> "STRINGOPTION"),
          Map("SOMETHING" -> true, "SOMETHINGELSE" -> false),
          List("SOMEOTHER"))) generates
        """/*
            |   The following statement was originally given the following OPTIONS:
            |
            |    Expression options:
            |
            |     MAXRECURSION = 10
            |     OPTIMIZE = `FOR`
            |
            |    String options:
            |
            |     SOMESTROPT = 'STRINGOPTION'
            |
            |    Boolean options:
            |
            |     SOMETHING ON
            |     SOMETHINGELSE OFF
            |
            |    Auto options:
            |
            |     SOMEOTHER AUTO
            |
            |
            | */
            |SELECT * FROM t""".stripMargin
    }
  }

  "Filter" should {
    "transpile to WHERE" in {
      ir.Filter(
        ir.Project(namedTable("t1"), Seq(ir.Id("c1"))),
        ir.CallFunction("IS_DATE", Seq(ir.Id("c2")))) generates "(SELECT c1 FROM t1) WHERE IS_DATE(c2)"
    }
  }

  "MergeIntoTable" should {
    "transpile to MERGE" in {
      ir.MergeIntoTable(
        namedTable("t"),
        namedTable("s"),
        ir.Equals(
          ir.Column(Some(ir.ObjectReference(ir.Id("t"))), ir.Id("a")),
          ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("a"))),
        Seq(
          ir.UpdateAction(
            None,
            Seq(
              ir.Assign(
                ir.Column(Some(ir.ObjectReference(ir.Id("t"))), ir.Id("b")),
                ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("b"))))),
          ir.DeleteAction(
            Some(ir.LessThan(ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("b")), ir.Literal(10))))),
        Seq(
          ir.InsertAction(
            None,
            Seq(
              ir.Assign(ir.Column(None, ir.Id("a")), ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("a"))),
              ir.Assign(ir.Column(None, ir.Id("b")), ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("b")))))),
        List.empty) generates
        s"""MERGE INTO t
           |USING s
           |ON t.a = s.a
           | WHEN MATCHED THEN UPDATE SET t.b = s.b WHEN MATCHED AND s.b < 10 THEN DELETE
           | WHEN NOT MATCHED THEN INSERT (a, b) VALUES (s.a, s.b)
           |
           |""".stripMargin
    }
    "transpile to MERGE with comments" in {
      ir.WithOptions(
        ir.MergeIntoTable(
          ir.NamedTable("t", Map(), is_streaming = false),
          ir.NamedTable("s", Map(), is_streaming = false),
          ir.Equals(
            ir.Column(Some(ir.ObjectReference(ir.Id("t"))), ir.Id("a")),
            ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("a"))),
          Seq(
            ir.UpdateAction(
              None,
              Seq(
                ir.Assign(
                  ir.Column(Some(ir.ObjectReference(ir.Id("t"))), ir.Id("b")),
                  ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("b")))))),
          Seq(
            ir.InsertAction(
              None,
              Seq(
                ir.Assign(ir.Column(None, ir.Id("a")), ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("a"))),
                ir.Assign(ir.Column(None, ir.Id("b")), ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("b")))))),
          List.empty),
        ir.Options(
          Map(
            "KEEPFIXED" -> ir.Column(None, ir.Id("PLAN")),
            "FAST" -> ir.Literal(666),
            "MAX_GRANT_PERCENT" -> ir.Literal(30)),
          Map(),
          Map("FLAME" -> false, "QUICKLY" -> true),
          List())) generates
        """/*
          |   The following statement was originally given the following OPTIONS:
          |
          |    Expression options:
          |
          |     KEEPFIXED = PLAN
          |     FAST = 666
          |     MAX_GRANT_PERCENT = 30
          |
          |    Boolean options:
          |
          |     FLAME OFF
          |     QUICKLY ON
          |
          |
          | */
          |MERGE INTO t
          |USING s
          |ON t.a = s.a
          | WHEN MATCHED THEN UPDATE SET t.b = s.b
          | WHEN NOT MATCHED THEN INSERT (a, b) VALUES (s.a, s.b)
          |
          |""".stripMargin
    }
  }

  "UpdateTable" should {
    "transpile to UPDATE" in {
      ir.UpdateTable(
        namedTable("t"),
        None,
        Seq(
          ir.Assign(ir.Column(None, ir.Id("a")), ir.Literal(1)),
          ir.Assign(ir.Column(None, ir.Id("b")), ir.Literal(2))),
        Some(ir.Equals(ir.Column(None, ir.Id("c")), ir.Literal(3)))) generates
        "UPDATE t SET a = 1, b = 2 WHERE c = 3"
    }
  }

  "InsertIntoTable" should {
    "transpile to INSERT" in {
      ir.InsertIntoTable(
        namedTable("t"),
        Some(Seq(ir.Id("a"), ir.Id("b"))),
        ir.Values(Seq(Seq(ir.Literal(1), ir.Literal(2))))) generates "INSERT INTO t (a, b) VALUES (1,2)"
    }
  }

  "DeleteFromTable" should {
    "transpile to DELETE" in {
      ir.DeleteFromTable(
        target = namedTable("t"),
        where = Some(ir.Equals(ir.Column(None, ir.Id("c")), ir.Literal(3)))) generates
        "DELETE FROM t WHERE c = 3"
    }
  }

  "Join" should {
    "transpile to JOIN" in {
      crossJoin(namedTable("t1"), namedTable("t2")) generates "t1 CROSS JOIN t2"

      ir.Join(
        namedTable("t1"),
        namedTable("t2"),
        None,
        ir.InnerJoin,
        Seq(),
        ir.JoinDataType(is_left_struct = false, is_right_struct = false)) generates "t1, t2"

      ir.Join(
        namedTable("t1"),
        namedTable("t2"),
        Some(ir.CallFunction("IS_DATE", Seq(ir.Id("c1")))),
        ir.InnerJoin,
        Seq(),
        ir.JoinDataType(is_left_struct = false, is_right_struct = false)) generates "t1 INNER JOIN t2 ON IS_DATE(c1)"

      ir.Join(
        namedTable("t1"),
        namedTable("t2"),
        Some(ir.CallFunction("IS_DATE", Seq(ir.Id("c1")))),
        ir.RightOuterJoin,
        Seq("c1", "c2"),
        ir.JoinDataType(
          is_left_struct = false,
          is_right_struct = false)) generates "t1 RIGHT JOIN t2 ON IS_DATE(c1) USING (c1, c2)"

      ir.Join(
        namedTable("t1"),
        namedTable("t2"),
        None,
        ir.NaturalJoin(ir.LeftOuterJoin),
        Seq(),
        ir.JoinDataType(is_left_struct = false, is_right_struct = false)) generates "t1 NATURAL LEFT JOIN t2"
    }
  }

  "SetOperation" should {
    "transpile to UNION" in {
      ir.SetOperation(
        namedTable("a"),
        namedTable("b"),
        ir.UnionSetOp,
        is_all = false,
        by_name = false,
        allow_missing_columns = false) generates "(a) UNION (b)"
      ir.SetOperation(
        namedTable("a"),
        namedTable("b"),
        ir.UnionSetOp,
        is_all = true,
        by_name = false,
        allow_missing_columns = false) generates "(a) UNION ALL (b)"
      ir.SetOperation(
        namedTable("a"),
        namedTable("b"),
        ir.UnionSetOp,
        is_all = true,
        by_name = true,
        allow_missing_columns = false)
        .doesNotTranspile
    }

    "transpile to INTERSECT" in {
      ir.SetOperation(
        namedTable("a"),
        namedTable("b"),
        ir.IntersectSetOp,
        is_all = false,
        by_name = false,
        allow_missing_columns = false) generates "(a) INTERSECT (b)"
      ir.SetOperation(
        namedTable("a"),
        namedTable("b"),
        ir.IntersectSetOp,
        is_all = true,
        by_name = false,
        allow_missing_columns = false) generates "(a) INTERSECT ALL (b)"
    }

    "transpile to EXCEPT" in {
      ir.SetOperation(
        namedTable("a"),
        namedTable("b"),
        ir.ExceptSetOp,
        is_all = false,
        by_name = false,
        allow_missing_columns = false) generates "(a) EXCEPT (b)"
      ir.SetOperation(
        namedTable("a"),
        namedTable("b"),
        ir.ExceptSetOp,
        is_all = true,
        by_name = false,
        allow_missing_columns = false) generates "(a) EXCEPT ALL (b)"
    }

    "unspecified" in {
      ir.SetOperation(
        namedTable("a"),
        namedTable("b"),
        ir.UnspecifiedSetOp,
        is_all = true,
        by_name = true,
        allow_missing_columns = false)
        .doesNotTranspile
    }
  }

  "transpile to LIMIT" in {
    ir.Limit(namedTable("a"), ir.Literal(10)) generates "a LIMIT 10"
  }

  "transpile to OFFSET" in {
    ir.Offset(namedTable("a"), ir.Literal(10)) generates "a OFFSET 10"
  }

  "transpile to ORDER BY" in {
    ir.Sort(
      namedTable("a"),
      Seq(ir.SortOrder(ir.Id("c1"), ir.Ascending, ir.NullsFirst))) generates "a ORDER BY c1 NULLS FIRST"
  }

  "transpile to VALUES" in {
    ir.Values(Seq(Seq(ir.Literal(1), ir.Literal(2)), Seq(ir.Literal(3), ir.Literal(4)))) generates "VALUES (1,2), (3,4)"
  }

  "Aggregate" should {
    "transpile to GROUP BY" in {
      ir.Aggregate(namedTable("t1"), ir.GroupBy, Seq(ir.Id("c1")), None) generates "t1 GROUP BY c1"
    }

    "transpile to PIVOT" in {
      ir.Aggregate(
        namedTable("t1"),
        ir.Pivot,
        Seq(ir.Id("c1")),
        Some(ir.Pivot(ir.Id("c2"), Seq(ir.Literal(1), ir.Literal(2))))) generates
        "t1 PIVOT(c1 FOR c2 IN(1, 2))"
    }

    "transpile to SELECT DISTINCT" in {
      ir.Deduplicate(
        namedTable("t1"),
        Seq(ir.Id("c1"), ir.Id("c2")),
        all_columns_as_keys = false,
        within_watermark = false) generates "SELECT DISTINCT c1, c2 FROM t1"

      ir.Deduplicate(
        namedTable("t1"),
        Seq(),
        all_columns_as_keys = true,
        within_watermark = false) generates "SELECT DISTINCT * FROM t1"
    }

  }

  "transpile to AS" in {
    ir.TableAlias(
      namedTable("table1"),
      "t1",
      Seq(ir.Id("c1"), ir.Id("c2"), ir.Id("c3"))) generates "table1 AS t1(c1, c2, c3)"
  }

  "CreateTableCommand" should {
    "transpile to CREATE TABLE" in {
      ir.CreateTableCommand(
        "t1",
        Seq(
          ir.ColumnDeclaration(
            "c1",
            ir.IntegerType,
            constraints = Seq(ir.Nullability(nullable = false), ir.PrimaryKey())),
          ir.ColumnDeclaration(
            "c2",
            ir.StringType))) generates "CREATE TABLE t1 (c1 INT NOT NULL PRIMARY KEY, c2 STRING )"
    }
  }

  "TableSample" should {
    "transpile to TABLESAMPLE" in {
      ir.TableSample(
        namedTable("t1"),
        ir.RowSamplingFixedAmount(BigDecimal(10)),
        Some(BigDecimal(10))) generates "(t1) TABLESAMPLE (10 ROWS) REPEATABLE (10)"
    }
  }

  "CreateTableParameters" should {
    "transpile to CREATE TABLE" in {
      ir.CreateTableParams(
        ir.CreateTable(
          "some_table",
          None,
          None,
          None,
          ir.StructType(Seq(ir.StructField("a", ir.IntegerType), ir.StructField("b", ir.VarcharType(Some(10)))))),
        Map("a" -> Seq.empty, "b" -> Seq.empty),
        Map("a" -> Seq.empty, "b" -> Seq.empty),
        Seq.empty,
        Seq.empty,
        None,
        Some(Seq.empty)) generates "CREATE TABLE some_table (a INT, b VARCHAR(10))"
    }

    "transpile to CREATE TABLE with commented options" in {
      ir.CreateTableParams(
        ir.CreateTable(
          "some_table",
          None,
          None,
          None,
          ir.StructType(Seq(ir.StructField("a", ir.IntegerType), ir.StructField("b", ir.VarcharType(Some(10)))))),
        Map("a" -> Seq.empty, "b" -> Seq.empty),
        Map("a" -> Seq(ir.OptionUnresolved("Unsupported Option: SPARSE")), "b" -> Seq.empty),
        Seq(
          ir.NamedConstraint(
            "c1",
            ir.CheckConstraint(ir.GreaterThan(ir.Column(None, ir.Id("a")), ir.Literal(0, ir.IntegerType))))),
        Seq.empty,
        None,
        Some(Seq.empty)) generates
        "CREATE TABLE some_table (a INT /* Unsupported Option: SPARSE */, b VARCHAR(10), CONSTRAINT c1 CHECK (a > 0))"
    }

    "transpile to CREATE TABLE with default values" in {
      ir.CreateTableParams(
        ir.CreateTable(
          "some_table",
          None,
          None,
          None,
          ir.StructType(Seq(ir.StructField("a", ir.IntegerType), ir.StructField("b", ir.VarcharType(Some(10)))))),
        Map(
          "a" -> Seq(ir.DefaultValueConstraint(ir.Literal(0, ir.IntegerType))),
          "b" -> Seq(ir.DefaultValueConstraint(ir.Literal("foo", ir.StringType)))),
        Map("a" -> Seq.empty, "b" -> Seq.empty),
        Seq.empty,
        Seq.empty,
        None,
        Some(Seq.empty)) generates
        "CREATE TABLE some_table (a INT DEFAULT 0, b VARCHAR(10) DEFAULT 'foo')"
    }

    "transpile to CREATE TABLE with foreign key table constraint" in {
      ir.CreateTableParams(
        ir.CreateTable(
          "some_table",
          None,
          None,
          None,
          ir.StructType(Seq(ir.StructField("a", ir.IntegerType), ir.StructField("b", ir.VarcharType(Some(10)))))),
        Map("a" -> Seq.empty, "b" -> Seq.empty),
        Map("a" -> Seq.empty, "b" -> Seq.empty),
        Seq(ir.NamedConstraint("c1", ir.ForeignKey("a, b", "other_table", "c, d", Seq.empty))),
        Seq.empty,
        None,
        Some(Seq.empty)) generates
        "CREATE TABLE some_table (a INT, b VARCHAR(10), CONSTRAINT c1 FOREIGN KEY (a, b) REFERENCES other_table(c, d))"
    }

    "transpile to CREATE TABLE with a primary key, foreign key and a Unique column" in {
      ir.CreateTableParams(
        ir.CreateTable(
          "some_table",
          None,
          None,
          None,
          ir.StructType(Seq(ir.StructField("a", ir.IntegerType), ir.StructField("b", ir.VarcharType(Some(10)))))),
        Map("a" -> Seq(ir.PrimaryKey()), "b" -> Seq(ir.Unique())),
        Map("a" -> Seq.empty, "b" -> Seq.empty),
        Seq(ir.ForeignKey("b", "other_table", "b", Seq.empty)),
        Seq.empty,
        None,
        Some(Seq.empty)) generates
        "CREATE TABLE some_table (a INT PRIMARY KEY, b VARCHAR(10) UNIQUE, FOREIGN KEY (b) REFERENCES other_table(b))"
    }

    "transpile to CREATE TABLE with various complex column constraints" in {
      ir.CreateTableParams(
        ir.CreateTable(
          "example_table",
          None,
          None,
          None,
          ir.StructType(Seq(
            ir.StructField("id", ir.IntegerType),
            ir.StructField("name", ir.VarcharType(Some(50)), nullable = false),
            ir.StructField("age", ir.IntegerType),
            ir.StructField("email", ir.VarcharType(Some(100))),
            ir.StructField("department_id", ir.IntegerType)))),
        Map(
          "name" -> Seq.empty,
          "email" -> Seq(ir.Unique()),
          "department_id" -> Seq.empty,
          "age" -> Seq.empty,
          "id" -> Seq(ir.PrimaryKey())),
        Map(
          "name" -> Seq.empty,
          "email" -> Seq.empty,
          "department_id" -> Seq.empty,
          "age" -> Seq.empty,
          "id" -> Seq.empty),
        Seq(
          ir.CheckConstraint(ir.GreaterThanOrEqual(ir.Column(None, ir.Id("age")), ir.Literal(18, ir.IntegerType))),
          ir.ForeignKey("department_id", "departments", "id", Seq.empty)),
        Seq.empty,
        None,
        Some(Seq.empty)) generates
        "CREATE TABLE example_table (id INT PRIMARY KEY, name VARCHAR(50) NOT NULL, age INT," +
        " email VARCHAR(100) UNIQUE, department_id INT, CHECK (age >= 18)," +
        " FOREIGN KEY (department_id) REFERENCES departments(id))"
    }
    "transpile to CREATE TABLE with a named NULL constraint" in {
      ir.CreateTableParams(
        ir.CreateTable(
          "example_table",
          None,
          None,
          None,
          ir.StructType(Seq(ir.StructField("id", ir.VarcharType(Some(10)))))),
        Map("id" -> Seq.empty),
        Map("id" -> Seq.empty),
        Seq(ir.NamedConstraint("c1", ir.CheckConstraint(ir.IsNotNull(ir.Column(None, ir.Id("id")))))),
        Seq.empty,
        None,
        Some(Seq.empty)) generates "CREATE TABLE example_table (id VARCHAR(10), CONSTRAINT c1 CHECK (id IS NOT NULL))"
    }

    "transpile unsupported table level options to comments" in {
      ir.CreateTableParams(
        ir.CreateTable("example_table", None, None, None, ir.StructType(Seq(ir.StructField("id", ir.IntegerType)))),
        Map("id" -> Seq.empty),
        Map("id" -> Seq.empty),
        Seq.empty,
        Seq.empty,
        None,
        Some(Seq(ir.OptionUnresolved("LEDGER=ON")))) generates
        """/*
          |   The following options are unsupported:
          |
          |   LEDGER=ON
          |*/
          |CREATE TABLE example_table (id INT)""".stripMargin
    }
  }
}
