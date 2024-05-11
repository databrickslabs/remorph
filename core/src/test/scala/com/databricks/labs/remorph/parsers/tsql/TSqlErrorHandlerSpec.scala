package com.databricks.labs.remorph.parsers.tsql

import ch.qos.logback.classic.{Level, Logger}
import ch.qos.logback.classic.spi.ILoggingEvent
import ch.qos.logback.core.read.ListAppender
import com.databricks.labs.remorph.parsers.{ErrorCollector, ErrorDetail}
import org.antlr.v4.runtime.CommonToken
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import org.slf4j.LoggerFactory

import scala.collection.convert.ImplicitConversions.`collection AsScalaIterable`

class TSqlErrorHandlerSpec extends AnyFlatSpec with Matchers {

  "ErrorCollector" should "collect syntax errors correctly" in {
    val errorCollector = new ErrorCollector("sourceCode", "fileName")
    val token = new CommonToken(1)
    val recognizer: Null = null
    val e: Null = null
    errorCollector.syntaxError(recognizer, token, 1, 1, "msg", e)
    errorCollector.errors.head shouldBe ErrorDetail(1, 1, "msg", token)
  }

  it should "format errors correctly" in {
    val errorCollector = new ErrorCollector("sourceCode", "fileName")
    val token = new CommonToken(1)
    token.setLine(1)
    token.setCharPositionInLine(1)
    token.setText("text")
    errorCollector.errors += ErrorDetail(1, 1, "msg", token)
    errorCollector.formatErrors().head should include("Token: text")
  }

  it should "convert errors to JSON correctly" in {
    val errorCollector = new ErrorCollector("sourceCode", "fileName")
    val token = new CommonToken(1)
    token.setLine(1)
    token.setCharPositionInLine(1)
    token.setText("text")
    errorCollector.errors += ErrorDetail(1, 1, "msg", token)
    errorCollector.errorsAsJson() should include("\"line\":1")
  }

  it should "count errors correctly" in {
    val errorCollector = new ErrorCollector("sourceCode", "fileName")
    val token = new CommonToken(1)
    token.setLine(1)
    token.setCharPositionInLine(1)
    token.setText("text")
    errorCollector.errors += ErrorDetail(1, 1, "msg", token)
    errorCollector.errorCount() shouldBe 1
  }

  it should "window long lines correctly" in {
    val longLine = "a" * 40 + "error" + "a" * 40
    val errorCollector = new ErrorCollector(longLine, "fileName")
    val token = new CommonToken(1)
    token.setLine(1)
    token.setCharPositionInLine(40)
    token.setStartIndex(40)
    token.setStopIndex(44)
    token.setText("error")
    errorCollector.errors += ErrorDetail(1, 40, "msg", token)

    // Call the method
    val formattedErrors = errorCollector.formatErrors()

    // Check the windowing
    val s = "..." + "a" * 32 + "error" + "a" * 31 + "...\n" + " " * 35 + "^^^^^"
    formattedErrors.head should include(s)
  }

  it should "log errors correctly" in {
    val errorCollector = new ErrorCollector("sourceCode", "fileName")
    val token = new CommonToken(1)
    token.setLine(1)
    token.setCharPositionInLine(1)
    token.setText("text")
    errorCollector.errors += ErrorDetail(1, 1, "msg", token)

    // Capture the logs
    val logger = LoggerFactory.getLogger("com.databricks.labs.remorph.parsers.ErrorCollector").asInstanceOf[Logger]
    val originalLevel = logger.getLevel
    logger.setLevel(Level.ERROR)
    val listAppender = new ListAppender[ILoggingEvent]
    listAppender.start()
    logger.addAppender(listAppender)

    // Call the method
    errorCollector.logErrors()

    // Check the logs
    val logs = listAppender.list.map(_.getFormattedMessage)
    logs.exists(log => log.startsWith("File: fileName, Line: 1")) shouldBe true

    // Reset the logger
    logger.detachAppender(listAppender)
    logger.setLevel(originalLevel)
  }
}
