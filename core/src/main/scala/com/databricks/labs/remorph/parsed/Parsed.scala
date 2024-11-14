package com.databricks.labs.remorph.parsed

import org.antlr.v4.runtime.{ParserRuleContext, Token}

case class ParsedLocation(line: Int, column: Int, tokenIndex: Int)

object ParsedLocation {
  val empty: ParsedLocation = ParsedLocation(-1, -1, -1)

  def fromToken(token: Token): ParsedLocation =
    ParsedLocation(token.getLine, token.getCharPositionInLine, token.getTokenIndex)
}

case class ParsedRange(start: ParsedLocation, end: ParsedLocation) {

  def isAfterLine(line: Int): Boolean = start.line > line

}

object ParsedRange {

  val empty: ParsedRange = ParsedRange(ParsedLocation.empty, ParsedLocation.empty)

  def fromParserRuleContext(ctx: ParserRuleContext): ParsedRange = {
    ParsedRange(ParsedLocation.fromToken(ctx.start), ParsedLocation.fromToken(ctx.stop))
  }
}

class ParsedNode[+A](val value: A, val range: ParsedRange) {

  override def equals(other: Any): Boolean = {
    other match {
      case parsed: ParsedNode[A] =>
        value == parsed.value
      case _ => false
    }
  }
  override def hashCode(): Int = value.hashCode()

}

object ParsedNode {

  implicit def asNode[N](parsed: ParsedNode[N]): N = parsed.value

}

