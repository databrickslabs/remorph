package com.databricks.labs.remorph.preprocessor

import org.antlr.v4.runtime.CharStreams
import org.scalatest.wordspec.AnyWordSpec

class TokenizerTest extends AnyWordSpec {

  "Preprocessor" should {
    "process statement block" in {

      // NB: These will be moved to a PreProcessorTestCommon trait
      val input = CharStreams.fromString("{% input %}")
      val Tokenizer = new Tokenizer(input)
      val token = Tokenizer.nextToken()
      assert(token.getType == 1)
    }

  }

}
