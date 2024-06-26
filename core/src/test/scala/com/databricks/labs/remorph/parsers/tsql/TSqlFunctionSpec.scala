package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{IRHelpers, intermediate => ir}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlFunctionSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers with IRHelpers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = new TSqlExpressionBuilder

  "translate functions with no parameters" in {
    example("APP_NAME()", _.expression(), ir.CallFunction("APP_NAME", List()))
    example("SCOPE_IDENTITY()", _.expression(), ir.CallFunction("SCOPE_IDENTITY", List()))
  }

  "translate functions with variable numbers of parameters" in {
    example(
      "CONCAT('a', 'b', 'c')",
      _.expression(),
      ir.CallFunction(
        "CONCAT",
        Seq(ir.Literal(string = Some("a")), ir.Literal(string = Some("b")), ir.Literal(string = Some("c")))))

    example(
      "CONCAT_WS(',', 'a', 'b', 'c')",
      _.expression(),
      ir.CallFunction(
        "CONCAT_WS",
        List(
          ir.Literal(string = Some(",")),
          ir.Literal(string = Some("a")),
          ir.Literal(string = Some("b")),
          ir.Literal(string = Some("c")))))
  }

  "translate functions with functions as parameters" in {
    example(
      "CONCAT(Greatest(42, 2, 4, \"ali\"), 'c')",
      _.expression(),
      ir.CallFunction(
        "CONCAT",
        List(
          ir.CallFunction(
            "Greatest",
            List(
              ir.Literal(integer = Some(42)),
              ir.Literal(integer = Some(2)),
              ir.Literal(integer = Some(4)),
              ir.Column(None, ir.Id("ali", caseSensitive = true)))),
          ir.Literal(string = Some("c")))))
  }

  "translate functions with complicated expressions as parameters" in {
    example(
      "CONCAT('a', 'b' || 'c', Greatest(42, 2, 4, \"ali\"))",
      _.standardFunction(),
      ir.CallFunction(
        "CONCAT",
        List(
          ir.Literal(string = Some("a")),
          ir.Concat(ir.Literal(string = Some("b")), ir.Literal(string = Some("c"))),
          ir.CallFunction(
            "Greatest",
            List(
              ir.Literal(integer = Some(42)),
              ir.Literal(integer = Some(2)),
              ir.Literal(integer = Some(4)),
              ir.Column(None, ir.Id("ali", caseSensitive = true)))))))
  }

  "translate unknown functions as unresolved" in {
    example(
      "UNKNOWN_FUNCTION()",
      _.expression(),
      ir.UnresolvedFunction("UNKNOWN_FUNCTION", List(), is_distinct = false, is_user_defined_function = false))
  }

  "translate functions with invalid function argument counts" in {
    // Later, we will register a semantic or lint error
    example(
      "USER_NAME('a', 'b', 'c', 'd')", // USER_NAME function only accepts 0 or 1 argument
      _.expression(),
      ir.UnresolvedFunction(
        "USER_NAME",
        Seq(
          ir.Literal(string = Some("a")),
          ir.Literal(string = Some("b")),
          ir.Literal(string = Some("c")),
          ir.Literal(string = Some("d"))),
        is_distinct = false,
        is_user_defined_function = false,
        has_incorrect_argc = true))

    example(
      "FLOOR()", // FLOOR requires 1 argument
      _.expression(),
      ir.UnresolvedFunction(
        "FLOOR",
        List(),
        is_distinct = false,
        is_user_defined_function = false,
        has_incorrect_argc = true))
  }

  "translate functions that we know cannot be converted" in {
    // Later, we will register a semantic or lint error
    example(
      "CONNECTIONPROPERTY('property')",
      _.expression(),
      ir.UnresolvedFunction(
        "CONNECTIONPROPERTY",
        List(ir.Literal(string = Some("property"))),
        is_distinct = false,
        is_user_defined_function = false))
  }

  "translate windowing functions in all forms" in {
    example(
      """SUM(salary) OVER (PARTITION BY department ORDER BY employee_id
         RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)""",
      _.expression(),
      ir.Window(
        ir.CallFunction("SUM", Seq(simplyNamedColumn("salary"))),
        Seq(simplyNamedColumn("department")),
        Seq(ir.SortOrder(simplyNamedColumn("employee_id"), ir.AscendingSortDirection, ir.SortNullsUnspecified)),
        Some(ir.WindowFrame(ir.RangeFrame, ir.UnboundedPreceding, ir.CurrentRow))))
    example(
      "SUM(salary) OVER (PARTITION BY department ORDER BY employee_id ROWS UNBOUNDED PRECEDING)",
      _.expression(),
      ir.Window(
        ir.CallFunction("SUM", Seq(simplyNamedColumn("salary"))),
        Seq(simplyNamedColumn("department")),
        Seq(ir.SortOrder(simplyNamedColumn("employee_id"), ir.AscendingSortDirection, ir.SortNullsUnspecified)),
        Some(ir.WindowFrame(ir.RowsFrame, ir.UnboundedPreceding, ir.NoBoundary))))

    example(
      "SUM(salary) OVER (PARTITION BY department ORDER BY employee_id ROWS 66 PRECEDING)",
      _.expression(),
      ir.Window(
        ir.CallFunction("SUM", Seq(simplyNamedColumn("salary"))),
        Seq(simplyNamedColumn("department")),
        Seq(ir.SortOrder(simplyNamedColumn("employee_id"), ir.AscendingSortDirection, ir.SortNullsUnspecified)),
        Some(ir.WindowFrame(ir.RowsFrame, ir.PrecedingN(ir.Literal(integer = Some(66))), ir.NoBoundary))))

    example(
      query = """
      AVG(salary) OVER (PARTITION BY department_id ORDER BY employee_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
    """,
      _.expression(),
      ir.Window(
        ir.CallFunction("AVG", Seq(simplyNamedColumn("salary"))),
        Seq(simplyNamedColumn("department_id")),
        Seq(ir.SortOrder(simplyNamedColumn("employee_id"), ir.AscendingSortDirection, ir.SortNullsUnspecified)),
        Some(ir.WindowFrame(ir.RowsFrame, ir.UnboundedPreceding, ir.CurrentRow))))

    example(
      query = """
      SUM(sales) OVER (ORDER BY month ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING)
    """,
      _.expression(),
      ir.Window(
        ir.CallFunction("SUM", Seq(simplyNamedColumn("sales"))),
        List(),
        Seq(ir.SortOrder(simplyNamedColumn("month"), ir.AscendingSortDirection, ir.SortNullsUnspecified)),
        Some(ir.WindowFrame(ir.RowsFrame, ir.CurrentRow, ir.FollowingN(ir.Literal(integer = Some(2)))))))

    example(
      "ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC)",
      _.selectListElem(),
      ir.Window(
        ir.CallFunction("ROW_NUMBER", Seq.empty),
        Seq(simplyNamedColumn("department")),
        Seq(ir.SortOrder(simplyNamedColumn("salary"), ir.DescendingSortDirection, ir.SortNullsUnspecified)),
        None))

    example(
      "ROW_NUMBER() OVER (PARTITION BY department)",
      _.selectListElem(),
      ir.Window(ir.CallFunction("ROW_NUMBER", Seq.empty), Seq(simplyNamedColumn("department")), List(), None))

  }

  "translate functions with DISTINCT arguments" in {
    example(
      "COUNT(DISTINCT salary)",
      _.expression(),
      ir.CallFunction("COUNT", Seq(ir.Distinct(simplyNamedColumn("salary")))))
  }

  "translate special keyword functions" in {
    example(
      // TODO: Returns UnresolvedFunction as it is not convertible - create UnsupportedFunction
      "@@CURSOR_ROWS",
      _.expression(),
      ir.UnresolvedFunction("@@CURSOR_ROWS", List(), is_distinct = false, is_user_defined_function = false))

    example(
      // TODO: Returns UnresolvedFunction as it is not convertible - create UnsupportedFunction
      "@@FETCH_STATUS",
      _.expression(),
      ir.UnresolvedFunction("@@FETCH_STATUS", List(), is_distinct = false, is_user_defined_function = false))

    example("SESSION_USER", _.expression(), ir.CallFunction("SESSION_USER", List()))

    example("USER", _.expression(), ir.CallFunction("USER", List()))
  }

  "translate analytic windowing functions in all forms" in {

    example(
      query = "FIRST_VALUE(Salary) OVER (PARTITION BY DepartmentID ORDER BY Salary DESC)",
      _.expression(),
      ir.Window(
        ir.CallFunction("FIRST_VALUE", Seq(simplyNamedColumn("Salary"))),
        Seq(simplyNamedColumn("DepartmentID")),
        Seq(ir.SortOrder(simplyNamedColumn("Salary"), ir.DescendingSortDirection, ir.SortNullsUnspecified)),
        None))

    example(
      query = """
        LAST_VALUE(salary) OVER (PARTITION BY department_id ORDER BY employee_id DESC)
    """,
      _.expression(),
      ir.Window(
        ir.CallFunction("LAST_VALUE", Seq(simplyNamedColumn("salary"))),
        Seq(simplyNamedColumn("department_id")),
        Seq(ir.SortOrder(simplyNamedColumn("employee_id"), ir.DescendingSortDirection, ir.SortNullsUnspecified)),
        None))

    example(
      query = "PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY Salary) OVER (PARTITION BY DepartmentID)",
      _.expression(),
      ir.Window(
        ir.WithinGroup(
          ir.CallFunction("PERCENTILE_CONT", Seq(ir.Literal(float = Some(0.5f)))),
          Seq(ir.SortOrder(simplyNamedColumn("Salary"), ir.AscendingSortDirection, ir.SortNullsUnspecified))),
        Seq(simplyNamedColumn("DepartmentID")),
        List(),
        None))

    example(
      query = """
    LEAD(salary, 1) OVER (PARTITION BY department_id ORDER BY employee_id DESC)
  """,
      _.expression(),
      ir.Window(
        ir.CallFunction("LEAD", Seq(simplyNamedColumn("salary"), ir.Literal(integer = Some(1)))),
        Seq(simplyNamedColumn("department_id")),
        Seq(ir.SortOrder(simplyNamedColumn("employee_id"), ir.DescendingSortDirection, ir.SortNullsUnspecified)),
        None))
  }

  "translate 'functions' with non-standard syntax" in {
    example(
      query = "NEXT VALUE FOR mySequence",
      _.expression(),
      ir.CallFunction("MONOTONICALLY_INCREASING_ID", List.empty))
  }

  "translate JSON_ARRAY in various forms" in {
    example(
      query = "JSON_ARRAY(1, 2, 3 ABSENT ON NULL)",
      _.expression(),
      ir.CallFunction(
        "TO_JSON",
        Seq(
          ir.ValueArray(Seq(ir.FilterExpr(
            Seq(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2)), ir.Literal(integer = Some(3))),
            ir.LambdaFunction(
              ir.Not(ir.IsNull(ir.UnresolvedNamedLambdaVariable(Seq("x")))),
              Seq(ir.UnresolvedNamedLambdaVariable(Seq("x"))))))))))

    example(
      query = "JSON_ARRAY(4, 5, 6)",
      _.expression(),
      ir.CallFunction(
        "TO_JSON",
        Seq(
          ir.ValueArray(Seq(ir.FilterExpr(
            Seq(ir.Literal(integer = Some(4)), ir.Literal(integer = Some(5)), ir.Literal(integer = Some(6))),
            ir.LambdaFunction(
              ir.Not(ir.IsNull(ir.UnresolvedNamedLambdaVariable(Seq("x")))),
              Seq(ir.UnresolvedNamedLambdaVariable(Seq("x"))))))))))

    example(
      query = "JSON_ARRAY(1, 2, 3 NULL ON NULL)",
      _.expression(),
      ir.CallFunction(
        "TO_JSON",
        Seq(
          ir.ValueArray(
            Seq(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2)), ir.Literal(integer = Some(3)))))))

    example(
      query = "JSON_ARRAY(1, col1, x.col2 NULL ON NULL)",
      _.expression(),
      ir.CallFunction(
        "TO_JSON",
        Seq(
          ir.ValueArray(
            Seq(
              ir.Literal(integer = Some(1)),
              simplyNamedColumn("col1"),
              ir.Column(Some(ir.ObjectReference(ir.Id("x"))), ir.Id("col2")))))))
  }

  "translate JSON_OBJECT in various forms" in {
    example(
      query = "JSON_OBJECT('one': 1, 'two': 2, 'three': 3 ABSENT ON NULL)",
      _.expression(),
      ir.CallFunction(
        "TO_JSON",
        Seq(
          ir.FilterStruct(
            ir.NamedStruct(
              keys = Seq(
                ir.Literal(string = Some("one")),
                ir.Literal(string = Some("two")),
                ir.Literal(string = Some("three"))),
              values =
                Seq(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2)), ir.Literal(integer = Some(3)))),
            ir.LambdaFunction(
              ir.Not(ir.IsNull(ir.UnresolvedNamedLambdaVariable(Seq("v")))),
              Seq(ir.UnresolvedNamedLambdaVariable(Seq("k", "v"))))))))

    example(
      query = "JSON_OBJECT('a': a, 'b': b, 'c': c NULL ON NULL)",
      _.expression(),
      ir.CallFunction(
        "TO_JSON",
        Seq(
          ir.NamedStruct(
            Seq(ir.Literal(string = Some("a")), ir.Literal(string = Some("b")), ir.Literal(string = Some("c"))),
            Seq(simplyNamedColumn("a"), simplyNamedColumn("b"), simplyNamedColumn("c"))))))
  }

  "translate functions using ALL" in {
    example(query = "COUNT(ALL goals)", _.expression(), ir.CallFunction("COUNT", Seq(simplyNamedColumn("goals"))))
  }

  "translate freetext functions as inconvertible" in {
    example(
      query = "FREETEXTTABLE(table, col, 'search')",
      _.expression(),
      ir.UnresolvedFunction("FREETEXTTABLE", List.empty, is_distinct = false, is_user_defined_function = false))
  }

  "translate $PARTITION functions as inconvertible" in {
    example(
      query = "$PARTITION.partitionFunction(col)",
      _.expression(),
      ir.UnresolvedFunction("$PARTITION", List.empty, is_distinct = false, is_user_defined_function = false))
  }

  "translate HIERARCHYID static method as inconvertible" in {
    example(
      query = "HIERARCHYID::Parse('1/2/3')",
      _.expression(),
      ir.UnresolvedFunction("HIERARCHYID", List.empty, is_distinct = false, is_user_defined_function = false))
  }
}
