package com.databricks.labs.remorph.parsers

import org.antlr.v4.runtime.{RuleContext}
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
   * Formats the text of a given `RuleContext` by concatenating the text of all its children nodes,
   * separated by spaces.
   *
   * @param ctx the `RuleContext` to format.
   * @return a `String` representing the concatenated text of all children nodes, separated by spaces.
   *         If the context has no children, returns an empty string.
   */
  def formatContext(contexts: RuleContext): ir.UnresolvedCommand = {
    def formatContextRecursive(ctx: RuleContext): String = {
      if (ctx.getChildCount == 0) {
        ctx.getText
      } else {
        val builder = new StringBuilder
        for (i <- 0 until ctx.getChildCount) {
          val child = ctx.getChild(i)
          if (child.isInstanceOf[RuleContext]) {
            builder.append(formatContextRecursive(child.asInstanceOf[RuleContext]))
          } else {
            builder.append(child.getText)
          }
          builder.append(" ")
        }
        // remove any trailing spaces and some regular expression
        // TODO Fix this to not include regex rather check based on Generic String Context Expression.
        builder.toString
          .stripSuffix(" ")
          .replaceAll("'\\s*(.*?)\\s*'", "'$1'")
          .replaceAll("\\s*\\(\\s*(.*?)\\s*\\)", "($1)")
      }
    }
    val contextAsString = formatContextRecursive(contexts)
    ir.UnresolvedCommand(contextAsString)
  }

}
