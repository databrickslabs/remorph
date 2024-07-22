package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.parsers.ProductionErrorCollector
import com.databricks.labs.remorph.parsers.intermediate.TreeNode
import com.databricks.labs.remorph.parsers.snowflake.{SnowflakeAstBuilder, SnowflakeLexer, SnowflakeParser}
import com.databricks.labs.remorph.parsers.tsql.{TSqlAstBuilder, TSqlLexer, TSqlParser}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream, Parser}

import scala.util.control.NonFatal

trait QueryRunner {
  def runQuery(inputQuery: String, expectedTranslation: String): ReportEntryReport
}

abstract class BaseParserQueryRunner[P <: Parser] extends QueryRunner {
  protected def makeParser(input: String): P
  protected def translate(parser: P): TreeNode

  private def showUnresolvedBits(result: TreeNode): String = {
    val pattern = "Unresolved[a-zA-Z]+\\([^,)]*".r
    pattern.findAllIn(result.toString).mkString(",")
  }

  override def runQuery(inputQuery: String, expectedTranslation: String): ReportEntryReport = {
    val parser = makeParser(inputQuery)
    val errHandler = new ProductionErrorCollector(inputQuery, "")
    parser.removeErrorListeners()
    parser.addErrorListener(errHandler)
    val report = ReportEntryReport()
    try {
      val result = translate(parser)

      if (result.toString.contains("Unresolved")) {
        if (!expectedTranslation.exists(_.isLetter)) {
          // expected translation is empty, indicating that we expect to have Unresolved bits
          // in the output
          report.copy(parsed = 1, statements = 1)
        } else {
          report.copy(
            parsed = 1,
            statements = 1,
            parsing_error = Some(s"Translated query contains unresolved bits: ${showUnresolvedBits(result)}"))
        }
      } else {
        report.copy(parsed = 1, statements = 1)
      }
    } catch {
      case NonFatal(e) =>
        val formattedErrors = errHandler.formatErrors
        val msg = if (formattedErrors.nonEmpty) {
          formattedErrors.mkString("\n")
        } else {
          Option(e.getMessage).getOrElse(s"Unexpected exception of class ${e.getClass} was thrown")
        }
        report.copy(parsing_error = Some(msg))
    }
  }

}

class IsResolvedAsSnowflakeQueryRunner(astBuilder: SnowflakeAstBuilder) extends BaseParserQueryRunner[SnowflakeParser] {

  override protected def makeParser(input: String): SnowflakeParser = {
    val inputString = CharStreams.fromString(input)
    val lexer = new SnowflakeLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new SnowflakeParser(tokenStream)
    parser
  }

  override protected def translate(parser: SnowflakeParser): TreeNode = astBuilder.visit(parser.snowflakeFile())

}

class IsResolvedAsTSqlQueryRunner(astBuilder: TSqlAstBuilder) extends BaseParserQueryRunner[TSqlParser] {

  override protected def makeParser(input: String): TSqlParser = {
    val inputString = CharStreams.fromString(input)
    val lexer = new TSqlLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new TSqlParser(tokenStream)
    parser
  }

  override protected def translate(parser: TSqlParser): TreeNode = astBuilder.visit(parser.tSqlFile())

}
