package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.{intermediate => ir}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlFunctionSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers with ir.IRHelpers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = vc.expressionBuilder

  "translate functions with no parameters" in {
    exampleExpr("APP_NAME()", _.expression(), ir.CallFunction("APP_NAME", List()))
    exampleExpr("SCOPE_IDENTITY()", _.expression(), ir.CallFunction("SCOPE_IDENTITY", List()))
  }

  "translate functions with variable numbers of parameters" in {
    exampleExpr(
      "CONCAT('a', 'b', 'c')",
      _.expression(),
      ir.CallFunction("CONCAT", Seq(ir.Literal("a"), ir.Literal("b"), ir.Literal("c"))))

    exampleExpr(
      "CONCAT_WS(',', 'a', 'b', 'c')",
      _.expression(),
      ir.CallFunction("CONCAT_WS", List(ir.Literal(","), ir.Literal("a"), ir.Literal("b"), ir.Literal("c"))))
  }

  "translate functions with functions as parameters" in {
    exampleExpr(
      "CONCAT(Greatest(42, 2, 4, \"ali\"), 'c')",
      _.expression(),
      ir.CallFunction(
        "CONCAT",
        List(
          ir.CallFunction(
            "Greatest",
            List(ir.Literal(42), ir.Literal(2), ir.Literal(4), ir.Column(None, ir.Id("ali", caseSensitive = true)))),
          ir.Literal("c"))))
  }

  "translate functions with complicated expressions as parameters" in {
    exampleExpr(
      "CONCAT('a', 'b' || 'c', Greatest(42, 2, 4, \"ali\"))",
      _.standardFunction(),
      ir.CallFunction(
        "CONCAT",
        List(
          ir.Literal("a"),
          ir.Concat(Seq(ir.Literal("b"), ir.Literal("c"))),
          ir.CallFunction(
            "Greatest",
            List(ir.Literal(42), ir.Literal(2), ir.Literal(4), ir.Column(None, ir.Id("ali", caseSensitive = true)))))))
  }

  "translate unknown functions as unresolved" in {
    exampleExpr(
      "UNKNOWN_FUNCTION()",
      _.expression(),
      ir.UnresolvedFunction(
        "UNKNOWN_FUNCTION",
        List(),
        is_distinct = false,
        is_user_defined_function = false,
        ruleText = "UNKNOWN_FUNCTION(...)",
        ruleName = "N/A",
        tokenName = Some("N/A"),
        message = "Function UNKNOWN_FUNCTION is not convertible to Databricks SQL"))
  }

  "translate functions with invalid function argument counts" in {
    exampleExpr(
      "USER_NAME('a', 'b', 'c', 'd')", // USER_NAME function only accepts 0 or 1 argument
      _.expression(),
      ir.UnresolvedFunction(
        "USER_NAME",
        Seq(ir.Literal("a"), ir.Literal("b"), ir.Literal("c"), ir.Literal("d")),
        is_distinct = false,
        is_user_defined_function = false,
        has_incorrect_argc = true,
        ruleText = "USER_NAME(...)",
        ruleName = "N/A",
        tokenName = Some("N/A"),
        message = "Invocation of USER_NAME has incorrect argument count"))

    exampleExpr(
      "FLOOR()", // FLOOR requires 1 argument
      _.expression(),
      ir.UnresolvedFunction(
        "FLOOR",
        List(),
        is_distinct = false,
        is_user_defined_function = false,
        has_incorrect_argc = true,
        ruleText = "FLOOR(...)",
        ruleName = "N/A",
        tokenName = Some("N/A"),
        message = "Invocation of FLOOR has incorrect argument count"))
  }

  "translate functions that we know cannot be converted" in {
    // Later, we will register a semantic or lint error
    exampleExpr(
      "CONNECTIONPROPERTY('property')",
      _.expression(),
      ir.UnresolvedFunction(
        "CONNECTIONPROPERTY",
        List(ir.Literal("property")),
        is_distinct = false,
        is_user_defined_function = false,
        ruleText = "CONNECTIONPROPERTY(...)",
        ruleName = "N/A",
        tokenName = Some("N/A"),
        message = "Function CONNECTIONPROPERTY is not convertible to Databricks SQL"))
  }

  "translate windowing functions in all forms" in {
    exampleExpr(
      """SUM(salary) OVER (PARTITION BY department ORDER BY employee_id
         RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)""",
      _.expression(),
      ir.Window(
        ir.CallFunction("SUM", Seq(simplyNamedColumn("salary"))),
        Seq(simplyNamedColumn("department")),
        Seq(ir.SortOrder(simplyNamedColumn("employee_id"), ir.UnspecifiedSortDirection, ir.SortNullsUnspecified)),
        Some(ir.WindowFrame(ir.RangeFrame, ir.UnboundedPreceding, ir.CurrentRow))))
    exampleExpr(
      "SUM(salary) OVER (PARTITION BY department ORDER BY employee_id ROWS UNBOUNDED PRECEDING)",
      _.expression(),
      ir.Window(
        ir.CallFunction("SUM", Seq(simplyNamedColumn("salary"))),
        Seq(simplyNamedColumn("department")),
        Seq(ir.SortOrder(simplyNamedColumn("employee_id"), ir.UnspecifiedSortDirection, ir.SortNullsUnspecified)),
        Some(ir.WindowFrame(ir.RowsFrame, ir.UnboundedPreceding, ir.NoBoundary))))

    exampleExpr(
      "SUM(salary) OVER (PARTITION BY department ORDER BY employee_id ROWS 66 PRECEDING)",
      _.expression(),
      ir.Window(
        ir.CallFunction("SUM", Seq(simplyNamedColumn("salary"))),
        Seq(simplyNamedColumn("department")),
        Seq(ir.SortOrder(simplyNamedColumn("employee_id"), ir.UnspecifiedSortDirection, ir.SortNullsUnspecified)),
        Some(ir.WindowFrame(ir.RowsFrame, ir.PrecedingN(ir.Literal(66)), ir.NoBoundary))))

    exampleExpr(
      query = """
      AVG(salary) OVER (PARTITION BY department_id ORDER BY employee_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
    """,
      _.expression(),
      ir.Window(
        ir.CallFunction("AVG", Seq(simplyNamedColumn("salary"))),
        Seq(simplyNamedColumn("department_id")),
        Seq(ir.SortOrder(simplyNamedColumn("employee_id"), ir.UnspecifiedSortDirection, ir.SortNullsUnspecified)),
        Some(ir.WindowFrame(ir.RowsFrame, ir.UnboundedPreceding, ir.CurrentRow))))

    exampleExpr(
      query = """
      SUM(sales) OVER (ORDER BY month ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING)
    """,
      _.expression(),
      ir.Window(
        ir.CallFunction("SUM", Seq(simplyNamedColumn("sales"))),
        List(),
        Seq(ir.SortOrder(simplyNamedColumn("month"), ir.UnspecifiedSortDirection, ir.SortNullsUnspecified)),
        Some(ir.WindowFrame(ir.RowsFrame, ir.CurrentRow, ir.FollowingN(ir.Literal(2))))))

    exampleExpr(
      "ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC)",
      _.selectListElem(),
      ir.Window(
        ir.CallFunction("ROW_NUMBER", Seq.empty),
        Seq(simplyNamedColumn("department")),
        Seq(ir.SortOrder(simplyNamedColumn("salary"), ir.Descending, ir.SortNullsUnspecified)),
        None))

    exampleExpr(
      "ROW_NUMBER() OVER (PARTITION BY department)",
      _.selectListElem(),
      ir.Window(ir.CallFunction("ROW_NUMBER", Seq.empty), Seq(simplyNamedColumn("department")), List(), None))

  }

  "translate functions with DISTINCT arguments" in {
    exampleExpr(
      "COUNT(DISTINCT salary)",
      _.expression(),
      ir.CallFunction("COUNT", Seq(ir.Distinct(simplyNamedColumn("salary")))))
  }

  "translate COUNT(*)" in {
    exampleExpr("COUNT(*)", _.expression(), ir.CallFunction("COUNT", Seq(ir.Star(None))))
  }

  "translate special keyword functions" in {
    exampleExpr(
      // TODO: Returns UnresolvedFunction as it is not convertible - create UnsupportedFunctionRule
      "@@CURSOR_ROWS",
      _.expression(),
      ir.UnresolvedFunction(
        "@@CURSOR_ROWS",
        List(),
        is_distinct = false,
        is_user_defined_function = false,
        ruleText = "@@CURSOR_ROWS(...)",
        ruleName = "N/A",
        tokenName = Some("N/A"),
        message = "Function @@CURSOR_ROWS is not convertible to Databricks SQL"))

    exampleExpr(
      // TODO: Returns UnresolvedFunction as it is not convertible - create UnsupportedFunctionRule
      "@@FETCH_STATUS",
      _.expression(),
      ir.UnresolvedFunction(
        "@@FETCH_STATUS",
        List(),
        is_distinct = false,
        is_user_defined_function = false,
        ruleText = "@@FETCH_STATUS(...)",
        ruleName = "N/A",
        tokenName = Some("N/A"),
        message = "Function @@FETCH_STATUS is not convertible to Databricks SQL"))

    exampleExpr("SESSION_USER", _.expression(), ir.CallFunction("SESSION_USER", List()))

    exampleExpr("USER", _.expression(), ir.CallFunction("USER", List()))
  }

  "translate analytic windowing functions in all forms" in {

    exampleExpr(
      query = "FIRST_VALUE(Salary) OVER (PARTITION BY DepartmentID ORDER BY Salary DESC)",
      _.expression(),
      ir.Window(
        ir.CallFunction("FIRST_VALUE", Seq(simplyNamedColumn("Salary"))),
        Seq(simplyNamedColumn("DepartmentID")),
        Seq(ir.SortOrder(simplyNamedColumn("Salary"), ir.Descending, ir.SortNullsUnspecified)),
        None))

    exampleExpr(
      query = """
        LAST_VALUE(salary) OVER (PARTITION BY department_id ORDER BY employee_id DESC)
    """,
      _.expression(),
      ir.Window(
        ir.CallFunction("LAST_VALUE", Seq(simplyNamedColumn("salary"))),
        Seq(simplyNamedColumn("department_id")),
        Seq(ir.SortOrder(simplyNamedColumn("employee_id"), ir.Descending, ir.SortNullsUnspecified)),
        None))

    exampleExpr(
      query = "PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY Salary ASC) OVER (PARTITION BY DepartmentID)",
      _.expression(),
      ir.Window(
        ir.WithinGroup(
          ir.CallFunction("PERCENTILE_CONT", Seq(ir.Literal(0.5f))),
          Seq(ir.SortOrder(simplyNamedColumn("Salary"), ir.Ascending, ir.SortNullsUnspecified))),
        Seq(simplyNamedColumn("DepartmentID")),
        List(),
        None))

    exampleExpr(
      query = """
    LEAD(salary, 1) OVER (PARTITION BY department_id ORDER BY employee_id DESC)
  """,
      _.expression(),
      ir.Window(
        ir.CallFunction("LEAD", Seq(simplyNamedColumn("salary"), ir.Literal(1))),
        Seq(simplyNamedColumn("department_id")),
        Seq(ir.SortOrder(simplyNamedColumn("employee_id"), ir.Descending, ir.SortNullsUnspecified)),
        None))

    exampleExpr(
      query = """
    LEAD(salary, 1) IGNORE NULLS OVER (PARTITION BY department_id ORDER BY employee_id DESC)
  """,
      _.expression(),
      ir.Window(
        ir.CallFunction("LEAD", Seq(simplyNamedColumn("salary"), ir.Literal(1))),
        Seq(simplyNamedColumn("department_id")),
        Seq(ir.SortOrder(simplyNamedColumn("employee_id"), ir.Descending, ir.SortNullsUnspecified)),
        None,
        ignore_nulls = true))

  }

  "translate 'functions' with non-standard syntax" in {
    exampleExpr(
      query = "NEXT VALUE FOR mySequence",
      _.expression(),
      ir.CallFunction("MONOTONICALLY_INCREASING_ID", List.empty))
  }

  "translate JSON_ARRAY in various forms" in {
    exampleExpr(
      query = "JSON_ARRAY(1, 2, 3 ABSENT ON NULL)",
      _.expression(),
      ir.CallFunction(
        "TO_JSON",
        Seq(
          ir.ValueArray(Seq(ir.FilterExpr(
            Seq(ir.Literal(1), ir.Literal(2), ir.Literal(3)),
            ir.LambdaFunction(
              ir.Not(ir.IsNull(ir.UnresolvedNamedLambdaVariable(Seq("x")))),
              Seq(ir.UnresolvedNamedLambdaVariable(Seq("x"))))))))))

    exampleExpr(
      query = "JSON_ARRAY(4, 5, 6)",
      _.expression(),
      ir.CallFunction(
        "TO_JSON",
        Seq(
          ir.ValueArray(Seq(ir.FilterExpr(
            Seq(ir.Literal(4), ir.Literal(5), ir.Literal(6)),
            ir.LambdaFunction(
              ir.Not(ir.IsNull(ir.UnresolvedNamedLambdaVariable(Seq("x")))),
              Seq(ir.UnresolvedNamedLambdaVariable(Seq("x"))))))))))

    exampleExpr(
      query = "JSON_ARRAY(1, 2, 3 NULL ON NULL)",
      _.expression(),
      ir.CallFunction("TO_JSON", Seq(ir.ValueArray(Seq(ir.Literal(1), ir.Literal(2), ir.Literal(3))))))

    exampleExpr(
      query = "JSON_ARRAY(1, col1, x.col2 NULL ON NULL)",
      _.expression(),
      ir.CallFunction(
        "TO_JSON",
        Seq(
          ir.ValueArray(
            Seq(
              ir.Literal(1),
              simplyNamedColumn("col1"),
              ir.Column(Some(ir.ObjectReference(ir.Id("x"))), ir.Id("col2")))))))
  }

  "translate JSON_OBJECT in various forms" in {
    exampleExpr(
      query = "JSON_OBJECT('one': 1, 'two': 2, 'three': 3 ABSENT ON NULL)",
      _.expression(),
      ir.CallFunction(
        "TO_JSON",
        Seq(
          ir.FilterStruct(
            ir.NamedStruct(
              keys = Seq(ir.Literal("one"), ir.Literal("two"), ir.Literal("three")),
              values = Seq(ir.Literal(1), ir.Literal(2), ir.Literal(3))),
            ir.LambdaFunction(
              ir.Not(ir.IsNull(ir.UnresolvedNamedLambdaVariable(Seq("v")))),
              Seq(ir.UnresolvedNamedLambdaVariable(Seq("k", "v"))))))))

    exampleExpr(
      query = "JSON_OBJECT('a': a, 'b': b, 'c': c NULL ON NULL)",
      _.expression(),
      ir.CallFunction(
        "TO_JSON",
        Seq(
          ir.NamedStruct(
            Seq(ir.Literal("a"), ir.Literal("b"), ir.Literal("c")),
            Seq(simplyNamedColumn("a"), simplyNamedColumn("b"), simplyNamedColumn("c"))))))
  }

  "translate functions using ALL" in {
    exampleExpr(query = "COUNT(ALL goals)", _.expression(), ir.CallFunction("COUNT", Seq(simplyNamedColumn("goals"))))
  }

  "translate freetext functions as inconvertible" in {
    exampleExpr(
      query = "FREETEXTTABLE(table, col, 'search')",
      _.expression(),
      ir.UnresolvedFunction(
        "FREETEXTTABLE",
        List.empty,
        is_distinct = false,
        is_user_defined_function = false,
        ruleText = "FREETEXTTABLE(...)",
        ruleName = "N/A",
        tokenName = Some("N/A"),
        message = "Function FREETEXTTABLE is not convertible to Databricks SQL"))
  }

  "translate $PARTITION functions as inconvertible" in {
    exampleExpr(
      query = "$PARTITION.partitionFunction(col)",
      _.expression(),
      ir.UnresolvedFunction(
        "$PARTITION",
        List.empty,
        is_distinct = false,
        is_user_defined_function = false,
        ruleText = "$PARTITION(...)",
        ruleName = "N/A",
        tokenName = Some("N/A"),
        message = "Function $PARTITION is not convertible to Databricks SQL"))
  }

  "translate HIERARCHYID static method as inconvertible" in {
    exampleExpr(
      query = "HIERARCHYID::Parse('1/2/3')",
      _.expression(),
      ir.UnresolvedFunction(
        "HIERARCHYID",
        List.empty,
        is_distinct = false,
        is_user_defined_function = false,
        ruleText = "HIERARCHYID(...)",
        ruleName = "N/A",
        tokenName = Some("N/A"),
        message = "Function HIERARCHYID is not convertible to Databricks SQL"))
  }
}
