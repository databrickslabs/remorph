package com.databricks.labs.remorph.parsers

import org.antlr.v4.runtime._
import org.antlr.v4.runtime.misc.IntervalSet

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

  // Note that it is not possible to get this error from the current grammar, we would have to do an inordinate
  // amount of mocking to raise this. It isn't worth the effort.
  // $COVERAGE-OFF$
  override protected def reportNoViableAlternative(recognizer: Parser, e: NoViableAltException): Unit = {
    val tokens = recognizer.getInputStream
    var input: String = null
    if (tokens != null)
      if (e.getStartToken.getType == Token.EOF) input = "<EOF>"
      else input = tokens.getText(e.getStartToken, e.getOffendingToken)
    else input = "<unknown input>"
    val msg = new StringBuilder()
    msg.append("could not process ")
    msg.append(escapeWSAndQuote(input))
    recognizer.notifyErrorListeners(e.getOffendingToken, msg.toString(), e)
  }
  // $COVERAGE-ON$

  override protected def reportInputMismatch(recognizer: Parser, e: InputMismatchException): Unit = {
    val msg = new StringBuilder()
    msg.append(getTokenErrorDisplay(e.getOffendingToken))
    msg.append(" was unexpected ")
    msg.append(generateMessage(recognizer, e))
    msg.append("\nexpecting one of: ")
    msg.append(buildExpectedMessage(recognizer, e.getExpectedTokens))
    recognizer.notifyErrorListeners(e.getOffendingToken, msg.toString(), e)
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
