package com.databricks.labs.remorph.parsers

import org.antlr.v4.runtime.tree.{ParseTreeVisitor, RuleNode}

trait IncompleteParser[T] extends ParseTreeVisitor[T] {

  protected def wrapUnresolvedInput(unparsedInput: String): T
  abstract override def visitChildren(node: RuleNode): T = {
    super.visitChildren(node) match {
      case null =>
        // TODO: getText doesn't return the original text, this reporting will have to be improved
        wrapUnresolvedInput(node.getText)
      case x => x
    }
  }
}
