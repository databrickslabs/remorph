package com.databricks.labs.remorph.preprocessor

import com.databricks.labs.remorph.generators.sql.DataTypeGenerator.lift
import com.databricks.labs.remorph.parsers.preprocessor.DBTPreprocessorLexer
import com.databricks.labs.remorph.{OkResult, Transformation}
import org.antlr.v4.runtime.{CharStream, CommonTokenStream, Lexer, Token}

class DBTPreprocessor extends PreProcessor {

  override protected def createLexer(input: CharStream): Lexer = new DBTPreprocessorLexer(input)

  override protected def process(tokenStream: CommonTokenStream): Transformation[String] = {
    val result = new StringBuilder

    while (tokenStream.LA(1) != Token.EOF) {
      val token = tokenStream.LT(1)

      token match {
        case s if token.getType == DBTPreprocessorLexer.STATEMENT =>
          accumulate(tokenStream, result, DBTPreprocessorLexer.STATEMENT_END)
        case e if token.getType == DBTPreprocessorLexer.EXPRESSION =>
          accumulate(tokenStream, result, DBTPreprocessorLexer.EXPRESSION_END)
        case _ if token.getType == DBTPreprocessorLexer.CHAR =>
          result.append(token.getText)
        case _ =>
      }
      tokenStream.consume()
    }
    lift(OkResult(result.toString()))
  }

  private def accumulate(tokenStream: CommonTokenStream, result: StringBuilder, endType: Int): Unit = {
    var token = tokenStream.LT(1)
    while (token.getType != endType) {
      result.append(token.getText)
      tokenStream.consume()
      token = tokenStream.LT(1)
    }
  }
}
