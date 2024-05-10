package com.databricks.labs.remorph.parsers

import com.typesafe.scalalogging.Logger
import org.antlr.v4.runtime.{BaseErrorListener, RecognitionException, Recognizer, Token}
import org.json4s._
import org.json4s.jackson.Serialization
import org.json4s.jackson.Serialization.write

import scala.collection.mutable.ListBuffer

case class ErrorDetail(line: Int, charPositionInLine: Int, msg: String, offendingToken: Token)

class ErrorCollector(sourceCode: String, fileName: String) extends BaseErrorListener {
  val errors: ListBuffer[ErrorDetail] = ListBuffer()
  val logger: Logger = Logger[ErrorCollector]

  implicit val formats: Formats = Serialization.formats(NoTypeHints)

  override def syntaxError(
      recognizer: Recognizer[_, _],
      offendingSymbol: Any,
      line: Int,
      charPositionInLine: Int,
      msg: String,
      e: RecognitionException): Unit = {
    errors += ErrorDetail(line, charPositionInLine, msg, offendingSymbol.asInstanceOf[Token])
  }

  def formatErrors(): Seq[String] = {
    val lines = sourceCode.split("\n")
    errors.map { error =>
      val start = Math.max(0, error.offendingToken.getStartIndex - 32)
      val end = Math.min(lines(error.line - 1).length, error.offendingToken.getStopIndex + 32)
      val windowedLine = (if (start > 0) "..." else "") + lines(error.line - 1)
        .substring(start, end) + (if (end < lines(error.line - 1).length) "..." else "")
      val marker =
        " " * (error.offendingToken.getStartIndex - start) + "^" *
          (error.offendingToken.getStopIndex - error.offendingToken.getStartIndex + 1)
      s"File: $fileName, Line: ${error.line}, Token: ${error.offendingToken.getText}\n$windowedLine\n$marker"
    }
  }

  def logErrors(): Unit = {
    val formattedErrors = formatErrors()
    if (formattedErrors.nonEmpty) {
      formattedErrors.foreach(error => logger.error(error))
    }
  }

  def errorsAsJson(): String = {
    write(errors)
  }

  def errorCount(): Int = {
    errors.size
  }
}
