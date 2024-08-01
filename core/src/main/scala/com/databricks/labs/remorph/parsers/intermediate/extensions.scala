package com.databricks.labs.remorph.parsers.intermediate

trait AstExtension

abstract class ToRefactor extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}

// TODO: (nfx) refactor to align more with catalyst
case class Id(id: String, caseSensitive: Boolean = false) extends ToRefactor

// TODO: (nfx) refactor to align more with catalyst
case class ObjectReference(head: Id, tail: Id*) extends ToRefactor

// TODO: (nfx) refactor to align more with catalyst
case class Column(tableNameOrAlias: Option[ObjectReference], columnName: Id) extends ToRefactor with AstExtension {}
case class Identifier(name: String, isQuoted: Boolean) extends ToRefactor with AstExtension {}
case class DollarAction() extends ToRefactor with AstExtension {}
case class Distinct(expression: Expression) extends ToRefactor

case object Noop extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}

case object NoopNode extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}

// TODO: (nfx) refactor to align more with catalyst, UnaryNode
// case class UnresolvedWith(child: LogicalPlan, ctes: Seq[(String, SubqueryAlias)])
case class WithCTE(ctes: Seq[LogicalPlan], query: LogicalPlan) extends RelationCommon {
  override def output: Seq[Attribute] = query.output
  override def children: Seq[LogicalPlan] = ctes :+ query
}

// TODO: (nfx) refactor to align more with catalyst
// TOTO: remove this class, replace with SubqueryAlias
case class CTEDefinition(tableName: String, columns: Seq[Expression], cte: LogicalPlan) extends RelationCommon {
  override def output: Seq[Attribute] = columns.map(c => AttributeReference(c.toString, c.dataType))
  override def children: Seq[LogicalPlan] = Seq(cte)
}

// TODO: (nfx) refactor to align more with catalyst, rename to UnresolvedStar
case class Star(objectName: Option[ObjectReference] = None) extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}

// Assignment operators
// TODO: (ji) This needs to be renamed to Assignment as per Catalyst
case class Assign(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = UnresolvedType
}

// Some statements, such as SELECT, do not require a table specification
case class NoTable() extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}

case class LocalVarTable(id: Id) extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}

// Table hints are not directly supported in Databricks SQL, but at least some of
// them will have direct equivalents for the Catalyst optimizer. Hence they are
// included in the AST for the code generator to use them if it can. At worst,
// a comment can be generated with the hint text to guide the conversion.
abstract class TableHint
case class FlagHint(name: String) extends TableHint
case class IndexHint(indexes: Seq[Expression]) extends TableHint
case class ForceSeekHint(index: Option[Expression], indexColumns: Option[Seq[Expression]]) extends TableHint

// It was not clear whether the NamedTable options should be used for the alias. I'm assuming it is not what
// they are for.
case class TableAlias(child: LogicalPlan, alias: String, columns: Seq[Id] = Seq.empty) extends UnaryNode {
  override def output: Seq[Attribute] = columns.map(c => AttributeReference(c.id, StringType))
}

// TODO: (nfx) refactor to align more with catalyst
// TODO: remove this and replace with Hint(Hint(...), ...)
case class TableWithHints(child: LogicalPlan, hints: Seq[TableHint]) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class Batch(children: Seq[LogicalPlan]) extends LogicalPlan {
  override def output: Seq[Attribute] = children.lastOption.map(_.output).getOrElse(Seq())
}

case class FunctionParameter(name: String, dataType: DataType, defaultValue: Option[Expression])

sealed trait UDFRuntimeInfo
case class JavaUDFInfo(runtimeVersion: Option[String], imports: Seq[String], handler: String) extends UDFRuntimeInfo
case class PythonUDFInfo(runtimeVersion: Option[String], packages: Seq[String], handler: String) extends UDFRuntimeInfo
case object JavascriptUDFInfo extends UDFRuntimeInfo
case class ScalaUDFInfo(runtimeVersion: Option[String], imports: Seq[String], handler: String) extends UDFRuntimeInfo
case class SQLUDFInfo(memoizable: Boolean) extends UDFRuntimeInfo

case class CreateInlineUDF(
    name: String,
    returnType: DataType,
    parameters: Seq[FunctionParameter],
    runtimeInfo: UDFRuntimeInfo,
    acceptsNullParameters: Boolean,
    comment: Option[String],
    body: String)
    extends Catalog {}

// Used for raw expressions that have no context
case class Dot(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = UnresolvedType
}

case class ArrayAccess(array: Expression, index: Expression) extends Binary(array, index) {
  override def dataType: DataType = array.dataType
}

case class JsonAccess(json: Expression, path: Expression) extends Binary(json, path) {
  override def dataType: DataType = UnresolvedType
}

case class Collate(string: Expression, specification: String) extends Unary(string) {
  override def dataType: DataType = StringType
}

case class Timezone(expression: Expression, timeZone: Expression) extends Binary(expression, timeZone) {
  override def dataType: DataType = expression.dataType
}

case class WithinGroup(expression: Expression, order: Seq[SortOrder]) extends Unary(expression) {
  override def dataType: DataType = expression.dataType
}

sealed trait SamplingMethod
case class RowSamplingProbabilistic(probability: BigDecimal) extends SamplingMethod
case class RowSamplingFixedAmount(amount: BigDecimal) extends SamplingMethod
case class BlockSampling(probability: BigDecimal) extends SamplingMethod

// TODO: (nfx) refactor to align more with catalyst
case class TableSample(input: LogicalPlan, samplingMethod: SamplingMethod, seed: Option[BigDecimal]) extends UnaryNode {
  override def child: LogicalPlan = input
  override def output: Seq[Attribute] = input.output
}

// Note that Databricks SQL supports FILTER() used as an expression.
case class FilterExpr(input: Seq[Expression], lambdaFunction: LambdaFunction) extends Expression {
  override def children: Seq[Expression] = input :+ lambdaFunction
  override def dataType: DataType = UnresolvedType
}

case class ValueArray(expressions: Seq[Expression]) extends Expression {
  override def children: Seq[Expression] = expressions
  override def dataType: DataType = UnresolvedType
}

case class NamedStruct(keys: Seq[Expression], values: Seq[Expression]) extends Expression {
  override def children: Seq[Expression] = keys ++ values
  override def dataType: DataType = UnresolvedType
}

case class FilterStruct(input: NamedStruct, lambdaFunction: LambdaFunction) extends Expression {
  override def children: Seq[Expression] = Seq(input, lambdaFunction)
  override def dataType: DataType = UnresolvedType
}

// TSQL has some join types that are not natively supported in Databricks SQL, but can possibly be emulated
// using LATERAL VIEW and an explode function. Some things like functions are translatable at IR production
// time, but complex joins are better done at the translation from IR, via an optimizer rule as they are more involved
// than some simple prescribed action such as a rename
case object CrossApply extends JoinType
case object OuterApply extends JoinType

case class TableFunction(functionCall: Expression) extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}

case class Lateral(expr: LogicalPlan) extends UnaryNode {
  override def child: LogicalPlan = expr
  override def output: Seq[Attribute] = expr.output
}

case class Comment(text: String) extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}

case class Options(
    expressionOpts: Map[String, Expression],
    stringOpts: Map[String, String],
    boolFlags: Map[String, Boolean],
    autoFlags: List[String])
    extends Expression {
  override def children: Seq[Expression] = expressionOpts.values.toSeq
  override def dataType: DataType = UnresolvedType
}

case class WithOptions(input: LogicalPlan, options: Expression) extends UnaryNode {
  override def child: LogicalPlan = input
  override def output: Seq[Attribute] = input.output
}
