package com.databricks.labs.remorph.intermediate

import java.util.{UUID}

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

abstract class Unary(val child: Expression) extends Expression {
  override def children: Seq[Expression] = Seq(child)
}

abstract class Binary(left: Expression, right: Expression) extends Expression {
  override def children: Seq[Expression] = Seq(left, right)
}

case class WhenBranch(condition: Expression, expression: Expression) extends Binary(condition, expression) {
  override def dataType: DataType = expression.dataType
}

case class Case(expression: Option[Expression], branches: Seq[WhenBranch], otherwise: Option[Expression])
    extends Expression {
  override def children: Seq[Expression] = expression.toSeq ++
    branches.flatMap(b => Seq(b.condition, b.expression)) ++ otherwise
  override def dataType: DataType = branches.head.dataType
}

/** isnotnull(expr) - Returns true if `expr` is not null, or false otherwise. */
case class IsNotNull(left: Expression) extends Unary(left) {
  override def dataType: DataType = left.dataType
}

/** isnull(expr) - Returns true if `expr` is null, or false otherwise. */
case class IsNull(left: Expression) extends Unary(left) {
  override def dataType: DataType = left.dataType
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
    partition_spec: Seq[Expression] = Seq.empty,
    sort_order: Seq[SortOrder] = Seq.empty,
    frame_spec: Option[WindowFrame] = None,
    ignore_nulls: Boolean = false) // TODO: this is a property of Last(), not Window
    extends Expression {
  override def children: Seq[Expression] = Seq(window_function) ++ partition_spec ++ sort_order
  override def dataType: DataType = window_function.dataType
}

/** cast(expr AS type) - Casts the value `expr` to the target data type `type`. */
case class Cast(
    expr: Expression,
    dataType: DataType,
    type_str: String = "",
    returnNullOnError: Boolean = false,
    timeZoneId: Option[String] = None)
    extends Unary(expr)

case class CalendarInterval(months: Int, days: Int, microseconds: Long) extends LeafExpression {
  override def dataType: DataType = CalendarIntervalType
}

case class StructExpr(fields: Seq[StarOrAlias]) extends Expression {
  override def children: Seq[Expression] = fields.map {
    case a: Alias => a
    case s: Star => s
  }

  override def dataType: DataType = fields match {
    case Nil => UnresolvedType
    case Seq(Star(_)) => UnresolvedType
    case _ =>
      StructType(fields.map { case Alias(child, Id(name, _)) =>
        StructField(name, child.dataType)
      })
  }
}

case class UpdateFields(struct_expression: Expression, field_name: String, value_expression: Option[Expression])
    extends Expression {
  override def children: Seq[Expression] = struct_expression :: value_expression.toList
  override def dataType: DataType = UnresolvedType // TODO: Fix this
}

trait StarOrAlias

case class Alias(expr: Expression, name: Id) extends Unary(expr) with StarOrAlias {
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

case class Variable(name: String) extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}

case class SchemaReference(columnName: Expression) extends Unary(columnName) {
  override def dataType: DataType = UnresolvedType
}
