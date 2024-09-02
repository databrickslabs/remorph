package com.databricks.labs.remorph.parsers

import org.antlr.v4.runtime.RuleContext
import org.antlr.v4.runtime.tree.{ParseTreeVisitor, RuleNode}
import com.databricks.labs.remorph.parsers.{intermediate => ir}

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
  // TODO: Merge formatContext with visitChildren to consistent formatting.
  /**
   * Formats the text of a given `ParserRuleContext` by concatenating the text of all its children nodes,
   * separated by spaces.
   *
   * @param ctx the `RuleContext` to format.
   * @return a `String` representing the concatenated text of all children nodes, separated by spaces.
   *         If the context has no children, returns an empty string.
   */
  def formatContext(contexts: RuleContext): ir.UnresolvedCommand = {
    val contextAsString = if (contexts.getChildCount == 0) {
      ""
    } else {
      val builder = new StringBuilder
      for (i <- 0 until contexts.getChildCount) {
        builder.append(contexts.getChild(i).getText)
        builder.append(" ")
      }
      builder.toString.stripSuffix(" ") // remove any trailing spaces
    }
    ir.UnresolvedCommand(contextAsString)
  }
}
