package com.databricks.labs.remorph.parsers.intermediate

// Expression used to refer to fields, functions and similar. This can be used everywhere
// expressions in SQL appear.
abstract class Expression extends TreeNode {}

case class Literal() extends Expression {}
case class UnresolvedAttribute() extends Expression {}
case class UnresolvedFunction() extends Expression {}
case class ExpressionString() extends Expression {}
case class UnresolvedStar() extends Expression {}
case class Alias() extends Expression {}
case class Cast() extends Expression {}
case class UnresolvedRegex() extends Expression {}
case class SortOrder() extends Expression {}
case class LambdaFunction() extends Expression {}
case class Window() extends Expression {}
case class UnresolvedExtractValue() extends Expression {}
case class UpdateFields() extends Expression {}
case class UnresolvedNamedLambdaVariable() extends Expression {}
case class CommonInlineUserDefinedFunction() extends Expression {}
case class CallFunction() extends Expression {}
case class NamedArgumentExpression() extends Expression {}