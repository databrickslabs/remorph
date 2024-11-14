package com.databricks.labs.remorph.preprocessor.dbt

import com.databricks.labs.remorph.generators.sql.DataTypeGenerator.lift
import com.databricks.labs.remorph.intermediate.Origin
import com.databricks.labs.remorph.parsers.preprocessor.DBTPreprocessorLexer
import com.databricks.labs.remorph.preprocessor.PreProcessor
import com.databricks.labs.remorph.preprocessor.jinga.{CommentElement, ExpressionElement, StatementElement, TemplateManager}
import com.databricks.labs.remorph.{OkResult, Transformation}
import org.antlr.v4.runtime.misc.Interval
import org.antlr.v4.runtime.{CharStream, CommonTokenStream, Lexer, Token}

class DBTPreprocessor extends PreProcessor {

  val templateManager = new TemplateManager()

  override protected def createLexer(input: CharStream): Lexer = new DBTPreprocessorLexer(input)

  override protected def process(tokenStream: CommonTokenStream): Transformation[String] = {
    val result = new StringBuilder

    while (tokenStream.LA(1) != Token.EOF) {
      val token = tokenStream.LT(1)

      // TODO: Line statements and comments
      token match {
        case _ if token.getType == DBTPreprocessorLexer.STATEMENT =>
          accumulate(tokenStream, result, DBTPreprocessorLexer.STATEMENT_END)
        case _ if token.getType == DBTPreprocessorLexer.EXPRESSION =>
          accumulate(tokenStream, result, DBTPreprocessorLexer.EXPRESSION_END)
        case _ if token.getType == DBTPreprocessorLexer.COMMENT =>
          accumulate(tokenStream, result, DBTPreprocessorLexer.COMMENT_END)
        case _ if token.getType == DBTPreprocessorLexer.C =>
          result.append(token.getText)
          tokenStream.consume()
        case _ if token.getType == DBTPreprocessorLexer.WS =>
          result.append(token.getText)
          tokenStream.consume()
        case _ => // Mismatched template tokens - give an error here
      }
    }
    lift(OkResult(result.toString()))
  }

  private def accumulate(tokenStream: CommonTokenStream, result: StringBuilder, endType: Int): Unit = {

    // Was there any preceding whitespace? We need to know if this template element was specified like this:
    //   sometext_{{ expression }}
    val precedingWhitespace = hasSpace(tokenStream, -1)

    val start = tokenStream.LT(1)
    var token = start
    do {
      tokenStream.consume()
      token = tokenStream.LT(1)
    } while (token.getType != endType)
    tokenStream.consume()
    val span = new Interval(start.getStartIndex, token.getStopIndex)
    val text = tokenStream.getText(span)
    val followingWhitespace = hasSpace(tokenStream, 1)

    val origin =
      new Origin(
        Some(start.getLine),
        Some(start.getCharPositionInLine),
        Some(start.getStartIndex),
        Some(token.getStopIndex),
        Some(text))
    val template = endType match {
      case DBTPreprocessorLexer.STATEMENT_END =>
        StatementElement(origin, text, precedingWhitespace, followingWhitespace)
      case DBTPreprocessorLexer.EXPRESSION_END =>
        ExpressionElement(origin, text, precedingWhitespace, followingWhitespace)
      case DBTPreprocessorLexer.COMMENT_END =>
        CommentElement(origin, text, precedingWhitespace, followingWhitespace)
    }
    val templateRef = templateManager.add(template)
    result.append(templateRef)
  }

  private def hasSpace(tokenStream: CommonTokenStream, index: Int): Boolean = {
    Option(tokenStream.LT(index)) match {
      case None => false
      case Some(s) if s.getType == DBTPreprocessorLexer.WS => true
      case _ => false
    }
  }
}
