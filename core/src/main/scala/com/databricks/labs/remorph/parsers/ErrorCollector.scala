package com.databricks.labs.remorph.parsers

import org.antlr.v4.runtime._
import org.apache.logging.log4j.{LogManager, Logger}
import org.json4s._
import org.json4s.jackson.Serialization
import org.json4s.jackson.Serialization.write

import scala.collection.mutable.ListBuffer

sealed trait ErrorCollector extends BaseErrorListener {
  def logErrors(): Unit = {}
  def errorsAsJson: String = "{}"
  def errorCount: Int = 0
  private[parsers] def formatErrors: Seq[String] = Seq()
  def reset(): Unit = {}
}

class EmptyErrorCollector extends ErrorCollector

case class ErrorDetail(line: Int, charPositionInLine: Int, msg: String, offendingToken: Token)

class DefaultErrorCollector extends ErrorCollector {

  var count: Int = 0
  val antlrErr: ConsoleErrorListener = new ConsoleErrorListener()

  override def syntaxError(
      recognizer: Recognizer[_, _],
      offendingSymbol: Any,
      line: Int,
      charPositionInLine: Int,
      msg: String,
      e: RecognitionException): Unit = {
    antlrErr.syntaxError(recognizer, offendingSymbol, line, charPositionInLine, msg, e)
    count += 1
  }

  override def errorCount: Int = count
  override def reset(): Unit = count = 0
}

class ProductionErrorCollector(sourceCode: String, fileName: String) extends ErrorCollector {
  val errors: ListBuffer[ErrorDetail] = ListBuffer()
  val logger: Logger = LogManager.getLogger(classOf[ErrorCollector])

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

  override private[parsers] def formatErrors: Seq[String] = {
    val lines = sourceCode.split("\n")
    errors.map { error =>
      val start = Math.max(0, error.offendingToken.getStartIndex - 32)
      val end = Math.min(lines(error.line - 1).length, error.offendingToken.getStopIndex + 32)
      val windowedLine = (if (start > 0) "..." else "") + lines(error.line - 1)
        .substring(start, end) + (if (end < lines(error.line - 1).length) "..." else "")
      val markerStart =
        if (start > 0) error.offendingToken.getStartIndex - start + 3 else error.offendingToken.getStartIndex - start
      val marker =
        " " * markerStart + "^" *
          (error.offendingToken.getStopIndex - error.offendingToken.getStartIndex + 1)
      s"File: $fileName, Line: ${error.line}, Token: ${error.offendingToken.getText}\n$windowedLine\n$marker"
    }
  }

  override def logErrors(): Unit = {
    val formattedErrors = formatErrors
    if (formattedErrors.nonEmpty) {
      formattedErrors.foreach(error => logger.error(error))
    }
  }

  override def errorsAsJson: String = write(errors)

  override def errorCount: Int = errors.size

  override def reset(): Unit = errors.clear()
}
