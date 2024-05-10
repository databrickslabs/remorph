package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlFunctionBuilderSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = new TSqlFunctionBuilder

  "TSqlFunctionBuilder" should {

    "translate functions with no parameters" in {
      example("APP_NAME()", _.standardFunction(), ir.CallFunction("APP_NAME", List()))
      example("SCOPE_IDENTITY()", _.standardFunction(), ir.CallFunction("SCOPE_IDENTITY", List()))
    }

    "translate functions with variable numbers of parameters" in {
      example(
        "CONCAT('a', 'b', 'c')",
        _.standardFunction(),
        ir.CallFunction(
          "CONCAT",
          Seq(ir.Literal(string = Some("a")), ir.Literal(string = Some("b")), ir.Literal(string = Some("c")))))

      example(
        "CONCAT_WS(',', 'a', 'b', 'c')",
        _.standardFunction(),
        ir.CallFunction(
          "CONCAT_WS",
          List(
            ir.Literal(string = Some(",")),
            ir.Literal(string = Some("a")),
            ir.Literal(string = Some("b")),
            ir.Literal(string = Some("c")))))
    }

    "translate functions with complicated expressions as parameters" ignore {
      example(
        "CONCAT('a', 'b' || 'c', Greatest(42, 2, 4, \"ali\"))",
        _.standardFunction(),
        ir.CallFunction(
          "CONCAT",
          List(
            ir.Literal(string = Some("a")),
            ir.Concat(ir.Literal(string = Some("b")), ir.Literal(string = Some("c"))),
            ir.Literal(string = Some("d")))))
    }
  }
}
