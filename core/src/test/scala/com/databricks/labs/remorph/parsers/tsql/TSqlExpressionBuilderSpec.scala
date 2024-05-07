package com.databricks.labs.remorph.parsers.tsql

import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

import com.databricks.labs.remorph.parsers.intermediate._

class TSqlExpressionBuilderSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = new TSqlExpressionBuilder

  "TSqlExpressionBuilder" should {
    "translate literals" in {
      example("null", _.expression(), Literal(nullType = Some(NullType())))
      example("1", _.expression(), Literal(integer = Some(1)))
      example("1.1", _.expression(), Literal(float = Some(1.1f)))
      example("'foo'", _.expression(), Literal(string = Some("foo")))
    }
    // TODO: note that scientific notation and decimals are not correctly handled if we copy SnowFlake
    "translate scientific notation" ignore {
      example("1.1e2", _.expression(), Literal(integer = Some(110)))
      example("1.1e-2", _.expression(), Literal(float = Some(0.011f)))
      example("1e2", _.expression(), Literal(integer = Some(100)))
      example("0.123456789", _.expression(), Literal(double = Some(0.123456789)))
      example("0.123456789e-1234", _.expression(), Literal(decimal = Some(Decimal("0.123456789e-1234", None, None))))
    }
    "translate simple numeric binary expressions" in {
      example("1 + 2", _.expression(), Add(Literal(integer = Some(1)), Literal(integer = Some(2))))
      example("1 - 2", _.expression(), Subtract(Literal(integer = Some(1)), Literal(integer = Some(2))))
      example("1 * 2", _.expression(), Multiply(Literal(integer = Some(1)), Literal(integer = Some(2))))
      example("1 / 2", _.expression(), Divide(Literal(integer = Some(1)), Literal(integer = Some(2))))
      example("1 % 2", _.expression(), Mod(Literal(integer = Some(1)), Literal(integer = Some(2))))
      example("'A' || 'B'", _.expression(), Concat(Literal(string = Some("A")), Literal(string = Some("B"))))
      example("4 ^ 2", _.expression(), BitwiseXor(Literal(integer = Some(4)), Literal(integer = Some(2))))
    }
    "translate complex binary expressions" in {
      example("a + b * 2", _.expression(), Add(Column("a"), Multiply(Column("b"), Literal(integer = Some(2)))))
      example("(a + b) * 2", _.expression(), Multiply(Add(Column("a"), Column("b")), Literal(integer = Some(2))))
      example("a & b | c", _.expression(), BitwiseOr(BitwiseAnd(Column("a"), Column("b")), Column("c")))
      example("(a & b) | c", _.expression(), BitwiseOr(BitwiseAnd(Column("a"), Column("b")), Column("c")))
      example(
        "a % 3 + b * 2 - c / 5",
        _.expression(),
        Subtract(
          Add(Mod(Column("a"), Literal(integer = Some(3))), Multiply(Column("b"), Literal(integer = Some(2)))),
          Divide(Column("c"), Literal(integer = Some(5)))))
      example(
        "(a % 3 + b) * 2 - c / 5",
        _.expression(),
        Subtract(
          Multiply(Add(Mod(Column("a"), Literal(integer = Some(3))), Column("b")), Literal(integer = Some(2))),
          Divide(Column("c"), Literal(integer = Some(5)))))
      example(query = "a || b || c", _.expression(), Concat(Concat(Column("a"), Column("b")), Column("c")))
    }
    "correctly apply operator precedence and associativity" in {
      example(
        "1 + -++-2",
        _.expression(),
        Add(Literal(integer = Some(1)), UMinus(UPlus(UPlus(UMinus(Literal(integer = Some(2))))))))
      example(
        "1 + ~ 2 * 3",
        _.expression(),
        Add(Literal(integer = Some(1)), Multiply(BitwiseNot(Literal(integer = Some(2))), Literal(integer = Some(3)))))
      example(
        "1 + -2 * 3",
        _.expression(),
        Add(Literal(integer = Some(1)), Multiply(UMinus(Literal(integer = Some(2))), Literal(integer = Some(3)))))
      example(
        "1 + -2 * 3 + 7 & 66",
        _.expression(),
        BitwiseAnd(
          Add(
            Add(Literal(integer = Some(1)), Multiply(UMinus(Literal(integer = Some(2))), Literal(integer = Some(3)))),
            Literal(integer = Some(7))),
          Literal(integer = Some(66))))
      example(
        "1 + -2 * 3 + 7 ^ 66",
        _.expression(),
        BitwiseXor(
          Add(
            Add(Literal(integer = Some(1)), Multiply(UMinus(Literal(integer = Some(2))), Literal(integer = Some(3)))),
            Literal(integer = Some(7))),
          Literal(integer = Some(66))))
      example(
        "1 + -2 * 3 + 7 | 66",
        _.expression(),
        BitwiseOr(
          Add(
            Add(Literal(integer = Some(1)), Multiply(UMinus(Literal(integer = Some(2))), Literal(integer = Some(3)))),
            Literal(integer = Some(7))),
          Literal(integer = Some(66))))
      example(
        "1 + -2 * 3 + 7 + ~66",
        _.expression(),
        Add(
          Add(
            Add(Literal(integer = Some(1)), Multiply(UMinus(Literal(integer = Some(2))), Literal(integer = Some(3)))),
            Literal(integer = Some(7))),
          BitwiseNot(Literal(integer = Some(66)))))
      example(
        "1 + -2 * 3 + 7 | 1980 || 'leeds1' || 'leeds2' || 'leeds3'",
        _.expression(),
        Concat(
          Concat(
            Concat(
              BitwiseOr(
                Add(
                  Add(
                    Literal(integer = Some(1)),
                    Multiply(UMinus(Literal(integer = Some(2))), Literal(integer = Some(3)))),
                  Literal(integer = Some(7))),
                Literal(integer = Some(1980))),
              Literal(string = Some("leeds1"))),
            Literal(string = Some("leeds2"))),
          Literal(string = Some("leeds3"))))
    }
    "correctly respect explicit precedence with parentheses" in {
      example(
        "(1 + 2) * 3",
        _.expression(),
        Multiply(Add(Literal(integer = Some(1)), Literal(integer = Some(2))), Literal(integer = Some(3))))
      example(
        "1 + (2 * 3)",
        _.expression(),
        Add(Literal(integer = Some(1)), Multiply(Literal(integer = Some(2)), Literal(integer = Some(3)))))
      example(
        "(1 + 2) * (3 + 4)",
        _.expression(),
        Multiply(
          Add(Literal(integer = Some(1)), Literal(integer = Some(2))),
          Add(Literal(integer = Some(3)), Literal(integer = Some(4)))))
      example(
        "1 + (2 * 3) + 4",
        _.expression(),
        Add(
          Add(Literal(integer = Some(1)), Multiply(Literal(integer = Some(2)), Literal(integer = Some(3)))),
          Literal(integer = Some(4))))
      example(
        "1 + (2 * 3 + 4)",
        _.expression(),
        Add(
          Literal(integer = Some(1)),
          Add(Multiply(Literal(integer = Some(2)), Literal(integer = Some(3))), Literal(integer = Some(4)))))
      example(
        "1 + (2 * (3 + 4))",
        _.expression(),
        Add(
          Literal(integer = Some(1)),
          Multiply(Literal(integer = Some(2)), Add(Literal(integer = Some(3)), Literal(integer = Some(4))))))
      example(
        "(1 + (2 * (3 + 4)))",
        _.expression(),
        Add(
          Literal(integer = Some(1)),
          Multiply(Literal(integer = Some(2)), Add(Literal(integer = Some(3)), Literal(integer = Some(4))))))
    }
  }
}
