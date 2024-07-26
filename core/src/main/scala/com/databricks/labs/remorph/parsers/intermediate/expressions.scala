package com.databricks.labs.remorph.parsers.intermediate

import java.util.{Locale, UUID}

// Expression used to refer to fields, functions and similar. This can be used everywhere
// expressions in SQL appear.
abstract class Expression extends TreeNode[Expression] {
  lazy val resolved: Boolean = childrenResolved

  def dataType: DataType

  def childrenResolved: Boolean = children.forall(_.resolved)

  def references: AttributeSet = new AttributeSet(children.flatMap(_.references): _*)
}

/** Expression without any child expressions */
abstract class LeafExpression extends Expression {
  override final def children: Seq[Expression] = Nil
}

object NamedExpression {
  private val curId = new java.util.concurrent.atomic.AtomicLong()
  private[intermediate] val jvmId = UUID.randomUUID()
  def newExprId: ExprId = ExprId(curId.getAndIncrement(), jvmId)
  def unapply(expr: NamedExpression): Option[(String, DataType)] = Some((expr.name, expr.dataType))
}

case class ExprId(id: Long, jvmId: UUID) {
  override def hashCode(): Int = id.hashCode()
  override def equals(other: Any): Boolean = other match {
    case ExprId(id, jvmId) => this.id == id && this.jvmId == jvmId
    case _ => false
  }
}

object ExprId {
  def apply(id: Long): ExprId = ExprId(id, NamedExpression.jvmId)
}

trait NamedExpression extends Expression {
  def name: String
  def exprId: ExprId

  /**
   * Returns a dot separated fully qualified name for this attribute. Given that there can be multiple qualifiers, it is
   * possible that there are other possible way to refer to this attribute.
   */
  def qualifiedName: String = (qualifier :+ name).mkString(".")

  /**
   * Optional qualifier for the expression. Qualifier can also contain the fully qualified information, for e.g,
   * Sequence of string containing the database and the table name
   *
   * For now, since we do not allow using original table name to qualify a column name once the table is aliased, this
   * can only be:
   *
   *   1. Empty Seq: when an attribute doesn't have a qualifier, e.g. top level attributes aliased in the SELECT clause,
   *      or column from a LocalRelation. 2. Seq with a Single element: either the table name or the alias name of the
   *      table. 3. Seq with 2 elements: database name and table name 4. Seq with 3 elements: catalog name, database
   *      name and table name
   */
  def qualifier: Seq[String]

  def toAttribute: Attribute

  /** Returns a copy of this expression with a new `exprId`. */
  def newInstance(): NamedExpression
}

class AttributeSet(val attrs: NamedExpression*) extends Set[NamedExpression] {
  def this(attrs: Set[NamedExpression]) = this(attrs.toSeq: _*)

  override def iterator: Iterator[NamedExpression] = attrs.iterator

  override def +(elem: NamedExpression): AttributeSet = new AttributeSet(attrs :+ elem: _*)

  override def -(elem: NamedExpression): AttributeSet = new AttributeSet(attrs.filterNot(_ == elem): _*)

  def --(other: AttributeSet): AttributeSet = new AttributeSet(attrs.filterNot(other.contains): _*)

  override def contains(key: NamedExpression): Boolean = attrs.contains(key)
}

abstract class Attribute extends LeafExpression with NamedExpression {

  @transient
  override lazy val references: AttributeSet = new AttributeSet(this)

  override def toAttribute: Attribute = this
}

case class AttributeReference(
    name: String,
    dataType: DataType,
    nullable: Boolean = true,
    exprId: ExprId = NamedExpression.newExprId,
    qualifier: Seq[String] = Seq.empty[String])
    extends Attribute {
  override def newInstance(): NamedExpression = copy(exprId = NamedExpression.newExprId)
}

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
    extends Expression {
  override def children: Seq[Expression] = window_function +: partition_spec
  override def dataType: DataType = window_function.dataType
}

abstract class SortDirection
case object UnspecifiedSortDirection extends SortDirection
case object AscendingSortDirection extends SortDirection
case object DescendingSortDirection extends SortDirection

abstract class NullOrdering
case object SortNullsUnspecified extends NullOrdering
case object SortNullsFirst extends NullOrdering
case object SortNullsLast extends NullOrdering

case class SortOrder(child: Expression, direction: SortDirection, nullOrdering: NullOrdering) extends Expression {
  override def children: Seq[Expression] = child :: Nil
  override def dataType: DataType = child.dataType
}

/** cast(expr AS type) - Casts the value `expr` to the target data type `type`. */
case class Cast(
    expr: Expression,
    dataType: DataType,
    type_str: String = "",
    returnNullOnError: Boolean = false,
    timeZoneId: Option[String] = None)
    extends Unary(expr)

case class Decimal(value: String, precision: Option[Int], scale: Option[Int]) extends LeafExpression {
  override def dataType: DataType = DecimalType(precision, scale)
}

case class CalendarInterval(months: Int, days: Int, microseconds: Long) extends LeafExpression {
  override def dataType: DataType = CalendarIntervalType
}

case class ArrayExpr(dataType: DataType, elements: Seq[Expression]) extends Expression {
  override def children: Seq[Expression] = elements
}

case class JsonExpr(dataType: DataType, fields: Seq[(String, Literal)]) extends Expression {
  override def children: Seq[Expression] = fields.map(_._2)
}

case class MapExpr(key_type: DataType, value_type: DataType, keys: Seq[Literal], values: Seq[Expression])
    extends Expression {
  override def children: Seq[Expression] = keys ++ values
  override def dataType: DataType = MapType(key_type, value_type)
}

case class Struct(dataType: DataType, elements: Seq[Literal]) extends Expression {
  override def children: Seq[Expression] = elements
}

object Literal {
  def apply(value: Array[Byte]): Literal = Literal(binary = Some(value))
  def apply(value: Boolean): Literal = Literal(boolean = Some(value))
  def apply(value: Byte): Literal = Literal(byte = Some(value.intValue()))
  def apply(value: Short): Literal = Literal(short = Some(value.intValue()))
  def apply(value: Int): Literal = Literal(integer = Some(value))
  def apply(value: Long): Literal = Literal(long = Some(value))
  def apply(value: Float): Literal = Literal(float = Some(value))
  def apply(value: Decimal): Literal = Literal(decimal = Some(value))
  def apply(value: Double): Literal = Literal(double = Some(value))
  def apply(value: String): Literal = Literal(string = Some(value))
  def apply(value: java.sql.Date): Literal = Literal(date = Some(value.getTime))
  def apply(value: java.sql.Timestamp): Literal = Literal(timestamp = Some(value.getTime))
  def apply(value: Map[String, Expression]): Literal = Literal(map = Some(
    MapExpr(
      StringType,
      value.values.head.dataType,
      value.keys.map(key => Literal(string = Some(key))).toSeq,
      value.values.toSeq)))
  def apply(values: Seq[Expression]): Literal =
    Literal(array = Some(ArrayExpr(values.headOption.map(_.dataType).getOrElse(UnresolvedType), values)))
}

case class Literal(
    // TODO enhance to respect the datatype when defined in combination with datatypes.
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
    date: Option[Long] = None,
    timestamp: Option[Long] = None,
    timestamp_ntz: Option[Long] = None,
    calendar_interval: Option[CalendarInterval] = None,
    year_month_interval: Option[Int] = None,
    day_time_interval: Option[Long] = None,
    array: Option[ArrayExpr] = None,
    map: Option[MapExpr] = None,
    json: Option[JsonExpr] = None)
    extends LeafExpression {

  override def dataType: DataType = {
    this match {
      case _ if binary.isDefined => BinaryType
      case _ if boolean.isDefined => BooleanType
      case _ if byte.isDefined => ByteType(byte)
      case _ if short.isDefined => ShortType
      case _ if integer.isDefined => IntegerType
      case _ if long.isDefined => LongType
      case _ if float.isDefined => FloatType
      case _ if decimal.isDefined => DecimalType(decimal.get.precision, decimal.get.scale)
      case _ if double.isDefined => DoubleType
      case _ if string.isDefined => StringType
      case _ if date.isDefined => DateType
      case _ if timestamp.isDefined => TimestampType
      case _ if timestamp_ntz.isDefined => TimestampNTZType
      case _ if calendar_interval.isDefined => CalendarIntervalType
      case _ if year_month_interval.isDefined => YearMonthIntervalType
      case _ if day_time_interval.isDefined => DayTimeIntervalType
      case _ if array.isDefined => ArrayType(array.map(_.dataType).getOrElse(UnresolvedType))
      case _ if map.isDefined =>
        MapType(map.map(_.key_type).getOrElse(UnresolvedType), map.map(_.value_type).getOrElse(UnresolvedType))
      case _ if json.isDefined => UDTType()
      case _ => NullType
    }
  }
}

case class UnresolvedAttribute(unparsed_identifier: String, plan_id: Long = 0, is_metadata_column: Boolean = false)
    extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}

case class UnresolvedFunction(
    function_name: String,
    arguments: Seq[Expression],
    is_distinct: Boolean,
    is_user_defined_function: Boolean,
    has_incorrect_argc: Boolean = false)
    extends Expression {
  override def children: Seq[Expression] = arguments
  override def dataType: DataType = UnresolvedType
}

// TODO: remove this type
case class ExpressionString(expression: String) extends LeafExpression {
  override def dataType: DataType = StringType
}

case class UnresolvedStar(unparsed_target: String) extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}

case class UnresolvedRegex(col_name: String, plan_id: Long) extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}

case class UnresolvedExtractValue(child: Expression, extraction: Expression) extends Expression {
  override def children: Seq[Expression] = child :: extraction :: Nil
  override def dataType: DataType = UnresolvedType
}

case class UpdateFields(struct_expression: Expression, field_name: String, value_expression: Option[Expression])
    extends Expression {
  override def children: Seq[Expression] = struct_expression :: value_expression.toList
  override def dataType: DataType = UnresolvedType // TODO: Fix this
}

case class Alias(expr: Expression, name: Seq[Id], metadata: Option[String]) extends Expression {
  override def children: Seq[Expression] = expr :: Nil
  override def dataType: DataType = expr.dataType
}

case class LambdaFunction(function: Expression, arguments: Seq[UnresolvedNamedLambdaVariable]) extends Expression {
  override def children: Seq[Expression] = function +: arguments
  override def dataType: DataType = UnresolvedType // TODO: Fix this
}

case class UnresolvedNamedLambdaVariable(name_parts: Seq[String]) extends Expression {
  override def children: Seq[Expression] = Nil
  override def dataType: DataType = UnresolvedType
}

case class PythonUDF(output_type: DataType, eval_type: Int, command: Array[Byte], python_ver: String)
    extends LeafExpression {
  override def dataType: DataType = output_type
}

case class ScalarScalaUDF(payload: Array[Byte], inputTypes: Seq[DataType], outputType: DataType, nullable: Boolean)
    extends LeafExpression {
  override def dataType: DataType = outputType
}

case class JavaUDF(class_name: String, output_type: Option[DataType], aggregate: Boolean) extends LeafExpression {
  override def dataType: DataType = output_type.getOrElse(UnresolvedType)
}

case class CommonInlineUserDefinedFunction(
    function_name: String,
    deterministic: Boolean,
    arguments: Seq[Expression],
    python_udf: Option[PythonUDF],
    scalar_scala_udf: Option[ScalarScalaUDF],
    java_udf: Option[JavaUDF])
    extends Expression {
  override def children: Seq[Expression] = arguments ++ python_udf.toSeq ++ scalar_scala_udf.toSeq ++ java_udf.toSeq
  override def dataType: DataType = UnresolvedType
}

case class CallFunction(function_name: String, arguments: Seq[Expression]) extends Expression with Fn {
  override def children: Seq[Expression] = arguments
  override def dataType: DataType = UnresolvedType
  override def prettyName: String = function_name.toUpperCase(Locale.getDefault)
}

case class NamedArgumentExpression(key: String, value: Expression) extends Expression {
  override def children: Seq[Expression] = value :: Nil
  override def dataType: DataType = UnresolvedType
}
