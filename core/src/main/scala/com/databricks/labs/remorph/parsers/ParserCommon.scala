package com.databricks.labs.remorph.parsers

import scala.collection.JavaConverters._
import org.antlr.v4.runtime.ParserRuleContext
import com.databricks.labs.remorph.parsers.{intermediate => ir}

import org.antlr.v4.runtime.tree.{ParseTree, ParseTreeVisitor}

trait ParserCommon extends ParseTreeVisitor[AnyRef] {
  def typedVisit[T](ctx: ParseTree): T = {
    ctx.accept(this).asInstanceOf[T]
  }

  protected def asExpressions(ctxs: java.util.List[_ <: ParserRuleContext]): Seq[ir.Expression] = {
    ctxs.asScala.map(typedVisit[ir.Expression](_))
  }

  protected def expression(ctx: ParserRuleContext): ir.Expression = typedVisit(ctx)
}
