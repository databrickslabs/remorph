package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlExpressionBuilderSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = new TSqlExpressionBuilder

  "TSqlExpressionBuilder" should {
    "translate literals" in {
      example("null", _.expression(), ir.Literal(nullType = Some(ir.NullType())))
      example("1", _.expression(), ir.Literal(integer = Some(1)))
      example("1.1", _.expression(), ir.Literal(float = Some(1.1f)))
      example("'foo'", _.expression(), ir.Literal(string = Some("foo")))
    }
    // TODO: note that scientific notation and decimals are not correctly handled if we copy SnowFlake
    "translate scientific notation" ignore {
      example("1.1e2", _.expression(), ir.Literal(integer = Some(110)))
      example("1.1e-2", _.expression(), ir.Literal(float = Some(0.011f)))
      example("1e2", _.expression(), ir.Literal(integer = Some(100)))
      example("0.123456789", _.expression(), ir.Literal(double = Some(0.123456789)))
      example(
        "0.123456789e-1234",
        _.expression(),
        ir.Literal(decimal = Some(ir.Decimal("0.123456789e-1234", None, None))))
    }
    "translate simple numeric binary expressions" in {
      example("1 + 2", _.expression(), ir.Add(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2))))
      example("1 - 2", _.expression(), ir.Subtract(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2))))
      example("1 * 2", _.expression(), ir.Multiply(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2))))
      example("1 / 2", _.expression(), ir.Divide(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2))))
      example("1 % 2", _.expression(), ir.Mod(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2))))
      example("'A' || 'B'", _.expression(), ir.Concat(ir.Literal(string = Some("A")), ir.Literal(string = Some("B"))))
      example("4 ^ 2", _.expression(), ir.BitwiseXor(ir.Literal(integer = Some(4)), ir.Literal(integer = Some(2))))
    }
    "translate complex binary expressions" in {
      example(
        "a + b * 2",
        _.expression(),
        ir.Add(ir.Column("a"), ir.Multiply(ir.Column("b"), ir.Literal(integer = Some(2)))))
      example(
        "(a + b) * 2",
        _.expression(),
        ir.Multiply(ir.Add(ir.Column("a"), ir.Column("b")), ir.Literal(integer = Some(2))))
      example("a & b | c", _.expression(), ir.BitwiseOr(ir.BitwiseAnd(ir.Column("a"), ir.Column("b")), ir.Column("c")))
      example(
        "(a & b) | c",
        _.expression(),
        ir.BitwiseOr(ir.BitwiseAnd(ir.Column("a"), ir.Column("b")), ir.Column("c")))
      example(
        "a % 3 + b * 2 - c / 5",
        _.expression(),
        ir.Subtract(
          ir.Add(
            ir.Mod(ir.Column("a"), ir.Literal(integer = Some(3))),
            ir.Multiply(ir.Column("b"), ir.Literal(integer = Some(2)))),
          ir.Divide(ir.Column("c"), ir.Literal(integer = Some(5)))))
      example(
        "(a % 3 + b) * 2 - c / 5",
        _.expression(),
        ir.Subtract(
          ir.Multiply(
            ir.Add(ir.Mod(ir.Column("a"), ir.Literal(integer = Some(3))), ir.Column("b")),
            ir.Literal(integer = Some(2))),
          ir.Divide(ir.Column("c"), ir.Literal(integer = Some(5)))))
      example(
        query = "a || b || c",
        _.expression(),
        ir.Concat(ir.Concat(ir.Column("a"), ir.Column("b")), ir.Column("c")))
    }
    "correctly apply operator precedence and associativity" in {
      example(
        "1 + -++-2",
        _.expression(),
        ir.Add(ir.Literal(integer = Some(1)), ir.UMinus(ir.UPlus(ir.UPlus(ir.UMinus(ir.Literal(integer = Some(2))))))))
      example(
        "1 + ~ 2 * 3",
        _.expression(),
        ir.Add(
          ir.Literal(integer = Some(1)),
          ir.Multiply(ir.BitwiseNot(ir.Literal(integer = Some(2))), ir.Literal(integer = Some(3)))))
      example(
        "1 + -2 * 3",
        _.expression(),
        ir.Add(
          ir.Literal(integer = Some(1)),
          ir.Multiply(ir.UMinus(ir.Literal(integer = Some(2))), ir.Literal(integer = Some(3)))))
      example(
        "1 + -2 * 3 + 7 & 66",
        _.expression(),
        ir.BitwiseAnd(
          ir.Add(
            ir.Add(
              ir.Literal(integer = Some(1)),
              ir.Multiply(ir.UMinus(ir.Literal(integer = Some(2))), ir.Literal(integer = Some(3)))),
            ir.Literal(integer = Some(7))),
          ir.Literal(integer = Some(66))))
      example(
        "1 + -2 * 3 + 7 ^ 66",
        _.expression(),
        ir.BitwiseXor(
          ir.Add(
            ir.Add(
              ir.Literal(integer = Some(1)),
              ir.Multiply(ir.UMinus(ir.Literal(integer = Some(2))), ir.Literal(integer = Some(3)))),
            ir.Literal(integer = Some(7))),
          ir.Literal(integer = Some(66))))
      example(
        "1 + -2 * 3 + 7 | 66",
        _.expression(),
        ir.BitwiseOr(
          ir.Add(
            ir.Add(
              ir.Literal(integer = Some(1)),
              ir.Multiply(ir.UMinus(ir.Literal(integer = Some(2))), ir.Literal(integer = Some(3)))),
            ir.Literal(integer = Some(7))),
          ir.Literal(integer = Some(66))))
      example(
        "1 + -2 * 3 + 7 + ~66",
        _.expression(),
        ir.Add(
          ir.Add(
            ir.Add(
              ir.Literal(integer = Some(1)),
              ir.Multiply(ir.UMinus(ir.Literal(integer = Some(2))), ir.Literal(integer = Some(3)))),
            ir.Literal(integer = Some(7))),
          ir.BitwiseNot(ir.Literal(integer = Some(66)))))
      example(
        "1 + -2 * 3 + 7 | 1980 || 'leeds1' || 'leeds2' || 'leeds3'",
        _.expression(),
        ir.Concat(
          ir.Concat(
            ir.Concat(
              ir.BitwiseOr(
                ir.Add(
                  ir.Add(
                    ir.Literal(integer = Some(1)),
                    ir.Multiply(ir.UMinus(ir.Literal(integer = Some(2))), ir.Literal(integer = Some(3)))),
                  ir.Literal(integer = Some(7))),
                ir.Literal(integer = Some(1980))),
              ir.Literal(string = Some("leeds1"))),
            ir.Literal(string = Some("leeds2"))),
          ir.Literal(string = Some("leeds3"))))
    }
    "correctly respect explicit precedence with parentheses" in {
      example(
        "(1 + 2) * 3",
        _.expression(),
        ir.Multiply(
          ir.Add(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2))),
          ir.Literal(integer = Some(3))))
      example(
        "1 + (2 * 3)",
        _.expression(),
        ir.Add(
          ir.Literal(integer = Some(1)),
          ir.Multiply(ir.Literal(integer = Some(2)), ir.Literal(integer = Some(3)))))
      example(
        "(1 + 2) * (3 + 4)",
        _.expression(),
        ir.Multiply(
          ir.Add(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2))),
          ir.Add(ir.Literal(integer = Some(3)), ir.Literal(integer = Some(4)))))
      example(
        "1 + (2 * 3) + 4",
        _.expression(),
        ir.Add(
          ir.Add(
            ir.Literal(integer = Some(1)),
            ir.Multiply(ir.Literal(integer = Some(2)), ir.Literal(integer = Some(3)))),
          ir.Literal(integer = Some(4))))
      example(
        "1 + (2 * 3 + 4)",
        _.expression(),
        ir.Add(
          ir.Literal(integer = Some(1)),
          ir.Add(
            ir.Multiply(ir.Literal(integer = Some(2)), ir.Literal(integer = Some(3))),
            ir.Literal(integer = Some(4)))))
      example(
        "1 + (2 * (3 + 4))",
        _.expression(),
        ir.Add(
          ir.Literal(integer = Some(1)),
          ir.Multiply(
            ir.Literal(integer = Some(2)),
            ir.Add(ir.Literal(integer = Some(3)), ir.Literal(integer = Some(4))))))
      example(
        "(1 + (2 * (3 + 4)))",
        _.expression(),
        ir.Add(
          ir.Literal(integer = Some(1)),
          ir.Multiply(
            ir.Literal(integer = Some(2)),
            ir.Add(ir.Literal(integer = Some(3)), ir.Literal(integer = Some(4))))))
    }
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
          is_user_defined_function = false))

      example(
        "FLOOR()", // FLOOR requires 1 argument
        _.expression(),
        ir.UnresolvedFunction("FLOOR", List(), is_distinct = false, is_user_defined_function = false))
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
    "correctly resolve dot delimited plain references" in {
      example("a", _.expression(), Identifier("a", isQuoted = false))
      example("a.b", _.expression(), Dot(Identifier("a", isQuoted = false), Identifier("b", isQuoted = false)))
      example(
        "a.b.c",
        _.expression(),
        Dot(
          Identifier("a", isQuoted = false),
          Dot(Identifier("b", isQuoted = false), Identifier("c", isQuoted = false))))
    }
    "correctly resolve quoted identifiers" in {
      example("\"a\"", _.expression(), Identifier("\"a\"", isQuoted = true))
      example("[a]", _.expression(), Identifier("\"a\"", isQuoted = true))
      example("[a].[b]", _.expression(), Dot(Identifier("[a]", isQuoted = true), Identifier("[b]", isQuoted = true)))
      example(
        "[a].[b].[c]",
        _.expression(),
        Dot(
          Identifier("[a]", isQuoted = true),
          Dot(Identifier("[b]", isQuoted = true), Identifier("[c]", isQuoted = true))))
    }
  }
}
