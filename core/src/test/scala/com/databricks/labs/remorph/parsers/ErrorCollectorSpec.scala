package com.databricks.labs.remorph.parsers

import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

class ErrorCollectorSpec extends AnyWordSpec with Matchers with MockitoSugar {

  "ProductionErrorCollector.formatError" should {
    val line = "AAA BBB CCC DDD EEE FFF GGG HHH III JJJ"
    val prodCollector = new ProductionErrorCollector(line, "example.sql")

    "not clip lines shorter than window width" in {

      prodCollector.formatError(line, 4, 3) shouldBe
        """AAA BBB CCC DDD EEE FFF GGG HHH III JJJ
          |    ^^^""".stripMargin
    }

    "clip longer lines on the right when the offending token is close to the start" in {
      prodCollector.formatError(line, 4, 3, 20) shouldBe
        """AAA BBB CCC DDD E...
          |    ^^^""".stripMargin
    }

    "clip longer lines on the left when the offending token is close to the end" in {
      prodCollector.formatError(line, 32, 3, 20) shouldBe
        """...F GGG HHH III JJJ
          |             ^^^""".stripMargin
    }

    "clip longer lines on both sides when the offending toke is too far from both ends" in {
      prodCollector.formatError(line, 16, 3, 20) shouldBe
        """... DDD EEE FFF G...
          |        ^^^""".stripMargin
    }
  }
}
