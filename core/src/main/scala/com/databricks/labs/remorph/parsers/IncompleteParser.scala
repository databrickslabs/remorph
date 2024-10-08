package com.databricks.labs.remorph.parsers

import com.typesafe.scalalogging.LazyLogging
import org.antlr.v4.runtime.tree.{ParseTreeVisitor, RuleNode}

trait IncompleteParser[T] extends ParseTreeVisitor[T] with LazyLogging {

  // Note that this is never called from here, but may be useful in implementing visitors
  // that recognize they are unable to handle some part of the input context they are given.
  protected def wrapUnresolvedInput(unparsedInput: RuleNode): T

  /**
   * Overrides the default visitChildren to report that there is an unimplemented
   * visitor def for the given RuleNode, then call the ANTLR default visitor
   * @param node the RuleNode that was not visited
   * @return T an instance of the type returned by the implementing visitor
   */
  abstract override def visitChildren(node: RuleNode): T = {
    val stackTrace = Thread.currentThread().getStackTrace
    val callingMethod = stackTrace(4).getMethodName
    val implementingClass = this.getClass.getSimpleName
    logger.warn(s"Unimplemented visitor for method: $callingMethod in class: $implementingClass")
    super.visitChildren(node)
  }
}
