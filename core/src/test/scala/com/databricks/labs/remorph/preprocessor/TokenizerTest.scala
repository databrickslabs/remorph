package com.databricks.labs.remorph.preprocessor

import com.databricks.labs.remorph.parsers.preprocessor.Preprocessor
import org.antlr.v4.runtime.CharStreams
import org.scalatest.wordspec.AnyWordSpec

class TokenizerTest extends AnyWordSpec {

  "Preprocessor" should {
    "process statement block" in {

      // NB: These will be moved to a PreProcessorTestCommon trait
      val input = CharStreams.fromString("{% input %}")
      val tokenizer = new Preprocessor(input)
      val token = tokenizer.nextToken()
      assert(token.getType == Preprocessor.STATEMENT)
      for (i <- 1 to 7) {
        val token = tokenizer.nextToken()
        assert(token.getType == Preprocessor.CHAR)
      }
      val token2 = tokenizer.nextToken()
      assert(token2.getType == Preprocessor.STATEMENT_END)
    }

  }

}
