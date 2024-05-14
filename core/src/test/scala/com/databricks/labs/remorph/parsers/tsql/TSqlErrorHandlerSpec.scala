package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{ErrorDetail, ProductionErrorCollector}
import org.antlr.v4.runtime.CommonToken
import org.apache.logging.log4j.core.appender.AbstractAppender
import org.apache.logging.log4j.core.config.{Configuration, Configurator}
import org.apache.logging.log4j.core.layout.PatternLayout
import org.apache.logging.log4j.core.{LogEvent, LoggerContext}
import org.apache.logging.log4j.{Level, LogManager, Logger}
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

import scala.collection.mutable.ListBuffer

class TSqlErrorHandlerSpec extends AnyFlatSpec with Matchers {

  "ErrorCollector" should "collect syntax errors correctly" in {
    val errorCollector = new ProductionErrorCollector("sourceCode", "fileName")
    val token = new CommonToken(1)
    val recognizer: Null = null
    val e: Null = null
    errorCollector.syntaxError(recognizer, token, 1, 1, "msg", e)
    errorCollector.errors.head shouldBe ErrorDetail(1, 1, "msg", token)
  }

  it should "format errors correctly" in {
    val errorCollector = new ProductionErrorCollector("sourceCode", "fileName")
    val token = new CommonToken(1)
    token.setLine(1)
    token.setCharPositionInLine(1)
    token.setText("text")
    errorCollector.errors += ErrorDetail(1, 1, "msg", token)
    errorCollector.formatErrors.head should include("Token: text")
  }

  it should "convert errors to JSON correctly" in {
    val errorCollector = new ProductionErrorCollector("sourceCode", "fileName")
    val token = new CommonToken(1)
    token.setLine(1)
    token.setCharPositionInLine(1)
    token.setText("text")
    errorCollector.errors += ErrorDetail(1, 1, "msg", token)
    errorCollector.errorsAsJson should include("\"line\":1")
  }

  it should "count errors correctly" in {
    val errorCollector = new ProductionErrorCollector("sourceCode", "fileName")
    val token = new CommonToken(1)
    token.setLine(1)
    token.setCharPositionInLine(1)
    token.setText("text")
    errorCollector.errors += ErrorDetail(1, 1, "msg", token)
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
    errorCollector.errors += ErrorDetail(1, 40, "msg", token)

    // Call the method
    val formattedErrors = errorCollector.formatErrors

    // Check the windowing
    val s = "..." + "a" * 32 + "error" + "a" * 31 + "...\n" + " " * 35 + "^^^^^"
    formattedErrors.head should include(s)
  }

  it should "log errors correctly" in {
    val errorCollector = new ProductionErrorCollector("sourceCode", "fileName")
    val token = new CommonToken(1)
    token.setLine(1)
    token.setCharPositionInLine(1)
    token.setText("text")
    errorCollector.errors += ErrorDetail(1, 1, "msg", token)

    // Capture the logs
    val logger: Logger = LogManager.getLogger("com.databricks.labs.remorph.parsers.ErrorCollector")
    Configurator.setLevel(logger.getName, Level.ERROR)
    val layout = PatternLayout.createDefaultLayout()

    // Create a custom appender to capture the logs
    val appenderName = "CaptureAppender"
    val appender = new AbstractAppender(appenderName, null, layout, false, null) {
      val logMessages: ListBuffer[String] = ListBuffer()

      override def append(event: LogEvent): Unit = {
        logMessages += event.getMessage.getFormattedMessage
      }

      def getLogMessages: List[String] = logMessages.toList
    }
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
}
