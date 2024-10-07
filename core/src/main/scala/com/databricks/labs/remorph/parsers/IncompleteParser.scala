package com.databricks.labs.remorph.parsers

import com.typesafe.scalalogging.LazyLogging
import org.antlr.v4.runtime.tree.{ParseTreeVisitor, RuleNode}

trait IncompleteParser[T] extends ParseTreeVisitor[T] with LazyLogging {

  protected def wrapUnresolvedInput(unparsedInput: RuleNode): T

  /**
   * If a visitor returns null then we wrap the unparsed input in an UnresolvedInput
   * @param unparsedInput the RuleNode that was not visited
   * @return T an instance of the type returned by the implementing visitor
   */
  abstract override def visitChildren(node: RuleNode): T = {
    val stackTrace = Thread.currentThread().getStackTrace
    val callingMethod = stackTrace(2).getMethodName // Adjust the index if necessary
    logger.warn(s"Unimplemented visitor for method: $callingMethod")
    super.visitChildren(node) match {
      case null =>
        wrapUnresolvedInput(node)
      case x => x
    }
  }
}
