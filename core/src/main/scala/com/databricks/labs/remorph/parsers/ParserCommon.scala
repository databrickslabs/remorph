package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.{intermediate => ir}
import com.typesafe.scalalogging.LazyLogging
import org.antlr.v4.runtime.misc.Interval
import org.antlr.v4.runtime.tree._
import org.antlr.v4.runtime.{ParserRuleContext, RuleContext, Token}

import scala.collection.JavaConverters._

trait ParserCommon[A] extends ParseTreeVisitor[A] with LazyLogging { self: AbstractParseTreeVisitor[A] =>

  val vc: VisitorCoordinator

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
   * @param ruleText Which piece of source code the unresolved object represents
   * @param message What message the unresolved object should contain, such as missing visitor
   * @return An instance of the type returned by the implementing visitor
   */
  protected def unresolved(ruleText: String, message: String): A

  protected override def defaultResult(): A = {
    unresolved(contextText(currentNode.getRuleContext), s"Unimplemented visitor $caller in class $implementor")
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
  def contextText(ctx: RuleContext): String = try {
    ctx match {
      case ctx: ParserRuleContext =>
        ctx.getStart.getInputStream.getText(new Interval(ctx.getStart.getStartIndex, ctx.getStop.getStopIndex))
      case _ => "Unsupported RuleContext type - cannot generate source string"
    }
  } catch {
    // Anything that does this will have been mocked and the mockery will be huge to get the above code to work
    case _: Throwable => "Mocked string"
  }

  /**
   * <p>
   *   Returns the rule name that a particular context represents.
   * </p>
   * <p>
   *   We can do this by referencing the vocab stored in the visitor coordinator
   * </p>
   * @param ctx The context for which we want the rule name
   * @return the rule name for the context
   */
  def contextRuleName(ctx: ParserRuleContext): String =
    vc.ruleName(ctx)

  /**
   * Given a token, return its symbolic name (what it is called in the lexer)
   */
  def tokenName(tok: Token): String =
    vc.tokenName(tok)

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
    val result = super.visitChildren(node)
    result match {
      case c: ir.Unresolved[A] =>
        node match {
          case ctx: ParserRuleContext =>
            c.annotate(contextRuleName(ctx), Some(tokenName(ctx.getStart)))
        }
      case _ =>
        result
    }
  }

  /**
   * If the parser recognizes a syntax error, then it generates an ErrorNode. The ErrorNode represents unparsable text
   * and contains a manufactured token that encapsulates all the text that the parser ignored when it recovered
   * from the error. Note that if the error recovery strategy inserts a token rather than deletes one, then an
   * error node will not be created; those errors will only be reported via the ErrorCollector
   * TODO: It may be reasonable to add a check for inserted tokens and generate an error node in that case
   *
   * @param ctx the context to check for error nodes
   * @return The unresolved object representing the error and containing the text that was skipped
   */
  def errorCheck(ctx: ParserRuleContext): Option[A] = {
    val unparsedText = Option(ctx.children)
      .map(_.asScala)
      .getOrElse(Seq.empty)
      .collect { case e: ErrorNode =>
        s"Unparsable text: ${e.getSymbol.getText}"
      }
      .mkString("\n")

    if (unparsedText.nonEmpty) {
      Some(unresolved(unparsedText, "Unparsed input - ErrorNode encountered"))
    } else {
      None
    }
  }
}
