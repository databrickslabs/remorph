package com.databricks.labs.remorph.preprocessors

import com.databricks.labs.remorph._
import com.databricks.labs.remorph.intermediate.IncoherentState
import org.antlr.v4.runtime.{CharStream, Lexer}

trait Processor extends TransformationConstructors {
  protected def createLexer(input: CharStream): Lexer
  final def pre: Transformation[Unit] = {
    get.flatMap {
      case p: PreProcessing =>
        preprocess(p.source).flatMap{ preprocessedString =>
          set(Parsing(preprocessedString, p.filename, Some(p)))
        }
      case other => ko(WorkflowStage.PARSE, IncoherentState(other, classOf[PreProcessing]))
    }
  }

  def preprocess(input: String): Transformation[String]
  def post(input: String): Transformation[String]
}
