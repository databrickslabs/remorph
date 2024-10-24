package com.databricks.labs.remorph.parsers

import org.antlr.v4.runtime._
import org.antlr.v4.runtime.misc.{Interval, IntervalSet, Pair}
import org.antlr.v4.runtime.tree.ErrorNodeImpl

/**
 * Custom error strategy for SQL parsing <p> While we do not do anything super special here, we wish to override a
 * couple of the message generating methods and the token insert and delete messages, which do not create an exception
 * and don't allow us to create an error message in context. Additionally, we can now implement i18n, should that ever
 * become necessary.</p>
 *
 * <p>At the moment, we require valid SQL as input to the conversion process, but if we ever change that strategy, then
 * we can implement custom recovery steps here based upon context, though there is no improvement on the sync()
 * method.</p>
 */
abstract class SqlErrorStrategy extends DefaultErrorStrategy {

  private def createErrorNode(token: Token, text: String): ErrorNodeImpl = {
    val errorToken = new CommonToken(
      new Pair(token.getTokenSource, token.getInputStream),
      Token.INVALID_TYPE,
      Token.DEFAULT_CHANNEL,
      token.getStartIndex,
      token.getStopIndex)
    errorToken.setText(text)
    errorToken.setLine(token.getLine)
    errorToken.setCharPositionInLine(token.getCharPositionInLine)
    new ErrorNodeImpl(errorToken)
  }

  override def recover(recognizer: Parser, e: RecognitionException): Unit = {
    val tokens: TokenStream = recognizer.getInputStream
    val startIndex: Int = tokens.index
    val first = tokens.LT(1)
    super.recover(recognizer, e)
    val endIndex: Int = tokens.index
    if (startIndex < endIndex) {
      val interval = new Interval(startIndex, endIndex)
      val errorText = s"parser recovered by ignoring: ${tokens.getText(interval)}"
      val errorNode = createErrorNode(first, errorText)

      // Here we add the error node to the current context so that we can report it in the correct place
      recognizer.getContext.addErrorNode(errorNode)
    }
  }

  override protected def reportNoViableAlternative(recognizer: Parser, e: NoViableAltException): Unit = {
    val tokens = recognizer.getInputStream
    val input = if (tokens != null) {
      if (e.getStartToken.getType == Token.EOF) "<EOF>"
      else tokens.getText(e.getStartToken, e.getOffendingToken)
    } else "<unknown input>"

    val msg = new StringBuilder()
    msg.append("input is not parsable ")
    msg.append(escapeWSAndQuote(input))
    recognizer.notifyErrorListeners(e.getOffendingToken, msg.toString(), e)

    // Here we add the error node to the current context so that we can report it in the correct place
    val errorNode = createErrorNode(e.getStartToken, input)
    recognizer.getContext.addErrorNode(errorNode)
  }

  override protected def reportInputMismatch(recognizer: Parser, e: InputMismatchException): Unit = {
    val msg = new StringBuilder()
    msg.append(getTokenErrorDisplay(e.getOffendingToken))
    msg.append(" was unexpected ")
    msg.append(generateMessage(recognizer, e))
    msg.append("\nexpecting one of: ")
    msg.append(buildExpectedMessage(recognizer, e.getExpectedTokens))
    recognizer.notifyErrorListeners(e.getOffendingToken, msg.toString(), e)

    // Here we add the error node to the current context so that we can report it in the correct place
    val errorNode = createErrorNode(e.getOffendingToken, msg.toString())
    recognizer.getContext.addErrorNode(errorNode)
  }

  override protected def reportUnwantedToken(recognizer: Parser): Unit = {
    if (inErrorRecoveryMode(recognizer)) return
    beginErrorCondition(recognizer)
    val t = recognizer.getCurrentToken
    val tokenName = getTokenErrorDisplay(t)
    val expecting = getExpectedTokens(recognizer)
    val msg = new StringBuilder()
    msg.append("unexpected extra input ")
    msg.append(tokenName)
    msg.append(' ')
    msg.append(generateMessage(recognizer, new InputMismatchException(recognizer)))
    msg.append("\nexpecting one of: ")
    msg.append(buildExpectedMessage(recognizer, expecting))
    recognizer.notifyErrorListeners(t, msg.toString(), null)

    // Here we add the error node to the current context so that we can report it in the correct place
    val errorNode = createErrorNode(t, msg.toString())
    recognizer.getContext.addErrorNode(errorNode)
  }

  override protected def reportMissingToken(recognizer: Parser): Unit = {
    if (inErrorRecoveryMode(recognizer)) return

    beginErrorCondition(recognizer)
    val t = recognizer.getCurrentToken
    val expecting = getExpectedTokens(recognizer)
    val msg = new StringBuilder()
    msg.append("missing ")
    msg.append(buildExpectedMessage(recognizer, expecting))
    msg.append(" at ")
    msg.append(getTokenErrorDisplay(t))
    msg.append('\n')
    msg.append(generateMessage(recognizer, new InputMismatchException(recognizer)))
    recognizer.notifyErrorListeners(t, msg.toString(), null)

    // Here we add the error node to the current context so that we can report it in the correct place
    val errorNode = createErrorNode(t, msg.toString())
    recognizer.getContext.addErrorNode(errorNode)
  }

  val capitalizedSort: Ordering[String] = Ordering.fromLessThan((a, b) =>
    (a.exists(_.isLower), b.exists(_.isLower)) match {
      case (true, false) => true
      case (false, true) => false
      case _ => a.compareTo(b) < 0
    })

  protected def generateMessage(recognizer: Parser, e: RecognitionException): String
  protected def buildExpectedMessage(recognizer: Parser, expected: IntervalSet): String
}
