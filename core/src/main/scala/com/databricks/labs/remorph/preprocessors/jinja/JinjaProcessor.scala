package com.databricks.labs.remorph.preprocessors.jinja

import com.databricks.labs.remorph._
import com.databricks.labs.remorph.intermediate.{Origin, PreParsingError, RemorphErrors}
import com.databricks.labs.remorph.parsers.preprocessor.DBTPreprocessorLexer
import com.databricks.labs.remorph.preprocessors.Processor
import org.antlr.v4.runtime._

import scala.collection.mutable.ListBuffer

class JinjaProcessor extends Processor {

  val templateManager = new TemplateManager()

  override protected def createLexer(input: CharStream): Lexer = new DBTPreprocessorLexer(input)

  override def preprocess(input: String): Transformation[String] = {

    val inputString = CharStreams.fromString(input)
    val tokenizer = createLexer(inputString)
    val tokenStream = new CommonTokenStream(tokenizer)

    val errors: ListBuffer[PreParsingError] = ListBuffer()
    val result = new StringBuilder

    while (tokenStream.LA(1) != Token.EOF) {
      val token = tokenStream.LT(1)

      // TODO: Line statements and comments
      token.getType match {
        case DBTPreprocessorLexer.STATEMENT =>
          result.append(buildElement(tokenStream, DBTPreprocessorLexer.STATEMENT_END))
        case DBTPreprocessorLexer.EXPRESSION =>
          result.append(buildElement(tokenStream, DBTPreprocessorLexer.EXPRESSION_END))
        case DBTPreprocessorLexer.COMMENT =>
          result.append(buildElement(tokenStream, DBTPreprocessorLexer.COMMENT_END))
        case DBTPreprocessorLexer.C =>
          result.append(token.getText)
          tokenStream.consume()
        case DBTPreprocessorLexer.WS =>
          result.append(token.getText)
          tokenStream.consume()
        case _ =>
          errors.append(
            PreParsingError(
              token.getLine,
              token.getCharPositionInLine,
              token.getText,
              "Malformed template element was unexpected"))
      }
    }
    if (errors.nonEmpty) {
      lift(PartialResult(result.toString(), RemorphErrors(errors.toList)))
    } else {
      ok(result.toString())
    }
  }

  def post(input: String): Transformation[String] = {
    val processedResult = templateManager.rebuild(input)
    lift(OkResult(processedResult))
  }

  /**
   * Accumulates tokens from the token stream into the template element, while building a regex to match the template element.
   * It handles preceding and trailing whitespace, and optionally elides trailing commas.
   * An accumulated template definition is added to the template manager, and it returns the placeholder name
   * of the template to be used instead of the raw template text.
   *
   * @param tokenStream the token stream to process
   * @param endType the token type that signifies the end of the template element
   */
  private def buildElement(tokenStream: CommonTokenStream, endType: Int): String = {

    // Builds the regex that matches the template element
    val regex = new StringBuilder

    // Was there any preceding whitespace? We need to know if this template element was specified like this:
    //   sometext_{{ expression }}
    // or like this:
    //   sometext_ {{ expression }}
    //
    // So that our regular expression can elide any whitespace that was inserted by the SQL generator
    if (!hasSpace(tokenStream, -1)) {
      regex.append("[\t\f ]*")
    }

    // Preserve new lines etc in the template text as it is much easier than doing this at replacement time
    val preText = preFix(tokenStream, -1)

    val start = tokenStream.LT(1)
    var token = start
    do {
      tokenStream.consume()
      token = tokenStream.LT(1)
    } while (token.getType != endType)
    tokenStream.consume()

    // What is the next template placeholder?
    val templateKey = templateManager.nextKey
    regex.append(templateKey)

    // If there is no trailing space following the template element definition, then we need to elide any
    // that are inserted by the SQL generator
    if (!hasSpace(tokenStream, 1)) {
      regex.append("[\t\f ]*")
    }

    // If there is no trailing comma after the template element definition, then we need to elide any
    // that are automatically inserted by the SQL generator - we therefore match any whitespace and newlines
    // and just delete them, because the postfix will accumulate the original whitespace and newlines in the
    // template text
    if (!hasTrailingComma(tokenStream, 1)) {
      regex.append("[\n\t\f ]*[,]?[ ]?")
    }

    // Preserve new lines and space in the template text as it is much easier than doing this at replacement time
    val text = preText + tokenStream.getText(start, token) + postFix(tokenStream, 1)

    val origin =
      Origin(
        Some(start.getLine),
        Some(start.getCharPositionInLine),
        Some(start.getStartIndex),
        Some(token.getStopIndex),
        Some(text))
    val template = endType match {
      case DBTPreprocessorLexer.STATEMENT_END =>
        StatementElement(origin, text, regex.toString())
      case DBTPreprocessorLexer.EXPRESSION_END =>
        ExpressionElement(origin, text, regex.toString())
      case DBTPreprocessorLexer.COMMENT_END =>
        CommentElement(origin, text, regex.toString())
    }
    templateManager.add(templateKey, template)
    templateKey
  }

  /**
   * Checks if the token at the specified index in the token stream is a whitespace token.
   *
   * @param tokenStream the token stream to check
   * @param index the index of the token to check
   * @return true if the token at the specified index is a whitespace token, false otherwise
   */
  private def hasSpace(tokenStream: CommonTokenStream, index: Int): Boolean =
    Option(tokenStream.LT(index)) match {
      case None => false
      case Some(s) if s.getType == DBTPreprocessorLexer.WS => true
      case _ => false
    }

  /**
   * Accumulates preceding whitespace and newline tokens from the given index in the token stream.
   *
   * @param tokenStream the token stream to search backwards from (inclusive)
   * @param index the starting index in the token stream
   * @return a string containing the accumulated whitespace and newline tokens
   */
  private def preFix(tokenStream: CommonTokenStream, index: Int): String = {
    val builder = new StringBuilder
    var token = tokenStream.LT(index)
    var i = 1
    while (token != null && (token.getType == DBTPreprocessorLexer.WS || token.getText == "\n")) {
      builder.insert(0, token.getText)
      token = tokenStream.LT(index - i)
      i += 1
    }

    // We do not accumulate the prefix if the immediately preceding context was another
    // template element as that template will have accumulated the whitespace etc in its
    // postfix
    if (token != null && (token.getType == DBTPreprocessorLexer.STATEMENT_END ||
        token.getType == DBTPreprocessorLexer.EXPRESSION_END ||
        token.getType == DBTPreprocessorLexer.COMMENT_END)) {
      ""
    } else {
      builder.toString()
    }
  }

  /**
   * Accumulates trailing whitespace and newline tokens from the given index in the token stream.
   *
   * @param tokenStream the token stream to search forwards from (inclusive)
   * @param index the starting index in the token stream
   * @return a string containing the accumulated whitespace and newline tokens
   */
  private def postFix(tokenStream: CommonTokenStream, index: Int): String = {
    val builder = new StringBuilder
    var token = tokenStream.LT(index)
    while (token != null && (token.getType == DBTPreprocessorLexer.WS || token.getText == "\n")) {
      builder.append(token.getText)
      token = tokenStream.LT(index + builder.length)
    }
    builder.toString()
  }

  private def hasTrailingComma(tokenStream: CommonTokenStream, index: Int): Boolean = {
    var token = tokenStream.LT(index)
    var i = 1
    while (token != null && (token.getType == DBTPreprocessorLexer.WS || token.getText == "\n")) {
      token = tokenStream.LT(index + i)
      i += 1
    }
    token != null && token.getText == ","
  }
}
