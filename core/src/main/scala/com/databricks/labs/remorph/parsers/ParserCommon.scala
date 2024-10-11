package com.databricks.labs.remorph.parsers

import com.typesafe.scalalogging.LazyLogging
import org.antlr.v4.runtime.misc.Interval
import org.antlr.v4.runtime.tree.{AbstractParseTreeVisitor, ParseTree, ParseTreeVisitor, RuleNode}
import org.antlr.v4.runtime.{ParserRuleContext, RuleContext}

import scala.collection.JavaConverters._

trait ParserCommon[A] extends ParseTreeVisitor[A] with LazyLogging { self: AbstractParseTreeVisitor[A] =>
  protected def occursBefore(a: ParseTree, b: ParseTree): Boolean = {
    a != null && b != null && a.getSourceInterval.startsBeforeDisjoint(b.getSourceInterval)
  }

  def visitMany[R <: RuleContext](contexts: java.lang.Iterable[R]): Seq[A] = contexts.asScala.map(_.accept(self)).toSeq

  /**
   * <p>
   *   An implementation of this should return some type of ir.UnresolvedXYZ object that represents the
   *   unresolved input that we have no visitor for. This is used in the default visitor to wrap the
   *   unresolved input.
   * </p>
   * @param msg What message the unresolved object should contain
   * @return An instance of the type returned by the implementing visitor
   */
  protected def unresolved(msg: String): A

  protected override def defaultResult(): A = {
    unresolved(
      s"Unimplemented visitor $caller in class $implementor" +
        s" for ${contextText(currentNode.getRuleContext)}")
  }

  /**
   * <p>
   *   Creates a string representation of the text represented by the given ANTLR ParserRuleContext.
   * </p>
   * <p>
   *   Note that this should exactly reflect the original input text as bounded by the source interval
   *   recorded by the parser.
   * </p>
   */
  def contextText(ctx: RuleContext): String = ctx match {
    case ctx: ParserRuleContext =>
      ctx.start.getInputStream.getText(new Interval(ctx.start.getStartIndex, ctx.stop.getStopIndex))
    case _ => "Unsupported RuleContext type - cannot generate source string"
  }

  /**
   * Used in visitor methods when they detect that they are unable to handle some
   * part of the input, or they are placeholders for a real implementation that has not yet been
   * implemented
   * @param unparsedInput The RuleNode that we wish to indicate is unsupported right now
   * @return An  instance of the Unresolved representation of the type returned by the implementing visitor
   */
  protected def wrapUnresolvedInput(unparsedInput: RuleNode): A =
    unresolved(contextText(unparsedInput.getRuleContext))

  /**
   * <p>
   *   The default visitor needs some way to aggregate the results of visiting all children and so calls this method. In
   *   fact, we should never rely on this as there is no way to know exactly what to do in all circumstances.
   * </p>
   * <p>
   *   Note that while we have unimplemented visitors, some parts of the IR building will 'work by accident' as
   *   this method will just produce the first and only result in agg. But we should implement the missing visitor that
   *   explicitly returns the required result as it is flaky to rely on the default here
   * </p>
   * <p>
   *   We do not try and resolve what the input should actually be as that is the job of a concrete
   *   visitor.
   * </p>
   *
   * @param agg The current result as seen by the default visitor
   * @param next The next result that should somehow be aggregated to form a single result
   * @return The aggregated result from the two supplied results (accumulate error strings)
   */
  override def aggregateResult(agg: A, next: A): A =
    Option(next).getOrElse(agg)

  protected var currentNode: RuleNode = _
  protected var caller: String = _
  protected var implementor: String = _

  /**
   * Overrides the default visitChildren to report that there is an unimplemented
   * visitor def for the given RuleNode, then call the ANTLR default visitor
   * @param node the RuleNode that was not visited
   * @return T an instance of the type returned by the implementing visitor
   */
  abstract override def visitChildren(node: RuleNode): A = {
    caller = Thread.currentThread().getStackTrace()(4).getMethodName
    implementor = this.getClass.getSimpleName
    logger.warn(
      s"Unimplemented visitor for method: $caller in class: $implementor" +
        s" for: ${contextText(node.getRuleContext)}")
    currentNode = node
    super.visitChildren(node)
  }
}
