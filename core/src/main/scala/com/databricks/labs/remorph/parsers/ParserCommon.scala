package com.databricks.labs.remorph.parsers

import org.antlr.v4.runtime.RuleContext
import org.antlr.v4.runtime.tree.{AbstractParseTreeVisitor, ParseTree}
import scala.collection.JavaConverters._
trait ParserCommon[A] { self: AbstractParseTreeVisitor[A] =>
  protected def occursBefore(a: ParseTree, b: ParseTree): Boolean = {
    a != null && b != null && a.getSourceInterval.startsBeforeDisjoint(b.getSourceInterval)
  }

  def visitMany[R <: RuleContext](contexts: java.lang.Iterable[R]): Seq[A] = contexts.asScala.map(_.accept(self)).toSeq
}
