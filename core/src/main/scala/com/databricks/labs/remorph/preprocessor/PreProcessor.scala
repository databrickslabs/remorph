package com.databricks.labs.remorph.preprocessor

import com.databricks.labs.remorph.{Parsing, Transformation}
import org.antlr.v4.runtime.{CharStream, CharStreams, CommonTokenStream, Lexer}

trait PreProcessor {

  protected def createLexer(input: CharStream): Lexer
  protected def process(tokenStream: CommonTokenStream): Transformation[String]

  def process(input: Parsing): Transformation[String] = {
    val inputString = CharStreams.fromString(input.source)
    val tokenizer = createLexer(inputString)
    val tokenStream = new CommonTokenStream(tokenizer)
    process(tokenStream)
  }
}
