package com.databricks.labs.remorph.generators.py

import com.databricks.labs.remorph.generators.{GeneratorContext, GeneratorTestCommon}
import com.databricks.labs.remorph.{Generating, intermediate => ir}
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

class ExpressionGeneratorTest
    extends AnyWordSpec
    with GeneratorTestCommon[ir.Expression]
    with MockitoSugar
    with ir.IRHelpers {

  override protected val generator = new ExpressionGenerator

  private val logical = new LogicalPlanGenerator

  override def initialState(expr: ir.Expression): Generating =
    Generating(optimizedPlan = ir.Batch(Seq.empty), currentNode = expr, ctx = GeneratorContext(logical))

  "name" in {
    ir.Name("a") generates "a"
  }

  "literals" should {
    "generate string" in {
      ir.Literal("a") generates "'a'"
    }
    "generate int" in {
      ir.Literal(1) generates "1"
    }
    "generate float" in {
      ir.DoubleLiteral(1.0) generates "1.0"
    }
    "generate boolean" in {
      ir.Literal(true) generates "True"
      ir.Literal(false) generates "False"
    }
    "generate null" in {
      ir.Literal(null) generates "None"
    }
  }

  "predicates" should {
    "a > b" in {
      ir.GreaterThan(ir.Name("a"), ir.Name("b")) generates "a > b"
    }
    "a >= b" in {
      ir.GreaterThanOrEqual(ir.Name("a"), ir.Name("b")) generates "a >= b"
    }
    "a < b" in {
      ir.LessThan(ir.Name("a"), ir.Name("b")) generates "a < b"
    }
    "a <= b" in {
      ir.LessThanOrEqual(ir.Name("a"), ir.Name("b")) generates "a <= b"
    }
    "a != b" in {
      ir.NotEquals(ir.Name("a"), ir.Name("b")) generates "a != b"
    }
    "a == b" in {
      ir.Equals(ir.Name("a"), ir.Name("b")) generates "a == b"
    }
    "~a" in {
      ir.Not(ir.Name("a")) generates "~(a)"
    }
    "a or b" in {
      ir.Or(ir.Name("a"), ir.Name("b")) generates "a or b"
    }
    "a and b" in {
      ir.And(ir.Name("a"), ir.Name("b")) generates "a and b"
    }
  }

  "arithmetic" should {
    "a + b" in {
      ir.Add(ir.Name("a"), ir.Name("b")) generates "a + b"
    }
    "a - b" in {
      ir.Subtract(ir.Name("a"), ir.Name("b")) generates "a - b"
    }
    "a * b" in {
      ir.Multiply(ir.Name("a"), ir.Name("b")) generates "a * b"
    }
    "a / b" in {
      ir.Divide(ir.Name("a"), ir.Name("b")) generates "a / b"
    }
    "a % b" in {
      ir.Mod(ir.Name("a"), ir.Name("b")) generates "a % b"
    }
    "-a" in {
      ir.UMinus(ir.Name("a")) generates "-a"
    }
    "+a" in {
      ir.UPlus(ir.Name("a")) generates "+a"
    }
  }

  "python calls" should {
    "f()" in {
      Call(ir.Name("f"), Seq.empty, Seq.empty) generates "f()"
    }
    "f(a)" in {
      Call(ir.Name("f"), Seq(ir.Name("a")), Seq.empty) generates "f(a)"
    }
    "f(a, b)" in {
      Call(ir.Name("f"), Seq(ir.Name("a"), ir.Name("b")), Seq.empty) generates "f(a, b)"
    }
    "f(a, c=1)" in {
      Call(ir.Name("f"), Seq(ir.Name("a")), Seq(Keyword(ir.Name("c"), ir.Literal(1)))) generates "f(a, c=1)"
    }
    "f(a, b, c=1, d=2)" in {
      Call(
        ir.Name("f"),
        Seq(ir.Name("a")),
        Seq(Keyword(ir.Name("c"), ir.Literal(1)), Keyword(ir.Name("d"), ir.Literal(2)))) generates "f(a, c=1, d=2)"
    }
  }

  "dicts" should {
    "{}" in {
      Dict(Seq.empty, Seq.empty) generates "{}"
    }
    "{a: b}" in {
      Dict(Seq(ir.Name("a")), Seq(ir.Name("b"))) generates "{a: b}"
    }
    "{a: b, c: d}" in {
      Dict(Seq(ir.Name("a"), ir.Name("c")), Seq(ir.Name("b"), ir.Name("d"))) generates "{a: b, c: d}"
    }
  }

  "slices" should {
    ":" in {
      Slice(None, None, None) generates ":"
    }
    "a:" in {
      Slice(Some(ir.Name("a")), None, None) generates "a:"
    }
    ":b" in {
      Slice(None, Some(ir.Name("b")), None) generates ":b"
    }
    "a:b" in {
      Slice(Some(ir.Name("a")), Some(ir.Name("b")), None) generates "a:b"
    }
    "::c" in {
      Slice(None, None, Some(ir.Name("c"))) generates "::c"
    }
    "a::c" in {
      Slice(Some(ir.Name("a")), None, Some(ir.Name("c"))) generates "a::c"
    }
    ":b:c" in {
      Slice(None, Some(ir.Name("b")), Some(ir.Name("c"))) generates ":b:c"
    }
    "a:b:c" in {
      Slice(Some(ir.Name("a")), Some(ir.Name("b")), Some(ir.Name("c"))) generates "a:b:c"
    }
  }

  "if expr" should {
    "a if b else c" in {
      IfExp(test = ir.Name("a"), body = ir.Name("b"), orElse = ir.Name("c")) generates "b if a else c"
    }
  }

  "sets" should {
    "set()" in {
      Set(Seq.empty) generates "set()"
    }
    "set(a)" in {
      Set(Seq(ir.Name("a"))) generates "{a}"
    }
    "set(a, b)" in {
      Set(Seq(ir.Name("a"), ir.Name("b"))) generates "{a, b}"
    }
  }

  "lists" should {
    "[]" in {
      List(Seq.empty) generates "[]"
    }
    "[a]" in {
      List(Seq(ir.Name("a"))) generates "[a]"
    }
    "[a, b]" in {
      List(Seq(ir.Name("a"), ir.Name("b"))) generates "[a, b]"
    }
  }

  "subscripts" should {
    "a[b]" in {
      Subscript(ir.Name("a"), ir.Name("b")) generates "a[b]"
    }
  }

  "attributes" should {
    "a.b" in {
      Attribute(ir.Name("a"), ir.Name("b")) generates "a.b"
    }
  }

  "tuples" should {
    "(a,)" in {
      Tuple(Seq(ir.Name("a"))) generates "(a,)"
    }
    "(a, b)" in {
      Tuple(Seq(ir.Name("a"), ir.Name("b"))) generates "(a, b,)"
    }
  }

  "lambdas" should {
    "lambda a, b: c" in {
      Lambda(Arguments(args = Seq(ir.Name("a"), ir.Name("b"))), ir.Name("c")) generates "lambda a, b: c"
    }
    "lambda *args: c" in {
      Lambda(Arguments(vararg = Some(ir.Name("args"))), ir.Name("c")) generates "lambda *args: c"
    }
    "lambda **kw: c" in {
      Lambda(Arguments(kwargs = Some(ir.Name("kw"))), ir.Name("c")) generates "lambda **kw: c"
    }
    "lambda pos1, pos2, *other, **keywords: c" in {
      Lambda(
        Arguments(
          args = Seq(ir.Name("pos1"), ir.Name("pos2")),
          vararg = Some(ir.Name("other")),
          kwargs = Some(ir.Name("keywords"))),
        ir.Name("c")) generates "lambda pos1, pos2, *other, **keywords: c"
    }
  }

  "comprehensions" should {
    "[a*2 for a in b]" in {
      ListComp(
        ir.Multiply(ir.Name("a"), ir.Literal(2)),
        Seq(Comprehension(ir.Name("a"), ir.Name("b"), Seq.empty))) generates "[a * 2 for a in b]"
    }
    "[a*2 for a in b if len(a) > 2]" in {
      ListComp(
        ir.Multiply(ir.Name("a"), ir.Literal(2)),
        Seq(
          Comprehension(
            ir.Name("a"),
            ir.Name("b"),
            Seq(
              ir.GreaterThan(
                Call(ir.Name("len"), Seq(ir.Name("a"))),
                ir.Literal(2)))))) generates "[a * 2 for a in b if len(a) > 2]"
    }
    "{a for a in b}" in {
      SetComp(ir.Name("a"), Seq(Comprehension(ir.Name("a"), ir.Name("b"), Seq.empty))) generates "{a for a in b}"
    }
    "{a:1 for a in b}" in {
      DictComp(
        ir.Name("a"),
        ir.Literal(1),
        Seq(Comprehension(ir.Name("a"), ir.Name("b"), Seq.empty))) generates "{a: 1 for a in b}"
    }
  }
}
