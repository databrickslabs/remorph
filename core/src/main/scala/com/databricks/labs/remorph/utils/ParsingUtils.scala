package com.databricks.labs.remorph.utils

import org.antlr.v4.runtime.misc.Interval

object ParsingUtils {

  /**
   * Creates a string representation of the text represented by the given ANTLR ParserRuleContext.
   *
   * Note that this should exactly reflect the original input text as bounded by the source interval
   * recorded by the pareser.
   */
  def getTextFromParserRuleContext(ctx: org.antlr.v4.runtime.ParserRuleContext): String =
    ctx.start.getInputStream.getText(new Interval(ctx.start.getStartIndex, ctx.stop.getStopIndex))
}
