package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlFunctionBuilderSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = new TSqlFunctionBuilder

  // TODO: What we see as Column here will change to Identifier once other PRs are merged
  "TSqlFunctionBuilder" should {

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

    "throw an exception for invalid function arguments" in {
      // Later, we will not throw an exception but register a semantic error
      intercept[IllegalArgumentException] {
        example(
          "USER_NAME('a', 'b', 'c', 'd')", // USER_NAME function only accepts 0 or 1 argument
          _.expression(),
          ir.Noop)
      }
      intercept[IllegalArgumentException] {
        example(
          "FLOOR()", // FLOOR requires 1 argument
          _.expression(),
          ir.Noop)
      }
    }
  }
}
