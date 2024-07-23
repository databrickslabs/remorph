package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.GeneratorContext
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar
import com.databricks.labs.remorph.parsers.{intermediate => ir}

class ExpressionGeneratorTest extends AnyWordSpec with Matchers with MockitoSugar {
  private def generate(expr: ir.Expression): String = {
    new ExpressionGenerator().expression(new GeneratorContext(), expr)
  }

  "literal" should {
    "be generated" in {
      generate(ir.Literal()) shouldBe "NULL"

      generate(ir.Literal(binary = Some(Array(0x01, 0x02, 0x03)))) shouldBe "010203"

      generate(ir.Literal(boolean = Some(true))) shouldBe "TRUE"

      generate(ir.Literal(short = Some(123))) shouldBe "123"

      generate(ir.Literal(integer = Some(123))) shouldBe "123"

      generate(ir.Literal(long = Some(123))) shouldBe "123"

      generate(ir.Literal(float = Some(123.4f))) shouldBe "123.4"

      generate(ir.Literal(double = Some(123.4))) shouldBe "123.4"

      generate(ir.Literal(string = Some("abc"))) shouldBe "\"abc\""

      generate(ir.Literal(date = Some(1721757801000L))) shouldBe "\"2024-07-23\""

      generate(ir.Literal(timestamp = Some(1721757801000L))) shouldBe "\"2024-07-23 20:03:21.000\""
    }

    "arrays" in {
      generate(ir.Literal(Seq(ir.Literal("abc"), ir.Literal("def")))) shouldBe "ARRAY(\"abc\", \"def\")"
    }

    "maps" in {
      generate(
        ir.Literal(
          Map(
            "foo" -> ir.Literal("bar"),
            "baz" -> ir.Literal("qux")))) shouldBe "MAP(\"foo\", \"bar\", \"baz\", \"qux\")"
    }
  }
}
