package com.databricks.labs.remorph.preprocessors.jinja

import com.databricks.labs.remorph._
import com.databricks.labs.remorph.intermediate.Origin
import com.databricks.labs.remorph.parsers.preprocessor.DBTPreprocessorLexer
import com.databricks.labs.remorph.preprocessors.Processor
import org.antlr.v4.runtime._

class JinjaProcessor extends Processor {

  val templateManager = new TemplateManager()

  override protected def createLexer(input: CharStream): Lexer = new DBTPreprocessorLexer(input)

  override def pre(input: PreProcessing): Transformation[Parsing] = {

    val inputString = CharStreams.fromString(input.source)
    val tokenizer = createLexer(inputString)
    val tokenStream = new CommonTokenStream(tokenizer)

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
        case _ => // TODO: Mismatched template tokens - accumulate error for partial result
      }
    }
    update { case _ => input }.flatMap(_ => lift(OkResult(Parsing(result.toString(), input.filename))))
  }

  def post(input: String): Transformation[String] = {
    val processedResult = templateManager.rebuild(input)
    lift(OkResult(processedResult))
  }

  /**
   * Accumulates tokens from the token stream into the result, building a regex to match the template element.
   * It handles preceding and trailing whitespace, and optionally elides trailing commas.
   *
   * @param tokenStream the token stream to process
   * @param result the StringBuilder to accumulate the placeholder into
   * @param endType the token type that signifies the end of the template element
   */
  private def accumulate(tokenStream: CommonTokenStream, result: StringBuilder, endType: Int): Unit = {

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
    val templateRef = templateManager.add(templateKey, template)
    result.append(templateRef)
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
