package com.databricks.labs.remorph.parsers.intermediate

// Expression used to refer to fields, functions and similar. This can be used everywhere
// expressions in SQL appear.
abstract class Expression extends TreeNode {}

abstract class FrameType
case object UndefinedFrame extends FrameType
case object RangeFrame extends FrameType
case object RowsFrame extends FrameType

sealed trait FrameBoundary
case object CurrentRow extends FrameBoundary
case object UnboundedPreceding extends FrameBoundary
case object UnboundedFollowing extends FrameBoundary
case class PrecedingN(n: Expression) extends FrameBoundary
case class FollowingN(n: Expression) extends FrameBoundary
case object NoBoundary extends FrameBoundary
case class WindowFrame(frame_type: FrameType, lower: FrameBoundary, upper: FrameBoundary)

case class Window(
    window_function: Expression,
    partition_spec: Seq[Expression],
    sort_order: Seq[SortOrder],
    frame_spec: Option[WindowFrame])
    extends Expression {}

abstract class SortDirection
case object UnspecifiedSortDirection extends SortDirection
case object AscendingSortDirection extends SortDirection
case object DescendingSortDirection extends SortDirection

abstract class NullOrdering
case object SortNullsUnspecified extends NullOrdering
case object SortNullsFirst extends NullOrdering
case object SortNullsLast extends NullOrdering

case class SortOrder(child: Expression, direction: SortDirection, nullOrdering: NullOrdering) extends Expression {}

case class Cast(expr: Expression, dataType: DataType, type_str: String = "", returnNullOnError: Boolean = false)
    extends Expression {}

case class Decimal(value: String, precision: Option[Int], scale: Option[Int]) extends Expression {}

case class CalendarInterval(months: Int, days: Int, microseconds: Long) extends Expression {}

case class ArrayExpr(dataType: Option[DataType], elements: Seq[Literal]) extends Expression {}

case class MapExpr(key_type: DataType, value_type: DataType, keys: Seq[Literal], values: Seq[Literal])
    extends Expression {}

case class Struct(struct_type: DataType, elements: Seq[Literal]) extends Expression {}

case class Literal(
    nullType: Option[DataType] = None,
    binary: Option[Array[Byte]] = None,
    boolean: Option[Boolean] = None,
    byte: Option[Int] = None,
    short: Option[Int] = None,
    integer: Option[Int] = None,
    long: Option[Long] = None,
    float: Option[Float] = None,
    decimal: Option[Decimal] = None,
    double: Option[Double] = None,
    string: Option[String] = None,
    date: Option[Int] = None,
    timestamp: Option[Long] = None,
    timestamp_ntz: Option[Long] = None,
    calendar_interval: Option[CalendarInterval] = None,
    year_month_interval: Option[Int] = None,
    day_time_interval: Option[Long] = None,
    array: Option[ArrayExpr] = None,
    map: Option[MapExpr] = None,
    struct: Option[Struct] = None)
    extends Expression {}

case class UnresolvedAttribute(unparsed_identifier: String, plan_id: Long, is_metadata_column: Boolean)
    extends Expression {}

case class UnresolvedFunction(
    function_name: String,
    arguments: Seq[Expression],
    is_distinct: Boolean,
    is_user_defined_function: Boolean,
    has_incorrect_argc: Boolean = false)
    extends Expression {}

case class ExpressionString(expression: String) extends Expression {}

case class UnresolvedStar(unparsed_target: String) extends Expression {}

case class UnresolvedRegex(col_name: String, plan_id: Long) extends Expression {}

case class UnresolvedExtractValue(child: Expression, extraction: Expression) extends Expression {}

case class UpdateFields(struct_expression: Expression, field_name: String, value_expression: Option[Expression])
    extends Expression {}

case class Alias(expr: Expression, name: Seq[Id], metadata: Option[String]) extends Expression {}

case class LambdaFunction(function: Expression, arguments: Seq[UnresolvedNamedLambdaVariable]) extends Expression {}

case class UnresolvedNamedLambdaVariable(name_parts: Seq[String]) extends Expression {}

case class PythonUDF(output_type: DataType, eval_type: Int, command: Array[Byte], python_ver: String)
    extends Expression {}

case class ScalarScalaUDF(payload: Array[Byte], inputTypes: Seq[DataType], outputType: DataType, nullable: Boolean)
    extends Expression {}

case class JavaUDF(class_name: String, output_type: Option[DataType], aggregate: Boolean) extends Expression {}

case class CommonInlineUserDefinedFunction(
    function_name: String,
    deterministic: Boolean,
    arguments: Seq[Expression],
    python_udf: Option[PythonUDF],
    scalar_scala_udf: Option[ScalarScalaUDF],
    java_udf: Option[JavaUDF])
    extends Expression {}

case class CallFunction(function_name: String, arguments: Seq[Expression]) extends Expression {}

case class NamedArgumentExpression(key: String, value: Expression) extends Expression {}
