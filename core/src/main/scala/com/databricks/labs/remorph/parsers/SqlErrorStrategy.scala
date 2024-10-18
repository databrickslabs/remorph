package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.SqlCommandContext
import com.databricks.labs.remorph.parsers.tsql.TSqlParser.SqlClausesContext
import org.antlr.v4.runtime._
import org.antlr.v4.runtime.misc.{IntervalSet, Pair}
import org.antlr.v4.runtime.tree.TerminalNodeImpl

import java.util
import scala.jdk.CollectionConverters._
import org.antlr.v4.runtime.misc.{Interval, IntervalSet, Pair}
import org.antlr.v4.runtime.tree.ErrorNodeImpl
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

  @throws[RecognitionException]
  override def sync(recognizer: Parser): Unit = {
    val tokens: TokenStream = recognizer.getInputStream
    val startIndex: Int = tokens.index
    val first = tokens.LT(1)
    try {
      super.sync(recognizer)
    } catch {
      case e: RecognitionException => throw e // Throw back to parser
    } finally {
      val endIndex: Int = tokens.index
      if (startIndex < endIndex) {
        val interval = new Interval(startIndex, endIndex)
        val errorToken: CommonToken = new CommonToken(
          new Pair(first.getTokenSource, first.getInputStream),
          Token.INVALID_TYPE,
          Token.DEFAULT_CHANNEL,
          first.getStartIndex,
          tokens.LT(1).getStopIndex)
        errorToken.setText(first.getInputStream.getText(interval))
        errorToken.setLine(first.getLine)
        errorToken.setCharPositionInLine(first.getCharPositionInLine)
        val errorNode = new ErrorNodeImpl(errorToken)

        // Here we add the error node to the highest level context in the tree for the particular parser,
        // so that we do not have to search for error nodes in the children of every visitor context.
        // If we added it to the current context, it would mean that every visitor method would
        // have to check for it, which would soon become unwieldy. We may come back to that though
        // if preserved skipped text is generated far away from the original text in error.
        findHighestContext(recognizer.getContext).addErrorNode(errorNode)
      }
    }
  }

  def findHighestContext(ctx: ParserRuleContext): ParserRuleContext = {
    @annotation.tailrec
    def findContext(currentCtx: ParserRuleContext): ParserRuleContext = {
      currentCtx match {
        case _: SqlClausesContext | _: SqlCommandContext => currentCtx
        case _ if currentCtx.getParent == null => currentCtx
        case _ => findContext(currentCtx.getParent.asInstanceOf[ParserRuleContext])
      }
    }

    findContext(ctx)
  }

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
