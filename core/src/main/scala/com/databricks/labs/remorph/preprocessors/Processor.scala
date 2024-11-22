package com.databricks.labs.remorph.preprocessors

import com.databricks.labs.remorph._
import org.antlr.v4.runtime.{CharStream, Lexer}

trait Processor extends TransformationConstructors {
  protected def createLexer(input: CharStream): Lexer
  def pre(input: PreProcessing): Transformation[Parsing]
  def post(input: String): Transformation[String]
}
