package com.databricks.labs.remorph.parsers

import org.antlr.v4.runtime.RuleContext
import org.antlr.v4.runtime.tree.{AbstractParseTreeVisitor, ParseTree}

trait ParserCommon[A] { self: AbstractParseTreeVisitor[A] =>
  protected def occursBefore(a: ParseTree, b: ParseTree): Boolean = {
    a != null && b != null && a.getSourceInterval.startsBeforeDisjoint(b.getSourceInterval)
  }

  def visitSeq(contexts: Seq[RuleContext]): Seq[A] = contexts.map(_.accept(self))
}
