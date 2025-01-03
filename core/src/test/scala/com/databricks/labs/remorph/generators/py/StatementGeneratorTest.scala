package com.databricks.labs.remorph.generators.py

import com.databricks.labs.remorph.generators.{GeneratorContext, GeneratorTestCommon}
import com.databricks.labs.remorph.{Generating, intermediate => ir}
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

class StatementGeneratorTest
    extends AnyWordSpec
    with GeneratorTestCommon[Statement]
    with MockitoSugar
    with ir.IRHelpers {

  override protected val generator = new StatementGenerator(new ExpressionGenerator)

  override protected def initialState(statement: Statement) =
    Generating(
      optimizedPlan = ir.Batch(Seq.empty),
      currentNode = statement,
      ctx = GeneratorContext(new LogicalPlanGenerator))

  "imports" should {
    "import a, b as c" in {
      Import(Seq(Alias(ir.Name("a")), Alias(ir.Name("b"), Some(ir.Name("c"))))) generates "import a, b as c"
    }
    "from foo.bar import a, b as c" in {
      ImportFrom(
        Some(ir.Name("foo.bar")),
        Seq(Alias(ir.Name("a")), Alias(ir.Name("b"), Some(ir.Name("c"))))) generates "from foo.bar import a, b as c"
    }
  }

  "functions" should {
    "@foo" in {
      Decorator(ir.Name("foo")) generates "@foo"
    }
    "simple" in {
      FunctionDef(ir.Name("foo"), Arguments(), Seq(Pass)) generates "def foo():\n  pass\n"
    }
    "decorated" in {
      FunctionDef(
        ir.Name("foo"),
        Arguments(),
        Seq(Pass),
        Seq(Decorator(ir.Name("bar")))) generates "@bar\ndef foo():\n  pass\n"
    }
  }

  "classes" should {
    "simple" in {
      ClassDef(ir.Name("Foo"), Seq(), Seq(Pass)) generates "class Foo:\n  pass\n"
    }
    "with bases" in {
      ClassDef(ir.Name("Foo"), Seq(ir.Name("Bar")), Seq(Pass)) generates "class Foo(Bar):\n  pass\n"
    }
    "with decorators" in {
      ClassDef(ir.Name("Foo"), Seq(), Seq(Pass), Seq(Decorator(ir.Name("bar")))) generates "@bar\nclass Foo:\n  pass\n"
    }
    "with decorated functions" in {
      ClassDef(
        ir.Name("Foo"),
        Seq(),
        Seq(
          FunctionDef(ir.Name("foo"), Arguments(), Seq(Pass), Seq(Decorator(ir.Name("bar")))))) generates """class Foo:
                     |  @bar
                     |  def foo():
                     |    pass
                     |
                     |""".stripMargin
    }
  }

  "assign" should {
    "a = b" in {
      Assign(Seq(ir.Name("a")), ir.Name("b")) generates "a = b"
    }
    "a, b = c, d" in {
      Assign(Seq(ir.Name("a"), ir.Name("b")), Tuple(Seq(ir.Name("c"), ir.Name("d")))) generates "a, b = (c, d,)"
    }
  }

  "for loop" should {
    "for a in b: pass" in {
      For(ir.Name("a"), ir.Name("b"), Seq(Pass)) generates "for a in b:\n  pass\n"
    }
    "for a in b: ... else: ..." in {
      For(ir.Name("a"), ir.Name("b"), Seq(Pass), Seq(Pass)) generates
        """for a in b:
          |  pass
          |else:
          |  pass
          |""".stripMargin
    }
    "for-else in function propagates whitespace for else branch" in {
      FunctionDef(
        ir.Name("foo"),
        Arguments(),
        Seq(For(ir.Name("a"), ir.Name("b"), Seq(Pass), Seq(Pass)))) generates """def foo():
                     |  for a in b:
                     |    pass
                     |  else:
                     |    pass
                     |
                     |""".stripMargin
    }
  }

  "while loop" should {
    "while a: pass" in {
      While(ir.Name("a"), Seq(Pass)) generates "while a:\n  pass\n"
    }
    "while a: ... else: ..." in {
      While(ir.Name("a"), Seq(Pass), Seq(Pass)) generates
        """while a:
          |  pass
          |else:
          |  pass
          |""".stripMargin
    }
  }

  "if statement" should {
    "if a: pass" in {
      If(ir.Name("a"), Seq(Pass)) generates "if a:\n  pass\n"
    }
    "if a: ... else: ..." in {
      If(ir.Name("a"), Seq(Pass), Seq(Pass)) generates
        """if a:
          |  pass
          |else:
          |  pass
          |""".stripMargin
    }
  }

  "with statement" should {
    "with a(), b() as c: pass" in {
      With(
        Seq(Alias(Call(ir.Name("a"), Seq())), Alias(Call(ir.Name("b"), Seq()), Some(ir.Name("c")))),
        Seq(Pass)) generates """with a(), b() as c:
                               |  pass
                               |""".stripMargin
    }
  }

  "try-except" should {
    "try: pass except: pass" in {
      Try(Seq(Pass), Seq(Except(None, Seq(Pass)))) generates
        """try:
          |  pass
          |except:
          |  pass
          |""".stripMargin
    }
    "try: pass except Foo: pass" in {
      Try(Seq(Pass), Seq(Except(Some(Alias(ir.Name("Foo"))), Seq(Pass)))) generates
        """try:
          |  pass
          |except Foo:
          |  pass
          |""".stripMargin
    }
    "try: pass except Foo as x: pass" in {
      Try(
        Seq(Pass),
        Seq(
          Except(Some(Alias(ir.Name("Foo"), Some(ir.Name("x")))), Seq(Pass)),
          Except(Some(Alias(ir.Name("NotFound"))), Seq(Pass))),
        Seq(Pass)) generates
        """try:
          |  pass
          |except Foo as x:
          |  pass
          |except NotFound:
          |  pass
          |else:
          |  pass
          |""".stripMargin
    }
    "try: ... finally: ..." in {
      Try(Seq(Pass), orFinally = Seq(Pass)) generates
        """try:
          |  pass
          |finally:
          |  pass
          |""".stripMargin
    }
    "if True: try: ... finally: ..." in {
      If(ir.Literal.True, Seq(Try(Seq(Pass), orFinally = Seq(Pass)))) generates
        """if True:
              |  try:
              |    pass
              |  finally:
              |    pass
              |
              |""".stripMargin
    }
  }

  "raise" should {
    "raise" in {
      Raise() generates "raise"
    }
    "raise Foo" in {
      Raise(Some(ir.Name("Foo"))) generates "raise Foo"
    }
    "raise Foo from Bar" in {
      Raise(Some(ir.Name("Foo")), Some(ir.Name("Bar"))) generates "raise Foo from Bar"
    }
  }

  "assert" should {
    "assert a" in {
      Assert(ir.Name("a")) generates "assert a"
    }
    "assert a, b" in {
      Assert(ir.Name("a"), Some(ir.Name("b"))) generates "assert a, b"
    }
  }

  "return" should {
    "return" in {
      Return(None) generates "return"
    }
    "return a" in {
      Return(Some(ir.Name("a"))) generates "return a"
    }
  }

  "delete" should {
    "delete a" in {
      Delete(Seq(ir.Name("a"))) generates "del a"
    }
    "delete a, b" in {
      Delete(Seq(ir.Name("a"), ir.Name("b"))) generates "del a, b"
    }
  }
}
