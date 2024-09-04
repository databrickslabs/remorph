package com.databricks.labs.remorph.parsers

import org.antlr.v4.runtime.{RuleContext, ParserRuleContext}
import org.antlr.v4.runtime.misc.Interval
import org.antlr.v4.runtime.tree.{AbstractParseTreeVisitor, ParseTree}

import scala.collection.JavaConverters._
trait ParserCommon[A] { self: AbstractParseTreeVisitor[A] =>
  protected def occursBefore(a: ParseTree, b: ParseTree): Boolean = {
    a != null && b != null && a.getSourceInterval.startsBeforeDisjoint(b.getSourceInterval)
  }

  def visitMany[R <: RuleContext](contexts: java.lang.Iterable[R]): Seq[A] = contexts.asScala.map(_.accept(self)).toSeq

  /**
   * Creates a string representation of the text represented by the given ANTLR ParserRuleContext.
   *
   * Note that this should exactly reflect the original input text as bounded by the source interval
   * recorded by the parser.
   */
  def getTextFromParserRuleContext(ctx: ParserRuleContext): String =
    ctx.start.getInputStream.getText(new Interval(ctx.start.getStartIndex, ctx.stop.getStopIndex))
}
