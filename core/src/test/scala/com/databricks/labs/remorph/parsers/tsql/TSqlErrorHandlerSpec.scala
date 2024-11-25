package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.intermediate.ParsingError
import com.databricks.labs.remorph.parsers.{DefaultErrorCollector, EmptyErrorCollector, ProductionErrorCollector}
import org.antlr.v4.runtime.CommonToken
import org.apache.logging.log4j.core.appender.AbstractAppender
import org.apache.logging.log4j.core.config.{Configuration, Configurator}
import org.apache.logging.log4j.core.layout.PatternLayout
import org.apache.logging.log4j.core.{LogEvent, LoggerContext}
import org.apache.logging.log4j.{Level, LogManager, Logger}
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

import java.io.{ByteArrayOutputStream, PrintStream}
import scala.collection.mutable.ListBuffer

class ListBufferAppender(appenderName: String, layout: PatternLayout)
    extends AbstractAppender(appenderName, null, layout, false, null) {
  val logMessages: ListBuffer[String] = ListBuffer()

  override def append(event: LogEvent): Unit = {
    logMessages += event.getMessage.getFormattedMessage
  }

  def getLogMessages: List[String] = logMessages.toList
}

class TSqlErrorHandlerSpec extends AnyFlatSpec with Matchers {

  "ErrorCollector" should "collect syntax errors correctly" in {
    val errorCollector = new ProductionErrorCollector("sourceCode", "fileName")
    val token = new CommonToken(1)
    errorCollector.syntaxError(null, token, 1, 1, "msg", null)
    errorCollector.errors.head shouldBe ParsingError(
      1,
      1,
      "msg",
      1,
      null,
      "unresolved token name",
      "unresolved rule name")
  }

  it should "format errors correctly" in {
    val errorCollector = new ProductionErrorCollector("sourceCode", "fileName")
    val token = new CommonToken(1)
    token.setLine(1)
    token.setCharPositionInLine(1)
    token.setText("text")
    errorCollector.errors += ParsingError(1, 1, "msg", 4, "text", "unresolved token name", "unresolved rule name")
    errorCollector.formatErrors.head should include("Token: text")
  }

  it should "convert errors to JSON correctly" in {
    val errorCollector = new ProductionErrorCollector("sourceCode", "fileName")
    val token = new CommonToken(1)
    token.setLine(1)
    token.setCharPositionInLine(1)
    token.setText("text")
    errorCollector.errors += ParsingError(1, 1, "msg", 4, "text", "unresolved token name", "unresolved rule name")
    errorCollector.errorsAsJson should include("starting at 1:1")
    errorCollector.errorsAsJson should include("'unresolved rule name'")
    errorCollector.errorsAsJson should include("'text'")
    errorCollector.errorsAsJson should include("(unresolved token name)")
    errorCollector.errorsAsJson should include("msg")
  }

  it should "count errors correctly" in {
    val errorCollector = new ProductionErrorCollector("sourceCode", "fileName")
    val token = new CommonToken(1)
    token.setLine(1)
    token.setCharPositionInLine(1)
    token.setText("text")
    errorCollector.errors += ParsingError(1, 1, "msg", 4, "text", "unresolved token name", "unresolved rule name")
    errorCollector.errorCount shouldBe 1
  }

  it should "window long lines correctly" in {
    val longLine = "a" * 40 + "error" + "a" * 40
    val errorCollector = new ProductionErrorCollector(longLine, "fileName")
    val token = new CommonToken(1)
    token.setLine(1)
    token.setCharPositionInLine(40)
    token.setStartIndex(40)
    token.setStopIndex(44)
    token.setText("error")
    errorCollector.errors += ParsingError(1, 40, "msg", 5, "error", "unresolved token name", "unresolved rule name")

    // Call the method
    val formattedErrors = errorCollector.formatErrors

    // Check the windowing
    val s = "..." + "a" * 34 + "error" + "a" * 35 + "...\n" + " " * 37 + "^^^^^"
    formattedErrors.head should include(s)
  }

  it should "log errors correctly" in {
    val errorCollector = new ProductionErrorCollector("sourceCode", "fileName")
    val token = new CommonToken(1)
    token.setLine(1)
    token.setCharPositionInLine(1)
    token.setText("text")
    errorCollector.errors += ParsingError(1, 1, "msg", 4, "text", "unresolved token name", "unresolved rule name")

    // Capture the logs
    val logger: Logger = LogManager.getLogger("com.databricks.labs.remorph.parsers.ErrorCollector")
    Configurator.setLevel(logger.getName, Level.ERROR)
    val layout = PatternLayout.createDefaultLayout()

    // Create a custom appender to capture the logs
    val appenderName = "CaptureAppender"
    val appender = new ListBufferAppender(appenderName, layout)
    appender.start()

    val context: LoggerContext = LogManager.getContext(false).asInstanceOf[LoggerContext]
    val config: Configuration = context.getConfiguration

    config.addAppender(appender)
    // Get the logger config
    val loggerConfig = config.getLoggerConfig(logger.getName)

    // Add the appender to the logger and set additivity to false
    loggerConfig.addAppender(appender, null, null)
    loggerConfig.setAdditive(false)

    // Update the logger context with the new configuration
    context.updateLoggers()

    // Call the method
    errorCollector.logErrors()

    // Check the logs
    val logs = appender.getLogMessages
    logs.exists(log => log.contains("File: fileName, Line: 1")) shouldBe true
  }

  it should "capture syntax errors correctly using syntaxError method" in {
    val errorCollector = new ProductionErrorCollector("sourceCode", "fileName")
    errorCollector.reset()
    val token = new CommonToken(1)
    token.setLine(10)
    token.setCharPositionInLine(5)
    token.setStartIndex(42)
    token.setStopIndex(50)
    token.setText("errorText")

    errorCollector.syntaxError(null, token, 10, 5, "Syntax error message", null)

    errorCollector.errorCount shouldBe 1
    errorCollector.errors should contain(
      ParsingError(10, 5, "Syntax error message", 9, "errorText", "unresolved token name", "unresolved rule name"))
  }

  def captureStdErr[T](block: => T): (T, String) = {
    val originalErr = System.err
    val errContent = new ByteArrayOutputStream()
    val printStream = new PrintStream(errContent)
    System.setErr(printStream)
    try {
      val result = block
      printStream.flush()
      (result, errContent.toString)
    } finally {
      System.setErr(originalErr)
    }
  }

  it should "capture syntax errors correctly using the default syntaxError method" in {
    val errorCollector = new DefaultErrorCollector()
    errorCollector.reset()
    val token = new CommonToken(1)
    token.setLine(10)
    token.setCharPositionInLine(5)
    token.setText("errorText")
    val (_, capturedErr) = captureStdErr {
      errorCollector.syntaxError(
        null,
        token,
        10,
        5,
        "Ignore this Syntax error message - it is supposed to be here",
        null)
    }
    errorCollector.errorCount shouldBe 1
    capturedErr should include("Ignore this Syntax error message")
  }

  it should "have sensible defaults" in {
    val errorCollector = new EmptyErrorCollector()
    errorCollector.errorCount shouldBe 0
    errorCollector.logErrors()
    errorCollector.reset()
    errorCollector.errorCount shouldBe 0
    errorCollector.formatErrors shouldBe List()
    errorCollector.errorsAsJson shouldBe "{}"
  }
}
