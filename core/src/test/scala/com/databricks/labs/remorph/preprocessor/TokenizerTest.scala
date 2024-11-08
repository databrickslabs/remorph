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
      for (i <- 0 to 7) {
        val token = tokenizer.nextToken()
        assert(token.getType == Preprocessor.CHAR)
      }
      assert(tokenizer.nextToken().getType == Preprocessor.STATEMENT_END)
    }

  }

}
