package com.databricks.labs.remorph.preprocessor

import org.antlr.v4.runtime.{CharStream, CommonToken, Token}

class Tokenizer(input: CharStream, config: Config = new Config) {

  def nextToken(): Token = {
    val token = new CommonToken(1, "some text")
    token
  }
}

object Tokenizer {

}
