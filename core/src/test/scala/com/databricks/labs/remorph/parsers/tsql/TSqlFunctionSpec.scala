package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlFunctionSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers {

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
              ir.Column("\"ali\""))),
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
              ir.Column("\"ali\""))))))
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
        ir.CallFunction("SUM", Seq(ir.Column("salary"))),
        Seq(ir.Column("department")),
        Seq(ir.SortOrder(ir.Column("employee_id"), ir.AscendingSortDirection, ir.SortNullsUnspecified)),
        ir.WindowFrame(
          ir.RangeFrame,
          ir.FrameBoundary(current_row = false, unbounded = true, ir.Noop),
          ir.FrameBoundary(current_row = true, unbounded = false, ir.Noop))))
    example(
      "SUM(salary) OVER (PARTITION BY department ORDER BY employee_id ROWS UNBOUNDED PRECEDING)",
      _.expression(),
      ir.Window(
        ir.CallFunction("SUM", Seq(ir.Column("salary"))),
        Seq(ir.Column("department")),
        Seq(ir.SortOrder(ir.Column("employee_id"), ir.AscendingSortDirection, ir.SortNullsUnspecified)),
        ir.WindowFrame(
          ir.RowsFrame,
          ir.FrameBoundary(current_row = false, unbounded = true, ir.Noop),
          ir.FrameBoundary(current_row = false, unbounded = false, ir.Noop))))

    example(
      "SUM(salary) OVER (PARTITION BY department ORDER BY employee_id ROWS 66 PRECEDING)",
      _.expression(),
      ir.Window(
        ir.CallFunction("SUM", Seq(ir.Column("salary"))),
        Seq(ir.Column("department")),
        Seq(ir.SortOrder(ir.Column("employee_id"), ir.AscendingSortDirection, ir.SortNullsUnspecified)),
        ir.WindowFrame(
          ir.RowsFrame,
          ir.FrameBoundary(current_row = false, unbounded = false, ir.Literal(integer = Some(66))),
          ir.FrameBoundary(current_row = false, unbounded = false, ir.Noop))))

    example(
      query = """
      AVG(salary) OVER (PARTITION BY department_id ORDER BY employee_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
    """,
      _.expression(),
      ir.Window(
        ir.CallFunction("AVG", Seq(ir.Column("salary"))),
        Seq(ir.Column("department_id")),
        Seq(ir.SortOrder(ir.Column("employee_id"), ir.AscendingSortDirection, ir.SortNullsUnspecified)),
        ir.WindowFrame(
          ir.RowsFrame,
          ir.FrameBoundary(current_row = false, unbounded = true, ir.Noop),
          ir.FrameBoundary(current_row = true, unbounded = false, ir.Noop))))

    example(
      query = """
      SUM(sales) OVER (ORDER BY month ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING)
    """,
      _.expression(),
      ir.Window(
        ir.CallFunction("SUM", Seq(ir.Column("sales"))),
        List(),
        Seq(ir.SortOrder(ir.Column("month"), ir.AscendingSortDirection, ir.SortNullsUnspecified)),
        ir.WindowFrame(
          ir.RowsFrame,
          ir.FrameBoundary(current_row = true, unbounded = false, ir.Noop),
          ir.FrameBoundary(current_row = false, unbounded = false, ir.Literal(integer = Some(2))))))

    example(
      "ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC)",
      _.selectListElem(),
      ir.Window(
        ir.CallFunction("ROW_NUMBER", Seq.empty),
        Seq(ir.Column("department")),
        Seq(ir.SortOrder(ir.Column("salary"), ir.DescendingSortDirection, ir.SortNullsUnspecified)),
        ir.WindowFrame(
          ir.UndefinedFrame,
          ir.FrameBoundary(current_row = false, unbounded = false, ir.Noop),
          ir.FrameBoundary(current_row = false, unbounded = false, ir.Noop))))

    example(
      "ROW_NUMBER() OVER (PARTITION BY department)",
      _.selectListElem(),
      ir.Window(
        ir.CallFunction("ROW_NUMBER", Seq.empty),
        Seq(ir.Column("department")),
        List(),
        ir.WindowFrame(
          ir.UndefinedFrame,
          ir.FrameBoundary(current_row = false, unbounded = false, ir.Noop),
          ir.FrameBoundary(current_row = false, unbounded = false, ir.Noop))))

  }

  // TODO: Analytic functions are next
  "translate analytic windowing functions in all forms" ignore {
    example(
      query = """
    LEAD(salary, 1) OVER (PARTITION BY department_id ORDER BY employee_id DESC)
  """,
      _.expression(),
      ir.Window(
        ir.CallFunction("LEAD", Seq(ir.Column("salary"), ir.Literal(integer = Some(1)))),
        Seq(ir.Column("department_id")),
        Seq(ir.SortOrder(ir.Column("employee_id"), ir.DescendingSortDirection, ir.SortNullsUnspecified)),
        ir.WindowFrame(
          ir.UndefinedFrame,
          ir.FrameBoundary(current_row = false, unbounded = false, ir.Noop),
          ir.FrameBoundary(current_row = false, unbounded = false, ir.Noop))))
  }
}
