package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.coverage.ErrorEncoders
import com.databricks.labs.remorph.intermediate.{ParsingError, RemorphError}
import org.antlr.v4.runtime._
import org.apache.logging.log4j.{LogManager, Logger}

import scala.collection.mutable.ListBuffer
import io.circe.syntax._

sealed trait ErrorCollector extends BaseErrorListener {
  def logErrors(): Unit = {}
  def errorsAsJson: String = "{}"
  def errorCount: Int = 0
  private[remorph] def formatErrors: Seq[String] = Seq()
  def reset(): Unit = {}
}

class EmptyErrorCollector extends ErrorCollector

class DefaultErrorCollector extends ErrorCollector {

  var count: Int = 0
  private val antlrErr: ConsoleErrorListener = new ConsoleErrorListener()

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

class ProductionErrorCollector(sourceCode: String, fileName: String) extends ErrorCollector with ErrorEncoders {
  val errors: ListBuffer[ParsingError] = ListBuffer()
  val logger: Logger = LogManager.getLogger(classOf[ErrorCollector])

  override def syntaxError(
      recognizer: Recognizer[_, _],
      offendingSymbol: Any,
      line: Int,
      charPositionInLine: Int,
      msg: String,
      e: RecognitionException): Unit = {
    val errorDetail = offendingSymbol match {
      case t: Token =>
        val width = t.getStopIndex - t.getStartIndex + 1
        ParsingError(line, charPositionInLine, msg, width, t.getText, tokenName(recognizer, t), ruleName(recognizer, e))
      case _ => ParsingError(line, charPositionInLine, msg, 0, "", "missing", ruleName(recognizer, e))
    }
    errors += errorDetail
  }

  override private[remorph] def formatErrors: Seq[String] = {
    val lines = sourceCode.split("\n")
    errors.map { error =>
      val errorLine = lines(error.line - 1)
      val errorText = formatError(errorLine, error.charPositionInLine, error.offendingTokenWidth)
      s"${error.msg}\nFile: $fileName, Line: ${error.line}, Token: ${error.offendingTokenText}\n$errorText"
    }
  }

  private[parsers] def tokenName(recognizer: Recognizer[_, _], token: Token): String = token match {
    case t: Token =>
      Option(recognizer)
        .map(_.getVocabulary.getSymbolicName(t.getType))
        .getOrElse("unresolved token name")
    case _ => "missing"
  }

  private[parsers] def ruleName(recognizer: Recognizer[_, _], e: RecognitionException): String =
    (Option(recognizer), Option(e)) match {
      case (Some(rec), Some(exc)) => rec.getRuleNames()(exc.getCtx.getRuleIndex)
      case _ => "unresolved rule name"
    }

  private[parsers] def formatError(
      errorLine: String,
      errorPosition: Int,
      errorWidth: Int,
      windowWidth: Int = 80): String = {
    val roomForContext = (windowWidth - errorWidth) / 2
    val clipLeft = errorLine.length > windowWidth && errorPosition >= roomForContext
    val clipRight =
      errorLine.length > windowWidth &&
        errorLine.length - errorPosition - errorWidth >= roomForContext
    val clipMark = "..."
    val (markerStart, clippedLine) = (clipLeft, clipRight) match {
      case (false, false) => (errorPosition, errorLine)
      case (true, false) =>
        (
          windowWidth - (errorLine.length - errorPosition),
          clipMark + errorLine.substring(errorLine.length - windowWidth + clipMark.length))
      case (false, true) =>
        (errorPosition, errorLine.take(windowWidth - clipMark.length) + clipMark)
      case (true, true) =>
        val start = errorPosition - roomForContext
        val clippedLineWithoutClipMarks =
          errorLine.substring(start, Math.min(start + windowWidth, errorLine.length - 1))
        (
          roomForContext,
          clipMark + clippedLineWithoutClipMarks.substring(
            clipMark.length,
            clipMark.length + windowWidth - 2 * clipMark.length) + clipMark)

    }
    clippedLine + "\n" + " " * markerStart + "^" * errorWidth
  }

  override def logErrors(): Unit = {
    val formattedErrors = formatErrors
    if (formattedErrors.nonEmpty) {
      formattedErrors.foreach(error => logger.error(error))
    }
  }

  override def errorsAsJson: String = errors.toList.map(_.asInstanceOf[RemorphError]).asJson.noSpaces

  override def errorCount: Int = errors.size

  override def reset(): Unit = errors.clear()
}
