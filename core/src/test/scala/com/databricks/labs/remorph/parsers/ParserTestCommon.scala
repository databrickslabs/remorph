package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.{intermediate => ir}
import org.antlr.v4.runtime._
import org.antlr.v4.runtime.tree.ParseTreeVisitor
import org.scalatest.{Assertion, Assertions}

trait ParserTestCommon[P <: Parser] extends PlanComparison { self: Assertions =>

  protected def makeLexer(chars: CharStream): TokenSource
  protected def makeParser(tokens: TokenStream): P
  protected def makeErrStrategy(): SqlErrorStrategy
  protected def makeErrListener(chars: String): ErrorCollector = new DefaultErrorCollector
  protected def astBuilder: ParseTreeVisitor[_]
  protected var errListener: ErrorCollector = _

  protected def parseString[R <: RuleContext](input: String, rule: P => R): R = {
    val inputString = CharStreams.fromString(input)
    val lexer = makeLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = makeParser(tokenStream)
    errListener = makeErrListener(input)
    parser.removeErrorListeners()
    parser.addErrorListener(errListener)
    parser.setErrorHandler(makeErrStrategy())
    val tree = rule(parser)

    // uncomment the following line if you need a peek in the Snowflake/TSQL AST
    // println(tree.toStringTree(parser))
    tree
  }

  protected def example[R <: RuleContext](
      query: String,
      rule: P => R,
      expectedAst: ir.LogicalPlan,
      failOnErrors: Boolean = true): Unit = {
    val sfTree = parseString(query, rule)
    if (errListener != null && errListener.errorCount != 0) {
      errListener.logErrors()
      if (failOnErrors) {
        fail(s"${errListener.errorCount} errors found in the child string")
      }
    }

    val result = astBuilder.visit(sfTree)
    comparePlans(expectedAst, result.asInstanceOf[ir.LogicalPlan])
  }

  protected def exampleExpr[R <: RuleContext](query: String, rule: P => R, expectedAst: ir.Expression): Unit = {
    val sfTree = parseString(query, rule)
    if (errListener != null && errListener.errorCount != 0) {
      errListener.logErrors()
      fail(s"${errListener.errorCount} errors found in the child string")
    }
    val result = astBuilder.visit(sfTree)
    val wrapExpr = (expr: ir.Expression) => ir.Filter(ir.NoopNode, expr)
    comparePlans(wrapExpr(expectedAst), wrapExpr(result.asInstanceOf[ir.Expression]))
  }

  /**
   * Used to pass intentionally bad syntax to the parser and check that it fails with an expected error
   * @param query
   * @param rule
   * @tparam R
   * @return
   */
  protected def checkError[R <: RuleContext](query: String, rule: P => R, errContains: String): Assertion = {
    parseString(query, rule)
    if (errListener != null && errListener.errorCount == 0) {
      fail(s"Expected an error in the child string\n$query\nbut no errors were found")
    }

    val errors = errListener.formatErrors
    assert(
      errors.exists(_.contains(errContains)),
      s"Expected error containing '$errContains' but got:\n${errors.mkString("\n")}")
  }

}
